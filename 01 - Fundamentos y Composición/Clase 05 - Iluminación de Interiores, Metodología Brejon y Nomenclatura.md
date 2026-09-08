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

## ¿Qué vamos a ver hoy?

1. **Bloque 1 (Teórico-Práctico)**: Cómo iluminar interiores con la metodología de **Chris Brejon** (*CG Cinematography*), tipos de luces locales en Unreal Engine 5 y cómo nombrar los assets según la guía oficial de Epic Games para mantener el proyecto limpio.
2. **Bloque 2 (Taller en Sala)**: Montaje paso a paso de una habitación cerrada con ventana fría, lámpara de velador cálida y luz de estudio de modelado.
3. **Bloque 3 (Evaluación)**: Calificación presencial individual de la **Entrega N°1** según la [[Rubrica_Entrega_01_3Point_y_Shaders]].

---

## 1. El Método de Chris Brejon (*CG Cinematography*)

Cuando nos toca iluminar un espacio cerrado en Unreal Engine, el error típico de principiante es empezar a tirar luces a tontas y a locas para que "se vea iluminado". En la industria se trabaja de manera opuesta: cada luz debe tener una justificación física o narrativa.

En su libro *CG Cinematography* (Capítulo 4: *Light Categories*), Chris Brejon plantea una distinción que aclara todo el panorama: **Categoría vs. Rol**.

```
Categoría (Lo que la luz ES en el mundo)  ──►  Natural / Practical / Dramatic
Rol (La función que cumple para la cámara) ──►  Key / Fill / Rim / Kicker / Bounce
```

### Las Tres Familias de Luces (Categorías)

1. **Natural Lights (Luces Naturales)**:
   * Fuentes del entorno exterior que no fabrica el ser humano: sol, cielo, luna o relámpagos.
   * En interiores entran por vanos de ventanas o tragaluces. Definen la hora del día, el clima y entregan la iluminación base ambiental de la habitación.
2. **Practical Lights (Luces Prácticas)**:
   * Fuentes de luz visibles integradas en la utilería o escenografía (*set dressing*): lámparas de velador, ampolletas colgando, tubos fluorescentes, velas o pantallas de TV.
   * Su función principal es romper la monotonía del fondo y **darle al jugador la excusa o justificación visual** de por qué hay luz en esa zona.
3. **Dramatic Lights (Luces Dramáticas / Studio Lights)**:
   * Luces invisibles fuera de cuadro que ponemos nosotros para modelar al personaje o prop principal.
   * Toman prestado el color y la dirección que insinúan las luces prácticas, pero con la potencia calibrada para esculpir volúmenes sin reventar la ampolleta en blanco puro.

> *"Una luz práctica no tiene por qué iluminar por completo al personaje. Su sola presencia en escena justifica ante el cerebro del espectador las luces de estudio invisibles que usamos para esculpirlo."* — Chris Brejon

---

## 2. El Flujo de Trabajo en 3 Capas para Interiores

Al abordar una habitación cerrada, trabajamos en este orden secuencial:

1. **Capa 1: Base Natural Exterior**: Ajustamos la luz que entra por la ventana desde afuera (~6.500K fría). Baña el suelo y las paredes en penumbra azulada.
2. **Capa 2: Lámparas Prácticas de Set**: Ubicamos las lámparas visibles en escritorios o veladores con intensidades físicas moderadas (~2.700K cálidas). Generan un charco acogedor en la mesa.
3. **Capa 3: Luces Dramáticas de Apoyo**: Introducimos focos suaves invisibles orientados desde la lámpara hacia el sujeto principal para recortar sus rasgos y darle tridimensionalidad.

---

## 3. Fuentes Locales y Parámetros en Unreal Engine 5

| Tipo de Luz en UE5 | Forma de Emisión | ¿Cuándo conviene usarla en interiores? |
| :--- | :--- | :--- |
| **Rect Light** | Plano rectangular | Ventanas, tubos fluorescentes de techo y pantallas. Proyecta sombras suaves muy realistas. |
| **Point Light** | Esfera en 360° | Ampolletas desnudas, velas o fogatas. |
| **Spot Light** | Cono direccional | Focos empotrados de techo, lámparas de escritorio dirigidas y linternas. |

### Dos Parámetros Críticos de Optimización:

* **Attenuation Radius (Radio de Atenuación)**: Define hasta dónde viaja la luz.
  * *Ojo con esto*: Nunca dejen el radio gigante por descuido. Si el radio atraviesa muros, la tarjeta de video calculará luz innecesaria en piezas contiguas, consumiendo recursos y provocando fugas de luz (*light leaking*).
* **Source Radius (Radio de la Fuente)**: Otorga dimensiones físicas reales al emisor.
  * *Efecto PBR*: En vez de un punto blanco microscópico irreal en los reflejos, verán el reflejo ancho, circular y suave de una bombilla real.

---

## 4. Nomenclatura Oficial de Assets en Unreal Engine

Para trabajar con orden profesional y que cualquier persona del equipo entienda su proyecto, seguimos el estándar oficial de Epic Games ([Recommended Asset Naming Conventions](https://dev.epicgames.com/documentation/en-us/unreal-engine/recommended-asset-naming-conventions-in-unreal-engine-projects)):

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

1. **Montar la Habitación**: Crear una caja simple cerrada con un vano de ventana (`SM_Window_Frame`), un escritorio (`SM_Desk_Wood`) y un busto escultórico sobre la mesa (`SM_Bust_Marble`).
2. **Paso 1 (Luz de Ventana)**: `Rect Light` fría (~6.500K) en el vano para simular la noche exterior entrando al cuarto.
3. **Paso 2 (Lámpara de Mesa)**: `Point Light` cálida (~2.700K) bajo la pantalla con `Source Radius = 3 cm` y `Attenuation Radius = 120 cm`.
4. **Paso 3 (Luz de Estudio de Modelado)**: `Spot Light` invisible apuntando a la cara del busto con el mismo tono cálido de la lámpara (~3.000K) para modelar la mejilla y nariz.
5. **Cierre de Clase**: Revisión y calificación presencial individual de la **Entrega N°1** según pauta oficial.

---
**Notas relacionadas**:
- [[Clase 01 - Fundamentos de la Luz y Esquema de 3 Puntos]]
- [[Clase 02 - Taller de Iluminación 3 Puntos, Sol y Cielo en Unreal Engine 5]]
- [[Clase 03 - Shaders PBR en el Busto, Sol y Fuentes Locales]]
- [[Clase 04 - Taller de Entrega 01, Shaders Nodales y Atmósfera Volumétrica]]
- [[Rubrica_Entrega_01_3Point_y_Shaders]]
- [[Glosario de Iluminación 3D]]
