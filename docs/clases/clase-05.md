# Clase 05: Iluminación de Interiores, Metodología Chris Brejon y Nomenclatura

Iluminación 3D · Docente Daniel Rojas (UNIACC)

---

## ¿Qué vamos a ver hoy?

En esta clase nos metemos de lleno a iluminar espacios interiores. Vamos a trabajar con la metodología de **Chris Brejon** (*CG Cinematography*), que es el estándar que usan los estudios de animación y videojuegos para no poner luces al azar. También veremos cómo configurar las luces locales en Unreal Engine 5 y cómo nombrar cada asset según la guía oficial de Epic Games para que el proyecto se mantenga impecable y ordenado.

Al final de la clase nos tomamos los últimos minutos para revisar y calificar en vivo la **Entrega N°1** según la [Rúbrica Oficial de 60 Puntos](/clases/rubrica-entrega-01).

---

## 1. El Método de Chris Brejon (*CG Cinematography*)

Cuando iluminamos un interior en Unreal Engine, el error típico de principiante es empezar a tirar luces para que "se vea iluminado". En el cine y en los videojuegos profesionales se hace al revés: cada luz tiene una razón de ser.

En su libro *CG Cinematography* (Capítulo 4: *Light Categories*), Chris Brejon deja clara una diferencia que les va a salvar la vida: **Categoría vs. Rol**.

```
Categoría (Lo que la luz ES físicamente) ──►  Natural Light  /  Practical Light  /  Dramatic Light
Rol (La función que cumple para la toma)  ──►  Key Light  /  Fill Light  /  Rim Light  /  Bounce
```

### Las Tres Familias de Luces (Categorías)

| Categoría en Brejon | ¿Qué es y dónde va? | ¿Qué función cumple en la escena? |
| :--- | :--- | :--- |
| **Natural Lights** | Luces del entorno exterior: sol, cielo, luna o relámpagos. | Entran por las ventanas y tragaluces. Nos dicen qué hora es, qué clima hay afuera y dan la iluminación base a la pieza. |
| **Practical Lights** | Luces que forman parte del decorado visible: lámparas de velador, ampolletas colgando, tubos fluorescentes, velas o pantallas. | Rompen la oscuridad del fondo y **le dan al espectador la justificación visual** de por qué hay luz en ese rincón. |
| **Dramatic Lights** *(Studio Lights)* | Focos invisibles fuera de cámara que ponemos nosotros para modelar al personaje o prop. | Toman prestado el color y la dirección de la luz práctica, pero con la potencia justa para esculpir los volúmenes sin quemar la lámpara. |

> [!TIP] La Regla de Oro de Brejon
> Una luz práctica no tiene por qué iluminar por completo al personaje. Su presencia en escena actúa como una "excusa visual" ante el cerebro del jugador para justificar las luces de estudio invisibles que usamos para esculpirlo.

---

## 2. Simulador Interactivo: Habitación Interior y Flujo en 3 Capas

Prueben el simulador aquí abajo. Pueden rotar la cámara arrastrando con el ratón y probar los botones de presets rápidos para ver la diferencia entre tener solo la lámpara o sumar la luz dramática:

<ClientOnly>
  <InteriorLightingViewer />
</ClientOnly>

### El Flujo de Trabajo en 3 Capas:
1. **Capa 1 (Base Natural Fría)**: Cuadramos la luz que entra por la ventana desde afuera (~6.500K). Baña el suelo y las paredes en tonos fríos.
2. **Capa 2 (Lámpara Práctica Cálida)**: Ponemos la lámpara de velador o escritorio con valores creíbles (~2.700K). Genera un charco cálido de luz en la mesa.
3. **Capa 3 (Luz Dramática de Modelado)**: Añadimos un foco invisible de estudio orientado desde la lámpara hacia el objeto principal para recortar sus rasgos y darle volumen.

---

## 3. Fuentes Locales en Unreal Engine 5

Para iluminar interiores en Unreal usamos tres tipos de luces locales:

| Tipo de Luz en UE5 | Forma de emisión | ¿Cuándo conviene usarla en interiores? |
| :--- | :--- | :--- |
| **Rect Light (Luz de Área)** | Rectángulo plano | Ideal para ventanas, tubos fluorescentes de techo y pantallas de televisión o computador. Entrega sombras suaves muy naturales. |
| **Point Light (Puntual)** | Esfera en 360 grados | Ampolletas desnudas, velas o fuego. Ojo: ilumina hacia todos lados, así que hay que cuidar dónde choca. |
| **Spot Light (Focal)** | Cono direccional | Focos empotrados de techo, lámparas de escritorio dirigidas y linternas. |

### Dos Parámetros Clave que Deben Manejar:

* **Attenuation Radius (Radio de Atenuación)**: Define hasta qué distancia llega la luz.
  * *Ojo con esto*: Nunca dejen el radio gigante por flojera. Si la luz atraviesa las paredes, el motor va a calcular iluminación en piezas vacías contiguas, gastando recursos de la tarjeta de video por gusto y provocando fugas de luz (*light leaking*).
* **Source Radius (Radio de la Fuente)**: Le da tamaño físico real al emisor.
  * *Por qué importa*: Si el radio es 0, el reflejo especular en los objetos metálicos o plásticos se ve como un punto blanco microscópico irreal. Al subirle el radio a 2 o 5 cm, el reflejo se convierte en la forma redonda y suave de una ampolleta de verdad.

---

## 4. Nomenclatura Oficial de Assets en Unreal Engine

En cualquier estudio donde vayan a trabajar les van a pedir orden estricto en el Content Browser. Si tienen archivos llamados `NewBlueprint_1` o `Material_final_final`, nadie más del equipo va a poder trabajar en su escena.

Siguiendo el estándar oficial de Epic Games ([Recommended Asset Naming Conventions](https://dev.epicgames.com/documentation/en-us/unreal-engine/recommended-asset-naming-conventions-in-unreal-engine-projects)), la estructura que usamos es:

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

### Cómo Ordenar las Luces en el Outliner:
Para no volverse locos en el visor de Unreal con 20 luces sueltas, creen carpetas según las categorías de Brejon:
* `Lights_Natural/`: `L_Nat_Window_Rect`, `L_Nat_Sky_Ambient`
* `Lights_Practical/`: `L_Prac_DeskLamp_Point`, `L_Prac_Ceiling_Spot`
* `Lights_Dramatic/`: `L_Dram_Bust_Key`, `L_Dram_Desk_Fill`

---

## 5. Ejemplo Práctico: Iluminando un Rincón de Estudio Nocturno

Vamos a armar juntos este ejercicio paso a paso en el laboratorio:

1. **Construir el espacio básico**:
   * Levantamos una habitación cerrada simple con muros (`SM_Room_Wall`), suelo de madera (`SM_Room_Floor`) y un vano de ventana (`SM_Window_Frame`).
   * Al centro colocamos un escritorio (`SM_Desk_Wood`) y encima un busto o estatua (`SM_Bust_Marble`).
2. **Paso 1 - La Luz Natural Exterior**:
   * En el vano de la ventana ponemos una `Rect Light` (`L_Nat_Window_Rect`) mirando hacia adentro.
   * Color: Frío celeste (~6.500K). Intensidad moderada para simular el resplandor nocturno del cielo exterior bañando el suelo.
3. **Paso 2 - La Lámpara Práctica**:
   * Colocamos el modelo 3D de una lámpara de mesa (`SM_DeskLamp`).
   * Justo debajo de la pantalla ponemos una `Point Light` (`L_Prac_DeskLamp_Point`) cálida (~2.700K).
   * Ajustamos el `Source Radius` a 3 cm para que la ampolleta tenga volumen físico y `Attenuation Radius` justo al borde de la mesa (120 cm).
4. **Paso 3 - La Luz Dramática de Modelado**:
   * Si miramos el busto, verán que la lámpara solo le pega por abajo y deja el rostro a oscuras.
   * Agregamos una `Spot Light` o `Rect Light` oculta (`L_Dram_Bust_Key`), apuntando a la cara del busto con el mismo tono cálido de la lámpara (~3.000K).
   * Con esto conseguimos recortar la mejilla y la nariz sin reventar en blanco la mesa.
5. **Cierre y Evaluación de la Entrega N°1**:
   * En los últimos 20 minutos de la clase revisamos individualmente sus proyectos de la primera entrega según la pauta de 60 puntos.
