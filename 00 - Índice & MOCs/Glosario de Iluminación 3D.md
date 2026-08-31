---
tags:
  - glosario
  - conceptos-basicos
  - iluminacion3d
  - shaders
  - pbr
  - atmosfera
  - gamedev
date: 2026-08-31
---

# Glosario de Términos (Organizado Clase a Clase)

Diccionario técnico de **Iluminación 3D, Shaders y PBR para Videojuegos**, estructurado cronológicamente por sesión.

---

## Índice por Clases
- [Clase 01: Fundamentos de la Luz, Videojuegos vs. Cine y Shaders](#clase-01-fundamentos-3-point-lighting-y-shaders)
- [Clase 02: Iluminación Exterior, Movilidad Técnica y Análisis](#clase-02-iluminación-exterior-y-movilidad-de-luces)
- [Clase 03: Shaders PBR, Master Materials, Texturas ORM y Fuentes Locales](#clase-03-shaders-pbr-master-materials-texturas-orm-y-luces-locales)
- [Clase 04: Shaders Nodales Universales, Atmósfera y Niebla Volumétrica](#clase-04-shaders-nodales-universales-atmósfera-y-niebla-volumétrica)

---

## Clase 01: Fundamentos, 3-Point Lighting y Shaders

### Luz Digital en 3D
Cálculo vectorial que define posición, dirección, espectro cromático e intensidad para modelar la geometría tridimensional en motores gráficos.

### Renderizado en Tiempo Real vs. Offline / Path Tracing
* **Tiempo Real (Videojuegos)**: La escena se calcula instantáneamente entre 30 y 60+ veces por segundo. Presupuesto por fotograma: $\le 16.6\text{ ms}$ (a 60 FPS).
* **Offline (Cine / VFX)**: Cada fotograma individual puede tardar minutos u horas en calcular millones de rebotes de luz con máxima precisión física.

### Frametime (Tiempo de Fotograma)
El tiempo exacto en milisegundos ($ms$) que tarda la tarjeta de video en procesar un cuadro.

### Esquema de 3 Puntos (3-Point Lighting)
* **Key Light (Luz Principal)**: Emisor dominante (100% potencia) colocado a 45° lateral y 45° de elevación.
* **Fill Light (Luz de Relleno)**: Emisor opuesto con menor potencia (25–40%) para rescatar detalles en la penumbra.
* **Rim Light (Contraluz)**: Emisor posterior que genera un filo brillante para despegar al sujeto del fondo.

### Shader (Sombreador)
Programa computacional ejecutado en la GPU que calcula el color de cada píxel combinando luz, material y ángulo de cámara.

### PBR (Physically Based Rendering)
Estándar de renderizado basado en leyes físicas ópticas:
* **Base Color / Albedo**: Color puro sin sombras ni brillos pintados.
* **Roughness**: Micro-textura ($0.0$ espejo, $1.0$ mate).
* **Metallic**: Distingue dieléctricos ($0.0$) de metales puros ($1.0$).

---

## Clase 02: Iluminación Exterior y Movilidad de Luces

### Directional Light (Luz Solar)
Emisor en el infinito con rayos 100% paralelos. Solo influye su rotación (`Ctrl + L`).

### Sky Light (Luz de Cielo / Ambiente)
Luz hemisférica envolvente de 360° que baña las sombras con luz difusa teñida del color del cielo, impidiendo que las sombras sean negras puras ($RGB = 0, 0, 0$).

### Movilidad de Luces (Mobility)
* **Static**: 100% precalculada en mapas de textura (Lightmaps). Cero coste en GPU durante el juego.
* **Stationary**: Híbrida. Luz directa dinámica y rebotes indirectos horneados. Permite cambiar color e intensidad en runtime.
* **Movable**: 100% en tiempo real fotograma a fotograma. Máxima interactividad con mayor coste continuo.

### Regla de los 4 Canales (Stationary Overlap)
Máximo de 4 luces Stationary con sombras solapadas sobre una misma superficie (canales RGBA). Una 5ª luz pasa automáticamente a modo Movable.

---

## Clase 03: Shaders PBR, Master Materials, Texturas ORM y Fuentes Locales

### Master Material vs. Material Instance
* **Master Material (`M_Master_PBR`)**: Shader base parametrizado que contiene las fórmulas matemáticas.
* **Material Instance (`MI_Prop`)**: Copia ligera que permite ajustar texturas y parámetros en tiempo real sin recompilar shaders.

### Texturas Empaquetadas (ORM)
Combinación de tres mapas escalares en los canales R (Ambient Occlusion), G (Roughness) y B (Metallic) de una sola textura RGB.

### Normal Map (Mapa de Normales)
Textura RGB que modifica la orientación de los vectores normales para simular relieve tridimensional sin añadir polígonos a la malla.

### Attenuation Radius (Radio de Atenuación)
Distancia máxima en centímetros donde la potencia de la luz se anula ($I \propto 1/d^2$).

---

## Clase 04: Shaders Nodales Universales, Atmósfera y Niebla Volumétrica

### Sistema Nodal (Node-Based Shading)
Metodología de construcción visual de shaders mediante bloques interconectados. Principio idéntico en Unreal Engine (Material Editor), Unity (Shader Graph), Blender (Shader Editor) y Maya (Hypershade).

### Multiply Node (Operador de Tinte)
Operación matemática que multiplica cada canal de una textura por un color vectorial para variar el tinte de la superficie en tiempo real.

### SkyAtmosphere / Physical Sky
Componente atmosférico basado en física óptica real:
* **Dispersión de Rayleigh**: Genera el cielo azul diurno y los tonos cálidos del atardecer.
* **Dispersión de Mie**: Genera halos y bruma del horizonte.

### Exponential Height Fog (Niebla de Altura)
Niebla analítica que decae con la altitud y la distancia para aportar perspectiva aérea.

### Volumetric Fog (Niebla Volumétrica y God Rays)
Técnica de niebla 3D por vóxeles que interactúa con la luz generando haces luminosos visibles (*God Rays / Light Shafts*).

### Anisotropía de Dispersión ($g$)
Control angular de dispersión luminosa. Valores entre $0.7$ y $0.9$ generan haces frontales intensos (*Forward Scattering*).

### Mood (Atmósfera Escénica)
Uso coordinado de temperatura de color, contraste y niebla volumétrica para definir el tono emocional y narrativo de un entorno 3D.
