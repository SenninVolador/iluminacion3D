---
tags:
  - clase
  - fundamentos
  - 3-point-lighting
  - shaders
  - pipeline
date: 2026-08-18
---

# Clase 01: Introducción a la Iluminación 3D, Juegos vs. Cine y Shaders

Bienvenido a los fundamentos de la iluminación tridimensional. Esta clase sienta las bases para comprender cómo funciona la luz en los entornos virtuales, cómo se construye el volumen de un objeto y cómo los motores gráficos interpretan los materiales.

---

## 1.  La Luz: Del Mundo Físico al Espacio Digital

En la física real, la luz está compuesta por fotones que viajan en línea recta, rebotan miles de millones de veces en las superficies circundantes y entran en nuestros ojos o en la lente de una cámara.

En el mundo digital 3D:
* La luz no existe de forma física; **es un cálculo matemático**.
* Una "fuente de luz" en un motor 3D es un vector con una posición, una dirección, un color y una intensidad que interactúa con la geometría de la escena.
* **La luz define la forma**: Sin luz, un modelo 3D con millones de polígonos se vería como una silueta plana y sin profundidad. La sombra y el brillo son los que revelan el relieve, la curvatura y el volumen.

---

## 2.  Videojuegos vs.  Cine: Dos Paradigmas de Iluminación

Una de las distinciones más importantes para un artista de iluminación es comprender para qué medio está trabajando:

```
┌────────────────────────────────────────┬────────────────────────────────────────┐
│      ILUMINACIÓN PARA VIDEOJUEGOS    │          ILUMINACIÓN PARA CINE       │
│          (Real-Time Rendering)         │          (Offline / Path Tracing)      │
├────────────────────────────────────────┼────────────────────────────────────────┤
│ • Debe calcularse en tiempo real       │ • Puede tardar minutos u horas por     │
│   (30, 60 o 120 fotogramas por segundo)│   cada fotograma individual.           │
│ • Presupuesto por frame: ~16 miliseg.  │ • Máxima precisión física y fidelidad. │
│ • La cámara es libre e impredecible:   │ • La cámara es fija y controlada:      │
│   el jugador puede mirar a donde sea.  │   solo se ilumina el encuadre final.   │
│ • Requiere trucos de optimización,     │ • Simulaciones de luz global con       │
│   baking o aproximaciones dinámicas.   │   millones de muestras de rayos.       │
└────────────────────────────────────────┴────────────────────────────────────────┘
```

> [!NOTE] El reto del Lighting Artist en Videojuegos
> El artista de videojuegos debe lograr que una escena se sienta tan bella y cinematográfica como una película, pero logrando que la tarjeta gráfica del jugador la procese en una **fracción de milisegundo**.

---

## 3.  Esquema de Iluminación de 3 Puntos (3-Point Lighting)

El **esquema de 3 puntos** es la técnica clásica nacida en la fotografía y el cine tradicional para esculpir y dar volumen tridimensional a un personaje u objeto frente a la cámara.

```
                         [ BACK / RIM LIGHT ]
                         (Detrás del sujeto)
                                 │
                                 ▼
                         ╔═══════════════╗
                         ║    SUJETO     ║
                         ║  (Personaje)  ║
                         ╚═══════════════╝
                                ▲
                               │ ╲
                   45° hacia   │  ╲   45° hacia
                   la izquierda│   ╲  la derecha
                              │    │
                              │    ▼
             [ KEY LIGHT ]    │   [ FILL LIGHT ]
          (Luz Principal -    │   (Luz de Relleno -
           Más potente)       │    Menos potente / Suave)
                              │
                              ▼
                          [ CÁMARA ]
```

---

### A. Key Light (Luz Principal o Clave)
* **Posición**: Colocada a unos $45^\circ$ a un lado de la cámara y ligeramente elevada ($30^\circ - 45^\circ$ sobre el sujeto).
* **Función**: Es la luz dominante de la escena. Establece la dirección principal, crea el contraste principal y proyecta las sombras dominantes.
* **Intensidad**: La más alta del esquema (100% de referencia).

### B. Fill Light (Luz de Relleno)
* **Posición**: En el lado opuesto a la Key Light (a unos $45^\circ$ hacia el otro lateral).
* **Función**: Rellenar y suavizar las sombras oscuras que produce la Key Light, asegurando que el lado en sombra no quede completamente negro y revele detalles.
* **Intensidad**: Más suave y difusa (suele oscilar entre el 25% y el 50% de la intensidad de la Key Light).

### C. Rim Light / Back Light (Luz de Contorno o Contraluz)
* **Posición**: Detrás del sujeto, apuntando hacia su espalda y bordes.
* **Función**: Crea un fino y elegante borde brillante alrededor de la silueta del personaje (hombros, cabeza, contorno).
* **Propósito visual**: **Despegar al sujeto del fondo** para que no se confunda visualmente con una pared o un escenario oscuro.

---

## 4.  ¿Qué es un Shader? (La Relación entre Luz y Superficie)

A menudo los principiantes confunden **Textura**, **Material** y **Shader**:

```
 ┌───────────────┐     ┌────────────────┐     ┌────────────────────────────────┐
 │    TEXTURA    │  +  │    MATERIAL    │  +  │            SHADER              │
 │ Imagen 2D     │     │ Contenedor de  │     │ Código que calcula cómo rebota │
 │ (Albedo, etc) │     │ propiedades    │     │ la luz según el ángulo visual  │
 └───────────────┘     └────────────────┘     └────────────────────────────────┘
```

### Definición sencilla:
Un **Shader (Sombreador)** es un pequeño programa informático que corre directamente en la tarjeta gráfica (**GPU**). 

Su trabajo es responder a esta pregunta para cada píxel de la pantalla:
$$\text{Color Final} = \text{Luz Incidente} \times \text{Propiedades del Material (Color, Rugosidad, Metalicidad)} \times \text{Ángulo de la Cámara}$$

### El flujo de trabajo PBR moderno:
Los shaders modernos utilizan el estándar **PBR (Physically Based Rendering)** con tres propiedades maestras:
1. **Base Color / Albedo**: El color propio del objeto (sin sombras pintadas).
2. **Roughness (Rugosidad)**: Si es liso y refleja como espejo ($0.0$) o si es áspero y dispersa el brillo ($1.0$).
3. **Metallic (Metalicidad)**: Si el material es un metal conductor ($1.0$) o un dieléctrico/no-metal como plástico, madera o piel ($0.0$).

---

## Ejercicio Práctico Sugerido para Clase 1

1. **Crear una escena vacía** con un plano en el suelo y una esfera o busto 3D en el centro.
2. **Apagar todas las luces** (escena 100% a oscuras).
3. **Añadir una a una las 3 luces** del esquema clásico:
   - Primero la **Key Light**: observar cómo esculpe la forma y la sombra.
   - Luego la **Fill Light**: ajustar su potencia hasta que la zona en penumbra sea legible sin competir con la luz principal.
   - Finalmente la **Rim Light**: colocarla detrás para ver cómo la silueta se separa del fondo negro.
4. **Variar la rugosidad (Roughness)** del material del busto de 0 a 1 para ver cómo cambia la respuesta a las tres luces.

---
**Notas relacionadas**:
- [[Glosario de Iluminación 3D]]
- [[Tipos de Luces en Unreal Engine]]
- [[Lenguaje Visual y Guía al Jugador]]
