# Clase 05: Iluminación de Interiores, Metodología Chris Brejon y Nomenclatura

Iluminación 3D · Docente Daniel Rojas (UNIACC)

---

## Objetivos y Estructura de la Clase

En esta sesión abordaremos la iluminación de espacios interiores. Trabajaremos con la metodología de **Chris Brejon** (*CG Cinematography*), uno de los marcos de referencia más utilizados en estudios de animación y videojuegos para diseñar esquemas de luz con sentido físico y narrativo. Además, revisaremos la configuración de fuentes locales en Unreal Engine 5 y las convenciones oficiales de nomenclatura de Epic Games para mantener un proyecto profesional y ordenado.

Al cierre de la sesión realizaremos la revisión y calificación presencial de la **Entrega N°1** según la [Rúbrica Oficial de 60 Puntos](/clases/rubrica-entrega-01).

---

## 1. Metodología de Chris Brejon (*CG Cinematography*)

Al iluminar un espacio interior en Unreal Engine, un error común es colocar luces de manera arbitraria solo para aclarar la escena. En cinematografía y videojuegos profesionales, cada fuente de luz responde a una función específica y justificada.

En su libro *CG Cinematography* (Capítulo 4: *Light Categories*), Chris Brejon establece una distinción metodológica fundamental: **Categoría vs. Rol**.

```
Categoría (Lo que la luz ES físicamente) ──►  Natural Light  /  Practical Light  /  Dramatic Light
Rol (La función que cumple para la toma)  ──►  Key Light  /  Fill Light  /  Rim Light  /  Bounce
```

### Las Tres Familias de Luces (Categorías)

| Categoría en Brejon | Definición y Ubicación | Función en la Escena |
| :--- | :--- | :--- |
| **Natural Lights** | Fuentes del entorno exterior: sol, cielo, luna o relámpagos. | Ingresan por ventanas y tragaluces. Definen la hora del día, el clima exterior y entregan la iluminación ambiental base del espacio. |
| **Practical Lights** | Luces visibles integradas en la escenografía (*set dressing*): lámparas de mesa, ampolletas, tubos fluorescentes, velas o pantallas. | Rompen la oscuridad del fondo y **le entregan al espectador la justificación visual** de la luz en ese sector. |
| **Dramatic Lights** *(Studio Lights)* | Fuentes invisibles fuera de cuadro dedicadas a modelar al personaje o prop principal. | Adoptan la dirección y temperatura de color sugeridas por la luz práctica, pero con una intensidad calibrada para esculpir volúmenes sin sobreexponer la fuente visible. |

> [!TIP] La Regla de Oro de Brejon
> Una luz práctica no tiene por qué iluminar por completo al personaje. Su presencia en la escena justifica ante el espectador las luces de estudio invisibles (Dramatic Lights) que utilizamos para modelar el volumen y la silueta.

---

## 2. Simulador Interactivo: Habitación Interior y Flujo en 3 Capas

Prueba el simulador interactivo. Puedes rotar la cámara arrastrando con el ratón o deslizando en pantalla táctil, y alternar los presets para comparar el resultado de la escena con y sin luz dramática:

<ClientOnly>
  <InteriorLightingViewer />
</ClientOnly>

### El Flujo de Trabajo en 3 Capas:
1. **Capa 1 (Base Natural Fría)**: Configuramos la luz que ingresa desde el exterior por la ventana (~6.500K). Baña el suelo y los muros en tonos fríos.
2. **Capa 2 (Lámpara Práctica Cálida)**: Ubicamos la lámpara de mesa con valores físicos moderados (~2.700K), generando un área de luz cálida concentrada en el escritorio.
3. **Capa 3 (Luz Dramática de Modelado)**: Añadimos una luz de estudio invisible orientada desde la posición de la lámpara hacia el sujeto principal para definir sus rasgos y volumen.

---

## 3. Fuentes Locales en Unreal Engine 5

Para iluminar interiores en Unreal Engine utilizamos tres tipos de luces locales:

| Tipo de Luz en UE5 | Forma de emisión | Aplicación en Interiores |
| :--- | :--- | :--- |
| **Rect Light (Luz de Área)** | Rectángulo plano | Ventanas, tubos fluorescentes de techo y pantallas de televisor o computador. Entrega sombras suaves de alta fidelidad física. |
| **Point Light (Puntual)** | Esfera omnidireccional (360°) | Ampolletas desnudas, velas o fuego. Requiere controlar cuidadosamente su radio para evitar dispersión indeseada. |
| **Spot Light (Focal)** | Cono direccional (*Inner* y *Outer cone*) | Focos empotrados de techo, lámparas de escritorio dirigidas y linternas. |

### Parámetros Críticos de Iluminación:

* **Attenuation Radius (Radio de Atenuación)**: Delimita la distancia máxima de alcance de la luz.
  * *Criterio de optimización*: Eviten dejar radios excesivamente amplios por omisión. Si el radio atraviesa muros, el motor calculará iluminación innecesaria en habitaciones contiguas, consumiendo recursos de la tarjeta de video y provocando fugas de luz (*light leaking*).
* **Source Radius (Radio de la Fuente)**: Otorga dimensiones físicas reales al emisor.
  * *Efecto PBR*: Cuando el radio es cero, el reflejo especular sobre materiales brillantes se reduce a un punto microscópico irreal. Al asignarle un radio de 2 a 5 cm, el reflejo adopta la forma circular y suave correspondiente a una ampolleta real.

---

## 4. Nomenclatura Oficial de Assets en Unreal Engine

En proyectos profesionales de desarrollo de videojuegos, la consistencia y el orden de los archivos en el Content Browser son indispensables para el trabajo en equipo.

Siguiendo el estándar oficial de Epic Games ([Recommended Asset Naming Conventions](https://dev.epicgames.com/documentation/en-us/unreal-engine/recommended-asset-naming-conventions-in-unreal-engine-projects)), la estructura base es:

$$\text{[Prefijo]\_} \text{[NombreDelAsset]\_} \text{[Sufijo/Descriptor]}$$

### Tabla de Prefijos y Sufijos Oficiales

| Tipo de Asset | Prefijo / Formato | Ejemplo Oficial |
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

### Organización de Luces en el Outliner:
Para mantener el Outliner estructurado y legible en escenas complejas, agrupen las luces en carpetas según las categorías de Brejon:
* `Lights_Natural/`: `L_Nat_Window_Rect`, `L_Nat_Sky_Ambient`
* `Lights_Practical/`: `L_Prac_DeskLamp_Point`, `L_Prac_Ceiling_Spot`
* `Lights_Dramatic/`: `L_Dram_Bust_Key`, `L_Dram_Desk_Fill`

---

## 5. Ejemplo Práctico: Iluminación de un Rincón de Estudio Nocturno

Desarrollaremos este ejercicio paso a paso durante la sesión práctica:

1. **Construcción del espacio base**:
   * Ensamblar una habitación cerrada simple utilizando muros (`SM_Room_Wall`), suelo de madera (`SM_Room_Floor`) y un marco de ventana (`SM_Window_Frame`).
   * Disponer un escritorio central (`SM_Desk_Wood`) y colocar encima un busto escultórico (`SM_Bust_Marble`).
2. **Paso 1 - Luz Natural Exterior**:
   * En el vano de la ventana, posicionar una `Rect Light` (`L_Nat_Window_Rect`) orientada hacia el interior.
   * Color: Frío exterior (~6.500K). Intensidad moderada para simular el resplandor nocturno bañando el suelo.
3. **Paso 2 - Lámpara Práctica de Mesa**:
   * Ubicar el modelo de la lámpara de escritorio (`SM_DeskLamp`).
   * Bajo la pantalla, incorporar una `Point Light` (`L_Prac_DeskLamp_Point`) cálida (~2.700K).
   * Ajustar `Source Radius = 3 cm` para conferir volumen físico al emisor y delimitar el `Attenuation Radius = 120 cm` al área del escritorio.
4. **Paso 3 - Luz Dramática de Modelado**:
   * Al observar el busto, la lámpara solo iluminará la base, dejando el rostro en sombras.
   * Añadir una `Spot Light` o `Rect Light` invisible (`L_Dram_Bust_Key`), orientada hacia los rasgos faciales con la misma tonalidad cálida de la lámpara (~3.000K).
   * Esto permite recortar y definir mejilla y nariz sin sobreexponer la superficie de la mesa.
5. **Cierre y Evaluación de la Entrega N°1**:
   * En el bloque final de la clase se evaluarán de manera presencial e individual los proyectos de la primera entrega según la pauta de evaluación.
