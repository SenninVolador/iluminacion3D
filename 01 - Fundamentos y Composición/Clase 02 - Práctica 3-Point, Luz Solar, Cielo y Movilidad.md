---
tags:
  - clase
  - taller-practico
  - directional-light
  - sky-light
  - movilidad
  - analisis-juegos
date: 2026-08-18
---

# 🎓 Clase 02: Taller 3-Point Lighting, Sol, Cielo, Movilidad y Análisis en Juegos

Esta sesión se divide en cuatro bloques progresivos: la práctica directa del esquema clásico en Unreal Engine, el salto a la iluminación de exteriores con Sol y Cielo, el dominio de la movilidad técnica de luces, y el análisis de casos reales en la industria de los videojuegos.

---

## 🛠️ Bloque 1: Taller Práctico - Iluminando un Objeto con 3-Point Lighting

### 🎯 Objetivo:
Esculpir volumen, contraste y silueta en un modelo 3D (busto, esfera o personaje) partiendo desde la oscuridad absoluta.

```
                         [ RIM LIGHT ] (Back)
                         (Separación del fondo)
                                 │
                                 ▼
                         ╔═══════════════╗
                         ║    OBJETO     ║
                         ║  (Busto 3D)   ║
                         ╚═══════════════╝
                                ▲
                               │ ╲
                   45° Lateral │  ╲   45° Lateral
                   45° Altura  │   ╲  Más difusa
                              │    │
                              │    ▼
             [ KEY LIGHT ]    │   [ FILL LIGHT ]
          (Luz Principal -    │   (Relleno -
           Sombras marcadas)  │    25-40% de Key)
                              │
                              ▼
                          [ CÁMARA ]
```

### 📋 Paso a Paso en Unreal Engine:
1. **Preparar el Escenario**:
   * Crear un nivel vacío (`File -> New Level -> Empty Level`).
   * Añadir un plano de suelo (`Plane`) y colocar un objeto de prueba en el centro (coordenadas $0, 0, 0$).
2. **Paso 1: Key Light (Luz Principal)**:
   * Añadir una **Spot Light** o **Point Light** orientada a $45^\circ$ a la izquierda de la cámara y $45^\circ$ por encima de la cabeza del objeto.
   * Ajustar la intensidad hasta que ilumine claramente el rostro/superficie frontal y proyecte una sombra marcada en el lateral opuesto.
3. **Paso 2: Fill Light (Luz de Relleno)**:
   * Añadir una **Point Light** o **Spot Light** al lado derecho a $45^\circ$.
   * Desactivar `Cast Shadows` o bajar la intensidad a un **30%** de la Key Light.
   * *Objetivo*: Que el lado oscuro no quede negro carbón, sino con detalle visible.
4. **Paso 3: Rim Light (Luz de Contorno / Contraluz)**:
   * Añadir una **Spot Light** detrás del objeto, apuntando hacia su espalda y hombros.
   * Aumentar la intensidad y probar un tono ligeramente más frío o contrastado.
   * *Resultado*: Se forma un halo brillante en la silueta que lo despega mágicamente del fondo negro.

---

## ☀️ Bloque 2: Iluminando el Exterior (Directional Light + Sky Light)

En la naturaleza, un día soleado no está iluminado por bombillas locales, sino por un sistema dual: **Luz Solar Directa + Luz Difusa del Cielo**.

```
                ☀️ [ DIRECTIONAL LIGHT ] (Sol)
                Rayos directos, paralelos y sombras duras
                           │
                           │   ┌───────────────────────────┐
                           │   │  🌌 [ SKY LIGHT ] (Cielo) │
                           │   │  Luz ambiental hemisférica│
                           │   │  Relleno azul en sombras  │
                           ▼   └─────────────┬─────────────┘
                     ╔═══════════════╗       │
                     ║   EDIFICIO    ║◄──────┘
                     ╚═══════════════╝
```

### 1. Directional Light (El Sol)
* Simula una fuente a distancia infinita: **todos los rayos caen con el mismo ángulo paralelo**.
* **Propiedad clave**: Moverla de posición en el mapa no cambia nada; **solo importa su rotación**.
* **Atajo Pro**: Mantén presionado `Ctrl + L` y mueve el ratón en el viewport para girar el sol en vivo y ver cambiar la hora del día.

### 2. Sky Light (El Cielo y la Atmósfera)
* En un día real, las zonas en sombra bajo un árbol no son 100% negras porque la bóveda celeste azul actúa como una gigantesca lámpara difusa.
* La **Sky Light** captura los colores del cielo o de un mapa HDRI y "baña" uniformemente todas las superficies en sombra con esa tonalidad ambiental.

---

## ⚙️ Bloque 3: El Gran Dilema Técnico - Movilidad de Luces

En videojuegos, no todas las luces se calculan igual. Debemos elegir la movilidad según el tipo de juego y la plataforma:

```
┌───────────────┬───────────────────────────────┬───────────────────────────────┐
│   MOVILIDAD   │ ¿CÓMO SE CALCULA?             │ CUÁNDO USARLA                 │
├───────────────┼───────────────────────────────┼───────────────────────────────┤
│ 🪨 STATIC     │ 100% precalculada en texturas │ Juegos móviles, VR a 90 FPS,  │
│    (Estática) │ (Lightmaps). Cero coste GPU   │ entornos inmutables.          │
├───────────────┼───────────────────────────────┼───────────────────────────────┤
│ ⚖️ STATIONARY │ Híbrida: Luz directa dinámica  │ Entornos cerrados con luces   │
│ (Estacionaria)│ + rebotes y sombras baked.    │ fijas que cambian de color.   │
├───────────────┼───────────────────────────────┼───────────────────────────────┤
│ 🏃 MOVABLE    │ 100% tiempo real fotograma a  │ UE5 con Lumen, linternas,     │
│   (Dinámica)  │ fotograma. Máxima libertad.   │ ciclos día/noche, proyectiles.│
└───────────────┴───────────────────────────────┴───────────────────────────────┘
```

---

## 🎮 Bloque 4: Análisis de Casos Reales en la Industria

Veamos cómo grandes estudios han resuelto la iluminación según sus necesidades artísticas y técnicas:

### 1. 🌿 *The Last of Us Part I & II* (Naughty Dog)
* **Técnica reina**: **Baking de máxima fidelidad y Lightmaps de ultra resolución**.
* **¿Por qué?**: El juego busca un fotorrealismo cinematográfico desolador en interiores cubiertos de vegetación. Precalcular los rebotes de luz indirecta permite una suavidad física perfecta en las sombras sin ahogar la GPU de la consola.
* **Elemento dinámico**: La linterna de Joel/Ellie es una `Spot Light Movable` con sombras dinámicas que rompe la oscuridad de forma aterradora.

### 2. 🏙️ *Cyberpunk 2077* (CD Projekt RED)
* **Técnica reina**: **Iluminación Dinámica + Ray Tracing / Path Tracing**.
* **¿Por qué?**: Night City es un entorno urbano denso con cientos de pantallas emisivas, neones parpadeantes, lluvia con charcos reflectantes y ciclo día/noche continuo. El baking sería imposible debido al dinamismo total de la ciudad.

### 3. 🗡️ *The Legend of Zelda: Tears of the Kingdom* (Nintendo)
* **Técnica reina**: **Directional Light + Sky Light estilizado + Sombras en cascada optimizadas**.
* **¿Por qué?**: Nintendo Switch tiene una potencia gráfica limitada. El equipo diseñó una luz direccional muy limpia combinada con un shader cel-shading que aprovecha el contraste de colores complementarios (cielos azules dorados y sombras celestes).

### 4. 🧟 *Resident Evil 2 & 4 Remake* (Capcom - RE Engine)
* **Técnica reina**: **Contraste Extremo, Niebla Volumétrica y Linterna de Protagonista**.
* **¿Por qué?**: El terror se basa en la **ausencia de luz**. La luz direccional exterior casi no existe; todo se construye con pequeñas fuentes de luz puntuales temblorosas y la linterna del jugador que interactúa con el humo y la niebla volumétrica.

---
**Notas relacionadas**:
- [[MOC - Iluminación para Videojuegos]]
- [[Glosario de Iluminación 3D]]
- [[Tipos de Luces en Unreal Engine]]
- [[Movilidad de Luces (Static, Stationary, Movable)]]
- [[Lenguaje Visual y Guía al Jugador]]
