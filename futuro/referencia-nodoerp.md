Aquí tienes el análisis del archivo `nodoerp-app.html` basado exclusivamente en el código proporcionado:

### 1) Propósito general
La aplicación es una interfaz de **Knowledge Graph** (Grafo de Conocimiento) para un sistema llamado **Nexus ERP**. Su función principal es visualizar y explorar las relaciones entre diferentes componentes del ecosistema empresarial, como sistemas centrales, integraciones, clientes, documentos financieros y tickets de soporte, permitiendo ver métricas, documentación en Markdown y datos en formato JSON.

### 2) Pantallas/vistas y qué muestra cada una
*   **Barra lateral de navegación (Sidebar):**
    *   Logo: Icono de hexágono y texto "Nexus ERP".
    *   Enlaces de navegación: "Knowledge Graph", "Data Sources", "Integrations", "Wiki & Docs".
    *   Perfil de usuario: Imagen de usuario con los textos "Admin User" y "IT Systems".
*   **Cabecera (Header):**
    *   Barra de búsqueda: Input con el texto "Search entities, docs, or integrations...".
    *   Filtros de área: Botones con los textos "All Areas", "Core System", "CRM", "Finance", "Support".
    *   Iconos de acción: Campana de notificaciones (con punto rojo de alerta) e icono de engranaje (ajustes).
*   **Área principal del Grafo:**
    *   Contenedor del grafo (`network-container`) interactivo.
    *   Controles de navegación: Botones para "Zoom In", "Zoom Out" y "Fit to Screen".
    *   Leyenda de entidades ("Entity Legend"): Muestra etiquetas para "Core ERP System", "CRM / Customers", "Finance / Billing", "Support / Tickets" y "Data Entities".
*   **Panel lateral de detalles (Side Panel):**
    *   Cabecera del panel: Icono dinámico, badge de tipo (ej. "Entity"), badge de estado (ej. "Active") y título del nodo (ej. "Select a Node").
    *   Pestañas de contenido: "Knowledge View", "Dashboard", "Raw JSON".
    *   Contenedor de contenido:
        *   *Knowledge View:* Renderiza texto en Markdown (ej. "Click on a node in the graph to view its documentation...").
        *   *Dashboard:* Muestra un gráfico (Canvas) y una cuadrícula de KPIs.
        *   *Raw JSON:* Muestra un bloque de código con el objeto JSON del nodo seleccionado.
    *   Pie del panel: Botones "Edit Markdown" y "Sync Data".

### 3) Estructura de datos
La aplicación utiliza principalmente el objeto `entityDatabase` para definir los nodos y sus detalles:

*   **Objetos de Entidad (ejemplo genérico):**
    *   `id`: Número (ID único).
    *   `type`: Categoría (ej. 'System', 'Integration', 'Customer', 'Document', 'Ticket').
    *   `label`: Nombre mostrado.
    *   `icon`: Nombre del icono de Phosphor Icons.
    *   `color`: Código hexadecimal.
    *   `status`: Estado de la entidad (ej. 'Operational', 'Syncing', 'Warning', 'Active', 'Paid', 'Open').
    *   `markdown`: Cadena de texto con formato Markdown.
    *   `metrics`: Objeto con `labels` (array), `data` (array), `label` (string) y `type` (ej. 'line', 'bar').
    *   `kpis`: Array de objetos con `label` (string) y `val` (string).

*   **Estructura del Grafo (vis.js):**
    *   **Nodes:** `id`, `category`, `label`, `shape` (dot, box), `size`, `color` (objeto con `background` y `border`), `font` (objeto con `color`).
    *   **Edges:** `from` (ID origen), `to` (ID destino), `color` (objeto con `color` y `highlight`), `dashes` (booleano), `arrows` (string), `label` (string).

### 4) Cómo se relacionan los nodos/lotes entre sí
Las relaciones se definen mediante el array `edges` y se visualizan con etiquetas específicas:
*   **Nexus Core (1) $\leftrightarrow$ Integraciones (2, 3, 4):** Relación bidireccional con líneas discontinuas (`dashes: true`).
*   **Salesforce (2) $\rightarrow$ Acme Corp (5):** Relación "Owns Account".
*   **Acme Corp (5) $\rightarrow$ Stripe (3):** Relación "Billed Via".
*   **Acme Corp (5) $\rightarrow$ Zendesk (4):** Relación "Submits".
*   **Stripe (3) $\rightarrow$ INV-9042 (6):** Relación "Generated".
*   **Acme Corp (5) $\rightarrow$ INV-9042 (6):** Relación "Pays".
*   **Zendesk (4) $\rightarrow$ Ticket #4912 (7):** Relación "Manages".
*   **Acme Corp (5) $\rightarrow$ Ticket #4912 (7):** Relación "Opened".

### 5) Acciones del usuario y funciones JS
*   **Seleccionar Nodo:** Detectado por `network.on("selectNode", ...)` $\rightarrow$ Ejecuta `openPanel(nodeId)`.
*   **Deseleccionar Nodo:** Detectado por `network.on("deselectNode", ...)` $\rightarrow$ Ejecuta `closePanel()`.
*   **Filtrar Grafo:** Ejecutado por `filterGraph(category)` $\rightarrow$ Actualiza `currentCategoryFilter`, refresca los `DataView` de nodos y aristas, y ajusta la UI de los botones.
*   **Zoom In:** Ejecutado por `zoomIn()` $\rightarrow$ Aumenta la escala del network.
*   **Zoom Out:** Ejecutado por `zoomOut()` $\rightarrow$ Disminuye la escala del network.
*   **Ajustar al Pantalla:** Ejecutado por `fitGraph()` $\rightarrow$ Ajusta el zoom automáticamente.
*   **Cambiar Pestañas:** Ejecutado por `switchTab(tabId)` $\rightarrow$ Cambia la visibilidad de los contenedores de contenido (Knowledge, Dashboard, Raw).
*   **Mostrar Datos:** `openPanel(nodeId)` $\rightarrow$ Carga datos de `entityDatabase`, renderiza Markdown con `marked.parse`, genera el gráfico con `renderDashboard` y muestra el JSON.
*   **Cerrar Panel:** Ejecutado por `closePanel()` $\rightarrow$ Oculta el panel lateral y deselecciona nodos.

### 6) Registro/historial de cambios, roles o usuarios
*   **Usuarios:** Existe un objeto de usuario estático en la UI: "Admin User" perteneciente a "IT Systems".
*   **Historial:** No existe un registro de historial en el código.
*   **Roles:** No se definen roles específicos en el código, solo la información del usuario actual.

### 7) Librerías externas usadas (CDN)
*   **Phosphor Icons:** `https://unpkg.com/@phosphor-icons/web` (Iconos).
*   **Tailwind CSS:** `https://cdn.tailwindcss.com?plugins=typography` (Estilos y tipografía).
*   **vis-network:** `https://unpkg.com/vis-network/standalone/umd/vis-network.min.js` (Renderizado del grafo).
*   **Marked:** `https://cdn.jsdelivr.net/npm/marked/marked.min.js` (Procesamiento de Markdown).
*   **Chart.js:** `https://cdn.jsdelivr.net/npm/chart.js` (Gráficos dinámicos).

### 8) Visualización del grafo
El grafo se dibuja usando la librería **vis-network**.
*   **Física:** Utiliza el solver `forceAtlas2Based` con constantes de gravedad y resortes para el posicionamiento.
*   **Interactividad:** Soporta `hover`, `zoomView`, `dragView` y `tooltipDelay`.
*   **Personalización:** Los nodos tienen sombras activadas, diferentes formas (`dot` para sistemas/clientes, `box` para documentos/tickets) y colores basados en categorías. Las aristas tienen suavizado continuo (`continuous`) y flechas en ambos sentidos donde se especifique.
*   **Filtrado Dinámico:** Utiliza `vis.DataView` para filtrar qué nodos y aristas se muestran según la categoría seleccionada en los botones de la cabecera.