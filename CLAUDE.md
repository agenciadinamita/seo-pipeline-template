# CLAUDE.md — [NOMBRE DEL CLIENTE] SEO Pipeline

Context file for Claude Code. Read this fully before doing anything.

**Lee también [`CONVENTIONS.md`](./CONVENTIONS.md)** — reglas de formato, frontmatter, linking y
no-negociables, compartidas con todos los clientes de este pipeline. Ese archivo se actualiza
solo vía "pull" desde el repo plantilla — no le agregues nada específico de este cliente ahí, ni
edites su contenido directamente en este repo (el próximo pull lo sobrescribiría).

> **Instrucciones de uso de esta plantilla:** reemplaza cada `[PLACEHOLDER]` con la información real
> del cliente. Las secciones marcadas `EJEMPLO — borrar` muestran cómo se ve un caso ya resuelto
> (tomado de un proyecto real) — bórralas una vez que entiendas el patrón.

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
>   solo vive aquí nunca le llega.

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

## Voice (específico de este cliente)

[Define el tono real del cliente — directo/formal/cercano/técnico. A quién le habla el contenido
(ej. "a una familia protegiendo sus ahorros, no a un inversionista"). Ejemplo de regla útil:
"lidera con la respuesta honesta, aunque incomode".]

Una vez que exista al menos un artículo bien recibido por el cliente, referencia ese archivo aquí
("lee `content/08-articulo-de-referencia.md` antes de escribir algo nuevo, iguala su estilo") en
vez de repetir la descripción de la voz cada vez.

## External link whitelist (específico de este cliente)

**Máximo 1-2 links externos por artículo, solo de esta lista** (ver política completa en
`CONVENTIONS.md`):

- [Fuente oficial 1]: `https://...` — para temas de [tema]
- [Fuente oficial 2]: `https://...` — para temas de [tema]

**Nunca enlazar fuera de esta lista.** Si hace falta una fuente nueva, agrégala aquí primero
(verificada) en vez de improvisar un link a mitad de un artículo.

---

## Your job, Claude Code

Prioridad recomendada para arrancar con un cliente nuevo:

1. Llenar esta plantilla con la información real del cliente.
2. Investigar keywords reales (Ubersuggest u otra fuente), definir clusters.
3. Configurar WordPress: Application Password + `wp-yoast-rest.php`.
4. Si hay blog existente, auditarlo antes de escribir nada nuevo (ver `CONVENTIONS.md`).
5. Escribir y validar el primer artículo, correr `--dry-run`, luego push real de prueba.
6. Confirmar con el cliente el criterio de publicación (borrador con revisión, o en vivo directo)
   antes de automatizar nada.

**No publicar nada en vivo sin autorización explícita del cliente.** Borradores por default.
