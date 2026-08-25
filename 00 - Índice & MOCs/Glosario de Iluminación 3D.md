---
tags:
  - glosario
  - conceptos-basicos
  - iluminacion3d
  - shaders
  - pbr
  - gamedev
date: 2026-08-25
---

# 📖 Glosario de Términos (Organizado Clase a Clase)

Diccionario pedagógico de **Iluminación 3D, Shaders y PBR para Videojuegos**, estructurado en el orden cronológico en que se introducen los conceptos a lo largo del curso.

---

## 🗂️ Índice por Clases
- [Clase 01: Fundamentos de la Luz, Juegos vs. Cine, 3-Point Lighting y Shaders](#-clase-01-fundamentos-3-point-lighting-y-shaders)
- [Clase 02: Iluminación Exterior, Movilidad Técnica y Análisis](#-clase-02-iluminación-exterior-y-movilidad-de-luces)
- [Clase 03: Shaders PBR, Master Materials, Texturas ORM y Luces Locales](#-clase-03-shaders-pbr-master-materials-texturas-orm-y-luces-locales)

---

## 🎓 Clase 01: Fundamentos, 3-Point Lighting y Shaders

### 💡 Luz Digital en 3D
En los motores gráficos la luz no existe físicamente; es un vector matemático con posición, dirección, color e intensidad que interactúa con la geometría de la escena para modelar el volumen.

### 🎮 Real-Time Rendering vs. 🎬 Offline / Path Tracing
* **Real-Time (Videojuegos)**: La escena se calcula instantáneamente entre 30 y 120+ veces por segundo. Presupuesto por fotograma: $\approx 16.6\text{ ms}$ (a 60 FPS).
* **Offline (Cine / VFX)**: Cada fotograma individual puede tardar minutos u horas en calcular millones de rebotes de luz con máxima precisión física.

### ⏱️ Frametime (Tiempo de Fotograma)
El tiempo exacto en milisegundos ($ms$) que tarda la GPU en procesar un cuadro. Mantener el frametime estable por debajo de $16.6\text{ ms}$ es el objetivo clave de optimización.

### 📐 3-Point Lighting (Esquema de 3 Puntos)
Técnica clásica para esculpir tridimensionalidad en un sujeto desde la oscuridad absoluta:
* **Key Light (Luz Principal o Clave)**: La fuente más potente (100% de referencia) colocada a 45° lateral y 45° de elevación. Define el contraste y la dirección de las sombras principales.
* **Fill Light (Luz de Relleno)**: Situada en el lateral opuesto con menor potencia (25–40%). Suaviza las sombras duras para que la penumbra sea legible sin competir con la Key.
* **Rim Light / Back Light (Luz de Contorno o Contraluz)**: Colocada detrás del sujeto. Genera un filo brillante en bordes y hombros para **despegar al personaje del fondo**.

### 🧪 Shader (Sombreador)
Un pequeño programa informático que se ejecuta en paralelo en la GPU. Calcula el color, brillo y reflejo de cada píxel en pantalla según la luz incidente y las propiedades del material.

### 🧱 PBR (Physically Based Rendering)
Estándar de renderizado que simula la interacción física de la luz con las superficies basado en dos leyes: conservación de la energía y microgeometría de las superficies.

### 🎨 Base Color / Albedo
El color puro y plano de una superficie sin sombras pintadas, oclusiones ni brillos especulares.

### 🪞 Roughness (Rugosidad)
Propiedad que define qué tan lisa o áspera es la microestructura de un material:
* **Baja rugosidad ($0.0 - 0.1$)**: Superficie como espejo o cristal; reflejos especulares nítidos y concentrados.
* **Alta rugosidad ($0.8 - 1.0$)**: Superficie mate (tiza, tela, piel seca); la luz se dispersa suavemente en todas direcciones.

### ⚙️ Metallic (Metalicidad)
Parámetro que distingue los materiales conductores de los dieléctricos:
* **$0.0$ (No-Metal / Dieléctrico)**: Madera, plástico, piel, tela, piedra.
* **$1.0$ (Metal Puro)**: Oro, cromo, hierro, cobre, aluminio.

---

## 🎓 Clase 02: Iluminación Exterior y Movilidad de Luces

### ☀️ Directional Light (Luz Direccional / Sol)
Fuente de luz que simula un emisor a distancia infinita. Todos sus rayos viajan en **líneas 100% paralelas**. Su posición en el mundo no importa; solo influye su **rotación** (atajo: <kbd>Ctrl + L</kbd>).

### 🌌 Sky Light (Luz de Cielo / Ambiente)
Luz hemisférica envolvente de 360° que captura la cúpula celeste o un mapa HDRI. Baña las superficies en sombra con luz difusa teñida del color del cielo, **impidiendo que las sombras sean negras puras ($RGB = 0, 0, 0$)**.

### 🔄 Movilidad de Luces (Mobility)
Propiedad fundamental en Unreal Engine que define cómo se calculan la luz y las sombras en GPU:
* **🪨 Static (Estática)**: 100% precalculada en mapas de textura (**Lightmaps**). Cero coste de sombras dinámicas en runtime. Ideal para VR a 90 FPS y móviles.
* **⚖️ Stationary (Estacionaria)**: Híbrida. La luz directa y sombras sobre personajes son dinámicas; los rebotes indirectos van horneados. Permite cambiar color e intensidad en runtime pero no mover su posición.
* **🏃 Movable (Dinámica / Móvil)**: 100% en tiempo real fotograma a fotograma. Soporta movimiento, linternas, física y sistemas como Lumen, con mayor coste continuo en GPU.

### 🍞 Baking / Lightmass (Horneado de Luz)
El proceso de simular previamente la iluminación compleja y estamparla como sombras y colores fijos dentro de mapas de textura 2D (**Lightmaps**).

### 🚨 Regla de los 4 Canales (Stationary Overlap Limit)
En el renderizador diferido clásico de Unreal, solo pueden solaparse un máximo de **4 luces Stationary que proyecten sombras** en un mismo espacio (canales RGBA). Una 5ª luz se marca con una cruz roja (`❌`) y pasa automáticamente a modo *Movable*, duplicando el coste.

### 📶 Cascaded Shadow Maps (CSM - Sombras en Cascada)
Técnica para luces direccionales que divide el cono de visión de la cámara en capas de distancia: sombras nítidas y detalladas cerca de la cámara que reducen su resolución a lo lejos para ahorrar rendimiento.

### 🌡️ Color Temperature (Temperatura de Color / Kelvin)
Escala física ($K$) que describe el tono cromático de la luz: cálida ($2000K-3000K$), neutra ($5500K-6500K$) o fría ($7500K-10000K$).

### 🌫️ Atmospheric Scattering (Dispersión Atmosférica)
Fenómeno físico donde los rayos solares chocan con moléculas de gas y partículas en el aire (*Rayleigh y Mie Scattering*), creando cielos azules al mediodía y tonos anaranjados en el atardecer.

---

## 🎓 Clase 03: Shaders PBR, Master Materials, Texturas ORM y Luces Locales

### 🎛️ Master Material (Material Maestro)
Shader base parametrizado que contiene toda la lógica matemática y slots de texturas. Se compila una sola vez y sirve como plantilla matriz para todo el proyecto.

### 📄 Material Instance (Instancia de Material)
Hijo liviano de un Master Material. Permite intercambiar texturas, modificar valores de rugosidad, metalicidad o tintes de color **al instante en el Viewport sin recompilar shaders**.

### 🔢 Scalar Parameter (Parámetro Escalar)
Un número decimal configurable expuesto en una instancia de material (por ejemplo: multiplicador de rugosidad, escala de UV Tiling, intensidad emisiva).

### 🎨 Vector Parameter (Parámetro Vectorial)
Un valor de 4 canales (RGBA) expuesto en una instancia de material para controlar tintes cromáticos y colores base.

### 📦 Textura Empaquetada (Channel Packing / ORM)
Técnica de optimización que guarda tres mapas en escala de grises dentro de una sola textura RGB de 8 bits por canal:
* **Canal R (Rojo)**: **O**clusión Ambiental (*Ambient Occlusion*).
* **Canal G (Verde)**: **R**ugosidad (*Roughness*).
* **Canal B (Azul)**: **M**etalicidad (*Metallic*).

### ⚡ Texture Sampler (Muestreador de Texturas)
La operación en GPU que lee un píxel de una textura. El empaquetado ORM reduce el número de samplers necesarios de 3 lecturas a 1 sola llamada, ahorrando memoria VRAM y ancho de banda.

### 🌑 Ambient Occlusion (AO - Oclusión Ambiental)
Sombreado suave de micro-contacto que se produce de forma natural en grietas, cuencas oculares, pliegues de la nariz y hendiduras donde la luz ambiental difusa tiene dificultad para penetrar.

### 🗺️ Normal Map (Mapa de Normales)
Textura RGB que modifica la orientación de los vectores normales de la superficie para simular arrugas, poros, biseles y relieve 3D sin añadir polígonos a la malla.

### 🎚️ FlattenNormal (Fuerza de Normales)
Función en el Shader Graph que permite suavizar o exagerar la intensidad del relieve de un Normal Map mediante un parámetro escalar.

### 📐 UV Tiling (Texture Coordinate)
Multiplicador que define cuántas veces se repite una textura a lo largo de las coordenadas UV de la malla 3D.

### 💡 Point Light (Luz Puntual)
Fuente de luz que emite en **360° omnidireccional** desde un punto. Casos de uso: bombillas, velas, fuego, chispas.

### 🔦 Spot Light (Luz Focal / Cono)
Fuente de luz que proyecta un haz cónico direccional controlado por dos ángulos:
* **Inner Cone Angle**: Ángulo central con el 100% de intensidad.
* **Outer Cone Angle**: Ángulo exterior donde la intensidad decae suavemente a cero (penumbra).

### 🔲 Rect Light (Luz Rectangular / de Área)
Fuente de luz que emite desde una superficie plana rectangular en una semiesfera (Softbox fotográfico, paneles LED, pantallas de televisión).

### ⭕ Attenuation Radius (Radio de Atenuación)
La distancia física máxima en centímetros donde la luz deja de calcularse ($I \propto 1/d^2$). Mantenerlo ceñido evita que la luz atraviese paredes y provoque sobrecoste en habitaciones vecinas.

### ⚪ Source Radius / Soft Source Radius
Propiedad que define el radio geométrico del emisor de luz para suavizar las penumbras de sombra y generar reflejos especulares de tamaño realista.

### 💡 IES Profile (Perfil Fotométrico)
Textura fotométrica estandarizada `.ies` provista por fabricantes reales (como Philips u Osram) que describe con exactitud la distribución angular de la luz a través del cristal o reflector de una lámpara.

### 🎭 Iluminación Rembrandt
Técnica clásica de retrato donde la luz principal incide a 45° lateral, proyectando una sombra en la nariz que se une con la mejilla para formar un **pequeño triángulo luminoso** debajo del ojo en el lado en penumbra.

### ✨ Eye Catchlight (Brillo en la Pupila)
El pequeño punto o reflejo especular brillante que una fuente de luz puntual o focal produce en la córnea del ojo de un personaje, aportándole vida y viveza visual.

### 🔴 Shader Overdraw (Sobredibujado de Shaders)
Problema de rendimiento que ocurre cuando múltiples luces solapan sus radios de atenuación sobre los mismos píxeles de la pantalla, obligando a la GPU a recalcular la iluminación de esa superficie varias veces.

---
**Notas relacionadas**:
- [[MOC - Iluminación para Videojuegos]]
- [[Clase 01 - Introducción a la Iluminación 3D y Shaders]]
- [[Clase 02 - Práctica 3-Point, Luz Solar, Cielo y Movilidad]]
- [[Clase 03 - Shaders PBR, Master Materials y Luces Locales]]
- [[01 - Fundamentos PBR y Mapas de Textura]]
- [[02 - Anatomía del Shader Graph en Unreal (Master Materials e Instances)]]
