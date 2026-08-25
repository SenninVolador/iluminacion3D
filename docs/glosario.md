# Glosario Técnico de Términos

Cátedra de Iluminación 3D · Docente Daniel Rojas (UNIACC)

Este glosario explica los conceptos fundamentales de forma clara, directa y visual, organizados por el avance de cada clase del semestre.

---

## Unidad 1: Fundamentos de la Luz, Esquema de 3 Puntos y Shaders

### Luz Digital en 3D
En el mundo real la luz son partículas físicas (fotones). En un motor de videojuegos como Unreal Engine, la luz no existe físicamente: es una **operación matemática** (un vector de dirección, un color y una fuerza) que le dice a la tarjeta gráfica cómo iluminar cada polígono para que un objeto plano parezca tener volumen tridimensional.

### Renderizado en Tiempo Real vs. Cine (Offline)
* **Tiempo Real (Videojuegos)**: La computadora debe calcular toda la imagen entre **30 y 60 veces por segundo**. Cada cuadro debe resolverse en menos de **16.6 milisegundos**. Por eso se usan técnicas optimizadas y aproximaciones.
* **Offline (Cine y Animación)**: No hay prisa; la computadora puede tardar 2 horas en calcular un solo fotograma con millones de rayos de luz perfectos (Path Tracing).

### Frametime (Tiempo de Fotograma)
Los milisegundos ($ms$) que tarda la tarjeta de vídeo en dibujar un cuadro en pantalla. Para que un juego corra a 60 FPS estables, el frametime no puede superar los **16.6 ms**. Si ponemos demasiadas luces, el frametime sube a 30 ms o 40 ms y el juego se siente lento ("lag").

---

### Esquema de Tres Puntos (3-Point Lighting)
Es la técnica clásica nacida en el cine y la fotografía para esculpir el volumen de un personaje u objeto desde la oscuridad total usando tres luces:

<ClientOnly>
  <ThreePointLightingViewer />
</ClientOnly>

1. **Key Light (Luz Principal)**: Es la luz más fuerte (100% de potencia) colocada a 45° al lado de la cámara. Define la dirección principal de la luz y marca la sombra dominante en el rostro.
2. **Fill Light (Luz de Relleno)**: Luz más suave (30% de potencia) colocada al lado contrario. Su único trabajo es iluminar un poco el lado oscuro para que no quede negro carbón y se puedan ver los detalles.
3. **Rim Light (Contraluz o Luz de Contorno)**: Luz colocada **detrás del sujeto**. Dibuja una línea brillante en el borde del cabello y los hombros, logrando que el personaje se "despegue" visualmente del fondo oscuro.

---

### Shader (Sombreador)
Un shader es un pequeño programa matemático que corre directamente en la tarjeta de vídeo (GPU). Su trabajo es calcular qué color exacto tiene cada píxel en la pantalla multiplicando tres cosas:
$$\text{Color del Píxel} = \text{Color de la Luz} \times \text{Material del Objeto} \times \text{Ángulo de la Cámara}$$

---

### PBR (Physically Based Rendering)
Significa "Renderizado Basado en la Física". Es el estándar moderno de materiales en videojuegos donde los objetos reaccionan a la luz respetando leyes físicas reales:
* **Base Color / Albedo**: El color plano del objeto sin sombras ni brillos pintados (por ejemplo, el tono rojo puro de una manzana).
* **Roughness (Rugosidad)**: Si el material es liso como un espejo ($0.0$, reflejo nítido) o áspero como una tiza ($1.0$, reflejo mate y disperso).
* **Metallic (Metalicidad)**: Si el material es un metal conductor puro ($1.0$, como oro o cromo) o un no-metal / dieléctrico ($0.0$, como madera, plástico, ropa o piel).

<ClientOnly>
  <RoughnessViewer />
</ClientOnly>

---

## Unidad 2: Iluminación Exterior, Movilidad Técnica y Fuentes Locales

### Directional Light (Luz Solar)
Una luz que simula el Sol o la Luna. Como el Sol está a millones de kilómetros de distancia, todos sus rayos caen en **líneas perfectamente paralelas**.
* **Dato clave**: No importa dónde muevas la luz en el mapa; **solo importa hacia dónde está rotada**.
* **Atajo en Unreal**: Mantén presionado `Ctrl + L` y mueve el ratón para cambiar la hora del día en vivo.

### Sky Light (Luz de Cielo / Cúpula Celeste)
En un día soleado real, las sombras bajo un árbol no son negras porque el cielo azul actúa como una gigantesca lámpara difusa. La **Sky Light** captura los colores del cielo y baña todas las sombras con luz suave azulada, **evitando que las sombras queden en negro absoluto**.

---

### Temperatura de Color (Grados Kelvin - K)
Es la escala física que mide el tono cromático de una fuente de luz:
* **Valores bajos (1800K - 3000K)**: Luz cálida, anaranjada y acogedora (velas, fuego, bombillas incandescentes, atardeceres).
* **Valores medios (5500K - 6500K)**: Luz blanca neutra (el sol al mediodía).
* **Valores altos (7500K - 10000K)**: Luz fría y azulada (sombras exteriores en un día despejado, cielos nublados).

<ClientOnly>
  <KelvinViewer />
</ClientOnly>

---

### Movilidad de Luces (Static, Stationary, Movable)
En Unreal Engine, cada luz tiene un modo de "Movilidad" que define cómo se calcula en la GPU:
* **Static (Estática)**: La luz se calcula antes de jugar y se "hornea" (imprime) directamente en las texturas (**Lightmaps**). Durante el juego tiene **coste 0 en GPU**, pero no se puede mover ni apagar.
* **Stationary (Estacionaria)**: Modo híbrido. La luz sobre personajes es dinámica y proyecta sombras en tiempo real, pero el rebote de la luz en paredes va horneado. Permite cambiar color o intensidad en el juego, pero no mover la posición del foco.
* **Movable (Dinámica)**: Se calcula 100% en tiempo real en cada fotograma. Permite linternas móviles, explosiones, ciclos día/noche y destrucción, pero consume más recursos de GPU.

> **Regla de los 4 Canales (Stationary Overlap)**: En Unreal clásico no se pueden solapar más de 4 luces Stationary con sombras en el mismo espacio (canales R, G, B, A de la memoria de sombras). Si pones una 5ª luz, se marcará con una cruz roja (`❌`) y se volverá Movable automáticamente, duplicando el gasto en la tarjeta gráfica.

---

## Unidad 3: Master Materials, Texturas ORM y Fuentes Locales

### Master Material (Material Maestro)
Es un shader base matriz que contiene todas las fórmulas matemáticas y conexiones de texturas. Se compila una sola vez y sirve como plantilla para crear miles de variaciones en el juego sin gastar memoria.

### Material Instance (Instancia de Material)
Una copia ligera de un Master Material. Permite cambiar texturas, subir el brillo, cambiar el color o ajustar la rugosidad **al instante en el Viewport sin esperar a que Unreal recompile shaders**.

---

### Texturas Empaquetadas (Canales ORM)
Para no sobrecargar la tarjeta de vídeo leyendo tres archivos separados, combinamos tres mapas en escala de grises dentro de una sola imagen RGB:
* **Canal R (Rojo)**: **O**clusión Ambiental (*Ambient Occlusion*).
* **Canal G (Verde)**: **R**ugosidad (*Roughness*).
* **Canal B (Azul)**: **M**etalicidad (*Metallic*).

---

### Normal Map (Mapa de Normales)
Es una textura de color azulado/violeta que engaña a la tarjeta de vídeo alterando el ángulo en que la luz choca con la superficie. Permite simular poros, arrugas, tornillos, grietas y volumen 3D **sin añadir ningún polígono extra a la malla**:

<ClientOnly>
  <NormalMapViewer />
</ClientOnly>

---

### Tipos de Luces Locales

| Tipo de Luz | Cómo Emite la Luz | Casos de Uso Comunes |
| :--- | :--- | :--- |
| **Point Light (Luz Puntual)** | En todas direcciones ($360^\circ$) desde un punto central | Bombillas, velas, fuego, antorchas |
| **Spot Light (Luz Focal)** | En forma de cono hacia una dirección fija | Linternas, farolas de calle, luces de techo |
| **Rect Light (Luz de Área)** | Desde una superficie plana rectangular | Paneles LED, pantallas de TV, fluorescentes |

---

### Attenuation Radius (Radio de Atenuación)
Es la distancia máxima en centímetros donde la luz deja de existir físicamente ($I \propto 1/d^2$):

<ClientOnly>
  <AttenuationViewer />
</ClientOnly>

* **Consejo clave de optimización**: Mantén el radio lo más ajustado posible al objeto que deseas iluminar. Si el radio es gigante, la luz atravesará paredes invisibles y la tarjeta gráfica tendrá que calcular la luz en habitaciones contiguas innecesariamente (**Shader Overdraw**).

---

### Iluminación Rembrandt
Técnica clásica de retrato donde la luz principal incide a 45° lateral, proyectando una sombra en la nariz que se une con la mejilla para formar un **pequeño triángulo luminoso** debajo del ojo en el lado oscuro del rostro.

### Eye Catchlight (Brillo en la Pupila)
El pequeño punto blanco reflectante que una luz puntual o focal produce en la córnea del ojo de un personaje. Sin este brillo, los ojos de un personaje 3D se perciben planos, muertos o sin vida.
