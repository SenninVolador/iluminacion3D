---
tags:
  - unreal-engine
  - luces
  - movilidad
  - performance
date: 2026-08-18
---

# 🔄 Movilidad de Luces en Unreal Engine

En Unreal Engine, cada actor de luz tiene una propiedad fundamental llamada **Mobility** (Movilidad). Esta opción determina cómo se calculan las luces y las sombras, afectando drásticamente la calidad visual y el rendimiento en GPU.

```
       ┌─────────────────┬───────────────────┬──────────────────┐
       │     STATIC      │    STATIONARY     │     MOVABLE      │
───────┼─────────────────┼───────────────────┼──────────────────┤
Cálculo│ 100% Precalculado│ Híbrido (Dir. Dyn │ 100% Tiempo Real │
       │ (Lightmaps)     │ + Bounce Baked)   │ (Totalmente din.)│
───────┼─────────────────┼───────────────────┼──────────────────┤
Coste  │ Mínimo en GPU   │ Medio             │ Alto             │
GPU    │ (Solo textura)  │ (Shadow Maps dyn) │ (Coste continuo) │
───────┼─────────────────┼───────────────────┼──────────────────┤
Cambios│ Ninguno en juego│ Color/Intensidad  │ Todo (Posición,  │
en Run │                 │ (Posición fija)   │ Ángulo, Color...)│
───────┴─────────────────┴───────────────────┴──────────────────┘
```

---

## 1. 🪨 Static (Estática)

* **¿Cómo funciona?**: La luz y sus sombras se calculan previamente (Baking) con **Lightmass** y se guardan directamente en las texturas de los objetos (Lightmaps).
* **Ventajas**:
  * **Coste de render casi nulo en GPU durante el gameplay**: No calcula sombras dinámicas.
  * Rebotes de luz indirecta (GI) muy suaves y precisos.
* **Desventajas**:
  * No se puede mover ni cambiar color/intensidad durante la partida.
  * No proyecta sombras dinámicas sobre personajes u objetos móviles (requiere *Volumetric Lightmaps* / *Indirect Lighting Cache*).
  * Aumenta el uso de memoria RAM/VRAM por las texturas de lightmap.

---

## 2. ⚖️ Stationary (Estacionaria)

* **¿Cómo funciona?**: Enfoque híbrido:
  * **Luz Directa**: Se renderiza dinámicamente en tiempo real (proyecta sombras nítidas sobre personajes y objetos móviles).
  * **Luz Indirecta (GI)**: Se hornea en los Lightmaps.
* **Características Clave**:
  * Puedes cambiar su **color e intensidad** en tiempo de ejecución (Run-time).
  * **NO puedes mover su posición ni rotación**.
  * Utiliza un canal especial llamado **Distance Field Shadow Maps** para sombras precalculadas nítidas en objetos estáticos.
* **🚨 Regla de los 4 Canales (Overlap Limit)**:
  * En Unreal (Deferred Renderer clásico), solo pueden solaparse un máximo de **4 luces Stationary que proyecten sombras** en un mismo objeto/espacio (canales RGBA de la máscara de sombras).
  * Si solapas 5 o más, la luz excedente se convierte automáticamente en **Movable** (con un icono de cruz roja `❌` en el editor), disparando el coste de rendimiento.

---

## 3. 🏃 Movable (Dinámica / Móvil)

* **¿Cómo funciona?**: Se calcula completamente en tiempo real en cada fotograma.
* **Ventajas**:
  * Máxima interactividad: se puede mover, apagar, encender, cambiar parámetros vía Blueprints, proyectores dinámicos, linternas, ciclos día/noche.
  * Afecta y proyecta sombras dinámicas sobre todo tipo de objetos (estáticos y dinámicos).
  * En **Unreal Engine 5**, es el modo nativo ideal cuando se usa [[Lumen vs Baked Lighting (UE5)|Lumen]] y **Virtual Shadow Maps (VSM)**.
* **Desventajas**:
  * Mayor coste de procesamiento en GPU por fotograma.
  * Si no se usa Lumen o GI en tiempo real, carece de rebotes indirectos a menos que se configure SSGI o Ray Tracing.

---

## 🧭 ¿Cuándo usar cada tipo?

| Escenario | Movilidad Recomendada | Motivo |
| :--- | :--- | :--- |
| **Juegos móviles / VR / Gama baja (Forward Renderer)** | `Static` | Máximo rendimiento y bajo consumo térmico/GPU. |
| **Juegos de consola/PC con mapa horneado (Sin Lumen)** | `Stationary` | Balance perfecto entre sombras dinámicas para personajes y GI horneada de alta calidad. |
| **Proyectos modernos UE5 (Next-Gen PC / PS5 / Xbox Series)** | `Movable` + Lumen | Flujo de trabajo 100% dinámico, sin tiempos de espera de horneado (Baking). |
| **Linternas del jugador, vehículos, explosiones, luces que parpadean** | `Movable` | Requieren cambio continuo de posición/propiedades. |

---

> [!TIP]
> En Unreal Engine 5 con Lumen activado por defecto, la mayoría de luces se colocan como **Movable**. Sin embargo, comprender la diferencia es vital para optimizaciones y proyectos que deshabilitan Lumen por cuestiones de target de rendimiento (por ejemplo, 60/120 FPS competitivos o Steam Deck).

---
**Notas relacionadas**:
- [[Tipos de Luces en Unreal Engine]]
- [[Lumen vs Baked Lighting (UE5)]]
- [[Optimización de Iluminación y Profiling en UE5]]
