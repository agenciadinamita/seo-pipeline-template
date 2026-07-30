# SEO Pipeline — plantilla base

Punto de partida para montar el pipeline de contenido SEO (repo → WordPress → automatizaciones)
con un cliente nuevo. Es la versión genérica de un sistema ya probado en producción.

**Guía completa del sistema:** ver el playbook — pídele a Claude el link si no lo tienes a mano,
o revisa el historial de la sesión donde se creó esta plantilla.

**Registro de clientes activos:** [`CLIENTES.md`](./CLIENTES.md).

## Cómo arrancar con un cliente nuevo

1. **Crea el repo del cliente en GitHub** (vacío está bien).
2. **Abre un chat nuevo** en claude.ai/code, conéctalo a ese repo, y dile:
   > "Trae la estructura base de agenciadinamita/seo-pipeline-template a este repo."
3. **A partir de ahí, `CLAUDE.md` mismo le dice al agente qué preguntar y qué sigue** — tiene una
   sección de auto-diagnóstico ("Estado de configuración") que corre sola al empezar cada sesión:
   detecta qué falta (datos del cliente, keywords, WordPress, primer artículo, automatización,
   registro en `CLIENTES.md`) y te va guiando paso a paso, sin que tengas que recordar el orden.

Si prefieres verlo explícito, este es el orden que sigue internamente:
- Llenar `CLAUDE.md` con datos reales del cliente (nunca copiar las reglas de formato ahí — esas
  viven en `CONVENTIONS.md`, compartidas).
- Investigar keywords reales y definir clusters.
- Configurar WordPress (Application Password + `wp-yoast-rest.php`) y habilitar el acceso de red
  al dominio del cliente en el entorno de la sesión.
- Auditar blog existente, si lo hay, antes de escribir nada nuevo.
- Escribir y validar el primer artículo, `--dry-run`, push real de prueba.
- Decidir sobre automatización.
- Registrar al cliente en `CLIENTES.md`.

## Estructura

```
CLAUDE.md               ← específico del cliente: negocio, restricciones, clusters, voz,
                           y el checklist de auto-diagnóstico que guía el onboarding
CONVENTIONS.md          ← compartido entre TODOS los clientes: formato, frontmatter, no-negociables
CLIENTES.md              ← (solo en este repo plantilla) registro de qué clientes existen
content/                 ← artículos, uno por archivo .md, con frontmatter
keyword_backlog.json     ← cola de oportunidades de keywords, con status
.published.json          ← idempotencia: qué ya se subió a WP y con qué status
publish.py                ← script que empuja content/ → WordPress
wp-yoast-rest.php         ← snippet PHP para exponer campos de Yoast por REST
requirements.txt
.env.example
```

## Cómo actualizar un cliente ya existente cuando mejoras el template ("pull")

Esto **no pasa solo** — es una acción que tú disparas, cliente por cliente, cuando quieras. Entra
al chat de ese cliente y dile algo como:

> "Trae la versión más reciente de CONVENTIONS.md desde agenciadinamita/seo-pipeline-template y
> reemplaza el archivo CONVENTIONS.md de este repo con esa versión (créalo si no existe todavía).
> No toques CLAUDE.md ni content/. Ábrelo como PR para que yo lo revise antes de mergear."

Para actualizar los archivos de código (`publish.py`, `wp-yoast-rest.php`, `requirements.txt`), es
la misma idea: pídele que traiga la versión más reciente de esos archivos específicos desde el
template y abra un PR. Lo mismo aplica si mejoras el checklist de auto-diagnóstico en `CLAUDE.md`
— eso también hay que pedirlo explícitamente por cliente, no se propaga solo.

Usa [`CLIENTES.md`](./CLIENTES.md) para saber a qué clientes tienes que pedírselo — y anota ahí
cuando ya lo hayas hecho, en la tabla de "Historial de cambios propagados".

## Principios que no cambian entre clientes

- **`publish.py` nunca publica en vivo por default** — siempre `draft`, gate de aprobación humana.
- **Nunca inventar cifras específicas** en contenido legal/financiero/técnico — rangos,
  orientativos, remitir a fuente oficial.
- **Auditar contenido existente antes de escribir contenido nuevo**, si el cliente ya tiene blog.
- **Las decisiones de negocio del cliente se documentan en su `CLAUDE.md` con fecha**, sobre todo
  las que revierten una estrategia anterior — para que una sesión futura no las reabra sin saberlo.
- **Las automatizaciones en la nube (Routines) no leen ningún repo** — cualquier regla que deban
  seguir tiene que estar embebida directamente en su prompt, no solo en `CLAUDE.md`/`CONVENTIONS.md`.
- **Actualizar un cliente existente desde el template es manual, cliente por cliente** — no hay
  sincronización automática. Ver la sección de arriba.
