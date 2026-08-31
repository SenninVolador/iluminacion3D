---
tags:
  - presentacion
  - diapositivas
  - clase04
  - shaders-nodales
  - atmosfera
  - niebla-volumetrica
date: 2026-08-31
---

# Presentación: Clase 04 — Taller de Entrega N°1, Shaders Nodales y Atmósfera Volumétrica

> **Ramo**: Iluminación 3D  
> **Docente**: Daniel Rojas (UNIACC)  
> **Estructura**: 7 Diapositivas + Taller presencial con calificación en vivo  
> **Presentación en Pantalla**: [Presentación en Pantalla / Proyector (HTML)](file:///c:/Users/danie/OneDrive/Escritorio/Iluminacion3D/Presentacion_Clase_04.html)  
> **Ficha Técnica Editorial**: [Material Visual Clase 04 (PDF)](file:///c:/Users/danie/OneDrive/Escritorio/Iluminacion3D/Material_Visual_Clase_04.pdf)

---

## Índice de Diapositivas

```
[ Diapositiva 01 ] ──► Portada: Taller de Entrega N°1, Shaders Nodales y Atmósfera
[ Diapositiva 02 ] ──► Bloque 1: Entrega N°1, Requisitos y Calificación en Vivo
[ Diapositiva 03 ] ──► Shaders Nodales Universales: Lógica de Motores (Unreal, Unity, Blender, Maya)
[ Diapositiva 04 ] ──► Bloque 2: Stack Ambiental Exterior y Nombres en la Industria
[ Diapositiva 05 ] ──► Física Atmosférica: Dispersión de Rayleigh y Mie
[ Diapositiva 06 ] ──► Niebla Volumétrica por Vóxeles y Rayos de Luz (God Rays)
[ Diapositiva 07 ] ──► Desafío Práctico en Clase & Cierre de la Sesión
```

---

## Puntos de Charla y Guión

### Diapositiva 01: Portada y Estructura
* **Objetivo dual**: Primera mitad de la clase para corrección y entrega formal con calificación inmediata; segunda mitad para abrir el mundo exterior con atmósfera, niebla volumétrica y mood.

---

### Diapositiva 02: Entrega N°1 y Rúbrica
* Repasar con los estudiantes la tabla de 60 puntos: Key Light (7 pts), Fill Light (7 pts), Rim Light (6 pts), Material PBR (15 pts), Instancia con 3+ parámetros (15 pts), Nomenclatura y orden (10 pts).
* Aclarar dudas de calibración de intensidad o sombras cruzadas en vivo antes del cierre.

---

### Diapositiva 03: Sistemas Nodales Universales
* Demostrar que un *Shader Graph* es idéntico en Unreal, Unity, Blender o Maya.
* Operador `Multiply`: multiplicar textura por un color vectorial para tintes en tiempo real.
* Parámetros escalares: `Roughness` y `Metallic`.
* Manipulación de normales: `Normal Strength` / `FlattenNormal`.

---

### Diapositiva 04: Stack Ambiental Exterior y Equivalencias
* Desmitificar nombres propios de Unreal:
  * `Directional Light` = *Sun Light / Infinite Light*.
  * `SkyAtmosphere` = *Physical Sky / Atmospheric Scattering*.
  * `Sky Light` = *Ambient Probe / Environment Dome*.
  * `Exponential Height Fog` = *Height Fog / Distance Fog*.
  * `Volumetric Fog` = *Media Scatter / Voxel Fog*.

---

### Diapositiva 05: Física Atmosférica (Rayleigh y Mie)
* **Rayleigh**: Moléculas pequeñas que dispersan luz azul de día y tiñen el sol de rojo/naranja al atardecer por la distancia que recorren los rayos.
* **Mie**: Partículas más grandes (polvo, bruma) que causan el halo solar y la dispersión frontal.

---

### Diapositiva 06: Niebla Volumétrica y God Rays
* Explicar la grilla 3D de vóxeles del frustum de cámara.
* El parámetro de **Anisotropía ($g$)**: cómo subirlo a `0.75` produce rayos crepusculares cinematográficos (*God Rays*) que guían la mirada del jugador.

---

### Diapositiva 07: Desafío en Clase
1. Subir entrega formal y recibir nota presencial según rúbrica.
2. Construir un nivel exterior con sol, cielo físico y niebla volumétrica con rayos de luz visibles.

---
**Notas relacionadas**:
- [[Rubrica_Entrega_01_3Point_y_Shaders]]
- [[Clase 02 - Práctica 3-Point, Luz Solar, Cielo y Movilidad]]
- [[Clase 03 - Shaders PBR, Master Materials y Luces Locales]]
- [[Atmósfera y Niebla Volumétrica en UE5]]
- [[04 - Matemáticas de Shaders Esenciales (Fresnel, Lerp y Normales)]]
