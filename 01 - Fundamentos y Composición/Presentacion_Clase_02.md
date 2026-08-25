---
tags:
  - presentacion
  - diapositivas
  - clase02
  - iluminacion3d
  - shaders
date: 2026-08-18
---

# 📽️ Presentación: Clase 02 — Taller 3-Point, Sol, Cielo y Movilidad

> **Ramo**: Iluminación 3D y Shaders para Videojuegos  
> **Duración estimada**: 60 – 90 minutos  
> **Estructura**: 8 Diapositivas interactivas + Taller en Vivo en Unreal Engine 5  
> **Formato en vivo**: [Presentación en Pantalla / Proyector (HTML)](file:///c:/Users/danie/OneDrive/Escritorio/Iluminacion3D/Presentacion_Clase_02.html)

---

## 🗂️ Índice de Diapositivas

```
[ Diapositiva 01 ] ──► Portada & La Ecuación Fundamental (Luz × Material)
[ Diapositiva 02 ] ──► Taller en Vivo: Esquema de 3 Puntos (Key, Fill, Rim)
[ Diapositiva 03 ] ──► Cómo reacciona el Shader PBR a cada Luz (Roughness y Brillo)
[ Diapositiva 04 ] ──► El Mundo Exterior: Directional Light (Sol) y Rayos Paralelos
[ Diapositiva 05 ] ──► Sky Light: La Cúpula Celeste y por qué no hay sombras negras
[ Diapositiva 06 ] ──► Movilidad de Luces: Static vs. Stationary vs. Movable
[ Diapositiva 07 ] ──► Casos Reales con Enlaces: The Last of Us, Cyberpunk, Zelda y RE4
[ Diapositiva 08 ] ──► Desafío Práctico para los Alumnos & Próxima Clase
```

---

## 🎞️ Contenido y Puntos de Charla

### 🟢 Diapositiva 01: Portada y La Ecuación Fundamental
* **Título**: Luz y Shaders: Dos caras de la misma moneda.
* **La fórmula mental**:
  $$\text{Píxel Final} = \text{Luz (Ángulo + Color + Intensidad)} \times \text{Shader (Albedo + Roughness + Normal)}$$
* **Explicación**:
  * La **Luz** aporta los fotones y define el volumen espacial.
  * El **Shader** decide qué porcentaje de esos fotones se absorben (Albedo), cuántos rebotan como espejo (Roughness) o dispersan internamente (SSS).

---

### 🟢 Diapositiva 02: Taller en Vivo - 3-Point Lighting
* **1. Key Light (100%)**: 45° a un lateral y 45° de elevación. Establece la dirección dominante y esculpe las sombras principales.
* **2. Fill Light (25–40%)**: Lateral opuesto. Suaviza las sombras duras para rescatar detalle en la penumbra.
* **3. Rim Light (Contraluz)**: Detrás del sujeto. Traza una línea brillante en hombros y silueta para despegarlo del fondo oscuro.

---

### 🟢 Diapositiva 03: ¿Cómo interactúa el Shader con las 3 Luces?
* **Superficies Pulidas ($Roughness = 0.05 - 0.15$)**:
  * *Ejemplos*: Casco de astronauta, armadura de cromo, espada de acero, mármol pulido.
  * Puntos especulares diminutos y cegadores (*Specular Highlights*). La Rim Light produce un filo brillante.
* **Superficies Mates ($Roughness = 0.70 - 0.95$)**:
  * *Ejemplos*: Tela de abrigo, piel seca, madera rústica, hormigón.
  * La luz se dispersa suavemente. La **Fill Light es imprescindible** para evitar manchas negras planas.

---

### 🟢 Diapositiva 04: Directional Light (El Sol o la Luna)
* **Comportamiento físico**: Rayos 100% paralelos que provienen de una distancia infinita.
* **Regla técnica**: Mover la posición $X,Y,Z$ en el mapa no cambia nada; **solo importa su rotación**.
* **Ejemplo práctico**:
  * Mediodía ($90^\circ$ vertical): Sombras cortas y duras (desierto de *Red Dead Redemption 2*).
  * Atardecer ($15^\circ$ rasante): Sombras alargadas y luz dorada dramática.
* **Atajo**: Mantener <kbd>Ctrl + L</kbd> y arrastrar el ratón en el Viewport.

---

### 🟢 Diapositiva 05: Sky Light (Luz de Cielo y Atmósfera)
* **Concepto**: La atmósfera terrestre dispersa la luz azul en todas direcciones. La Sky Light simula esa cúpula envolvente de 360°.
* **Función**: Baña las superficies en sombra con luz difusa, evitando el negro absoluto ($RGB = 0, 0, 0$).
* **Modos en UE5**:
  * *Real Time Capture*: Recalcula el color ambiental en tiempo real cuando el sol gira.
  * *Specified Cubemap*: Carga mapas HDRI fotográficos para look cinematográfico.

---

### 🟢 Diapositiva 06: Movilidad Técnica de Luces (El Presupuesto de GPU)
* **🪨 Static (Estática)**: 100% horneada en Lightmaps. Cero coste de sombras dinámicas en runtime. Ideal para VR a 90 FPS y móviles.
* **⚖️ Stationary (Estacionaria)**: Híbrida. Sombras dinámicas sobre personajes + rebotes horneados. Permite cambiar color/intensidad. *Límite de 4 luces solapadas (canales RGBA)*.
* **🏃 Movable (Dinámica)**: 100% en tiempo real por fotograma. Máxima libertad para Lumen, linternas y ciclos día/noche.

---

### 🟢 Diapositiva 07: Casos de Estudio en la Industria (con Enlaces Oficiales)
* 🌿 [The Last of Us Part I/II (GDC Talk)](https://www.youtube.com/watch?v=R9_mD4oI6fU): Baking de ultra-precisión para fotorrealismo en interiores desolados + linterna dinámica en combate.
* 🏙️ [Cyberpunk 2077 (RTX / Path Tracing Breakdown)](https://www.youtube.com/watch?v=a3YxH_xK004): 100% dinámico y trazado de rayos por la enorme densidad de neones emisivos y clima variable.
* 🗡️ [Zelda: Tears of the Kingdom (Nintendo)](https://www.nintendo.com/games/detail/the-legend-of-zelda-tears-of-the-kingdom-switch/): Directional + Sky limpio con cel-shading y sombras en cascada optimizadas para Nintendo Switch.
* 🧟 [Resident Evil 4 Remake (Capcom RE Engine)](https://www.residentevil.com/re4/): Atmósfera claustrofóbica construida sobre la ausencia de luz solar, niebla volumétrica y la linterna del protagonista.

---

### 🟢 Diapositiva 08: Desafío Práctico en Clase
1. **Misión 1 (Interior)**: Busto 3D en 3 puntos. Crear nivel vacío, posicionar Key (45°), Fill (30%) y Rim. Modificar el *Roughness* (0.05 a 0.9) para ver la respuesta del material.
2. **Misión 2 (Exterior)**: Añadir Directional Light y Sky Light. Simular un atardecer cálido con <kbd>Ctrl + L</kbd> y verificar el tinte azulado en las sombras.

---
**Notas relacionadas**:
- [[MOC - Iluminación para Videojuegos]]
- [[Clase 02 - Práctica 3-Point, Luz Solar, Cielo y Movilidad]]
- [[Fundamentos PBR y Mapas de Textura]]
- [[Movilidad de Luces (Static, Stationary, Movable)]]
