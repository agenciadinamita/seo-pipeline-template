Este archivo vive en el repo plantilla (`seo-pipeline-template`), no en el repo de ningún cliente
— es el único lugar donde queda anotado qué clientes existen, dónde vive cada uno, y qué
automatizaciones tienen corriendo. Sin esto, "propagar una mejora a todos los clientes" depende de
la memoria de una persona.

**Cuándo actualizarlo:**
- Al arrancar un cliente nuevo (agrega su fila apenas crees su repo).
- Al crear o reemplazar una Routine (actualiza el `trigger_id` — recuerda que un `trigger_id` viejo
  que ya borraste no sirve de nada aquí, bórralo también de esta tabla).
- Al pausar o dar de baja a un cliente (cambia su Estado, no borres la fila — es historial).

**Cómo usarlo:** antes de propagar un cambio del template a los clientes existentes, revisa esta
tabla para saber exactamente cuáles repos y rutinas tocar — no confíes en la memoria de la sesión.

---

## Clientes

| Cliente | Repo | Dominio WordPress | Rutina semanal (trigger_id) | Rutina refresh (trigger_id) | Estado | Notas |
|---|---|---|---|---|---|---|
| AJI Patrimonial | [`agenciadinamita/aji-seo-content`](https://github.com/agenciadinamita/aji-seo-content) | ajipatrimonial.com | `trig_013ptnrwt3PSAFNzkHURfphv` ("AJI Patrimonial — Contenido semanal", contrato estándar CONVENTIONS.md) | `trig_01CgDfQtmrchiujGKXJAAnRq` ("AJI Patrimonial — Refresh keywords mensual", contrato estándar CONVENTIONS.md) | 🟢 Activo | Restricción de cliente: nada de contenido sobre "terreno ejidal" (ver su `CLAUDE.md`). 49 posts legacy se conservan en vivo por decisión del cliente, sin redirects. Conector Ubersuggest sigue sin poder adjuntarse vía API (restricción de la organización) — la rutina mensual reporta y se detiene si no lo tiene disponible. |
| Transportes Niu | [`agenciadinamita/transportes-niu-seo-content`](https://github.com/agenciadinamita/transportes-niu-seo-content) | transportesniu.com | `trig_013XBxmW31dNJJQasrquoTmM` ("Transportes Niu — Contenido semanal", contrato estándar CONVENTIONS.md) | `trig_01Jk8vMtwK7gbVmDX7PZXCP8` ("Transportes Niu — Refresh keywords mensual", contrato estándar CONVENTIONS.md) | 🟢 Activo | 3 clusters completos (8 artículos en `content/`, publicados como `draft` en WordPress). 40 posts legacy se conservan por decisión del cliente (2026-07-30), sin redirects ni consolidación. Whitelist de links externos: SICT y CANACAR. Conector Ubersuggest tampoco disponible para esta Routine (misma restricción de organización que AJI) — la rutina mensual reporta y se detiene si no lo tiene disponible. |

*(Agrega una fila por cada cliente nuevo, en el mismo formato.)*

---

## Historial de cambios propagados desde el template

Cuando mejores algo en `seo-pipeline-template` y lo apliques manualmente a un cliente ya existente,
anótalo aquí — para saber qué clientes ya recibieron qué mejora y cuáles siguen atrasados.

| Fecha | Cambio | Aplicado a |
|---|---|---|
| 2026-07-30 | es-MX por default (incl. `image_alt`) + contrato estándar de las 2 Routines en `CONVENTIONS.md` | AJI Patrimonial ([PR #2](https://github.com/agenciadinamita/aji-seo-content/pull/2), mergeado — creó `CONVENTIONS.md` por primera vez, no existía) · Transportes Niu ([PR #2](https://github.com/agenciadinamita/transportes-niu-seo-content/pull/2), mergeado) |
| 2026-07-30 | `image_alt` backfill en los 24 artículos activos + sync de `keyword_backlog.json` ([PR #3](https://github.com/agenciadinamita/aji-seo-content/pull/3), pendiente de revisión) y recreación de las 2 Routines siguiendo el contrato estándar (acceso a repo, workflow de PR, ya no embebidas standalone) | AJI Patrimonial |
