# Clase 05: Iluminación de Interiores, Metodología Chris Brejon y Nomenclatura

Iluminación 3D · Docente Daniel Rojas (UNIACC)

---

## Dinámica de la Sesión

La sesión se divide en dos fases:
1. **Fase Teórico-Práctica**: Introducción a la iluminación de espacios confinados mediante la taxonomía de **Chris Brejon (*CG Cinematography*)**, fuentes de luz locales en Unreal Engine 5 y estándares oficiales de nomenclatura de Epic Games.
2. **Fase de Evaluación**: Montaje de una escena interior simple y **calificación presencial al cierre de la clase de la Entrega N°1** según la [Rúbrica Oficial de 60 Puntos](/clases/rubrica-entrega-01).

---

## 1. Metodología Chris Brejon (*CG Cinematography*)

En los estudios de animación y videojuegos, la iluminación profesional no se realiza colocando luces al azar. En el libro fundamental *CG Cinematography* (Capítulo 4: *Light Categories*), Chris Brejon establece una distinción técnica crítica: **Categoría vs. Rol**.

```
Categoría (Lo que la luz ES)   ──►  Natural Light  /  Practical Light  /  Dramatic Light
Rol (La función según cámara)  ──►  Key Light  /  Fill Light  /  Rim Light  /  Bounce
```

### Las Tres Familias de Luces (Categorías)

| Categoría en Brejon | Definición y Ubicación | Función en la Escena |
| :--- | :--- | :--- |
| **Natural Lights** | Luces no manufacturadas del entorno exterior (Sol, cielo, luna, fuego). | Ingresan por aberturas (ventanas/tragaluces) y marcan la base ambiental y la hora del día. |
| **Practical Lights** | Fuentes visibles que forman parte de la escenografía (*set dressing*): lámparas de velador, tubos fluorescentes, velas, pantallas de TV. | Rompen la monotonía del fondo y **sirven como justificación o motivación visual**. |
| **Dramatic Lights** *(Studio Lights)* | Fuentes invisibles fuera de cuadro dedicadas a modelar sujetos y contar la historia. | Esculpen al personaje o prop principal con el color y dirección justificados por la luz práctica, sin quemarla. |

> **La Regla de Oro de Brejon**: *"Una luz práctica no tiene por qué iluminar por completo al personaje; su mera presencia en escena justifica ante el cerebro del espectador las luces de estudio (Dramatic Lights) que usamos para esculpirlo."*

---

## 2. Simulador Interactivo: Habitación Interior y Flujo por Capas

Experimenta con el flujo de trabajo por capas propuesto por Brejon. Prueba encender la luz de ventana fría, la lámpara práctica cálida y la luz dramática de modelado:

<ClientOnly>
  <InteriorLightingViewer />
</ClientOnly>

### El Flujo de Trabajo en 3 Pasos para Interiores:
1. **Capa 1 (Base Natural)**: Ajustar la luz que ingresa desde el exterior por las ventanas (fría, ~6.500K).
2. **Capa 2 (Practical Lights)**: Calibrar las lámparas del decorado con valores físicos moderados para no saturar los píxeles (cálida, ~2.800K).
3. **Capa 3 (Dramatic Lights)**: Añadir focos de apoyo invisibles (*Key/Fill*) motivados por las lámparas para modelar el punto focal con nitidez.

---

## 3. Fuentes Locales y Parámetros de Interior en Unreal Engine 5

| Tipo de Luz en UE5 | Emisión Geométrica | Caso de Uso en Interiores |
| :--- | :--- | :--- |
| **Rect Light (Luz de Área)** | Superficie rectangular plana | Vano de ventanas, paneles LED de oficina, tubos fluorescentes, pantallas. Proyecta sombras suaves físicamente correctas. |
| **Point Light (Puntual)** | Esfera omnidireccional (360°) | Ampolletas desnudas, velas, fogatas. |
| **Spot Light (Focal)** | Cono direccional (*Inner* y *Outer cone*) | Focos empotrados de techo, lámparas de mesa con pantalla, linternas. |

### Parámetros Físicos Indispensables:
* **Attenuation Radius (Radio de Atenuación)**: Limita la distancia máxima donde la luz tiene efecto.  
  * *Criterio técnico*: Ajustar el radio estrictamente al espacio de la habitación. Si el radio atraviesa muros, la GPU calculará luz innecesaria en habitaciones contiguas (*Shader Overdraw*) y provocará fugas de luz (*Light Leaking*).
* **Source Radius y Source Length**: Permite que el emisor tenga dimensiones físicas reales (un radio esférico o el largo de un tubo fluorescente).  
  * *Efecto PBR*: Transforma el reflejo especular de un punto microscópico irreal en un reflejo ancho y suave propio de una bombilla real.

---

## 4. Nomenclatura Oficial de Assets en Unreal Engine

En proyectos profesionales de videojuegos, el orden de los archivos es evaluado con rigor. Siguiendo las directrices oficiales de Epic Games ([Recommended Asset Naming Conventions](https://dev.epicgames.com/documentation/en-us/unreal-engine/recommended-asset-naming-conventions-in-unreal-engine-projects)), la estructura estándar es:

$$\text{[PrefijoTipoAsset]\_} \text{[NombreDelAsset]\_} \text{[Descriptor/Sufijo]}$$

### Tabla de Prefijos y Sufijos Recomendados

| Tipo de Elemento | Prefijo / Formato | Ejemplo Oficial |
| :--- | :--- | :--- |
| **Master Material** | `M_` | `M_Wood_Floor`, `M_Master_PBR` |
| **Material Instance** | `MI_` | `MI_DeskLamp_Brass`, `MI_Bust_Marble` |
| **Material Function** | `MF_` | `MF_RoughnessRemap` |
| **Textura: Base Color** | `T_` ... `_BC` (o `_D`) | `T_Chair_Wood_BC` |
| **Textura: Normal Map** | `T_` ... `_N` | `T_Chair_Wood_N` |
| **Textura: Empaquetada ORM** | `T_` ... `_ORM` | `T_Chair_Wood_ORM` |
| **Textura: Rugosidad / Metal** | `T_` ... `_R` / `_M` | `T_Metal_Vault_R`, `T_Metal_Vault_M` |
| **Textura: Emissive** | `T_` ... `_E` | `T_NeonSign_E` |
| **Static Mesh (Malla 3D)** | `SM_` | `SM_Desk_Office`, `SM_Window_Frame` |
| **Blueprint** | `BP_` | `BP_DeskLamp_Interactive` |
| **Nivel / Mapa** | `L_` (o `LVL_`) | `L_Interior_Office_Study` |

### Nomenclatura del Rig de Iluminación en el Outliner
Para mantener el Outliner limpio y legible en escenas complejas, organiza las luces en carpetas según la metodología de Brejon:
* `Lights_Natural/`: `L_Nat_Sun_Directional`, `L_Nat_Sky_Ambient`, `L_Nat_Window_Portal`
* `Lights_Practical/`: `L_Prac_DeskLamp_Point`, `L_Prac_Ceiling_Spot`
* `Lights_Dramatic/`: `L_Dram_Key_Character`, `L_Dram_Fill_Desk`

---

## 5. Ejercicio Práctico de la Clase

1. **Construcción de Habitación Simple**: Crear una sala básica cerrada con un vano de ventana y un prop central sobre una mesa.
2. **Aplicación de Capas**:
   * Configurar una `Rect Light` o `Directional Light` fría en la ventana (Capa Natural).
   * Colocar una lámpara de utilería con una `Point Light` o `Spot Light` cálida y `Source Radius` ajustado (Capa Practical).
   * Añadir una luz de estudio suave para resaltar el prop sin quemar la lámpara (Capa Dramatic).
3. **Cierre de Sesión**: Revisión y calificación individual de la **Entrega N°1** según rúbrica.
