# CONVENTIONS.md — reglas compartidas del pipeline SEO

> **Este archivo es idéntico entre todos los clientes.** No le agregues nada específico de un
> cliente aquí (eso va en su `CLAUDE.md`, sección "Voice" y "External link whitelist"). Este
> archivo es el que se sincroniza cuando se hace "pull" del template — ver instrucciones al final.

`CLAUDE.md` de cada cliente debe decir, cerca del principio: *"Lee también `CONVENTIONS.md` —
reglas de formato y no-negociables compartidas con todos los clientes de este pipeline."*

---

## Idioma — español de México (es-MX), por default en todo el pipeline

**Todo el contenido dirigido al lector va en español de México**, sin excepción: título, `seo_title`,
`meta_description`, `excerpt`, cuerpo del artículo, FAQ, CTA, y **`image_alt`** (alt text de la
imagen destacada). Esto es el default compartido — solo cambia si el `CLAUDE.md` de un cliente
específico declara explícitamente otro idioma en su sección "The project".

**Única excepción:** `image_query` (el término de búsqueda para el banco de imágenes en
`publish.py`) puede quedar en inglés — es un campo técnico que nunca se muestra al lector y los
bancos de imágenes (Pexels) devuelven mejores resultados con queries en inglés.

## Frontmatter schema — all fields required

```yaml
---
title: "H1 the reader sees — en español de México"
slug: "url-slug"
featured_image: "images/nombre.jpg"
image_query: "descripcion en inglés para el banco de imágenes (única excepción al idioma)"
image_alt: "Alt text descriptivo en español de México — no repitas el título tal cual"
focus_keyword: "primary keyword"
seo_title: "Google title — HARD LIMIT 60 chars — en español de México"
meta_description: "Google description — HARD LIMIT 155 chars — en español de México"
excerpt: "Short summary for the blog listing — en español de México"
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

## Automatizaciones (Routines en la nube) — dos por cliente, estándar

Todo cliente activo debe terminar con **exactamente dos** Routines, siempre con estos nombres,
cadencias y contratos — no improvises variantes por cliente salvo que él pida algo distinto
explícitamente (y si lo pide, documéntalo en su `CLAUDE.md`).

**Reglas generales para ambas:**

- **Viven aisladas del repo** — el *trigger* (cron + prompt) no relee `CLAUDE.md` ni `content/` por
  sí mismo. Todo lo que la sesión disparada necesite para decidir *qué* hacer (voz, formato, reglas
  del cliente, whitelist de links, restricciones) debe estar **embebido directamente en el texto del
  prompt**, no solo referenciado con un "revisa el CLAUDE.md". La sesión disparada sí tiene el repo
  clonado vía su `environment_id` — úsalo para leer `content/`, `.published.json`,
  `keyword_backlog.json` y para hacer commits/PRs, pero las reglas de negocio van en el prompt.
- **Nunca `--status publish`** — ambas rutinas trabajan siempre en `draft` (contenido) o vía PR
  (backlog de keywords). Publicar en vivo lo decide el cliente, nunca la automatización.
- Restricciones de contenido del cliente (si las hay) van copiadas tal cual en el prompt de ambas
  rutinas donde aplique — ver su `CLAUDE.md`.
- Una vez creada por un agente, solo ese agente (o sesiones que hereden su contexto, misma cuenta)
  puede editarla/borrarla. Si se creó por otra vía, la única opción es crear una de reemplazo y
  pedirle al humano que borre la vieja.
- El parámetro para adjuntar conectores MCP (ej. Ubersuggest) a una Routine puede estar
  deshabilitado a nivel organización sin previo aviso — pruébalo al crear la rutina, no lo asumas.
- Registra el `trigger_id` de cada una en `CLIENTES.md` en cuanto la crees.

### Rutina 1 — Contenido semanal

- **Nombre:** `[Cliente] — Contenido semanal`
- **Cron:** `0 15 * * 1` (lunes 9:00 am hora Ciudad de México)
- **Modo:** `create_new_session_on_fire: true`, `environment_id` del cliente (repo + acceso de red
  a su WordPress).
- **Qué hace, en este orden:**
  1. Lee `content/` y `.published.json` del repo para ver qué ya existe.
  2. Elige la siguiente keyword pendiente: primero pilares sin cubrir del content plan del
     `CLAUDE.md`, luego soporte, luego `keyword_backlog.json` con `status: "pending"`.
  3. Escribe UN artículo completo en español de México siguiendo el formato de este archivo
     (frontmatter completo incl. `image_alt`, Resumen rápido, H2/H3 sentence case, los cuatro
     recursos de formato, linking interno 3-5 y externo máx 1-2 solo de la whitelist del cliente,
     CTA, FAQ opcional, disclaimer si aplica, word count según `size`).
  4. Guarda el archivo en `content/` con el siguiente número de secuencia disponible.
  5. Corre `python publish.py --dry-run`, revisa que no haya errores.
  6. Corre `python publish.py` (status `draft`, nunca `publish`).
  7. Hace commit del artículo y abre un PR contra `main` con un resumen del artículo.
  8. Si no queda ninguna keyword pendiente, no inventa una — reporta backlog vacío y se detiene.
- **El prompt debe embeber, literalmente pegados:** nombre/repo/dominio del cliente, la sección
  "Voice" completa de su `CLAUDE.md`, sus restricciones (o "ninguna"), su whitelist de links
  externos, y sus datos de contacto para el CTA.

### Rutina 2 — Refresh de keywords mensual

- **Nombre:** `[Cliente] — Refresh keywords mensual`
- **Cron:** `0 15 1 * *` (día 1 de cada mes, 9:00 am hora Ciudad de México)
- **Modo:** `create_new_session_on_fire: true`, mismo `environment_id`, con el conector Ubersuggest
  adjunto si la organización lo permite.
- **Qué hace, en este orden:**
  1. Lee `keyword_backlog.json` y el content plan del `CLAUDE.md` del cliente.
  2. Con Ubersuggest: revisa volumen/dificultad actual de las keywords ya usadas en `content/`
     (detecta caídas grandes o cambios relevantes) y busca oportunidades nuevas relacionadas a los
     clusters existentes que no estén ya cubiertas ni en el backlog.
  3. Si el conector no está disponible, lo reporta explícitamente y se detiene — nunca inventa
     cifras de volumen/dificultad.
  4. Agrega oportunidades nuevas a `keyword_backlog.json` con `status: "pending"` — nunca borra
     entradas existentes ni revierte un `"rejected"` a `"pending"` sin que el cliente lo pida.
  5. Nunca propone como keyword ningún tema listado en las restricciones de contenido del cliente
     (si las hay).
  6. Abre un PR con los cambios a `keyword_backlog.json` y un resumen (oportunidades nuevas,
     keywords en decadencia, o "nada relevante este mes").
  7. No toca `content/` ni `publish.py` — esta rutina solo actualiza el backlog.
- **El prompt debe embeber:** nombre/repo/dominio del cliente y sus restricciones de contenido.

---

## Cómo "hacer pull" de este archivo en el chat de un cliente

Cuando actualices este archivo (`CONVENTIONS.md`) en el repo plantilla, para llevar el cambio a un
cliente ya existente, entra a su chat y dile algo como:

> "Trae la versión más reciente de CONVENTIONS.md desde agenciadinamita/seo-pipeline-template y
> reemplaza el archivo CONVENTIONS.md de este repo con esa versión (o créalo si no existe todavía).
> No toques CLAUDE.md ni content/. Ábrelo como PR para que yo lo revise."

Esto es una acción manual, cliente por cliente — no se propaga sola. Usa `CLIENTES.md` en el repo
plantilla para saber a cuáles clientes hacérselo.
