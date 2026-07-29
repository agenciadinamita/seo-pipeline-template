# CLAUDE.md — [NOMBRE DEL CLIENTE] SEO Pipeline

Context file for Claude Code. Read this fully before doing anything.

> **Instrucciones de uso de esta plantilla:** reemplaza cada `[PLACEHOLDER]` con la información real
> del cliente. Las secciones marcadas `EJEMPLO — borrar` muestran cómo se ve un caso ya resuelto
> (tomado de un proyecto real) — bórralas una vez que entiendas el patrón. El resto de la
> estructura (encabezados, reglas no negociables, formato) está pensada para copiarse tal cual.

---

## The project

**Client:** [Nombre del cliente] (`[dominio-del-cliente.com]`)
**Business:** [Qué vende / qué servicio ofrece, en una línea]
**Stack:** WordPress + [Elementor / otro constructor] + Yoast SEO
**Language:** [Español (es-MX) / el idioma que corresponda]. **Deja explícito el idioma de todo el contenido.**
**Differentiators (reales, nunca inventados — sácalos de su sitio/material actual):** [diferenciador 1], [diferenciador 2], [diferenciador 3]
**Contact used in CTAs:** [teléfono] · [correo]

---

## ⚠️ Restricciones del cliente (si las hay)

> **EJEMPLO — borrar.** Un cliente real de este pipeline pidió, a mitad de proyecto: *"no quiero
> ningún contenido SEO sobre X, bajo ninguna variante."* La entrada quedó así:
>
> - No escribir, proponer ni sugerir contenido sobre X, aunque el volumen/dificultad se vea
>   atractivo — esto incluye no "reencuadrarlo" como otro tipo de artículo.
> - El contenido ya existente sobre X se archivó en `content/archived-X/` — fuera del pipeline
>   activo, nunca se borra (registro histórico), nunca se usa como referencia de estilo.
> - Las keywords de ese tema en `keyword_backlog.json` se marcaron `"status": "rejected"` con
>   `rejected_reason` — no moverlas de vuelta a `pending`.
> - **Si hay una automatización en la nube corriendo (Routine), la restricción tiene que escribirse
>   también, explícitamente, en su prompt** — la Routine no lee este archivo, así que una regla que
>   solo vive aquí nunca le llega. Ver sección de Automatizaciones abajo.

Si este cliente tiene restricciones de contenido, documentálas aquí con la misma estructura: qué
no se debe hacer, dónde vive lo ya existente sobre ese tema, y qué automatizaciones hay que
blindar también.

---

## Content plan — clusters

Cada cluster tiene un **pilar** (la keyword de mayor volumen del grupo) y varios artículos de
soporte. Todas las keywords deben venir de investigación real (Ubersuggest u otra fuente de datos
de búsqueda) — nunca inventadas ni estimadas.

### ⬜ Cluster 1 — [Nombre del cluster]
- **Pillar:** `[keyword principal]` ([volumen]/mo, SD [dificultad]) — [tipo de artículo], [tamaño]
- `[keyword de soporte]` ([volumen], SD [dificultad]) — [tipo], [tamaño]
- `[keyword de soporte]` ([volumen], SD [dificultad]) — [tipo], [tamaño]

### ⬜ Cluster 2 — [Nombre del cluster]
- **Pillar:** `[keyword principal]` ([volumen]/mo, SD [dificultad]) — [tipo de artículo], [tamaño]
- `[keyword de soporte]` ([volumen], SD [dificultad]) — [tipo], [tamaño]

*(Agrega tantos clusters como tenga sentido para el negocio del cliente. 3-6 clusters con 4-6
artículos cada uno es un punto de partida razonable.)*

---

## ⚠️ Si el cliente ya tiene contenido existente: auditar ANTES de escribir nada nuevo

No asumas que un blog existente está bien, ni lo ignores. Antes de publicar contenido nuevo:

1. Trae el listado completo de posts existentes vía la API de WordPress (no solo lo que se ve en
   la página del blog — usa `/wp-json/wp/v2/posts?per_page=100&status=publish,draft`).
2. Categorízalos por tema/intención de búsqueda.
3. Identifica canibalización: ¿varios posts compiten por la misma keyword genérica?
4. Propone una decisión explícita (consolidar en menos piezas + redirects, dejar como está,
   despublicar) y **haz que el cliente decida — no lo decidas tú solo**, sobre todo si implica
   tocar contenido que ya está en vivo.
5. Documenta la decisión aquí, con fecha, para que una sesión futura no la reabra sin saber que ya
   se resolvió.

**Publicar contenido nuevo encima de un problema de canibalización sin resolver empeora el
problema, no lo arregla.**

---

## Writing conventions

Una vez que exista al menos un artículo bien recibido por el cliente, referencia ese archivo aquí
("lee `content/08-articulo-de-referencia.md` antes de escribir algo nuevo, iguala su estilo") en
vez de repetir la descripción de la voz cada vez.

**Frontmatter schema — all fields required:**
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

**Voice:** [Define el tono real del cliente — directo/formal/cercano/técnico. A quién le habla el
contenido (ej. "a una familia protegiendo sus ahorros, no a un inversionista"). Ejemplo de regla
útil: "lidera con la respuesta honesta, aunque incomode".]

**Formato obligatorio de cada artículo:**
1. Caja "Resumen rápido" al inicio (3-4 bullets con la idea honesta, no un resumen completo).
2. Encabezados H2/H3 en sentence case (nunca Title Case, nunca mayúsculas). Máximo 12 H2.
3. Usa los cuatro recursos de formato en cada artículo: bold para la frase que sostiene cada
   sección, tablas para comparaciones, 1-2 blockquotes para la frase que merece destacarse sola,
   listas donde ayude a escanear.
4. Cierra con CTA: link + teléfono + correo del cliente.
5. FAQ opcional (2-4 preguntas) después del CTA.
6. Disclaimer en cursiva al final, si el contenido es legal/financiero/de salud o cualquier tema
   donde una afirmación incorrecta tenga consecuencias reales.

**Linking rules:**
- Interno: 3-5 links por artículo, por slug, a otros artículos genuinamente relacionados en
  `content/`. Nunca a contenido archivado/descontinuado.
- Externo: máximo 1-2 por artículo, **solo de una whitelist verificada explícitamente aquí abajo**
  (nunca un link improvisado a mitad de redacción):
  - [Fuente oficial 1]: `https://...` — para temas de [tema]
  - [Fuente oficial 2]: `https://...` — para temas de [tema]
  - **Nunca enlazar fuera de esta lista.** Si hace falta una fuente nueva, agrégala aquí primero
    (verificada) en vez de improvisar un link a mitad de un artículo.

**Word counts:** XL 1,700–2,200 · LG 900–1,300 · MD 650–900

**NON-NEGOTIABLE RULES:**
1. **Nunca inventar cifras, tasas, precios o plazos específicos.** Dar rangos, etiquetarlos como
   orientativos, remitir a un profesional/fuente oficial para el número exacto.
2. Todo artículo legal/financiero/técnico-sensible lleva el disclaimer.
3. Este contenido construye confianza — estar equivocado es peor que ser vago.

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
  de la rutina — ver la sección de restricciones arriba.
- Una vez creada por un agente, solo ese agente (o sesiones que hereden su contexto) puede
  editarla/borrarla. Si se creó por otra vía (API externa, panel web), un agente no podrá tocarla —
  la única opción es crear una de reemplazo y pedirle al humano que borre la vieja.
- El parámetro para adjuntar conectores MCP (ej. Ubersuggest) a una Routine puede estar
  deshabilitado a nivel organización sin previo aviso — pruébalo temprano, no lo asumas.

---

## Your job, Claude Code

Prioridad recomendada para arrancar con un cliente nuevo:

1. Llenar esta plantilla con la información real del cliente.
2. Investigar keywords reales (Ubersuggest u otra fuente), definir clusters.
3. Configurar WordPress: Application Password + `wp-yoast-rest.php`.
4. Si hay blog existente, auditarlo antes de escribir nada nuevo.
5. Escribir y validar el primer artículo, correr `--dry-run`, luego push real de prueba.
6. Confirmar con el cliente el criterio de publicación (borrador con revisión, o en vivo directo)
   antes de automatizar nada.

**No publicar nada en vivo sin autorización explícita del cliente.** Borradores por default.
