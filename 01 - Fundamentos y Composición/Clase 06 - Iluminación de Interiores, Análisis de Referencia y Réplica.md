---
tags:
  - clase06
  - interiores
  - tlou
  - the-last-of-us
  - referencia
  - replica
  - brejon
  - unreal-engine
date: 2026-09-15
---

# Clase 06: Iluminación de Interiores — Análisis de Referencia y Réplica en Unreal Engine 5

Iluminación 3D · Docente Daniel Rojas (UNIACC)

---

## Objetivos y Estructura de la Clase

1. **Bloque 1 (Análisis y Demostración en Pantalla)**: Estudio técnico de iluminación cinematográfica sobre el prólogo nocturno de *The Last of Us* (Naughty Dog) y reconstrucción en vivo en Unreal Engine 5 mediante el método de capas de Chris Brejon.
2. **Bloque 2 (Encargo y Taller Práctico)**: Elección individual de un entorno interior y una referencia visual (película o videojuego) para iniciar la réplica en sala bajo supervisión docente.

---

## 1. Caso de Estudio: Análisis de Iluminación en *The Last of Us*

En el prólogo de *The Last of Us*, la escena en el dormitorio y la sala de estar presenta una atmósfera nocturna de tensión y vulnerabilidad. El esquema lumínico utiliza una clave tonal baja (*Low-Key*) y una clara separación cromática.

Aplicando la taxonomía de **Chris Brejon (*CG Cinematography*)**, descomponemos la escena en tres familias de fuentes de luz:

```
                  ┌────────────────────────────────────────────────────────┐
                  │          DESGLOSE DE CAPAS DE ILUMINACIÓN              │
                  ├────────────────────────────────────────────────────────┤
                  │ 1. Natural Light  ──► Luna exterior fría (~7.500K)     │
                  │ 2. Practical Light ──► Pantalla de TV + Luz de pasillo │
                  │ 3. Dramatic Light ──► Rim light sutil de silueta       │
                  └────────────────────────────────────────────────────────┘
```

### Desglose Técnico de las Fuentes:

| Capa en Brejon | Elemento en Escena | Propiedades Físicas | Función Narrativa y Visual |
| :--- | :--- | :--- | :--- |
| **Natural Light** | Ventanal hacia el exterior | Azul frío (~7.500K – 8.000K). Intensidad moderada. | Establece la penumbra nocturna base, marca la hora dramática y proyecta sombras suaves en el suelo. |
| **Practical Light (A)** | Pantalla de TV en la sala | Luz de área (*Rect Light*) cian-blanca (~6.500K) con fluctuación leve de emisión. | Punto focal de alta intensidad que baña el mobiliario frontal y proyecta sombras duras en la oscuridad. |
| **Practical Light (B)** | Luz del pasillo / puerta entreabierta | Tungsteno cálido (~2.700K). Fuente puntual con radio controlado. | Genera un marcado **contraste térmico** (naranja vs. azul) que guía la mirada hacia la puerta. |
| **Dramatic Light** | Focos de estudio fuera de cuadro | Temperatura calibrada según la fuente motivadora (~6.500K o ~3.000K). Intensidad tenue. | Recorta la silueta del personaje (*Rim Light*) para despegarlo del fondo oscuro sin lavar los negros de la sala. |

---

## 2. Flujo de Trabajo para Replicar una Referencia en Unreal Engine 5

1. **Paso 1 (Calibración de Exposición)**:
   * Añadir un actor `PostProcessVolume` con `Infinite Extent (Unbound)`.
   * En `Exposure`, fijar el método en **Manual** y ajustar el valor `EV100` para interiores nocturnos (entre $4.0$ y $6.0$). Esto evita que el motor compense y aclare la escena artificialmente.
2. **Paso 2 (Luz Natural Exterior)**:
   * Ubicar una `Rect Light` en el marco de la ventana orientada hacia el interior.
   * Asignar temperatura de color fría (~7.500K) e intensidad moderada.
3. **Paso 3 (Luces Prácticas de Escenografía)**:
   * **Televisor**: Material con canal `Emissive` en la pantalla + `Rect Light` frontal apuntando a la habitación.
   * **Lámpara de Pasillo**: `Point Light` o `Spot Light` cálida (~2.700K) con `Source Radius = 3 cm` y `Attenuation Radius` ceñido a las paredes.
4. **Paso 4 (Luces Dramáticas de Apoyo)**:
   * Si el sujeto queda completamente empastado en negro, añadir una `Spot Light` tenue con cono amplio motivada por la luz del televisor o la luna para generar un ligero recorte de silueta (*Rim Light*).

---

## 3. Encargo Práctico: Elección de Referencia y Réplica

### Requisitos del Ejercicio:

1. **Selección del Espacio Interior**: Escenario cerrado o modular en Unreal Engine 5.
2. **Selección de Referencia Visual**: Una captura de alta resolución de un interior de un **videojuego** o una **película**.
3. **Ficha de Desglose Previa**:
   * Identificar: Luz Natural, Luces Prácticas visibles, Luces Dramáticas de apoyo, temperaturas de color y punto focal.
4. **Montaje en Sala**:
   * Comenzar la iluminación en clase, estructurando las luces por capas y aplicando la nomenclatura oficial de Epic Games en el Outliner.

### Nomenclatura Recomendada en el Outliner:
* `Lights_Natural/`: `L_Nat_Window_Rect`, `L_Nat_Sky_Ambient`
* `Lights_Practical/`: `L_Prac_TV_Rect`, `L_Prac_Hall_Point`, `L_Prac_DeskLamp_Spot`
* `Lights_Dramatic/`: `L_Dram_Char_Rim`, `L_Dram_Table_Bounce`

---
**Notas relacionadas**:
- [[Clase 05 - Iluminación de Interiores, Metodología Brejon y Nomenclatura]]
- [[Clase 01 - Fundamentos de la Luz y Esquema de 3 Puntos]]
- [[Clase 02 - Taller de Iluminación 3 Puntos, Sol y Cielo en Unreal Engine 5]]
- [[Clase 03 - Shaders PBR en el Busto, Sol y Fuentes Locales]]
- [[Glosario de Iluminación 3D]]
