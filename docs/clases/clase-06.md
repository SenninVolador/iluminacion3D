# Clase 06: Iluminación de Interiores — Análisis de Referencia y Réplica en Unreal Engine 5

Iluminación 3D · Docente Daniel Rojas (UNIACC)

---

## Objetivos y Estructura de la Clase

En esta sesión aplicamos la metodología de iluminación de interiores a un caso práctico de producción. La clase se estructura en dos momentos:

1. **Análisis y Demostración en Pantalla**: Desglose técnico de iluminación cinematográfica a partir de una escena emblemática de la industria: el **prólogo nocturno de *The Last of Us*** (Naughty Dog). Veremos cómo identificar cada capa de luz en la referencia y cómo reconstruirla en Unreal Engine 5 en vivo.
2. **Taller Práctico en Sala**: Cada estudiante seleccionará un espacio interior y una referencia visual (de un videojuego o una película) para comenzar su réplica técnica durante la sesión bajo supervisión docente.

---

## 1. Caso de Estudio: Análisis de Iluminación en *The Last of Us*

En el prólogo de *The Last of Us*, la protagonista despierta sola en su habitación en plena noche. La escena destaca por su atmósfera de vulnerabilidad y tensión, lograda mediante un esquema de iluminación de alto contraste (*Low-Key*) y una estricta separación de temperaturas de color.

Al aplicar la metodología de **Chris Brejon (*CG Cinematography*)**, descomponemos la escena en tres familias de fuentes de luz:

```
                  ┌────────────────────────────────────────────────────────┐
                  │          DESGLOSE DE CAPAS DE ILUMINACIÓN              │
                  ├────────────────────────────────────────────────────────┤
                  │ 1. Natural Light  ──► Luna exterior fría (~7.500K)     │
                  │ 2. Practical Light ──► Pantalla de TV + Luz de pasillo │
                  │ 3. Dramatic Light ──► Rim light sutil de silueta       │
                  └────────────────────────────────────────────────────────┘
```

### Desglose Técnico de las Fuentes:

| Capa en Brejon | Elemento en Escena | Propiedades Físicas | Función Narrativa y Visual |
| :--- | :--- | :--- | :--- |
| **Natural Light** | Ventanal exterior hacia la ciudad | Color azul frío (~7.500K – 8.000K). Intensidad moderada. | Establece la penumbra nocturna base, marca la hora dramática y proyecta sombras suaves en el suelo. |
| **Practical Light (A)** | Pantalla de televisor en la sala | Luz de área (*Rect Light*) cian-blanca (~6.500K) con fluctuación leve de emisión. | Punto focal de alta intensidad que ilumina el mobiliario frontal y proyecta sombras duras en la oscuridad. |
| **Practical Light (B)** | Luz del pasillo / puerta entreabierta | Tungsteno cálido (~2.700K). Fuente puntual con radio controlado. | Genera un marcado **contraste térmico** (naranja vs. azul) que guía la mirada del jugador hacia la puerta. |
| **Dramatic Light** | Focos de estudio fuera de cuadro | Temperatura calibrada según la fuente motivadora (~6.500K o ~3.000K). Intensidad tenue. | Recorta la silueta del personaje (*Rim Light*) para despegarlo del fondo oscuro sin lavar los negros de la sala. |

---

## 2. Simulador Interactivo: Desglose de Capas en Escena Nocturna

Prueba el simulador interactivo para examinar cómo interactúan las capas de luz en un interior nocturno similar al analizado. Puedes rotar la cámara arrastrando con el ratón o deslizando en pantalla táctil:

<ClientOnly>
  <TLOUInteriorViewer />
</ClientOnly>

### Criterios Clave Observados en el Simulador:
* **El valor de las sombras**: La escena no utiliza una luz ambiental plana para aclarar las zonas oscuras. Los rincones se mantienen en valores bajos de luminancia para preservar el suspenso.
* **Contraste térmico complementario**: El diálogo entre el azul frío exterior y el ámbar cálido del pasillo genera profundidad espacial inmediata.
* **Motivación visual**: La silueta del personaje solo se ilumina en los bordes donde físicamente tendría sentido que llegue el rebote del televisor o la luz de luna.

---

## 3. Flujo de Trabajo para Replicar una Referencia en Unreal Engine 5

Durante la demostración en pantalla, seguimos esta secuencia técnica para trasladar la referencia al motor:

### Paso 1: Calibración de Exposición y Post-Process
Antes de colocar cualquier luz, es indispensable fijar la exposición de la cámara para evitar que el motor aclare la escena automáticamente (*Eye Adaptation*):
1. Añadir un actor **`PostProcessVolume`** y marcar **`Infinite Extent (Unbound)`**.
2. En la sección **Exposure**, cambiar el método a **Manual**.
3. Ajustar el valor **`Apply Physical Camera Exposure`** o fijar un **`EV100`** adecuado para interiores nocturnos (usualmente entre $4.0$ y $6.0$).

### Paso 2: Configuración de la Luz Natural Exterior
* Ubicar una **`Rect Light`** en el vano de la ventana, orientada hacia el interior.
* Ajustar las dimensiones de la luz (*Source Width* y *Source Height*) para que coincidan exactamente con el marco de la ventana.
* Asignar temperatura de color fría (~7.500K) e intensidad moderada.

### Paso 3: Luces Prácticas de Escenografía
* **Televisor o Pantallas**:
  * Aplicar un material con canal **Emissive** a la pantalla para el componente visual visible.
  * Colocar una **`Rect Light`** justo al frente de la pantalla apuntando hacia la habitación para proyectar la iluminación real sobre el suelo y el sofá.
* **Lámparas o Focos de Pasillo**:
  * Utilizar una **`Point Light`** o **`Spot Light`** con temperatura cálida (~2.700K).
  * Ajustar **`Source Radius`** a valores de bombilla física (entre $2\text{ cm}$ y $5\text{ cm}$) para que los reflejos especulares sean creíbles.
  * Ceñir el **`Attenuation Radius`** estrictamente al espacio donde rebota la luz para optimizar el rendimiento.

### Paso 4: Luces Dramáticas de Apoyo
* Evaluar la visibilidad del sujeto o punto focal desde el ángulo de cámara principal.
* Si el sujeto queda completamente empastado en negro, añadir una **`Spot Light`** tenue con cono amplio motivada por la luz del televisor o la luna para generar un ligero recorte de silueta (*Kicker* o *Rim*).

---

## 4. Encargo Práctico de Taller: Elección de Referencia y Réplica

Cada estudiante desarrollará una réplica técnica de iluminación de un espacio interior siguiendo las siguientes pautas:

### Requisitos del Ejercicio:

1. **Selección del Entorno Interior**:
   * Escoger una escena interior cerrada en Unreal Engine 5 (puede ser un escenario modular, un set de habitaciones o un rincón arquitectónico con mobiliario).
2. **Selección de Referencia Visual Obligatoria**:
   * Escoger **una captura de alta resolución** de un interior perteneciente a un **videojuego** o una **película**.
   * La referencia debe contar con una atmósfera clara y fuentes de luz identificables (por ejemplo: iluminación nocturna con lámparas, oficina con tubos fluorescentes, iglesia con vitrales o búnker con luces de emergencia).
3. **Ficha de Desglose Previa (Antes de Iluminar)**:
   * Identificar en la imagen:
     * ¿Cuál es la luz natural exterior (si existe)?
     * ¿Cuáles son las luces prácticas visibles en la escena?
     * ¿Dónde se ubican las luces dramáticas o de estudio?
     * Relación de contraste (¿escena clara en High-Key o contrastada en Low-Key?).
4. **Inicio de Réplica en Unreal Engine 5**:
   * Comenzar el montaje técnico en clase, apagando las luces por defecto y construyendo la escena capa por capa.
   * Aplicar la nomenclatura oficial de Epic Games en el Outliner (`L_Nat_...`, `L_Prac_...`, `L_Dram_...`).

---

## 5. Nomenclatura del Rig de Iluminación en el Outliner

Para mantener el proyecto ordenado durante el ejercicio, organicen las fuentes de luz en carpetas según la metodología de Brejon:

| Carpeta en Outliner | Prefijo Oficial | Tipo de Elemento |
| :--- | :--- | :--- |
| `Lights_Natural/` | `L_Nat_Window_Rect` | Luz de luna o sol exterior que entra por vanos |
| `Lights_Practical/` | `L_Prac_TV_Rect` | Luz emitida por pantallas de televisión |
| `Lights_Practical/` | `L_Prac_Hall_Point` | Lámpara de pasillo o bombilla visible |
| `Lights_Practical/` | `L_Prac_DeskLamp_Spot` | Lámpara de escritorio focalizada |
| `Lights_Dramatic/` | `L_Dram_Char_Rim` | Luz invisible de recorte de silueta |
| `Lights_Dramatic/` | `L_Dram_Table_Bounce` | Rebote invisible de apoyo en superficie |
