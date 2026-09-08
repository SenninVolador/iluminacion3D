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

## Estructura de la Sesión

1. **Bloque 1 (Teórico-Práctico)**: Metodología de Chris Brejon (*CG Cinematography*), fuentes locales de interior en Unreal Engine 5 y estándares oficiales de nomenclatura de Epic Games.
2. **Bloque 2 (Taller en Sala)**: Montaje e iluminación de una escena interior simple con ventana y lámpara de mesa.
3. **Bloque 3 (Evaluación)**: Calificación presencial individual de la **Entrega N°1** según la [[Rubrica_Entrega_01_3Point_y_Shaders]].

---

## 1. Metodología Chris Brejon (*CG Cinematography*)

En el libro de referencia *CG Cinematography* (Capítulo 4: *Light Categories*), Chris Brejon define la regla fundamental para todo artista técnico de iluminación: **Categoría vs. Rol**.

```
Categoría (Lo que la luz ES en el mundo)  ──►  Natural / Practical / Dramatic
Rol (La función que cumple para la cámara) ──►  Key / Fill / Rim / Kicker / Bounce
```

### Las Tres Familias de Luces (Categorías)

1. **Natural Lights (Luces Naturales)**:
   * Fuentes no manufacturadas del entorno exterior: Sol, cielo, luna, relámpagos.
   * En interiores entran por vanos de ventanas o tragaluces y marcan la orientación general y la hora del día.
2. **Practical Lights (Luces Prácticas)**:
   * Fuentes de luz visibles integradas en la utilería o escenografía (*set dressing*): lámparas de velador, bombillas desnudas, tubos fluorescentes, pantallas o velas.
   * Su función principal es romper la monotonía del fondo y **servir de motivación/justificación visual ante el espectador**.
3. **Dramatic Lights (Luces Dramáticas / Studio Lights)**:
   * Luces invisibles fuera de cuadro diseñadas con fines puramente narrativos para modelar el sujeto principal.
   * Toman la dirección y el color sugeridos por las luces prácticas pero con intensidades calibradas para esculpir el volumen sin quemar la bombilla visible.

> *"A practical light does not have to actually illuminate the character, but its mere presence unconsciously and illogically justifies other light sources that might be used to light the character, like a rim or key light."* — Chris Brejon

---

## 2. Flujo de Iluminación de Interiores en 3 Capas

Al abordar una habitación cerrada, Brejon establece un orden de trabajo secuencial:

1. **Capa 1: Luz Natural Exterior**: Configurar la luz del sol y el cielo que atraviesa el vano de la ventana. Usualmente tonos fríos (6.500K).
2. **Capa 2: Luces Prácticas de Set**: Ubicar las lámparas visibles en escritorios o techos con intensidades físicamente creíbles (~2.800K cálidas).
3. **Capa 3: Luces Dramáticas**: Introducir focos de apoyo suaves motivados por las lámparas para separar al personaje o prop del fondo.

---

## 3. Fuentes Locales y Parámetros en Unreal Engine 5

* **Rect Light (Luz de Área)**: Superficie emisora rectangular. Indispensable para ventanas, paneles LED de techo y pantallas de computadores.
* **Point Light**: Emisión omnidireccional en 360°. Para bombillas desnudas o faroles.
* **Spot Light**: Emisión en cono dirigido con ángulo interno (*Inner Cone*) y externo (*Outer Cone*).
* **Attenuation Radius**: Radio de corte de la luz. **Regla estricta**: Ajustar para que no traspase los muros del cuarto contiguo, evitando *Shader Overdraw* y fugas lumínicas.
* **Source Radius / Source Length**: Dimensión física del emisor para obtener reflejos especulares verosímiles en materiales PBR en lugar de puntos matemáticos rígidos.

---

## 4. Nomenclatura Recomendada de Assets (Epic Games)

Siguiendo el estándar oficial de Epic Games ([Recommended Asset Naming Conventions](https://dev.epicgames.com/documentation/en-us/unreal-engine/recommended-asset-naming-conventions-in-unreal-engine-projects)):

$$\text{[PrefijoTipoAsset]\_} \text{[NombreDelAsset]\_} \text{[Descriptor/Sufijo]}$$

### Tabla de Convenciones
* **Materiales**:
  * `M_` Master Material (ej. `M_Master_PBR`, `M_Wood_Floor`)
  * `MI_` Material Instance (ej. `MI_DeskLamp`, `MI_Bust_Marble`)
  * `MF_` Material Function (ej. `MF_RoughnessRange`)
* **Texturas**:
  * `T_` Textura base con descriptor final:
    * `_BC` / `_D`: Base Color / Diffuse (`T_Wood_Floor_BC`)
    * `_N`: Normal Map (`T_Wood_Floor_N`)
    * `_ORM`: Oclusión, Rugosidad y Metal empaquetados (`T_Wood_Floor_ORM`)
    * `_R`: Roughness individual (`T_Metal_R`)
    * `_M`: Metallic individual (`T_Metal_M`)
    * `_E`: Emissive (`T_LampBulb_E`)
* **Mallas y Geometría**:
  * `SM_` Static Mesh (`SM_Desk`, `SM_Window_Frame`)
  * `SK_` Skeletal Mesh (`SK_Character`)
* **Nivel / Mapa**:
  * `L_` / `LVL_` Nivel (`L_Interior_Study`)
* **Rig de Iluminación en el Outliner**:
  * `L_Nat_Sun`, `L_Nat_Sky`
  * `L_Prac_DeskLamp`, `L_Prac_CeilingSpot`
  * `L_Dram_Key_Hero`, `L_Dram_Fill_Desk`

---

## 5. Trabajo en Clase

* Montaje de una habitación interior simple con ventana y lámpara de mesa aplicando la taxonomía de Brejon.
* Evaluación presencial de la Entrega N°1 con rúbrica oficial.

---
**Notas relacionadas**:
- [[Rubrica_Entrega_01_3Point_y_Shaders]]
- [[Clase 03 - Shaders PBR, Master Materials y Luces Locales]]
- [[Clase 04 - Taller de Entrega 01, Sistemas Nodales y Atmósfera Volumétrica]]
- [[Tipos de Luces en Unreal Engine]]
