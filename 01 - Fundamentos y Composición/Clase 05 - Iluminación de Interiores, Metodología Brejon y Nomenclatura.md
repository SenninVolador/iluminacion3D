---
tags:
  - clase05
  - interiores
  - brejon
  - cg-cinematography
  - nomenclatura
  - epic-games
  - unreal-engine
date: 2026-09-08
---

# Clase 05: Iluminación de Interiores, Metodología Chris Brejon y Nomenclatura

Iluminación 3D · Docente Daniel Rojas (UNIACC)

---

## Objetivos y Estructura de la Clase

1. **Bloque 1 (Teórico-Práctico)**: Metodología de **Chris Brejon** (*CG Cinematography*), fuentes locales de interior en Unreal Engine 5 y estándares oficiales de nomenclatura de Epic Games para mantener el Content Browser organizado.
2. **Bloque 2 (Taller en Sala)**: Montaje e iluminación paso a paso de una habitación cerrada con ventana exterior fría, lámpara práctica cálida y luz de estudio para modelar el sujeto.
3. **Bloque 3 (Evaluación)**: Calificación presencial individual de la **Entrega N°1** según la [[Rubrica_Entrega_01_3Point_y_Shaders]].

---

## 1. Metodología de Chris Brejon (*CG Cinematography*)

Al abordar la iluminación de un espacio cerrado en Unreal Engine, un error frecuente es colocar luces de manera arbitraria solo para aclarar la escena. En cinematografía y videojuegos profesionales, cada fuente de luz responde a una función específica y justificada.

En su libro de referencia *CG Cinematography* (Capítulo 4: *Light Categories*), Chris Brejon establece una distinción fundamental: **Categoría vs. Rol**.

```
Categoría (Lo que la luz ES físicamente)  ──►  Natural / Practical / Dramatic
Rol (La función que cumple para la toma)  ──►  Key / Fill / Rim / Kicker / Bounce
```

### Las Tres Familias de Luces (Categorías)

1. **Natural Lights (Luces Naturales)**:
   * Fuentes del entorno exterior: sol, cielo, luna o relámpagos.
   * En interiores ingresan por ventanas o tragaluces. Definen la hora del día, el clima exterior y entregan la iluminación ambiental base del espacio.
2. **Practical Lights (Luces Prácticas)**:
   * Fuentes visibles integradas en la escenografía (*set dressing*): lámparas de mesa, ampolletas, tubos fluorescentes, velas o pantallas.
   * Su función principal es romper la oscuridad del fondo y **entregarle al espectador la justificación visual** de por qué hay luz en ese sector.
3. **Dramatic Lights (Luces Dramáticas / Studio Lights)**:
   * Fuentes invisibles fuera de cuadro dedicadas a modelar al personaje o prop principal.
   * Adoptan la dirección y temperatura de color sugeridas por la luz práctica, pero con una intensidad calibrada para esculpir volúmenes sin sobreexponer la fuente visible.

> *"Una luz práctica no tiene por qué iluminar por completo al personaje. Su sola presencia en escena justifica ante el espectador las luces de estudio invisibles que utilizamos para modelar el volumen y la silueta."* — Chris Brejon

---

## 2. El Flujo de Trabajo en 3 Capas para Interiores

Al trabajar en un espacio interior, Brejon propone una secuencia lógica de capas:

1. **Capa 1: Base Natural Exterior**: Configuramos la luz que ingresa desde el exterior por la ventana (~6.500K fría). Baña el suelo y los muros en penumbra azulada.
2. **Capa 2: Lámparas Prácticas de Set**: Ubicamos las lámparas de mesa o velador con valores físicos moderados (~2.700K cálidas), creando un área de luz cálida concentrada.
3. **Capa 3: Luces Dramáticas de Apoyo**: Añadimos focos de estudio invisibles orientados desde la posición de la lámpara hacia el sujeto principal para definir sus rasgos y volumen tridimensional.

---

## 3. Fuentes Locales y Parámetros en Unreal Engine 5

| Tipo de Luz en UE5 | Forma de Emisión | Aplicación en Interiores |
| :--- | :--- | :--- |
| **Rect Light (Área)** | Plano rectangular | Ventanas, tubos fluorescentes y pantallas. Proyecta sombras suaves físicamente correctas. |
| **Point Light (Puntual)** | Esfera omnidireccional (360°) | Ampolletas desnudas, velas o fuego. |
| **Spot Light (Focal)** | Cono direccional | Focos empotrados de techo, lámparas de escritorio dirigidas y linternas. |

### Parámetros Críticos de Optimización:

* **Attenuation Radius (Radio de Atenuación)**: Delimita la distancia máxima donde la luz tiene efecto.
  * *Criterio de optimización*: Eviten dejar radios excesivamente amplios por omisión. Si el radio atraviesa muros, la tarjeta de video calculará iluminación innecesaria en habitaciones contiguas, consumiendo recursos y provocando fugas de luz (*light leaking*).
* **Source Radius (Radio de la Fuente)**: Confiere dimensiones físicas reales al emisor.
  * *Efecto PBR*: En vez de un punto blanco microscópico irreal en los reflejos especulares, genera un reflejo circular y suave representativo de una bombilla real.

---

## 4. Nomenclatura Oficial de Assets en Unreal Engine

Para mantener la consistencia y el orden profesional en proyectos compartidos, seguimos el estándar oficial de Epic Games ([Recommended Asset Naming Conventions](https://dev.epicgames.com/documentation/en-us/unreal-engine/recommended-asset-naming-conventions-in-unreal-engine-projects)):

$$\text{[Prefijo]\_} \text{[NombreDelAsset]\_} \text{[Descriptor/Sufijo]}$$

### Tabla de Prefijos Recomendados

| Tipo de Elemento | Prefijo / Formato | Ejemplo Oficial |
| :--- | :--- | :--- |
| **Master Material** | `M_` | `M_Wood_Floor`, `M_Master_PBR` |
| **Material Instance** | `MI_` | `MI_DeskLamp_Brass`, `MI_Bust_Marble` |
| **Material Function** | `MF_` | `MF_RoughnessRemap` |
| **Textura: Base Color** | `T_` ... `_BC` (o `_D`) | `T_Chair_Wood_BC` |
| **Textura: Normal Map** | `T_` ... `_N` | `T_Chair_Wood_N` |
| **Textura: Empaquetada ORM** | `T_` ... `_ORM` | `T_Chair_Wood_ORM` |
| **Static Mesh (Malla 3D)** | `SM_` | `SM_Desk_Office`, `SM_Window_Frame` |
| **Blueprint** | `BP_` | `BP_DeskLamp_Interactive` |
| **Nivel / Mapa** | `L_` (o `LVL_`) | `L_Interior_Office_Study` |

### Organización en el Outliner por Categorías de Brejon:
* `Lights_Natural/`: `L_Nat_Window_Rect`, `L_Nat_Sky_Ambient`
* `Lights_Practical/`: `L_Prac_DeskLamp_Point`, `L_Prac_Ceiling_Spot`
* `Lights_Dramatic/`: `L_Dram_Bust_Key`, `L_Dram_Desk_Fill`

---

## 5. Ejercicio Práctico: Rincón de Estudio Nocturno

1. **Construcción del espacio base**: Crear una habitación cerrada simple utilizando muros (`SM_Room_Wall`), suelo de madera (`SM_Room_Floor`) y un marco de ventana (`SM_Window_Frame`), disponiendo un escritorio (`SM_Desk_Wood`) con un busto escultórico encima (`SM_Bust_Marble`).
2. **Paso 1 (Luz Natural Exterior)**: `Rect Light` fría (~6.500K) en el vano de la ventana para simular el resplandor nocturno exterior bañando el suelo.
3. **Paso 2 (Lámpara Práctica)**: `Point Light` cálida (~2.700K) bajo la pantalla de la lámpara (`SM_DeskLamp`) con `Source Radius = 3 cm` y `Attenuation Radius = 120 cm`.
4. **Paso 3 (Luz Dramática de Modelado)**: `Spot Light` invisible orientada hacia el rostro del busto con tonalidad cálida (~3.000K) para modelar mejilla y nariz sin sobreexponer la mesa.
5. **Cierre de Clase**: Revisión y calificación presencial individual de la **Entrega N°1** según la pauta oficial.

---
**Notas relacionadas**:
- [[Clase 01 - Fundamentos de la Luz y Esquema de 3 Puntos]]
- [[Clase 02 - Taller de Iluminación 3 Puntos, Sol y Cielo en Unreal Engine 5]]
- [[Clase 03 - Shaders PBR en el Busto, Sol y Fuentes Locales]]
- [[Clase 04 - Taller de Entrega 01, Shaders Nodales y Atmósfera Volumétrica]]
- [[Rubrica_Entrega_01_3Point_y_Shaders]]
- [[Glosario de Iluminación 3D]]
