# Guía para principiantes — Gestión de Nodos

Esta guía explica el proyecto **desde cero**: qué es, cómo está armado, cómo leer el código aunque no
sepas mucho Python y cómo probarlo. Leela en orden. Si una palabra no se entiende, buscala en el
[Glosario](#13-glosario).

---

## Índice
1. [Qué es este proyecto](#1-qué-es-este-proyecto)
2. [La idea en un dibujo](#2-la-idea-en-un-dibujo)
3. [Qué hay en cada carpeta](#3-qué-hay-en-cada-carpeta)
4. [Cómo instalarlo y usarlo](#4-cómo-instalarlo-y-usarlo)
5. [Python mínimo para leer el código](#5-python-mínimo-para-leer-el-código)
6. [SQL y SQLite mínimo](#6-sql-y-sqlite-mínimo)
7. [JSON en 1 minuto](#7-json-en-1-minuto)
8. [Las 4 capas del sistema](#8-las-4-capas-del-sistema)
9. [Recorrido completo: qué pasa cuando creás un lote](#9-recorrido-completo-qué-pasa-cuando-creás-un-lote)
10. [Los tests: qué son y cómo leerlos](#10-los-tests-qué-son-y-cómo-leerlos)
11. [Cómo leer un error](#11-cómo-leer-un-error)
12. [Git y GitHub en este proyecto](#12-git-y-github-en-este-proyecto)
13. [Glosario](#13-glosario)
14. [Preguntas frecuentes](#14-preguntas-frecuentes)

---

## 1. Qué es este proyecto

Es una **base de datos para organizar información de una empresa**, pensada como una **red de fichas
conectadas**, parecida al "grafo" de Obsidian o a la app de referencia **NodoERP**.

Tres ideas centrales:

| Idea | Qué significa | Ejemplo |
|---|---|---|
| **Lote** (nodo) | Una ficha con información precisa, separada en campos | Lote "Acme" del tipo *cliente*: razón social = "Acme SA", empleados = 12 |
| **Relación** (unión) | Una flecha que une dos lotes y dice cómo se relacionan | "Acme" → *paga* → "Factura 9042" |
| **Registro** | Un cuaderno donde se anota cada cambio | "06/10 14:32 — ana editó el lote 1: antes 'Acme', después 'Acme SA'" |

Además, cada lote pertenece a un **tipo de lote**, que funciona como un **molde**: dice qué campos
tiene que tener. Así ningún lote queda con datos mezclados o de más.

> **Materia:** Metodología y Testing (3.er semestre). Por eso el proyecto se trabaja **por versiones** y con
> **tests escritos antes que el código** (ver [HOJA-DE-RUTA.md](../HOJA-DE-RUTA.md)).

---

## 2. La idea en un dibujo

```
   TIPOS DE LOTE (moldes)                 LOTES (fichas) y RELACIONES (flechas)
  ┌────────────────────────┐
  │ cliente                │           ┌─────────┐   paga    ┌──────────────┐
  │  - razon_social (texto)│  ───────▶ │  Acme   │ ────────▶ │ Factura 9042 │
  │  - empleados (número)  │           └─────────┘           └──────────────┘
  └────────────────────────┘                │ abrió
  ┌────────────────────────┐                ▼
  │ factura                │           ┌─────────────┐
  │  - numero (texto)      │           │ Ticket 4912 │
  │  - monto (número)      │           └─────────────┘
  └────────────────────────┘

  REGISTRO (todo lo que pasó, del más nuevo al más viejo)
  #5  ana   relacionar   Acme → Ticket 4912
  #4  ana   relacionar   Acme → Factura 9042
  #3  ana   crear_lote   Ticket 4912
  ...
```

---

## 3. Qué hay en cada carpeta

```
gestion-nodos/
├── README.md               ← portada del proyecto
├── HOJA-DE-RUTA.md         ← el plan: qué se hace en cada versión (v1 … v5)
├── DISENO.md               ← el "plano" técnico de la v1: tablas, funciones, API
├── PUNTO-DE-GUARDADO.md    ← bitácora del avance: qué está hecho y qué sigue
├── docs/
│   └── GUIA-PRINCIPIANTES.md  ← esta guía
├── nodos/                  ← EL CÓDIGO del sistema (un "paquete" de Python)
│   ├── config.py           ← ★ LISTA DE MÓDULOS ACTIVOS (acá se quitan o agregan)
│   ├── app.py              ← el servidor web: carga las rutas de cada módulo activo
│   ├── web.py              ← ayudantes para las rutas (conexión, usuario, datos del pedido)
│   ├── repositorio.py      ← "fachada": junta las funciones de todos los módulos en un solo lugar
│   ├── templates/index.html ← la página que dibuja el grafo
│   ├── nucleo/             ← lo que el sistema necesita SIEMPRE
│   │   ├── db.py           ← abre la base y crea las tablas
│   │   ├── esquema.sql     ← tabla `registro` (la bitácora)
│   │   ├── registro.py     ← anotar acciones en la bitácora
│   │   ├── validacion.py   ← valida que un lote tenga los campos correctos
│   │   ├── eventos.py      ← avisos entre módulos
│   │   └── modulos.py      ← carga los módulos y revisa dependencias
│   └── modulos/            ← piezas intercambiables, una carpeta por módulo
│       ├── tipos/          ← moldes de lote
│       ├── lotes/          ← las fichas
│       ├── relaciones/     ← las flechas
│       ├── grafo/          ← arma la red para dibujarla
│       └── historial/      ← consulta la bitácora
├── tests/                  ← LAS PRUEBAS automáticas
│   ├── conftest.py         ← preparación común a todos los tests
│   ├── test_lotes.py       ← prueba el validador
│   ├── test_repositorio.py ← prueba las acciones sobre la base
│   ├── test_api.py         ← prueba el servidor web
│   └── test_modulos.py     ← prueba que se puedan quitar módulos
├── futuro/                 ← material guardado para versiones futuras (PostgreSQL, diseño completo)
├── semilla.py              ← carga datos de ejemplo
├── pyproject.toml          ← configuración de pytest
├── .venv/                  ← el "entorno virtual": Python y librerías del proyecto (no se sube a GitHub)
└── .gitignore              ← lista de archivos que Git debe ignorar
```

> Si algún archivo no aparece todavía, mirá `PUNTO-DE-GUARDADO.md` para saber en qué paso estamos.

---

## 4. Cómo instalarlo y usarlo

Todos los comandos se escriben en una **terminal** abierta en la carpeta del proyecto.
En VS Code: menú *Terminal → Nueva terminal* (o `Ctrl + ñ`).

### 4.1 La primera vez (en una compu nueva)
```bash
python3 -m venv .venv                 # crea el entorno virtual (una "caja" con su propio Python)
.venv/bin/pip install flask pytest    # instala las 2 librerías que usamos dentro de esa caja
```
> **¿Por qué `.venv/bin/...` delante de todo?** Para usar el Python *de la caja* y no el del sistema.
> Así las librerías del proyecto no se mezclan con las de otros programas.

### 4.2 Correr los tests
```bash
.venv/bin/pytest -v        # -v = "verbose": muestra cada test con su resultado
.venv/bin/pytest -q        # -q = "quiet": solo el resumen
.venv/bin/pytest -v tests/test_lotes.py   # solo un archivo
```
Verde (`PASSED`) = anda. Rojo (`FAILED`/`ERROR`) = algo no cumple lo esperado.

### 4.3 Usar la aplicación (cuando la v1 esté completa)
```bash
.venv/bin/python semilla.py        # crea nodos.db con datos de ejemplo
.venv/bin/python -m nodos.app      # levanta el servidor
```
Después abrí **http://127.0.0.1:5000** en el navegador. Para apagar el servidor: `Ctrl + C` en la terminal.

---

## 5. Python mínimo para leer el código

No hace falta saber todo Python. Con esto alcanza para entender el proyecto.

### 5.1 Variables y tipos de datos
```python
nombre = "Acme"          # texto (str)
empleados = 12           # número entero (int)
precio = 99.5            # número con decimales (float)
activo = True            # booleano (bool): True o False
etiquetas = ["a", "b"]   # lista (list): varios valores en orden
ficha = {"razon_social": "Acme", "empleados": 12}   # diccionario (dict): etiqueta → valor
nada = None              # "vacío", ausencia de valor
```
- Un **diccionario** es como una ficha: `ficha["razon_social"]` devuelve `"Acme"`.
- Una **lista** se recorre en orden: `etiquetas[0]` es `"a"` (se cuenta desde 0).

### 5.2 Funciones
```python
def saludar(nombre, saludo="Hola"):     # def = "defino una función"; saludo tiene valor por defecto
    """Devuelve un saludo."""          # docstring: explicación para humanos
    return f"{saludo}, {nombre}"       # return = lo que la función entrega
                                       # f"..." = texto con valores incrustados entre { }

saludar("Ana")              # → "Hola, Ana"
saludar("Ana", "Chau")      # → "Chau, Ana"
```
**La sangría (los espacios a la izquierda) importa.** Todo lo que está más adentro de `def` pertenece a esa función.

### 5.3 Decisiones y repeticiones
```python
if empleados > 10:          # si...
    print("empresa mediana")
elif empleados > 0:         # si no, si...
    print("empresa chica")
else:                       # si no...
    print("sin empleados")

for e in etiquetas:         # para cada elemento de la lista...
    print(e)
```

### 5.4 Errores a propósito
```python
if lote is None:
    raise ValueError("el lote no existe")   # corta la función y avisa que hubo un error
```
En este proyecto, cuando alguien usa mal el sistema (lote que no existe, datos inválidos…) se lanza un
`ValueError`. La web lo convierte en una respuesta "400 — error" para el navegador.

```python
try:
    algo_que_puede_fallar()
except ValueError as e:     # si falló con ValueError, en vez de romperse hace esto:
    print("falló:", e)
```

### 5.5 Importar
```python
import sqlite3                      # traigo una librería entera
from nodos import db                # traigo el archivo nodos/db.py
from nodos.lotes import validar_contenido   # traigo una sola función de nodos/lotes.py
from nodos import repositorio as repo       # lo traigo con un apodo más corto
```

### 5.6 Comentarios
```python
# Esto es un comentario: Python lo ignora, es para quien lee.
```

---

## 6. SQL y SQLite mínimo

- **SQL** es el idioma para hablar con una base de datos relacional (tablas con filas y columnas).
- **SQLite** es una base de datos que vive en **un solo archivo** (`nodos.db`) y viene incluida con Python:
  no hay que instalar ningún servidor. Ideal para la v1. En la v4 se pasa a **PostgreSQL**, que es lo
  que usan las empresas.

Las 4 órdenes básicas (el famoso **CRUD**: *Create, Read, Update, Delete*):
```sql
INSERT INTO lotes (tipo_id, titulo, contenido) VALUES (1, 'Acme', '{"razon_social":"Acme"}');  -- crear
SELECT id, titulo FROM lotes WHERE borrado = 0;                                              -- leer
UPDATE lotes SET titulo = 'Acme SA', version = version + 1 WHERE id = 1;                      -- modificar
DELETE FROM relaciones WHERE id = 3;                                                          -- borrar
```

Conceptos que aparecen en `esquema.sql`:

| Palabra | Qué significa |
|---|---|
| `CREATE TABLE IF NOT EXISTS` | crea la tabla solo si todavía no existe (así se puede ejecutar 2 veces sin error) |
| `PRIMARY KEY` | el identificador único de cada fila (el `id`) |
| `REFERENCES lotes(id)` | **clave foránea**: este valor tiene que ser el id de un lote que exista. Es el "puntero" |
| `NOT NULL` | la columna no puede quedar vacía |
| `DEFAULT ...` | valor que se pone solo si no se indica otro |
| `UNIQUE(...)` | no puede haber dos filas con esos mismos valores (ej.: la misma relación repetida) |
| `CHECK(...)` | una regla que cada fila debe cumplir (ej.: `origen_id <> destino_id`, un lote no se une consigo mismo) |
| `CURRENT_TIMESTAMP` | la fecha y hora actuales |

### Las 4 tablas del proyecto
| Tabla | Para qué | Columnas importantes |
|---|---|---|
| `tipos_lote` | los moldes | `nombre`, `campos` (JSON con la lista de campos) |
| `lotes` | las fichas | `tipo_id` (de qué molde), `titulo`, `contenido` (JSON), `version`, `borrado` |
| `relaciones` | las flechas | `origen_id`, `destino_id`, `tipo` ("paga", "parte_de"…) |
| `registro` | la bitácora | `fecha`, `usuario`, `accion`, `lote_id`, `detalle` (JSON con antes/después) |

> **Borrado lógico:** cuando se "borra" un lote no se elimina la fila: se marca `borrado = 1`. Así el historial
> nunca pierde información (requisito de trazabilidad).

---

## 7. JSON en 1 minuto

**JSON** es una forma estándar de escribir datos como texto. Se parece mucho a los diccionarios de Python:
```json
{
  "razon_social": "Acme SA",
  "empleados": 12,
  "activo": true,
  "etiquetas": ["proveedor", "nacional"]
}
```
En el proyecto se usa JSON para: el **contenido** de cada lote, la **definición de campos** de cada tipo, el
**detalle** de cada registro y las **respuestas de la API** web.

En Python: `json.dumps(dic)` convierte un diccionario en texto JSON (para guardarlo) y `json.loads(texto)`
hace lo contrario (para leerlo).

Ejemplo de definición de campos de un tipo de lote:
```json
[
  {"nombre": "razon_social", "tipo": "texto",  "obligatorio": true},
  {"nombre": "empleados",    "tipo": "numero", "obligatorio": false}
]
```
Tipos de campo permitidos: `texto`, `numero`, `fecha` (formato `AAAA-MM-DD`), `booleano` (`true`/`false`) y `lista`.

---

## 8. Las 4 capas del sistema

Cada capa tiene **una sola responsabilidad** y solo habla con la de abajo. Analogía: un restaurante.

```
  Navegador (vos)
       │  pide "crear lote"            ◀── el CLIENTE del restaurante
       ▼
  ┌──────────────┐
  │   app.py     │  recibe el pedido web, devuelve JSON      ◀── el MOZO
  └──────┬───────┘
         ▼
  ┌──────────────┐     ┌────────────┐
  │repositorio.py│ ──▶ │  lotes.py  │  ¿el contenido es válido?   ◀── COCINERO + CONTROL DE CALIDAD
  └──────┬───────┘     └────────────┘
         ▼
  ┌──────────────┐
  │    db.py     │  abre la base y crea las tablas      ◀── la LLAVE de la despensa
  └──────┬───────┘
         ▼
     nodos.db  (tablas de esquema.sql)                   ◀── la DESPENSA
```


### 8.0 Arquitectura modular: piezas que se ponen y se sacan

El sistema está dividido en un **núcleo** (lo imprescindible) y **módulos** (piezas intercambiables).
Cada módulo es una carpeta en `nodos/modulos/` con siempre la misma forma:

```
nodos/modulos/relaciones/
├── __init__.py    ← dice de qué otros módulos depende (DEPENDE_DE) y qué funciones ofrece
├── servicio.py    ← la lógica: funciones que trabajan con la base de datos
├── rutas.py       ← las direcciones web del módulo (opcional)
└── esquema.sql    ← las tablas que el módulo necesita (opcional)
```

**Los módulos activos se eligen en `nodos/config.py`:**
```python
MODULOS = ["tipos", "lotes", "relaciones", "grafo", "historial"]
```
- **Quitar un módulo:** borrarlo de esa lista. Sus tablas no se crean, sus rutas web desaparecen y la página
  oculta sus formularios. Si otro módulo lo necesita, el sistema avisa con un error claro
  (ej.: *"el módulo 'grafo' necesita 'relaciones'"*).
- **Agregar un módulo:** copiar la estructura de una carpeta existente, escribir su lógica y sumarlo a la lista.

| Módulo | Depende de | Tabla | Para qué |
|---|---|---|---|
| `tipos` | — | `tipos_lote` | moldes de lote |
| `lotes` | tipos | `lotes` | las fichas |
| `relaciones` | lotes | `relaciones` | las flechas |
| `grafo` | lotes, relaciones | — | arma la red para dibujar |
| `historial` | — | (usa `registro` del núcleo) | consultar la bitácora |

**Eventos (cómo se avisan los módulos sin depender entre sí):** cuando se borra un lote, el módulo `lotes`
*emite* el evento `"lote_borrado"`. El módulo `relaciones` está *suscripto* a ese evento y quita las flechas del
lote. Así `lotes` no necesita saber que `relaciones` existe: si quitás `relaciones`, `lotes` sigue andando.

**La fachada `repositorio.py`:** junta las funciones de todos los módulos activos para poder usar
`repo.crear_lote(...)` sin saber en qué carpeta está cada cosa. Es lo que usan los tests y `semilla.py`.

> En las secciones siguientes, "el repositorio" significa el conjunto de los `servicio.py` de los módulos.

### 8.1 `esquema.sql` — la despensa
Solo SQL. Cada módulo trae el `esquema.sql` de su tabla y el núcleo trae el de `registro`. No tienen lógica.

### 8.2 `nucleo/db.py` — la llave
Dos funciones:
- `conectar(ruta)`: abre la base. Con `":memory:"` crea una base **temporal en memoria** (se usa en los tests:
  cada test arranca con una base limpia y nada queda guardado). Activa las claves foráneas
  (`PRAGMA foreign_keys = ON`, que SQLite trae apagadas) y hace que cada fila se pueda leer por nombre de columna.
- `crear_esquema(conn, modulos)`: ejecuta el `esquema.sql` del núcleo y el de cada módulo activo.

### 8.3 `nucleo/validacion.py` — control de calidad
Una sola función: `validar_contenido(campos, contenido)`. Recibe el molde y la ficha y devuelve una
**lista de errores**. Lista vacía = todo bien.

| Contenido | Resultado |
|---|---|
| `{"razon_social": "Acme"}` | `[]` ✔ |
| `{}` | `["falta el campo obligatorio razon_social"]` |
| `{"razon_social": "Acme", "color": "rojo"}` | `["el campo color no está definido en el tipo"]` |
| `{"razon_social": 5}` | `["razon_social debe ser texto"]` |

> Detalle curioso: en Python `True` cuenta como número (vale 1). Por eso el validador revisa aparte que un campo
> `numero` **no** sea booleano. Hay un test justo para eso (`test_booleano_no_es_numero`).

### 8.4 Los `servicio.py` de cada módulo — el cocinero
Acá están **todas las acciones**, repartidas por módulo. Todas reciben `conn` (la conexión a la base) como primer dato.
Regla de oro: **cada acción que modifica algo también escribe una fila en `registro`**.

| Acción | Qué hace |
|---|---|
| `crear_tipo` | crea un molde |
| `crear_lote` | valida y crea una ficha |
| `editar_lote` | cambia título o contenido, sube la versión y registra el antes y el después |
| `borrar_lote` | borrado lógico; también quita sus flechas |
| `relacionar` / `quitar_relacion` | crea o quita una flecha |
| `obtener_lote`, `listar_lotes`, `listar_tipos` | consultas |
| `vecinos(lote)` | con qué lotes está unido (y si la flecha "sale" o "entra") |
| `grafo()` | todos los nodos y flechas, listo para dibujar |
| `historial(lote)` | el registro, del más nuevo al más viejo |

La tabla completa con lo que devuelve cada una está en [DISENO.md](../DISENO.md).

### 8.5 `app.py`, los `rutas.py` y `templates/index.html` — el mozo y el salón
- **Flask** es una librería para hacer servidores web en Python.
- Cada módulo define sus **rutas** en su `rutas.py` (un *Blueprint* de Flask): una dirección + un método, que ejecutan una función de su `servicio.py`. `app.py` registra las rutas de los módulos activos.
- Los **métodos HTTP** dicen qué querés hacer: `GET` = leer, `POST` = crear, `PUT` = modificar, `DELETE` = borrar.
- Las respuestas llevan un **código de estado**: `200` OK, `201` creado, `400` pedido inválido, `404` no existe.

| Ruta | Qué hace |
|---|---|
| `GET /` | la página con el grafo |
| `GET /api/grafo` | nodos y flechas en JSON |
| `GET /api/lotes/5` | el lote 5, sus vecinos y su historial |
| `POST /api/lotes` | crear un lote (los datos van en JSON) |
| `PUT /api/lotes/5` | editar el lote 5 |
| `DELETE /api/lotes/5` | borrar el lote 5 |
| `POST /api/relaciones` / `DELETE /api/relaciones/3` | unir / separar |
| `GET /api/historial` | todo el registro |

Quién hizo el cambio se indica con el encabezado `X-Usuario` (en la v1 no hay contraseñas; llegan en la v2).

La página `index.html` usa **vis-network** (la misma librería que NodoERP) para dibujar el grafo. Al hacer clic
en un nodo se abre un panel lateral con 3 pestañas: **Detalle**, **JSON** e **Historial**.

---

## 9. Recorrido completo: qué pasa cuando creás un lote

Supongamos que desde la web creás el lote "Acme" de tipo cliente:

1. **Navegador** → envía `POST /api/lotes` con `{"tipo_id": 1, "titulo": "Acme", "contenido": {"razon_social": "Acme"}}`
   y el encabezado `X-Usuario: ana`.
2. **`modulos/lotes/rutas.py`** → la ruta lee ese JSON y el usuario, y llama a
   `servicio.crear_lote(conn, 1, "Acme", {"razon_social": "Acme"}, "ana")`.
3. **`modulos/lotes/servicio.py`**:
   1. Le pide al módulo `tipos` los campos del tipo 1. Si no existe → `ValueError`.
   2. Llama a `nucleo/validacion.validar_contenido(campos_del_tipo, contenido)`. Si hay errores → `ValueError` con esos errores.
   3. `INSERT INTO lotes ...` guardando el contenido como texto JSON.
   4. `INSERT INTO registro ...` con `accion = "crear_lote"`, `usuario = "ana"` y `detalle = {"despues": {...}}`.
   5. `conn.commit()` → confirma y guarda los cambios en el archivo.
   6. Devuelve el `id` del lote nuevo.
4. **La ruta** → responde `201` con `{"id": 7}`.
   Si hubo `ValueError`, `app.py` lo atrapa y responde `400` con `{"error": "..."}`.
5. **Navegador** → vuelve a pedir `/api/grafo` y dibuja el nodo nuevo.

---

## 10. Los tests: qué son y cómo leerlos

### 10.1 La idea
Un **test** es un pequeño programa que usa el sistema y **verifica** que el resultado sea el esperado. Si
mañana alguien rompe algo, los tests lo detectan solos.

En este proyecto se trabaja con **TDD (Test Driven Development)**:
1. **Rojo:** primero se escribe el test (falla, porque el código no existe todavía).
2. **Verde:** se escribe el código mínimo para que pase.
3. **Refactor:** se mejora el código sin romper el test.

### 10.2 Tipos de prueba del proyecto
| Archivo | Tipo | Qué prueba |
|---|---|---|
| `test_lotes.py` | **unitaria** | una función sola (el validador), sin base de datos |
| `test_repositorio.py` | **integración** | el repositorio junto con una base SQLite real (en memoria) |
| `test_api.py` | **de API / sistema** | el servidor web completo, simulando un navegador |

### 10.3 Cómo leer un test
```python
def test_borrar_lote(conn, datos):
    repo.relacionar(conn, datos["a"], datos["b"], "referencia", "ana")  # PREPARAR: uno A con B
    repo.borrar_lote(conn, datos["a"], "ana")                           # ACTUAR: borro A
    assert repo.obtener_lote(conn, datos["a"])["borrado"] is True        # VERIFICAR: A figura borrado
    assert repo.vecinos(conn, datos["b"]) == []                          # VERIFICAR: B quedó sin vecinos
```
- Todo test es una función cuyo nombre empieza con `test_`. pytest las encuentra solo.
- Casi todos siguen el patrón **Preparar → Actuar → Verificar** (en inglés *Arrange, Act, Assert*).
- `assert X` = "verificá que X sea verdadero". Si no lo es, el test falla y pytest muestra por qué.
- `with pytest.raises(ValueError):` = "verificá que lo de adentro **lance** un ValueError". Se usa para probar
  que el sistema **rechaza** lo inválido.
- `@pytest.mark.parametrize(...)` = correr el mismo test varias veces con datos distintos.

### 10.4 Fixtures: la preparación automática (`conftest.py`)
Los parámetros `conn` y `datos` de los tests **no los pasa nadie a mano**: pytest los fabrica antes de cada test
porque están definidos como **fixtures** en `tests/conftest.py`:
- `conn` → una base de datos nueva, vacía y en memoria, con las tablas creadas.
- `datos` → sobre esa base, un tipo "cliente" y dos lotes: **A** ("Acme") y **B** ("Beta").

Así cada test arranca de cero y los tests no se pisan entre sí.

### 10.5 Qué conviene leer primero
`tests/test_repositorio.py`: cada test cuenta una "historia" del sistema y es la mejor documentación de cómo
se comporta.

---

## 11. Cómo leer un error

Cuando un test falla, pytest muestra algo así:
```
FAILED tests/test_lotes.py::test_falta_obligatorio - AssertionError: assert 0 == 1
```
- `tests/test_lotes.py` → el archivo.
- `test_falta_obligatorio` → el test que falló.
- `AssertionError: assert 0 == 1` → esperaba 1 error y el código devolvió 0.

Errores frecuentes de Python:
| Error | Significa |
|---|---|
| `ModuleNotFoundError` / `ImportError` | no encuentra un archivo o función (¿existe? ¿está bien escrito el nombre?) |
| `NameError` | se usa una variable que no existe |
| `TypeError` | se pasó un dato del tipo equivocado o con la cantidad equivocada de parámetros |
| `KeyError: 'x'` | se pidió la clave `'x'` a un diccionario que no la tiene |
| `IndentationError` | la sangría está mal |
| `sqlite3.IntegrityError` | se violó una regla de la base (UNIQUE, CHECK, clave foránea) |

> **Consejo:** leé el error **de abajo hacia arriba**: la última línea dice *qué* pasó y las de arriba *dónde*.

---

## 12. Git y GitHub en este proyecto

- **Git** guarda el historial de cambios del código. Cada "foto" del proyecto se llama **commit**.
- **GitHub** guarda una copia en internet. El repositorio es **privado**: `LDWinter/gestion-nodos`.

Comandos útiles:
```bash
git status            # qué archivos cambiaron
git log --oneline     # lista de commits (el más nuevo arriba)
git diff              # qué cambió exactamente, línea por línea
git pull              # traer lo último de GitHub
git add -A && git commit -m "mensaje"   # sacar una foto
git push              # subir a GitHub
```
En VS Code el ícono de **Control de código fuente** (3 circulitos unidos) muestra todo esto con botones.

Metodología: cada versión (v1, v2…) se trabaja en su **rama** y se marca con un **tag** al terminarla.

---

## 13. Glosario

| Término | Explicación simple |
|---|---|
| **Nodo / lote** | una ficha de información con campos definidos |
| **Tipo de lote** | el molde que dice qué campos tiene un lote |
| **Relación / arista** | la flecha que une dos lotes |
| **Grafo** | el conjunto de nodos y flechas: la "red" |
| **Registro / historial** | la bitácora de cambios (quién, cuándo, qué, antes/después) |
| **Trazabilidad** | poder reconstruir quién cambió qué y cuándo |
| **Base de datos relacional** | datos en tablas con filas y columnas, relacionadas por ids |
| **SQL** | idioma para pedirle cosas a la base de datos |
| **SQLite** | base de datos en un solo archivo, incluida en Python |
| **PostgreSQL** | base de datos "de empresa" (para la v4) |
| **Clave primaria (PK)** | el id único de cada fila |
| **Clave foránea (FK) / puntero** | columna que apunta al id de otra tabla |
| **Borrado lógico** | marcar como borrado en vez de eliminar |
| **JSON** | formato de texto estándar para datos tipo diccionario |
| **CRUD** | crear, leer, actualizar, borrar |
| **Función** | bloque de código con nombre que recibe datos y devuelve un resultado |
| **Módulo** | un archivo `.py` |
| **Paquete** | una carpeta con módulos (y un `__init__.py`) |
| **Librería** | código ya hecho que se importa (Flask, pytest, sqlite3) |
| **Entorno virtual (.venv)** | "caja" con el Python y las librerías del proyecto |
| **API** | la puerta por la que otro programa (ej.: la página web) le pide cosas al sistema |
| **Ruta / endpoint** | una dirección de la API, ej. `/api/lotes` |
| **HTTP: GET/POST/PUT/DELETE** | leer / crear / modificar / borrar por la web |
| **Código de estado** | número de la respuesta: 200 OK, 201 creado, 400 inválido, 404 no existe |
| **Flask** | librería para hacer servidores web en Python |
| **vis-network** | librería de JavaScript que dibuja grafos en el navegador |
| **Test unitario** | prueba una pieza sola |
| **Test de integración** | prueba varias piezas juntas (ej.: código + base) |
| **TDD** | escribir el test antes que el código |
| **Fixture** | preparación automática que pytest hace antes de un test |
| **assert** | "verificá que esto sea verdad" |
| **Commit (Git)** | una foto del código en un momento |
| **Commit (base de datos)** | confirmar los cambios para que queden guardados |
| **Repositorio (Git)** | la carpeta del proyecto con todo su historial |
| **`repositorio.py`** | ojo, otra cosa: la fachada que junta las acciones de todos los módulos |
| **Módulo (del sistema)** | carpeta de `nodos/modulos/` que se activa o desactiva en `config.py` |
| **Núcleo** | la parte imprescindible (`nodos/nucleo/`) |
| **Evento** | aviso que un módulo emite y otros escuchan, para no depender entre sí |
| **Blueprint** | grupo de rutas web de Flask; cada módulo tiene el suyo |
| **Fachada** | un archivo que reúne funciones de varios lugares en uno solo |

---

## 14. Preguntas frecuentes

**¿Por qué SQLite y no PostgreSQL?**
Para la v1 se buscó algo simple: SQLite no necesita instalar nada y la base es un archivo. El diseño ya
contempla pasar a PostgreSQL en la v4 (borrador en `futuro/`).

**¿Por qué el contenido de los lotes se guarda como JSON y no en columnas?**
Porque cada tipo de lote tiene campos distintos. Con JSON una sola tabla `lotes` sirve para todos los
tipos, y el orden lo garantiza el validador (`lotes.py`), que exige exactamente los campos del molde.

**¿Cómo agrego un módulo nuevo, por ejemplo "adjuntos"?**
1. Copiá la carpeta `nodos/modulos/historial/` como `nodos/modulos/adjuntos/`.
2. En `__init__.py` poné de qué depende (`DEPENDE_DE = ["lotes"]`) y qué funciones exporta.
3. Escribí sus tablas en `esquema.sql`, su lógica en `servicio.py` y sus direcciones web en `rutas.py`.
4. Sumalo a `MODULOS` en `nodos/config.py` (después de los módulos que necesita).
5. Escribí sus tests en `tests/test_adjuntos.py`.

**¿Por qué los tests usan `":memory:"`?**
Para que cada test tenga una base nueva y vacía, sea rápido y no ensucie el archivo `nodos.db` real.

**¿Por qué no se borran los lotes de verdad?**
Para no perder historia: el registro podría apuntar a un lote que ya no existe. Se marcan como borrados.

**¿Qué es `conn` que aparece en todas las funciones?**
La conexión abierta a la base de datos. Se pasa como parámetro para que las funciones sepan en qué base trabajar
(la real o la de pruebas).

**¿Qué significa `-> list[str]` o `-> int` en algunas funciones?**
Son *anotaciones de tipo*: una pista para quien lee sobre qué devuelve la función (lista de textos, número).
Python no las obliga; son documentación.

**Rompí algo, ¿cómo vuelvo atrás?**
`git status` muestra qué cambiaste y `git diff` cómo. `git restore archivo.py` descarta tus cambios en ese archivo
(¡se pierden!). Si ya hiciste commit, preguntá antes de deshacer.

**¿Dónde está la documentación en Drive?**
`FACULTAD / tercer semestre / METODOLOGIA Y TESTING / Gestión de Nodos`.
