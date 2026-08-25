---
tags:
  - unreal-engine
  - atmosfera
  - niebla
  - volumetrics
date: 2026-08-18
---

# 🌫️ Atmósfera, Cielo y Niebla Volumétrica en UE5

El sistema de atmósfera y niebla en Unreal Engine 5 proporciona profundidad, escala planetaria, perspectiva aérea y dramatismo cinematográfico mediante dispersión de luz basada en física real (*Rayleigh & Mie Scattering*).

---

## 🧩 El Stack de Iluminación Ambiental Exterior (Los 5 Actores Clave)

Para crear un entorno exterior realista en UE5, siempre se combinan estos 5 componentes en el nivel:

1. **Directional Light** (Con `Atmosphere Sun Light` activado).
2. **SkyAtmosphere** (Calcula la dispersión física de la atmósfera y el color del cielo según el ángulo solar).
3. **Sky Light** (Con `Real Time Capture` para rebotes de luz ambiental).
4. **Volumetric Cloud** (Simulación volumétrica de nubes procedurales con sombras en el suelo).
5. **Exponential Height Fog** (Con `Volumetric Fog` activado para rayos de luz y profundidad).

---

## 🔬 1. SkyAtmosphere: Física del Cielo

Simula la atmósfera de la Tierra (o de planetas alienígenas) calculando cómo la luz solar interactúa con las moléculas de aire:

* **Rayleigh Scattering (Dispersión de Rayleigh)**:
  * Dispersión de partículas muy pequeñas (gases atmosféricos).
  * Da al cielo su color azul durante el mediodía y tonos naranjas/rojizos en el atardecer (cuando la luz debe atravesar una capa de atmósfera más gruesa).
* **Mie Scattering (Dispersión de Mie)**:
  * Dispersión causada por partículas más grandes (polvo, polen, humedad/aerosoles).
  * Crea el halo brillante blanco/dorado alrededor del sol y la bruma del horizonte.
* **Absorption (Capa de Ozono)**:
  * Absorbe longitudes de onda específicas, dando al cielo el tono azul profundo característico durante la hora azul (justo después del atardecer).

---

## 🌫️ 2. Exponential Height Fog y Volumetric Fog

El actor **Exponential Height Fog** agrega densidad de niebla basada en la altitud (más densa en los valles, más clara en las cumbres).

### 💡 Activación de Niebla Volumétrica (Volumetric Fog)
Al activar la casilla `Volumetric Fog` dentro del componente:
1. El motor divide el cono de visión de la cámara en una cuadrícula 3D de vóxeles (*Frustum Voxel Grid*).
2. Cada luz (Point, Spot, Directional) puede iluminar e interactuar físicamente con esas partículas de niebla.
3. Se generan **Rayos Crepusculares (God Rays / Light Shafts)** cuando objetos o ventanas bloquean parcialmente la luz.

### Parámetros Críticos de la Niebla Volumétrica:
* **Fog Density**: Densidad base de la niebla.
* **Fog Height Falloff**: Cuán rápido desaparece la niebla a medida que subes en el eje Z.
* **Volumetric Fog Scattering Distribution (Anisotropía - $g$)**:
  * Controla la dirección en que se dispersa la luz al chocar con la niebla:
  * `0.0`: Dispersión isotrópica (igual en todas direcciones).
  * `> 0.5` (ej. `0.7` a `0.9`): Fuerte dispersión hacia adelante (*Forward Scattering*). Crea haces de luz y halos espectaculares cuando miras en dirección a la fuente de luz.
* **Volumetric Fog Extinction Scale**: Cuánta luz absorbe la niebla (valores altos oscurecen la niebla lejana).

---

## ⚙️ Control por Luz de la Niebla Volumétrica

Cada luz individual en tu nivel tiene dos parámetros específicos para afinar su impacto volumétrico:

* **Cast Volumetric Shadow**: Determina si los objetos que intersecan la luz proyectan sombras dentro de la niebla.
* **Volumetric Scattering Intensity**: Multiplicador de brillo específico dentro del volumen de niebla.
  * *Tip Pro*: Puedes dejar la luz tenue en las superficies pero subir este valor a `2.0` o `4.0` para que el haz de luz se vea intenso y cinematográfico.

---

> [!WARNING] Coste de Rendimiento
> La niebla volumétrica renderiza a una resolución de grid (por defecto $280 \times 160 \times 64$).
> - Puedes ajustar la calidad o distancia máxima con el comando de consola:
>   `r.VolumetricFog.GridPixelSize 8` (por defecto es 16; números menores aumentan calidad pero bajan FPS).
>   `r.VolumetricFog.HistoryMissSuperSampling 1`

---
**Notas relacionadas**:
- [[Tipos de Luces en Unreal Engine]]
- [[Lumen vs Baked Lighting (UE5)]]
- [[Exposición, Color Grading y ACES en UE5]]
