# Registro de clientes activos

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
| AJI Patrimonial | [`agenciadinamita/aji-seo-content`](https://github.com/agenciadinamita/aji-seo-content) | ajipatrimonial.com | `trig_01W7tuwXpjT6GMgTu9QpjWPx` (v3, sin ejidal) | `trig_01HsvUuBQHzbhDkLYuAX6kbC` (mensual, sin verificar todavía) | 🟢 Activo | Restricción de cliente: nada de contenido sobre "terreno ejidal" (ver su `CLAUDE.md`). 49 posts legacy se conservan en vivo por decisión del cliente, sin redirects. |

*(Agrega una fila por cada cliente nuevo, en el mismo formato.)*

---

## Historial de cambios propagados desde el template

Cuando mejores algo en `seo-pipeline-template` y lo apliques manualmente a un cliente ya existente,
anótalo aquí — para saber qué clientes ya recibieron qué mejora y cuáles siguen atrasados.

| Fecha | Cambio | Aplicado a |
|---|---|---|
| — | (ejemplo) Corregido bug en `publish.py` que duplicaba categorías | — |

*(Vacío por ahora — este repo plantilla es nuevo, todavía no hay mejoras que propagar.)*
