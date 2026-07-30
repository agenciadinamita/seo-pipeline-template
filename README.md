# SEO Pipeline — plantilla base

Punto de partida para montar el pipeline de contenido SEO (repo → WordPress → automatizaciones)
con un cliente nuevo. Es la versión genérica de un sistema ya probado en producción.

**Guía completa del sistema:** ver el playbook — pídele a Claude el link si no lo tienes a mano,
o revisa el historial de la sesión donde se creó esta plantilla.

**Registro de clientes activos:** [`CLIENTES.md`](./CLIENTES.md).

## Cómo arrancar con un cliente nuevo

1. **Clona/usa este repo como base** para el repo dedicado del cliente nuevo (uno por cliente,
   nunca compartido entre varios).
2. **Llena `CLAUDE.md`** con la información real del cliente — reemplaza cada `[PLACEHOLDER]`.
   Borra las secciones marcadas `EJEMPLO — borrar` una vez que entiendas el patrón. No copies las
   reglas de formato ahí — esas viven en `CONVENTIONS.md` y se comparten con todos los clientes.
3. **Borra `content/00-EJEMPLO-borrar-antes-de-usar.md`** una vez que hayas visto el formato — no
   es contenido real, es una plantilla de referencia.
4. **Configura WordPress:**
   - Crea un Application Password para un usuario admin (Ajustes → Usuarios → Perfil).
   - Instala `wp-yoast-rest.php` vía el plugin Code Snippets (sin esto, los campos de Yoast se
     pierden al publicar por API).
5. **Copia `.env.example` a `.env`** y llena `WP_URL`, `WP_USER`, `WP_APP_PASSWORD`.
6. **Investiga keywords reales** (Ubersuggest u otra fuente de datos de búsqueda) antes de definir
   los clusters de contenido en `CLAUDE.md` — nunca inventar volumen/dificultad.
7. Si el cliente **ya tiene un blog**, audítalo antes de escribir nada nuevo — ver `CONVENTIONS.md`.
8. Escribe el primer artículo, valida su frontmatter y conteo de palabras, corre:
   ```bash
   pip install -r requirements.txt
   python publish.py --dry-run
   python publish.py --only <slug-del-primer-articulo>
   ```
9. Revisa el borrador en WordPress antes de publicar nada en vivo.
10. **Agrega este cliente a [`CLIENTES.md`](./CLIENTES.md)** en este mismo repo plantilla.

## Estructura

```
CLAUDE.md               ← específico del cliente: negocio, restricciones, clusters, voz
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
template y abra un PR.

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
