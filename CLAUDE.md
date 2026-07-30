# CLAUDE.md — [NOMBRE DEL CLIENTE] SEO Pipeline

Context file for Claude Code. Read this fully before doing anything — **empieza por la sección
"Estado de configuración" de abajo, siempre, antes de atender cualquier otra cosa que te pida el
usuario**, salvo que la petición sea obviamente urgente y no relacionada con el setup.

**Lee también [`CONVENTIONS.md`](./CONVENTIONS.md)** — reglas de formato, frontmatter, linking y
no-negociables, compartidas con todos los clientes de este pipeline. Ese archivo se actualiza
solo vía "pull" desde el repo plantilla — no le agregues nada específico de este cliente ahí, ni
edites su contenido directamente en este repo (el próximo pull lo sobrescribiría).

> **Instrucciones de uso de esta plantilla:** reemplaza cada `[PLACEHOLDER]` con la información real
> del cliente. Las secciones marcadas `EJEMPLO — borrar` muestran cómo se ve un caso ya resuelto
> (tomado de un proyecto real) — bórralas una vez que entiendas el patrón.

---

## 🧭 Estado de configuración — revisa esto SIEMPRE al empezar una sesión en este repo

No le preguntes al usuario "¿qué necesitas?" a ciegas. Corre este checklist tú mismo, en orden,
y con lo que encuentres arma un reporte corto de qué está listo y cuál es **el siguiente paso
pendiente** — luego pregúntale al usuario si quiere seguir con ese paso, o hazlo directamente si
no requiere una decisión suya.

1. **¿Este `CLAUDE.md` sigue teniendo `[PLACEHOLDERS]` sin llenar** en "The project", "Content
   plan" o "Voice"? → Si sí, ese es el paso 1: pídele al usuario los datos reales del cliente
   (negocio, diferenciadores, contacto, idioma) y llénalos tú mismo en el archivo.
2. **¿Los clusters de "Content plan" tienen keywords reales** (con volumen/dificultad de
   Ubersuggest) o siguen siendo el placeholder de ejemplo? → Si son placeholder, investiga
   keywords reales del negocio del cliente y arma los clusters.
3. **¿Sigue existiendo `content/00-EJEMPLO-borrar-antes-de-usar.md`?** → Bórralo una vez que ya
   escribiste al menos un artículo real siguiendo su formato.
4. **¿Existe `.env` en este repo** (no vas a poder leer su contenido, pero sí confirmar que el
   archivo existe)? Si no existe, pregunta al usuario por `WP_URL`, `WP_USER`, `WP_APP_PASSWORD`
   del WordPress del cliente y créalo. Recuérdale instalar `wp-yoast-rest.php` vía Code Snippets
   si todavía no lo hizo.
5. **¿El entorno de esta sesión tiene acceso de red al dominio del cliente?** Pruébalo con un
   curl simple. Si falla, dile exactamente cómo habilitarlo (Network access → Custom → Allowed
   domains en la configuración del entorno) antes de seguir con cualquier cosa que toque WordPress.
6. **¿El cliente ya tenía un blog antes de este pipeline?** Si nunca se documentó una auditoría
   en este archivo, y hay contenido existente en su WordPress, detente y haz la auditoría (ver
   `CONVENTIONS.md`) antes de escribir nada nuevo — no lo saltes aunque el usuario no lo mencione.
7. **¿Hay al menos un artículo real publicado (o al menos en borrador) en WordPress?** Revisa
   `.published.json`. Si está vacío, ese es el siguiente paso: escribe y valida el primer
   artículo, corre `--dry-run`, luego push real.
8. **¿Existen ya las dos Routines estándar de este cliente** (contenido semanal + refresh de
   keywords mensual, definidas en `CONVENTIONS.md` → "Automatizaciones")? Si el usuario no lo ha
   mencionado, pregúntaselo explícitamente en vez de asumir que no las quiere — pero nunca las
   crees sin que él lo pida. Cuando las cree, usa los nombres, cron y contrato exactos de
   `CONVENTIONS.md` (no improvises variantes) y registra los `trigger_id` en `CLIENTES.md`.
9. **¿Este cliente ya está registrado en `CLIENTES.md`** del repo
   [`agenciadinamita/seo-pipeline-template`](https://github.com/agenciadinamita/seo-pipeline-template)?
   Si no, agrégalo (repo, dominio, `trigger_id` si aplica) en cuanto tengas esos datos — no hace
   falta esperar a que el usuario lo pida.

**Repórtale esto al usuario de forma breve** ("Ya tienes X e Y resueltos. Lo que sigue es Z —
¿seguimos con eso?") en vez de una lista larga — el checklist es para ti, no para mostrárselo
completo cada vez.

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

Si este cliente tiene restricciones de contenido, documéntalas aquí con la misma estructura: qué
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

**No publicar nada en vivo sin autorización explícita del cliente.** Borradores por default.

Para cualquier duda de "qué sigue", vuelve a correr el checklist de "Estado de configuración" de
arriba — es la fuente de verdad de en qué punto está este cliente, no una lista que se corre una
sola vez al principio.
