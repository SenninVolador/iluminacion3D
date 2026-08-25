# 🎓 Clase 01: Introducción a la Iluminación 3D, Juegos vs. Cine y Shaders

Bienvenido a los fundamentos de la iluminación tridimensional. Esta clase sienta las bases para comprender cómo funciona la luz en los entornos virtuales, cómo se construye el volumen de un objeto y cómo los motores gráficos interpretan los materiales.

---

## 1. 💡 La Luz: Del Mundo Físico al Espacio Digital

En la física real, la luz está compuesta por fotones que viajan en línea recta, rebotan miles de millones de veces en las superficies circundantes y entran en nuestros ojos o en la lente de una cámara.

En el mundo digital 3D:
* La luz no existe de forma física; **es un cálculo matemático**.
* Una "fuente de luz" en un motor 3D es un vector con una posición, una dirección, un color y una intensidad que interactúa con la geometría de la escena.
* **La luz define la forma**: Sin luz, un modelo 3D con millones de polígonos se vería como una silueta plana y sin profundidad. La sombra y el brillo son los que revelan el relieve, la curvatura y el volumen.

---

## 2. 🎮 Videojuegos vs. 🎬 Cine: Dos Paradigmas de Iluminación

| Característica | 🎮 Videojuegos (Real-Time) | 🎬 Cine (Offline / Path Tracing) |
| :--- | :--- | :--- |
| **Tiempo de Cálculo** | 30 a 120+ fotogramas por segundo | Minutos u horas por cada fotograma |
| **Presupuesto GPU** | $\approx 16.6\text{ ms}$ a 60 FPS | Sin límite estricto de tiempo |
| **Cámara** | Libre e impredecible (el jugador mira donde sea) | Fija y controlada por el director |
| **Estrategia** | Aproximaciones dinámicas, baking y trucos | Simulación de millones de rayos físicos |

---

## 3. 📐 Esquema de Iluminación de 3 Puntos (3-Point Lighting)

El **esquema de 3 puntos** es la técnica clásica para esculpir volumen sobre un personaje u objeto:

1. **Key Light (Luz Principal o Clave)**:
   * Colocada a $45^\circ$ a un lado de la cámara y $45^\circ$ por encima de la cabeza del objeto.
   * Define el contraste dominante y proyecta las sombras principales (100% intensidad).
2. **Fill Light (Luz de Relleno)**:
   * En el lateral opuesto (a $45^\circ$ hacia el otro lado).
   * Rellena y suaviza las sombras duras para que la penumbra sea legible (25% a 40% de la Key).
3. **Rim Light / Back Light (Luz de Contorno o Contraluz)**:
   * Colocada detrás del sujeto, apuntando hacia su espalda y hombros.
   * **Despega al personaje del fondo**, creando un fino borde luminoso alrededor de la silueta.

---

## 4. 🧪 ¿Qué es un Shader?

Un **Shader (Sombreador)** es un programa informático que se ejecuta directamente en la tarjeta gráfica (**GPU**):
$$\text{Color Final} = \text{Luz Incidente} \times \text{Material (Base Color, Rugosidad, Metalicidad)} \times \text{Ángulo de Vista}$$

### Propiedades PBR Maestras:
1. **Base Color / Albedo**: El color propio del objeto sin sombras pintadas.
2. **Roughness (Rugosidad)**: Si es liso y refleja como espejo ($0.0$) o si es mate y dispersa el brillo ($1.0$).
3. **Metallic (Metalicidad)**: Si el material es un metal conductor ($1.0$) o un dieléctrico como plástico, madera o piel ($0.0$).
