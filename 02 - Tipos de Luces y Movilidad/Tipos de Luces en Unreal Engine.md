---
tags:
  - unreal-engine
  - luces
  - componentes
date: 2026-08-18
---

# 💡 Tipos de Luces en Unreal Engine

Unreal Engine proporciona cinco fuentes de luz principales. Cada una tiene propiedades físicas, costes computacionales y usos artísticos específicos.

---

## 1. ☀️ Directional Light (Luz Direccional)
Simula una fuente de luz infinitamente distante (como el **Sol** o la **Luna**).

* **Comportamiento**: Todos los rayos de luz viajan en **líneas paralelas**.
* **Propiedad clave**: La posición del actor en el mundo no importa; solo influye su **rotación**.
* **Integración con la Atmósfera**:
  * Activa la casilla `Atmosphere Sun Light` (y define el `Atmosphere Sun Light Index`: 0 para Sol, 1 para Luna).
  * Controla la posición visual del disco solar en el [[Atmósfera y Niebla Volumétrica en UE5|SkyAtmosphere]].
* **Atajo en Editor**: Mantén pulsada la tecla `Ctrl + L` y mueve el ratón para cambiar interactivamente la hora del día y la orientación del sol.

---

## 2. 💡 Point Light (Luz Puntual)
Emite luz omnidireccional (en todas direcciones, esfera de 360°) desde un único punto en el espacio.

* **Casos de uso**: Bombillas desnudas, velas, fogatas, destellos, chispas.
* **Propiedades Clave**:
  * `Attenuation Radius`: Radio máximo de alcance de la luz. *(Mantenerlo tan ajustado como sea posible para optimizar el rendimiento)*.
  * `Source Radius` / `Soft Source Radius`: Radio físico del emisor (crea reflejos especulares realistas y penumbras en sombras suaves).
  * `Source Length`: Permite convertir la luz puntual en una luz en forma de tubo / fluorescente.
* **Unidades**: Candela ($cd$) o Lúmenes ($lm$).

---

## 3. 🔦 Spot Light (Luz Focal / Foco)
Emite luz en forma de cono desde un punto hacia una dirección específica.

* **Casos de uso**: Linternas, farolas de calle, luces de escenario, focos de techo empotrados (Downlights), faros de vehículos.
* **Propiedades Clave**:
  * `Inner Cone Angle`: Ángulo central donde la intensidad es del 100%.
  * `Outer Cone Angle`: Ángulo exterior donde la intensidad cae suavemente a cero (penumbra).
  * `Attenuation Radius`: Longitud/alcance del cono.
  * `IES Profiles`: Texturas fotométricas que imitan la distribución real del cristal o reflector de una lámpara real.

---

## 4. 🔲 Rect Light (Luz Rectangular / de Área)
Emite luz desde una superficie rectangular hacia una sola dirección (semiesfera).

* **Casos de uso**: Paneles LED, pantallas de TV/monitores, tragaluces o ventanas interiores, fluorescentes de techo en oficinas, cajas de luz fotográficas (Softboxes).
* **Propiedades Clave**:
  * `Source Width` y `Source Height`: Dimensiones físicas del rectángulo.
  * `Barn Door Angle` y `Barn Door Length`: Simula las "aletas" de iluminación de estudio para cortar y recortar el haz de luz.
* **Rendimiento**: Es más costosa que una Point o Spot Light, especialmente al calcular sombras dinámicas.

---

## 5. 🌌 Sky Light (Luz de Cielo / Ambiente)
Captura el entorno distante (cielo, nubes, montañas lejanas o mapa HDRI) y proyecta luz ambiental difusa e indirecta en toda la escena.

* **Modos de Captura**:
  * `SLS Captured Scene`: Captura dinámicamente el cielo actual del nivel (SkyAtmosphere / Volumetric Clouds). En tiempo real requiere `Real Time Capture` activado.
  * `SLS Specified Cubemap`: Aplica una textura HDRI / Cubemap estática personalizada (muy usada para look cinematográfico o previews de assets).
* **Función Clave**: Rellena las sombras que de otro modo quedarían 100% negras, dando color y tono al ambiente global.

---

## 📊 Tabla Comparativa de Rendimiento y Características

| Tipo de Luz | Complejidad de Sombras | Coste GPU | Soporte IES Profile | Uso Principal |
| :--- | :--- | :--- | :--- | :--- |
| **Directional** | Media / Alta (Cascadas/VSM) | Global | No | Sol / Luna / Exteriores |
| **Point Light** | Alta (6 caras de cubemap) | Local (Medio) | Sí | Bombillas / Fuego / Efectos |
| **Spot Light** | Media (1 proyección de cono) | Local (Bajo) | Sí | Linternas / Focos / Guía visual |
| **Rect Light** | Muy Alta | Local (Alto) | Sí (Texture) | Pantallas / Ventanas / Paneles |
| **Sky Light** | Muy Baja / Integrada en GI | Global | Cubemap | Luz ambiental de relleno |

---
**Notas relacionadas**:
- [[Movilidad de Luces (Static, Stationary, Movable)]]
- [[Atmósfera y Niebla Volumétrica en UE5]]
- [[Lumen vs Baked Lighting (UE5)]]
