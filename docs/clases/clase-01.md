# Clase 01: Fundamentos de la Luz, Videojuegos vs. Cine y Shaders

Cátedra de Iluminación 3D y Shaders para Videojuegos · Docente Daniel Rojas (UNIACC)

---

## 1. Naturaleza de la Luz en Entornos Virtuales

En la física óptica, la luz se compone de fotones que viajan en línea recta e interactúan mediante reflexión, refracción y absorción en las superficies del entorno.

En el cómputo gráfico 3D:
* La luz no posee existencia corpórea; **constituye un cálculo vectorial**.
* Cada emisor se define matemáticamente mediante coordenadas de posición, vector de dirección, espectro cromático y potencia radiométrica.
* **Modelado del volumen**: La luz y la sombra revelan la curvatura, micro-relieve y profundidad de la geometría tridimensional.

---

## 2. Paradigmas de Renderizado: Videojuegos vs. Cine

| Criterio | Videojuegos (Tiempo Real) | Cine y Efectos Visuales (Offline) |
| :--- | :--- | :--- |
| **Tiempo de Cómputo** | 30 a 120+ fotogramas por segundo | Minutos u horas por cada cuadro individual |
| **Presupuesto GPU** | $\le 16.6\text{ ms}$ por fotograma (a 60 FPS) | Sin restricción estricta de tiempo de ejecución |
| **Control de Cámara** | Interactiva y libre (perspectiva del jugador) | Predefinida y fija según el encuadre del plano |
| **Metodología** | Aproximaciones de sombreado, baking y rasterización | Simulación por trazado de caminos (Path Tracing) |

---

## 3. Esquema de Iluminación de Tres Puntos (3-Point Lighting)

Técnica clásica para la construcción de jerarquía visual y separación de planos sobre el sujeto:

1. **Key Light (Luz Principal o Clave)**:
   * Emisor dominante situado a $45^\circ$ lateral y $45^\circ$ de elevación respecto al eje de cámara.
   * Modela el volumen principal y proyecta la sombra dominante (100% de intensidad de referencia).
2. **Fill Light (Luz de Relleno)**:
   * Emisor difuso situado en el lateral opuesto a la luz principal.
   * Eleva el valor tonal de las zonas en penumbra para preservar la legibilidad (25% a 40% de la intensidad principal).
3. **Rim Light / Back Light (Luz de Contorno o Contraluz)**:
   * Emisor posterior dirigido hacia los hombros y bordes del sujeto.
   * Produce un fino filete de alta reflectancia que **separa al sujeto del fondo**.

---

## 4. Definición y Función del Shader

Un **Shader (Sombreador)** es un programa computacional ejecutado en paralelo por la unidad de procesamiento gráfico (**GPU**):
$$\text{Color del Píxel} = \text{Luz Incidente} \times \text{Función de Reflectancia (PBR)} \times \cos(\theta)$$

### Parámetros Fundamentales del Estándar PBR:
1. **Base Color / Albedo**: Reflectancia difusa intrínseca sin información de oclusión ni brillo especular.
2. **Roughness (Rugosidad)**: Distribución estadística de microfacetas (de $0.0$, reflexión especular especular pura, a $1.0$, dispersión lambertiana mate).
3. **Metallic (Metalicidad)**: Comportamiento electrodinámico del material ($0.0$ dieléctrico / no-metal, $1.0$ conductor metálico puro).
