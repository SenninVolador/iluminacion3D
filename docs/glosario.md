# Glosario Técnico de Términos

Iluminación 3D · Docente Daniel Rojas (UNIACC)

Este glosario reúne los conceptos fundamentales del ramo explicados de forma clara, directa y visual para estudiantes de primer año, ordenados por cada unidad del semestre.

---

## Unidad 1: Fundamentos de la Luz, Esquema de 3 Puntos y Shaders

### Luz Digital en 3D
En el mundo real la luz son fotones físicos emitidos por fuentes de energía. En un motor de videojuegos como Unreal Engine, la luz no existe físicamente: es una **operación matemática** (un vector de dirección, un color y una intensidad) que le indica a la tarjeta de video cómo iluminar cada polígono para que un modelo 3D plano adquiera volumen, profundidad y relieve.

---

### Renderizado en Tiempo Real vs. Cine (Offline)

* **Tiempo Real (Videojuegos)**:
  * La computadora debe calcular toda la imagen entre **30 y 60 veces por segundo**.
  * Cada fotograma debe resolverse en menos de **16.6 milisegundos**.
  * Obliga a usar técnicas optimizadas de sombreado y aproximaciones matemáticas.
* **Offline (Cine y Animación 3D)**:
  * No hay restricción estricta de tiempo por cuadro.
  * La computadora puede tardar minutos u horas en calcular millones de rayos de luz con trazado de caminos (*Path Tracing*).

---

### Frametime (Tiempo de Fotograma)
Es el tiempo exacto en milisegundos ($ms$) que tarda la tarjeta de video en procesar y dibujar un fotograma en pantalla.

* **Meta de rendimiento**: Para jugar a 60 FPS estables, el frametime no puede superar los **16.6 ms**.
* **Impacto técnico**: Si colocamos demasiadas luces dinámicas con sombras en un mismo espacio, el frametime sube a 35 ms o 50 ms y el videojuego sufre caídas bruscas de fluidez.

---

### Esquema de Tres Puntos (3-Point Lighting)
Técnica clásica para esculpir el volumen y la silueta de un personaje u objeto desde la oscuridad total usando tres fuentes de luz:

<ClientOnly>
  <ThreePointLightingViewer />
</ClientOnly>

* **1. Key Light (Luz Principal o Clave)**:
  * Es la luz más potente (100% de intensidad de referencia).
  * Se ubica a 45° al costado de la cámara y 45° elevada.
  * Modela la forma y proyecta la sombra dominante en el rostro o superficie.
* **2. Fill Light (Luz de Relleno)**:
  * Luz suave (25% a 40% de la potencia principal) ubicada en el lado opuesto.
  * Su objetivo es aclarar las sombras profundas para rescatar detalles en la penumbra.
* **3. Rim Light (Contraluz o Luz de Contorno)**:
  * Luz colocada detrás del sujeto, apuntando hacia su espalda y hombros.
  * Crea una fina línea brillante en los bordes para **despegar al personaje del fondo oscuro**.

---

### Shader (Sombreador)
Un shader es un pequeño programa informático que se ejecuta directamente en la tarjeta de video (GPU).

Su función es calcular el color final de cada píxel combinando tres factores:

* **1. La Luz**: Su dirección, color e intensidad.
* **2. El Material**: Su color base (albedo), rugosidad y metalicidad.
* **3. La Cámara**: El ángulo exacto desde donde el jugador está mirando la superficie.

---

### PBR (Physically Based Rendering)
Estándar de materiales basado en las leyes físicas reales de la óptica:

* **Base Color / Albedo**: El color plano del material sin luces ni sombras pintadas a mano (por ejemplo, el tono rojo puro de una manzana).
* **Roughness (Rugosidad)**: Controla el micro-relieve de la superficie:
  * `0.0`: Liso como un espejo (reflejo nítido y concentrado).
  * `1.0`: Áspero como tiza o tela (la luz se dispersa en un acabado mate).
* **Metallic (Metalicidad)**: Clasificación física del material:
  * `0.0 (Dieléctrico / No-metal)`: Madera, plástico, tela, piedra o piel.
  * `1.0 (Metal Puro)`: Cromo, oro, cobre o hierro.

<ClientOnly>
  <RoughnessViewer />
</ClientOnly>

---

## Unidad 2: Iluminación Exterior, Movilidad Técnica y Fuentes Locales

### Directional Light (Luz Solar) y Sky Light (Luz de Cielo)

* **Directional Light**: Modela una fuente a distancia infinita (el Sol o la Luna). Todos sus rayos viajan en **líneas 100% paralelas**. Su posición en el mapa no importa; **solo influye su rotación** (atajo en Unreal: `Ctrl + L`).
* **Sky Light**: Simula la cúpula celeste. En la atmósfera terrestre, las sombras bajo el sol no son negras porque el cielo azul actúa como una gigantesca lámpara difusa de 360°, **evitando que las sombras queden en negro absoluto**.

<ClientOnly>
  <SunShadowViewer />
</ClientOnly>

---

### Temperatura de Color (Grados Kelvin - K)
Escala física que describe el tono cromático de una fuente luminosa:

* **1800K – 3000K (Luz Cálida)**: Velas, fuego, bombillas incandescentes y atardeceres.
* **5500K – 6500K (Luz Neutra)**: Luz solar directa de mediodía.
* **7500K – 10000K (Luz Fría)**: Sombras exteriores en días despejados y cielos nublados.

<ClientOnly>
  <KelvinViewer />
</ClientOnly>

---

### Movilidad de Luces (Static, Stationary, Movable)

* **Static (Estática)**: La luz se calcula previamente antes del juego y se guarda fija en mapas de textura (**Lightmaps**). Tiene **coste cero en GPU durante la partida**, pero no se puede mover ni apagar.
* **Stationary (Estacionaria)**: Modo híbrido. Proyecta sombras dinámicas sobre personajes en movimiento, pero los rebotes en paredes van horneados. Permite cambiar color e intensidad en tiempo real.
* **Movable (Dinámica)**: Se calcula 100% en tiempo real en cada fotograma. Permite linternas, ciclos día/noche y física, con mayor consumo de recursos en GPU.

<ClientOnly>
  <MobilityViewer />
</ClientOnly>

> **Regla de los 4 Canales (Stationary Overlap)**: En Unreal clásico solo pueden solaparse un máximo de 4 luces Stationary con sombras sobre un mismo objeto (canales RGBA de la memoria de sombras). Si se añade una quinta luz, se marca con una cruz roja (`❌`) y pasa automáticamente a modo Movable, duplicando el consumo en GPU.

---

## Unidad 3: Master Materials, Texturas ORM y Fuentes Locales

### Master Material vs. Material Instance

* **Master Material (`M_Master_PBR`)**: Shader matriz que contiene todas las fórmulas matemáticas y conexiones. Se compila una sola vez para todo el proyecto.
* **Material Instance (`MI_Prop`)**: Copia ligera del Master Material. Permite cambiar texturas, rugosidades, metalicidades y colores **al instante en el Viewport sin esperar a que Unreal recompile shaders**.

---

### Texturas Empaquetadas (Canales ORM)
Para optimizar el uso de memoria de video (VRAM), combinamos tres mapas en escala de grises dentro de una sola imagen de tres canales RGB:

* **Canal R (Rojo)**: **O**clusión Ambiental (*Ambient Occlusion*).
* **Canal G (Verde)**: **R**ugosidad (*Roughness*).
* **Canal B (Azul)**: **M**etalicidad (*Metallic*).

---

### Normal Map (Mapa de Normales)
Textura de tono azulado que altera la inclinación con que la luz choca en la superficie. Simula poros, arrugas, biseles y relieve tridimensional **sin añadir polígonos extra a la geometría**:

<ClientOnly>
  <NormalMapViewer />
</ClientOnly>

---

### Fuentes de Luz Locales de Interior

| Tipo de Luz | Geometría de Emisión | Casos de Uso Comunes |
| :--- | :--- | :--- |
| **Point Light (Luz Puntual)** | Esfera omnidireccional de 360° | Bombillas desnudas, velas, fuego, antorchas |
| **Spot Light (Luz Focal)** | Cono direccional acotado | Linternas, focos de techo, farolas |
| **Rect Light (Luz de Área)** | Superficie plana rectangular | Paneles LED, pantallas de TV, fluorescentes |

<ClientOnly>
  <SpotConeViewer />
</ClientOnly>

---

### Attenuation Radius (Radio de Atenuación)
Distancia física en centímetros donde la potencia de la luz decae hasta anularse ($I \propto 1/d^2$):

<ClientOnly>
  <AttenuationViewer />
</ClientOnly>

* **Criterio de optimización**: Mantener el radio ajustado al foco. Si el radio es excesivo, la luz atravesará muros invisibles y la tarjeta de video calculará iluminación innecesaria en habitaciones contiguas (**Shader Overdraw**).

---

### Iluminación Rembrandt
Técnica clásica de retrato donde la luz principal incide a 45° lateral, proyectando una sombra en la nariz que se une con la mejilla para formar un **pequeño triángulo luminoso** debajo del ojo en el lado en penumbra.

### Eye Catchlight (Brillo en la Pupila)
El pequeño punto blanco especular que una fuente de luz produce en la córnea del ojo de un personaje. Aporta vitalidad y profundidad a la mirada en primeros planos.

---

## Unidad 4: Shaders Nodales, Atmósfera y Niebla Volumétrica

### Sistema Nodal (Node-Based Shading)
Forma estándar de construir materiales en la industria mediante bloques funcionales (nodos) interconectados por cables virtuales. La lógica es idéntica en Unreal Engine (Material Editor), Unity (Shader Graph), Blender (Shader Editor) y Maya (Hypershade).

<ClientOnly>
  <NodeShaderViewer />
</ClientOnly>

---

### Multiply Node (Operador de Tinte)
Operación matemática que multiplica el valor RGB de cada píxel de una textura por un color vectorial. Si se multiplica por blanco (`1, 1, 1`), la textura se mantiene original; si se multiplica por un color como rojo (`1, 0, 0`), la textura se tiñe de rojo en tiempo real.

---

### SkyAtmosphere / Physical Sky (Cielo Físico)
Componente que simula matemáticamente la atmósfera planetaria calculando la interacción física de la luz solar con las partículas de aire mediante dos fenómenos ópticos:
* **Dispersión de Rayleigh**: Provocada por moléculas de gas; dispersa longitudes de onda cortas generando el cielo azul de día y tonos rojizos en el atardecer.
* **Dispersión de Mie**: Provocada por polvo, humedad y partículas grandes; genera el halo blanco/dorado alrededor del sol y la bruma del horizonte.

---

### Exponential Height Fog (Niebla de Altura)
Componente analítico que agrega densidad de niebla en función de la altitud y la distancia a la cámara, creando perspectiva aérea (los objetos lejanos se ven menos contrastados y más azulados).

---

### Volumetric Fog (Niebla Volumétrica y God Rays)
Técnica de renderizado que divide el campo visual de la cámara en una grilla 3D de vóxeles. Permite que la luz interactúe con la niebla para generar **rayos crepusculares o haces de luz visibles (God Rays / Light Shafts)** cuando objetos o aberturas bloquean parcialmente el haz:

<ClientOnly>
  <VolumetricFogViewer />
</ClientOnly>

---

### Anisotropía de Dispersión ($g$)
Parámetro físico que controla hacia dónde rebota la luz al chocar con las partículas de niebla:
* `$g = 0.0$`: Dispersión isotrópica (la niebla se ilumina uniformemente en todas direcciones).
* `$g = 0.7 - 0.9$`: Dispersión frontal (*Forward Scattering*). La niebla genera rayos luminosos intensos cuando la cámara apunta en dirección a la fuente de luz.

---

### Mood (Atmósfera Emocional y Narrativa)
El uso coordinado de la temperatura de color, el contraste de sombras, la densidad de la niebla y la dirección del sol para evocar una emoción específica en el jugador (tensión, misterio, calidez, aislamiento, peligro o heroísmo).
