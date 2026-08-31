---
tags:
  - iluminacion3d
  - shaders
  - pbr
  - gamedev
  - unreal-engine
  - moc
date: 2026-08-25
---

# MOC - Iluminación 3D y Shaders para Videojuegos

Base de conocimiento integral para el ramo de **Iluminación 3D y Shaders para Videojuegos** (Game Lighting, Shaders, PBR & Tech Art).

---

## Accesos Rápidos
-  [[Glosario de Iluminación 3D]]: Diccionario unificado de términos de Iluminación, PBR y Shaders.
-  [[Clase 01 - Introducción a la Iluminación 3D y Shaders]]
-  [[Clase 02 - Práctica 3-Point, Luz Solar, Cielo y Movilidad]] |  [Material Visual PDF (Clase 02)](file:///c:/Users/danie/OneDrive/Escritorio/Iluminacion3D/Material_Visual_Clase_02.pdf) |  [Presentación HTML](file:///c:/Users/danie/OneDrive/Escritorio/Iluminacion3D/Presentacion_Clase_02.html)
-  [[Clase 03 - Shaders PBR, Master Materials y Luces Locales]] |  [Material Visual PDF (Clase 03)](file:///c:/Users/danie/OneDrive/Escritorio/Iluminacion3D/Material_Visual_Clase_03.pdf) |  [Presentación HTML](file:///c:/Users/danie/OneDrive/Escritorio/Iluminacion3D/Presentacion_Clase_03.html)

---

## Módulos Integrados del Ramo

### 1.  Fundamentos, Clases y Composición
- [[Clase 01 - Introducción a la Iluminación 3D y Shaders]]
- [[Clase 02 - Práctica 3-Point, Luz Solar, Cielo y Movilidad]]
- [[Clase 03 - Shaders PBR, Master Materials y Luces Locales]]
- [[Presentacion_Clase_02]] | [[Presentacion_Clase_03]]
- [[Lenguaje Visual y Guía al Jugador]]: Cómo dirigir la mirada del jugador, affordance y contraste.

### 2.  Shaders, Materiales y Pipeline PBR
- [[01 - Fundamentos PBR y Mapas de Textura]]: Base Color, Roughness, Metallic, Normal, AO y texturas ORM.
- [[02 - Anatomía del Shader Graph en Unreal (Master Materials e Instances)]]: Flujo profesional, parámetros y optimización.
- [[03 - Modelos de Sombreado (Shading Models)]]: Default Lit, Subsurface Scattering (piel/cera), Two Sided Foliage, Clear Coat.
- [[04 - Matemáticas de Shaders Esenciales (Fresnel, Lerp y Normales)]]: Fresnel, Lerp, Panning, World Position Offset.

### 3.  Fuentes de Luz y Movilidad en Motores
- [[Tipos de Luces en Unreal Engine]]: Directional Light, Point Light, Spot Light, Rect Light y Sky Light.
- [[Movilidad de Luces (Static, Stationary, Movable)]]: Cuándo usar cada movilidad, canales de sombras y costes.

### 4.  Iluminación Global (GI) y Baking
- [[Lumen vs Baked Lighting (UE5)]]: Arquitectura de Lumen vs Lightmass tradicional.

### 5.  Atmósfera, Niebla y Sombras
- [[Atmósfera y Niebla Volumétrica en UE5]]: SkyAtmosphere, Volumetric Cloud, Exponential Height Fog y God Rays.

### 6.  Post-Processing y Color Management
- [[Exposición, Color Grading y ACES en UE5]]: PostProcessVolume, Auto-Exposure, Curvas de Tonemapping y LUTs.

### 7.  Optimización y Rendimiento (Tech Art)
- [[Optimización de Iluminación y Profiling en UE5]]: `stat gpu`, GPU Visualizer (`Ctrl + Shift + ,`), Draw Calls y complejidad de shaders y luces.

---

> [!TIP] Atajos clave en el Viewport de Unreal Engine
> - `Alt + 4`: Vista Lit (Iluminada).
> - `Alt + 3`: Vista Unlit (Sin iluminación / Texturas base).
> - `Alt + 8`: Vista Light Complexity (Verde = óptimo, Rojo/Blanco = sobrecoste).
> - `Ctrl + L`: Mover el sol/luz direccional interactivamente.
> - `G`: Game View (Oculta iconos y gizmos).
