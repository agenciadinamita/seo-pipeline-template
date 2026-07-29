#!/usr/bin/env python3
"""
SEO content publisher — genérico, por cliente.

Reads Markdown articles from ./content/ and pushes them to WordPress
via the built-in REST API. Creates DRAFTS by default so you always
review before anything goes live.

Usage:
    python publish.py --dry-run          # show what would happen, touch nothing
    python publish.py                    # upload all unpublished articles as drafts
    python publish.py --only 01-mi-articulo
    python publish.py --status publish   # go straight to live (not recommended)

Config lives in .env (see .env.example).
"""

import argparse
import json
import os
import pathlib
import sys
import time

import frontmatter
import markdown
import requests
from dotenv import load_dotenv

load_dotenv()

WP_URL = os.getenv("WP_URL", "").rstrip("/")
WP_USER = os.getenv("WP_USER", "")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD", "")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")

CONTENT_DIR = pathlib.Path(__file__).parent / "content"
IMAGES_DIR = pathlib.Path(__file__).parent / "images"
STATE_FILE = pathlib.Path(__file__).parent / ".published.json"

MD_EXTENSIONS = ["extra", "sane_lists", "smarty"]

IMAGE_CONTENT_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
}


# ---------------------------------------------------------------- state

def load_state() -> dict:
    """Track what we've already pushed so re-running is safe (idempotent)."""
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {}


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


# ---------------------------------------------------------------- wp api

# Shared hosting often sits behind a WAF/security plugin that resets
# connections (TLS-level, not a clean 4xx/5xx) after a burst of requests
# in quick succession. Retrying with backoff rides through that instead
# of failing the whole run over what's usually a transient block.
RETRYABLE_EXCEPTIONS = (requests.exceptions.ConnectionError, requests.exceptions.Timeout)
RETRY_ATTEMPTS = 4
RETRY_BACKOFF_BASE = 5  # seconds: 5, 10, 20, 40


def request_with_retry(session_or_requests, method: str, url: str, **kwargs):
    last_exc = None
    for attempt in range(RETRY_ATTEMPTS):
        try:
            return session_or_requests.request(method, url, **kwargs)
        except RETRYABLE_EXCEPTIONS as exc:
            last_exc = exc
            if attempt < RETRY_ATTEMPTS - 1:
                wait = RETRY_BACKOFF_BASE * (2 ** attempt)
                print(f"    ! connection reset ({exc.__class__.__name__}), "
                      f"retrying in {wait}s ({attempt + 1}/{RETRY_ATTEMPTS})...")
                time.sleep(wait)
    raise last_exc


def wp_session() -> requests.Session:
    s = requests.Session()
    s.auth = (WP_USER, WP_APP_PASSWORD)
    s.headers.update({"User-Agent": "seo-pipeline-publisher/1.0"})
    return s


def check_connection(s: requests.Session) -> None:
    r = request_with_retry(s, "GET", f"{WP_URL}/wp-json/wp/v2/users/me", timeout=30)
    if r.status_code == 401:
        sys.exit("AUTH FAILED. Check WP_USER and WP_APP_PASSWORD in .env.")
    r.raise_for_status()
    print(f"  Connected to {WP_URL} as '{r.json().get('name')}'")


def get_or_create_category(s: requests.Session, name: str) -> int:
    """Find a category by name, create it if missing. Returns its ID."""
    r = request_with_retry(s, "GET", f"{WP_URL}/wp-json/wp/v2/categories",
                            params={"search": name, "per_page": 100}, timeout=30)
    r.raise_for_status()
    for cat in r.json():
        if cat["name"].strip().lower() == name.strip().lower():
            return cat["id"]

    r = request_with_retry(s, "POST", f"{WP_URL}/wp-json/wp/v2/categories",
                            json={"name": name}, timeout=30)
    if r.status_code == 400 and "term_exists" in r.text:
        return r.json()["data"]["term_id"]
    r.raise_for_status()
    print(f"    + created category '{name}'")
    return r.json()["id"]


# ---------------------------------------------------------------- images

def fetch_stock_image(query: str, dest_path: pathlib.Path) -> bool:
    """Search Pexels for `query`, download the top landscape result to dest_path.
    Returns True on success, False if no key/no results/error (caller just skips)."""
    if not PEXELS_API_KEY:
        return False

    try:
        r = requests.get(
            "https://api.pexels.com/v1/search",
            headers={"Authorization": PEXELS_API_KEY},
            params={"query": query, "per_page": 1, "orientation": "landscape"},
            timeout=30,
        )
        r.raise_for_status()
        photos = r.json().get("photos", [])
        if not photos:
            return False

        img_url = photos[0]["src"]["large"]
        img = requests.get(img_url, timeout=30)
        img.raise_for_status()

        dest_path.parent.mkdir(parents=True, exist_ok=True)
        dest_path.write_bytes(img.content)
        return True
    except requests.RequestException:
        return False


def upload_featured_image(s: requests.Session, image_path: pathlib.Path, alt_text: str) -> int:
    """Upload an image to the WP media library and return its media ID."""
    content_type = IMAGE_CONTENT_TYPES.get(image_path.suffix.lower(), "application/octet-stream")
    r = request_with_retry(
        s, "POST", f"{WP_URL}/wp-json/wp/v2/media",
        data=image_path.read_bytes(),
        headers={
            "Content-Disposition": f'attachment; filename="{image_path.name}"',
            "Content-Type": content_type,
        },
        timeout=60,
    )
    r.raise_for_status()
    media_id = r.json()["id"]

    request_with_retry(s, "POST", f"{WP_URL}/wp-json/wp/v2/media/{media_id}",
                        json={"alt_text": alt_text, "title": alt_text}, timeout=30)

    return media_id


def build_payload(s: requests.Session, post, html: str, status: str | None) -> dict:
    """status=None omits the field entirely — used for --update so we never
    change a post's current WP status (e.g. flip a manually-published post back to draft)."""
    meta = post.metadata

    payload = {
        "title": meta["title"],
        "slug": meta["slug"],
        "content": html,
        "excerpt": meta.get("excerpt", ""),
    }
    if status is not None:
        payload["status"] = status

    if meta.get("category"):
        payload["categories"] = [get_or_create_category(s, meta["category"])]

    # Yoast SEO fields. These only stick if you install wp-yoast-rest.php
    # (see README). Without it WordPress silently ignores them and you'd
    # set the meta title/description by hand in the Yoast box.
    yoast = {}
    if meta.get("seo_title"):
        yoast["_yoast_wpseo_title"] = meta["seo_title"]
    if meta.get("meta_description"):
        yoast["_yoast_wpseo_metadesc"] = meta["meta_description"]
    if meta.get("focus_keyword"):
        yoast["_yoast_wpseo_focuskw"] = meta["focus_keyword"]
    if yoast:
        payload["meta"] = yoast

    return payload


# ---------------------------------------------------------------- main

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="Print what would be sent. Makes no changes.")
    ap.add_argument("--status", default="draft",
                    choices=["draft", "publish", "pending", "future"])
    ap.add_argument("--only", help="Publish specific file(s) by stem, comma-separated, "
                    "e.g. 01-mi-articulo or 02-x,03-y,04-z")
    ap.add_argument("--force", action="store_true",
                    help="Re-upload even if already published (creates a duplicate).")
    ap.add_argument("--update", action="store_true",
                    help="For articles already in .published.json, update the existing WP "
                    "post in place (content/excerpt/categories/meta/slug) instead of "
                    "skipping. Never touches the post's current status. Does not affect "
                    "articles not yet published — those still need a normal run to create them.")
    args = ap.parse_args()

    files = sorted(CONTENT_DIR.glob("*.md"))
    if args.only:
        stems = {s.strip() for s in args.only.split(",")}
        files = [f for f in files if f.stem in stems]
        missing = stems - {f.stem for f in files}
        if missing:
            sys.exit(f"No file matching {sorted(missing)} in {CONTENT_DIR}")

    if not files:
        sys.exit(f"No .md files found in {CONTENT_DIR}")

    if not args.dry_run:
        if not all([WP_URL, WP_USER, WP_APP_PASSWORD]):
            sys.exit("Missing config. Copy .env.example to .env and fill it in.")
        s = wp_session()
        check_connection(s)
    else:
        s = None
        print("  DRY RUN — nothing will be sent.\n")

    state = load_state()
    md = markdown.Markdown(extensions=MD_EXTENSIONS)

    created, updated, skipped = 0, 0, 0

    for path in files:
        post = frontmatter.load(path)
        slug = post.metadata.get("slug", path.stem)

        is_update = slug in state and args.update
        if slug in state and not args.update and not args.force:
            print(f"  SKIP  {slug}  (already posted, ID {state[slug]['id']})")
            skipped += 1
            continue

        md.reset()
        html = md.convert(post.content)

        image_rel = post.metadata.get("featured_image")
        image_path = (pathlib.Path(__file__).parent / image_rel) if image_rel else None
        image_query = post.metadata.get("image_query") or post.metadata.get("focus_keyword")

        if args.dry_run:
            wc = len(post.content.split())
            action = "WOULD UPDATE" if is_update else "WOULD POST"
            print(f"  {action}  {slug}")
            print(f"     title : {post.metadata.get('title')}")
            print(f"     kw    : {post.metadata.get('focus_keyword')}")
            print(f"     words : {wc}")
            if is_update:
                print(f"     id    : {state[slug]['id']}  (status untouched)")
            else:
                print(f"     status: {args.status}")
                if image_rel:
                    if image_path.exists():
                        print(f"     image : {image_rel}  FOUND (local file)")
                    elif PEXELS_API_KEY:
                        print(f"     image : {image_rel}  WILL FETCH from Pexels (query: '{image_query}')")
                    else:
                        print(f"     image : {image_rel}  MISSING (no local file, no PEXELS_API_KEY set)")
                else:
                    print(f"     image : (none set — no featured_image in frontmatter)")
            print()
            created += 1
            continue

        payload = build_payload(s, post, html, None if is_update else args.status)

        if not is_update and image_rel:
            if not image_path.exists() and PEXELS_API_KEY:
                if fetch_stock_image(image_query, image_path):
                    print(f"        fetched stock image for '{image_query}' -> {image_rel}")
                else:
                    print(f"  WARN  {slug}  Pexels fetch failed for '{image_query}', skipping image")

            if image_path.exists():
                alt_text = post.metadata.get("image_alt") or post.metadata.get("title")
                media_id = upload_featured_image(s, image_path, alt_text)
                payload["featured_media"] = media_id
            else:
                print(f"  WARN  {slug}  featured_image '{image_rel}' not found, skipping image")

        if is_update:
            post_id = state[slug]["id"]
            r = request_with_retry(s, "POST", f"{WP_URL}/wp-json/wp/v2/posts/{post_id}",
                                    json=payload, timeout=60)
        else:
            r = request_with_retry(s, "POST", f"{WP_URL}/wp-json/wp/v2/posts",
                                    json=payload, timeout=60)

        if r.status_code not in (200, 201):
            print(f"  FAIL  {slug}  [{r.status_code}] {r.text[:200]}")
            continue

        data = r.json()
        state[slug] = {"id": data["id"], "link": data["link"], "status": data["status"]}
        save_state(state)
        if is_update:
            print(f"  UPDATED  {slug}  -> ID {data['id']}  ({data['status']})")
            updated += 1
        else:
            print(f"  OK    {slug}  -> ID {data['id']}  ({data['status']})")
            created += 1
        print(f"        {data['link']}")
        time.sleep(1)  # be polite to shared hosting

    print(f"\n  Done. {created} posted, {updated} updated, {skipped} skipped.")
    if not args.dry_run and args.status == "draft" and created:
        print("  Review the drafts in WP Admin, then publish from there.")


if __name__ == "__main__":
    main()
