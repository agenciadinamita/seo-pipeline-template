# CONVENTIONS.md — reglas compartidas del pipeline SEO

> **Este archivo es idéntico entre todos los clientes.** No le agregues nada específico de un
> cliente aquí (eso va en su `CLAUDE.md`, sección "Voice" y "External link whitelist"). Este
> archivo es el que se sincroniza cuando se hace "pull" del template — ver instrucciones al final.

`CLAUDE.md` de cada cliente debe decir, cerca del principio: *"Lee también `CONVENTIONS.md` —
reglas de formato y no-negociables compartidas con todos los clientes de este pipeline."*

---

## Frontmatter schema — all fields required

```yaml
---
title: "H1 the reader sees"
slug: "url-slug"
focus_keyword: "primary keyword"
seo_title: "Google title — HARD LIMIT 60 chars"
meta_description: "Google description — HARD LIMIT 155 chars"
excerpt: "Short summary for the blog listing"
category: "Categoría de WordPress"
cluster: "Nombre del cluster"
article_type: "Ultimate guide | How-to | Comparison | Listicle | FAQ | Explainer"
size: "xl | lg | md"
---
```

## Formato obligatorio de cada artículo

1. Caja "Resumen rápido" al inicio (3-4 bullets con la idea honesta, no un resumen completo).
2. Encabezados H2/H3 en sentence case (nunca Title Case, nunca mayúsculas). Máximo 12 H2.
3. Usa los cuatro recursos de formato en cada artículo: bold para la frase que sostiene cada
   sección, tablas para comparaciones, 1-2 blockquotes para la frase que merece destacarse sola,
   listas donde ayude a escanear.
4. Cierra con CTA: link + teléfono + correo del cliente (los datos exactos viven en el `CLAUDE.md`
   de cada cliente).
5. FAQ opcional (2-4 preguntas) después del CTA.
6. Disclaimer en cursiva al final, si el contenido es legal/financiero/de salud o cualquier tema
   donde una afirmación incorrecta tenga consecuencias reales.

## Linking rules (política — la whitelist de fuentes externas es específica de cada cliente)

- **Interno:** 3-5 links por artículo, por slug, a otros artículos genuinamente relacionados en
  `content/`. Nunca a contenido archivado/descontinuado.
- **Externo:** máximo 1-2 por artículo, **solo de la whitelist verificada que vive en el `CLAUDE.md`
  de ese cliente específico** — nunca un link improvisado a mitad de redacción. Si hace falta una
  fuente nueva, se agrega primero a esa whitelist (verificada) antes de usarla.

## Word counts

XL 1,700–2,200 · LG 900–1,300 · MD 650–900

## NON-NEGOTIABLE RULES

1. **Nunca inventar cifras, tasas, precios o plazos específicos.** Dar rangos, etiquetarlos como
   orientativos, remitir a un profesional/fuente oficial para el número exacto.
2. Todo artículo legal/financiero/técnico-sensible lleva el disclaimer.
3. Este contenido construye confianza — estar equivocado es peor que ser vago.

---

## Si el cliente ya tiene contenido existente: auditar ANTES de escribir nada nuevo

No asumas que un blog existente está bien, ni lo ignores. Antes de publicar contenido nuevo:

1. Trae el listado completo de posts existentes vía la API de WordPress (no solo lo que se ve en
   la página del blog — usa `/wp-json/wp/v2/posts?per_page=100&status=publish,draft`).
2. Categorízalos por tema/intención de búsqueda.
3. Identifica canibalización: ¿varios posts compiten por la misma keyword genérica?
4. Propón una decisión explícita (consolidar en menos piezas + redirects, dejar como está,
   despublicar) y **haz que el cliente decida — no lo decidas tú solo**, sobre todo si implica
   tocar contenido que ya está en vivo.
5. Documenta la decisión en el `CLAUDE.md` de ese cliente, con fecha, para que una sesión futura no
   la reabra sin saber que ya se resolvió.

**Publicar contenido nuevo encima de un problema de canibalización sin resolver empeora el
problema, no lo arregla.**

---

## The pipeline

`publish.py` → WordPress REST API → **drafts** (never auto-publishes by default).
Idempotente: registra los slugs ya publicados en `.published.json`, seguro de re-correr.

```bash
pip install -r requirements.txt
cp .env.example .env        # WP_URL, WP_USER, WP_APP_PASSWORD
python publish.py --dry-run
python publish.py
```

**Yoast:** los campos de meta solo persisten si `wp-yoast-rest.php` está instalado vía el plugin
Code Snippets en el WordPress del cliente. Sin eso, WordPress los descarta en silencio.

---

## Automatizaciones (Routines en la nube) — si aplica

Si vas a montar una rutina automática (semanal, mensual, etc.), recuerda:

- **Vive aislada del repo** — no lee `CLAUDE.md` ni `content/`. Todo lo que necesite (voz, formato,
  reglas del cliente, backlog de keywords, credenciales) debe estar **embebido directamente en su
  prompt**, no solo referenciado.
- **Nunca "publish" como status por default** — siempre "draft", como gate de aprobación humana.
- Si el cliente tiene restricciones de contenido, tienen que repetirse explícitamente en el prompt
  de la rutina — ver la sección de restricciones en su `CLAUDE.md`.
- Una vez creada por un agente, solo ese agente (o sesiones que hereden su contexto, bajo la misma
  cuenta) puede editarla/borrarla. Si se creó por otra vía (API externa, panel web), un agente no
  podrá tocarla — la única opción es crear una de reemplazo y pedirle al humano que borre la vieja.
- El parámetro para adjuntar conectores MCP (ej. Ubersuggest) a una Routine puede estar
  deshabilitado a nivel organización sin previo aviso — pruébalo temprano, no lo asumas.

---

## Cómo "hacer pull" de este archivo en el chat de un cliente

Cuando actualices este archivo (`CONVENTIONS.md`) en el repo plantilla, para llevar el cambio a un
cliente ya existente, entra a su chat y dile algo como:

> "Trae la versión más reciente de CONVENTIONS.md desde agenciadinamita/seo-pipeline-template y
> reemplaza el archivo CONVENTIONS.md de este repo con esa versión (o créalo si no existe todavía).
> No toques CLAUDE.md ni content/. Ábrelo como PR para que yo lo revise."

Esto es una acción manual, cliente por cliente — no se propaga sola. Usa `CLIENTES.md` en el repo
plantilla para saber a cuáles clientes hacérselo.
