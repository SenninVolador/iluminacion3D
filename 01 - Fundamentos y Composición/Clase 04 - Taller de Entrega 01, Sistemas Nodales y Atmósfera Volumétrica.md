---
tags:
  - clase04
  - entrega01
  - rubrica
  - shaders-nodales
  - atmosfera
  - niebla-volumetrica
  - mood
date: 2026-08-31
---

# Clase 04: Taller de Entrega N°1, Shaders Nodales Universales y Atmósfera Volumétrica

Iluminación 3D · Docente Daniel Rojas (UNIACC)

---

## Estructura y Dinámica de la Sesión

La sesión se articula en dos bloques pedagógicos complementarios:

1. **Bloque 1 (Taller de Apoyo y Calificación en Vivo)**:
   * Revisión individual y apoyo a los estudiantes para afinar su **Entrega N°1 (Estudio de 3 Puntos y Shader Paramétrico)**.
   * Plazo de entrega final: Cierre de la sesión con calificación inmediata según la **Rúbrica Oficial (Escala 1.0 a 7.0)**.
   * Análisis de la lógica universal de los sistemas nodales (*Shader Graphs*).
2. **Bloque 2 (Atmósfera, Cielo, Niebla Volumétrica y Mood)**:
   * Introducción a los componentes atmosféricos para construir ambientación cinematográfica y profundidad espacial.
   * Mapeo de terminología: nombres de componentes en Unreal Engine vs. nombres genéricos en la industria (Unity, Blender, Maya, Godot).

---

## 1. Bloque 1: Shaders Nodales Universales y Calificación

### Universalidad de los Sistemas Nodales
Un principio técnico fundamental del arte técnico: **los editores de materiales basados en nodos operan bajo la misma lógica matemática en cualquier software**:

| Motor / Software | Editor de Shaders | Nodo Maestro de Salida | Operador de Tinte |
| :--- | :--- | :--- | :--- |
| **Unreal Engine 5** | Material Graph | `Master Material (Root Node)` | `Multiply` + Vector Parameter |
| **Unity (URP / HDRP)**| Shader Graph | `Fragment / PBR Master` | `Multiply` + Color Property |
| **Blender** | Shader Editor | `Principled BSDF` | `Mix Color (Multiply)` |
| **Autodesk Maya** | Hypershade | `Standard Surface (aiStandard)`| `multiplyDivide` |
| **Godot Engine** | VisualShader | `VisualShaderNodePBR` | `VisualShaderNodeVectorOp` |

```
[ Texture Sample: Albedo (RGB) ] ──┐
                                   ├──► [ MULTIPLY ] ──► Base Color (Master Node)
[ Vector Parameter: Color Tint ] ──┘

[ Scalar Parameter: Roughness ]  ──────────────────────► Roughness (Master Node)
[ Scalar Parameter: Metallic ]   ──────────────────────► Metallic (Master Node)

[ Texture Sample: Normal Map ]   ──► [ Multiply / FlattenNormal ] ──► Normal (Master Node)
```

### Arquitectura del Shader Paramétrico (Caso Utah Teapot):
1. **Multiply (Tinte Cromático)**: Multiplica los valores normalizados ($0.0 - 1.0$) de cada canal de la textura por un color vectorial, permitiendo teñir la superficie en tiempo real sin abrir Photoshop.
2. **Roughness (Rugosidad)**: Controla la dispersión de microfacetas.
3. **Metallic (Metalicidad)**: Define si la reflectancia especular toma el color del albedo (metal) o se mantiene neutra (dieléctrico).
4. **Normal Strength (Intensidad de Normales)**: Escala los vectores tangenciales $X$ e $Y$ para profundizar o atenuar el relieve aparente.

---

## 2. Bloque 2: Atmósfera, Cielo y Niebla Volumétrica

Para dotar a una escena 3D de atmósfera, escala y **mood (estado anímico/narrativo)**, los motores gráficos integran un conjunto coordinado de componentes ambientales.

### Equivalencias Técnicas: Unreal Engine vs. Industria

| Componente en Unreal Engine 5 | Nombre Genérico en la Industria | Función Técnica Principal |
| :--- | :--- | :--- |
| **Directional Light** | *Sun Light / Infinite Light* | Emisor a distancia infinita con rayos estrictamente paralelos. Modela el sol o la luna. |
| **SkyAtmosphere** | *Physical Sky / Atmospheric Scattering* | Simula la dispersión óptica de Rayleigh y Mie en los gases de la atmósfera según el ángulo solar. |
| **Sky Light** | *Environment Probe / Ambient Dome* | Captura la radiancia difusa de 360° para bañar las sombras, impidiendo negros absolutos. |
| **Exponential Height Fog** | *Height Fog / Distance Fog* | Niebla analítica basada en altitud y distancia para aportar perspectiva aérea y profundidad. |
| **Volumetric Fog** | *Media Scatter / Voxel Fog* | Niebla volumétrica resuelta en una grilla 3D de vóxeles que interactúa con la luz creando **God Rays**. |
| **Volumetric Clouds** | *Procedural Cloud Layer* | Capa de nubes 3D volumétricas con auto-sombreado y sombras proyectadas en el suelo. |

---

### Física Atmosférica: Dispersión de Rayleigh y Mie

* **Dispersión de Rayleigh (Moléculas de gas)**:
  * Las partículas diminutas de la atmósfera dispersan con mayor facilidad las longitudes de onda cortas (azul/violeta).
  * Por eso el cielo es azul al mediodía y se torna naranja o rojo en el atardecer (cuando los rayos solares atraviesan una capa atmosférica mucho más densa).
* **Dispersión de Mie (Polvo, bruma y humedad)**:
  * Partículas más grandes generan el halo luminoso alrededor del disco solar y la neblina blanquecina en el horizonte.

---

### Niebla Volumétrica y Rayos Crepusculares (God Rays)

Al habilitar la niebla volumétrica, cada haz de luz interactúa con las partículas suspendidas en el aire:

1. **Frustum Voxel Grid**: El motor subdivide el volumen visual de la cámara en miles de celdas cúbicas 3D (vóxeles).
2. **Anisotropía de Dispersión (Parámetro $g$)**:
   * `$g = 0.0$`: Dispersión isotrópica (la niebla brilla igual sin importar hacia dónde mires).
   * `$g = 0.7 - 0.9$`: Dispersión hacia adelante (*Forward Scattering*). Genera haces de luz intensos y contrastados (**God Rays / Light Shafts**) cuando la cámara encuadra en dirección a la fuente de luz.

---

## 3. Desafío Práctico de la Sesión

1. **Cierre de Entrega N°1**: Revisar la calibración de las 3 luces (Key, Fill, Rim) y verificar que los 3 parámetros de la Instancia de Material funcionen correctamente en el Viewport.
2. **Taller de Atmósfera**: Añadir `SkyAtmosphere`, `Exponential Height Fog` y activar `Volumetric Fog`. Calibrar la anisotropía a $0.75$ y posicionar una luz que atraviese una abertura para proyectar rayos de luz volumétricos.

---
**Documentos relacionados**:
- [[Rubrica_Entrega_01_3Point_y_Shaders]]
- [[Clase 02 - Práctica 3-Point, Luz Solar, Cielo y Movilidad]]
- [[Clase 03 - Shaders PBR, Master Materials y Luces Locales]]
- [[Atmósfera y Niebla Volumétrica en UE5]]
- [[04 - Matemáticas de Shaders Esenciales (Fresnel, Lerp y Normales)]]
