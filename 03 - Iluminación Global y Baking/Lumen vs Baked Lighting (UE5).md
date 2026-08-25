---
tags:
  - unreal-engine
  - lumen
  - baking
  - global-illumination
date: 2026-08-18
---

# 🌐 Lumen vs. Baked Lighting en Unreal Engine 5

La iluminación global (GI) simula cómo la luz rebota en las superficies, tiñendo el entorno (*color bleeding*) y rellenando los interiores de forma natural. En Unreal Engine 5 existen dos filosofías principales: **Lumen (Dinámico)** y **Lightmass (Horneado / Baked)**.

---

## ⚡ 1. Lumen: Iluminación Global y Reflejos en Tiempo Real

Lumen es el sistema de iluminación global y reflejos dinámico de UE5. Diseñado para trabajar de la mano con **Nanite** y **Virtual Shadow Maps (VSM)**.

### ¿Cómo funciona la arquitectura de Lumen?
Lumen combina varias técnicas para resolver rebotes de luz sin necesidad de hardware dedicado a Raytracing en todo momento:

1. **Screen Traces (Trazado en espacio de pantalla)**:
   * Traza rayos rápidos sobre lo que ya es visible en la cámara.
   * Muy rápido y detallado, pero si algo sale de la pantalla (fuera de cámara), no tiene datos.
2. **Mesh Distance Fields (Software Ray Tracing - SRT)**:
   * Representación volumétrica simplificada de cada Static Mesh (SDF).
   * Permite a Lumen trazar rayos en el mundo 3D independientemente del campo de visión de la cámara.
   * Funciona en cualquier GPU moderna (no requiere RT Cores).
3. **Surface Cache (Caché de Superficie)**:
   * Captura la textura y el color de los objetos desde diferentes ángulos a baja resolución para que los rayos sepan qué color rebotar.
4. **Hardware Ray Tracing (HWRT)**:
   * Modo opcional de máxima calidad para GPUs compatibles (RTX / RDNA2+).
   * Traza rayos contra la geometría real y soporta Skinned Meshes (personajes animados) de forma mucho más precisa.

### Ventajas de Lumen:
* **Iteración instantánea**: Mueves una pared, abres una puerta o cambias la hora del día y la luz se adapta en milisegundos.
* Soporta escenas con destrucción, ciclos día/noche y niveles procedurales.
* Elimina el proceso de empaquetar UVs de lightmaps y tiempos de horneado de horas.

### Desventajas / Limitaciones:
* **Coste de GPU**: 3 ms - 8 ms por fotograma en consolas/PC.
* Dificultades con mallas muy delgadas (foliage/hojas sin grosor, planos de un solo lado) o interiores completamente cerrados con fugas de luz (*light leaking*).
* Ruido temporal (*temporal noise*) en transiciones muy bruscas de luz.

---

## 🍞 2. Baked Lighting (Lightmass / GPU Lightmass)

El método tradicional donde una herramienta externa (CPU Lightmass o GPU Lightmass) simula millones de fotones mediante *Path Tracing* antes del juego y guarda el resultado en mapas de textura (**Lightmaps**).

### Ventajas del Baking:
* **Rendimiento insuperable**: 0 ms de cálculo de GI en tiempo de ejecución.
* **Calidad fotográfica libre de ruido**: Los rebotes indirectos son físicamente perfectos.
* Ideal para realidad virtual (VR a 90/120 FPS), dispositivos móviles y hardware modesto.

### Desventajas del Baking:
* Cero interactividad: Si mueves un mueble, su sombra y su rebote permanecen en el suelo.
* **Tiempos de horneado**: Puede tomar horas compilar mapas grandes.
* Consumo alto de memoria de texturas (Lightmap VRAM).
* Requiere UVs secundarias limpias y sin solapamiento para cada asset 3D.

---

## ⚖️ Cuadro Comparativo

| Característica | Lumen (Tiempo Real) | GPU / CPU Lightmass (Baking) |
| :--- | :--- | :--- |
| **Tiempo de Setup** | Inmediato (Automático) | Lento (Requiere Lightmap UVs + Baking) |
| **Consumo de GPU (Frametime)** | Alto (~4-8 ms) | Prácticamente Cero |
| **Consumo de Memoria VRAM** | Medio (Surface Cache) | Alto si hay muchos mapas grandes |
| **Cambios Dinámicos (Día/Noche)** | Sí, nativo | No (Requiere múltiples escenarios / streams) |
| **Target Ideal** | PC Gamer, PS5, Xbox Series X/S | VR, Móvil, PC de oficina, 120 FPS eSports |

---

## 🛠️ Modos de Depuración de Lumen en UE5

Para inspeccionar cómo ve Lumen tu nivel, en el viewport ve a:
`View Mode (Lit) -> Lumen`:
- **Lumen Overview**: Muestra cómo el motor reconstruye la iluminación indirecta.
- **Surface Cache**: Si los objetos aparecen en **Rosa/Rojo**, significa que Lumen no puede generar una buena caché de superficie (común en mallas combinadas gigantes). *Solución: Modularizar los meshes*.
- **Mesh Distance Fields**: Muestra la representación volumétrica para el software raytracing.

---
**Notas relacionadas**:
- [[Movilidad de Luces (Static, Stationary, Movable)]]
- [[Atmósfera y Niebla Volumétrica en UE5]]
- [[Optimización de Iluminación y Profiling en UE5]]
