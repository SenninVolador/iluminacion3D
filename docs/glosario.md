# Glosario Técnico de Términos

Cátedra de Iluminación 3D y Shaders para Videojuegos · Docente Daniel Rojas (UNIACC)

---

## Unidad 1: Fundamentos de la Luz, Esquema de 3 Puntos y Shaders

### Luz Digital en 3D
Cálculo vectorial que define posición, dirección, espectro cromático e intensidad para modelar la geometría tridimensional en motores gráficos.

### Renderizado en Tiempo Real vs. Offline
* **Tiempo Real (Videojuegos)**: Cómputo resuelto a razón de 30 a 120 fotogramas por segundo ($\le 16.6\text{ ms}$ a 60 FPS).
* **Offline (Cine / VFX)**: Simulación estocástica por trazado de rayos (Path Tracing) sin límite estricto de tiempo por cuadro.

### Frametime (Tiempo de Fotograma)
Duración en milisegundos que tarda la GPU en renderizar un cuadro completo.

### Esquema de Tres Puntos (3-Point Lighting)
* **Key Light (Luz Principal)**: Emisor dominante situado a $45^\circ$ lateral y $45^\circ$ cenital que define el modelado y las sombras principales.
* **Fill Light (Luz de Relleno)**: Emisor secundario opuesto (25–40% de intensidad) destinado a elevar las penumbras.
* **Rim Light (Contraluz)**: Emisor trasero alineado con los hombros para separar al sujeto del fondo.

### Shader (Sombreador)
Programa computacional ejecutado en la GPU que determina la reflectancia, absorción y color de cada píxel en pantalla.

### PBR (Physically Based Rendering)
Estándar de sombreado fundamentado en leyes ópticas de conservación de energía y teoría de microfacetas.

### Base Color / Albedo
Reflectancia difusa intrínseca de una superficie sin influencia de sombras ni brillos especulares.

### Roughness (Rugosidad)
Parámetro escalar que describe la micro-textura de una superficie ($0.0$ especular puro, $1.0$ dispersión difusa).

### Metallic (Metalicidad)
Parámetro binario que distingue materiales dieléctricos ($0.0$) de conductores metálicos ($1.0$).

---

## Unidad 2: Iluminación Exterior, Movilidad Técnica y Fuentes Locales

### Directional Light (Luz Direccional / Sol)
Emisor situado en el infinito que proyecta rayos paralelos; su cálculo depende únicamente de la orientación angular.

### Sky Light (Luz de Cielo / Hemisférica)
Emisor hemisférico envolvente que baña las superficies en sombra con luz difusa ambiental, evitando valores de negro absoluto ($RGB = 0, 0, 0$).

### Movilidad de Luces (Mobility)
* **Static**: Iluminación y sombras precomputadas en mapas de textura (Lightmaps). Coste nulo en ejecución.
* **Stationary**: Luz directa dinámica combinada con iluminación global horneada. Permite variar intensidad y color en tiempo real.
* **Movable**: Resuelta cuadro a cuadro en tiempo real. Máxima interactividad con mayor coste computacional.

### Baking / Lightmass
Cómputo previo de iluminación indirecta estocástica almacenado en texturas 2D (Lightmaps).

### Cascaded Shadow Maps (CSM)
Segmentación por distancia del mapa de sombras para luces direccionales, optimizando la resolución en función de la proximidad a la cámara.

### Temperatura de Color (Kelvin)
Escala termodinámica ($K$) que describe el espectro cromático de una fuente luminosa.

### Master Material (Material Maestro)
Sombreador base parametrizado que centraliza la lógica computacional para todo el proyecto.

### Material Instance (Instancia de Material)
Derivación ligera de un Master Material que permite permutar texturas y valores escalares en tiempo real sin recompilar código de sombreado.

### Textura Empaquetada (ORM)
Técnica de optimización que almacena Ambient Occlusion en el canal Rojo, Roughness en el Verde y Metallic en el Azul en un único archivo de textura.

### Normal Map (Mapa de Normales)
Textura RGB que modifica la orientación de los vectores normales para simular relieve tridimensional sin añadir densidad poligonal.

### Point Light (Luz Puntual)
Emisor omnidireccional ($360^\circ$) desde un punto del espacio tridimensional.

### Spot Light (Luz Focal)
Emisor cónico direccional con ángulos de apertura interna (*Inner Cone*) y externa (*Outer Cone*).

### Rect Light (Luz Rectangular / de Área)
Emisor plano que proyecta luz difusa en una semiesfera (Softbox fotográfico o paneles LED).

### Attenuation Radius (Radio de Atenuación)
Distancia física máxima donde la intensidad de un emisor se anula ($I \propto 1/d^2$).
