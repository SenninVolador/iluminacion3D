---
tags:
  - unreal-engine
  - post-processing
  - exposicion
  - color-grading
  - aces
date: 2026-08-18
---

# 🎬 Exposición, Color Grading y ACES en UE5

El **PostProcessVolume** es el lente de la cámara en Unreal Engine. Define cómo la información física de luz (HDR en espacio lineal) se convierte en la imagen final visible en la pantalla (SDR / HDR display).

---

## 👁️ 1. Exposición y Adaptación Ocular (Auto Exposure)

En la vida real, los ojos (o el sensor de una cámara) se adaptan al pasar de un exterior brillante a una cueva oscura.

### Modos de Exposición en el PostProcessVolume:
1. **Auto Exposure Histogram (Recomendado)**:
   * Analiza el histograma de luminancia de la escena para ajustar automáticamente el valor de exposición (EV100).
   * Parámetros clave:
     * `Min EV100` / `Max EV100`: Limitan el rango de compensación automática para evitar que la escena se vuelva completamente blanca o negra.
     * `Speed Up` / `Speed Down`: Velocidad a la que el ojo se acostumbra a la luz o a la oscuridad.
2. **Manual Exposure**:
   * Desactiva la adaptación ocular dinámica y fija el valor exacto de la cámara usando ajustes fotográficos reales: **ISO**, **Apertura (f-stop)** y **Shutter Speed**.
   * Es el estándar para **Cinemáticas (Sequencer)** y para calibrar niveles con valores lumínicos físicamente correctos (Lux/Lúmenes).

> [!TIP] Regla de Oro para Iluminar
> Para no engañarte con la adaptación automática mientras iluminas un escenario, fija temporalmente `Min EV100 = 10` y `Max EV100 = 10` (mismo valor). Así verás la intensidad real de tus luces sin compensaciones automáticas.

---

## 🎨 2. Tonemapping y ACES en Unreal Engine

Unreal Engine 5 utiliza una curva de mapeo tonal basada en **ACES (Academy Color Encoding System)** por defecto.

### ¿Qué hace el Tonemapper?
Convierte los valores lineales de alto rango dinámico ($[0, \infty)$) al rango visible del monitor ($[0, 1]$), aplicando una suave compresión en las altas luces (*Roll-off / Shoulder*) para que los objetos muy brillantes no se quemen de golpe (*clipping*) y mantengan matices cromáticos.

### Controles de Curva en PostProcess:
* **Slope**: Ajusta el contraste general de la curva.
* **Toe**: Controla cómo se comprimen los tonos oscuros / sombras.
* **Shoulder**: Controla cómo se comprimen las altas luces (luces brillantes).
* **Black Clip / White Clip**: Define los umbrales absolutos de negro y blanco.

---

## 🌈 3. Color Grading y LUTs

El Color Grading permite establecer el tono emocional de una escena (terror, misterio, calidez veraniega, ciencia ficción ciberpunk).

### Controles Principales:
* **Temperature & Tint**:
  * `White Balance Temp`: Ajusta el balance en grados Kelvin (más frío $\approx 4000K$ o más cálido $\approx 7500K$).
* **Global / Shadows / Midtones / Highlights (Color Wheels)**:
  * Permite modificar **Saturation**, **Contrast**, **Gamma**, **Gain** y **Offset** de forma separada para cada rango de luminosidad.
* **Color Lookup Tables (LUTs)**:
  * Texturas especiales de 3D Cube que aplican transformaciones de color complejas diseñadas en Photoshop o DaVinci Resolve.
  * En UE5 con ACES, se recomienda calibrar primero con las ruedas de color nativas y usar LUTs solo para toques estilísticos sutiles.

---

## 🔮 4. Bloom (Resplandor)

El resplandor se produce cuando la luz excede el rango dinámico de la cámara y "sangra" en las lentes.

* **Modos de Bloom**:
  * **Standard (Convolution)**: Utiliza un kernel fotográfico realista para emular la suciedad o diafragma de una lente anamórfica/esférica.
  * **Gaussian**: Método rápido y estilizado basado en múltiples pasos de desenfoque gaussiano.
* **Threshold**: Nivel de brillo mínimo que debe tener un píxel antes de empezar a emitir Bloom.

---
**Notas relacionadas**:
- [[Atmósfera y Niebla Volumétrica en UE5]]
- [[Lenguaje Visual y Guía al Jugador]]
- [[Optimización de Iluminación y Profiling en UE5]]
