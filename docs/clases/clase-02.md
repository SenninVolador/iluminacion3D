# 🎓 Clase 02: Taller 3-Point, Sol, Cielo y Movilidad de Luces

En esta sesión realizamos el taller práctico del esquema clásico en Unreal Engine, comprendemos la iluminación de exteriores con Sol y Cielo, y dominamos la movilidad técnica de luces.

---

## 🕹️ Simulador Interactivo: Estudio de 3 Puntos
Prueba a encender y apagar las luces individualmente para ver cómo se complementan:

<ThreePointLightingViewer />

---

## 🛠️ 1. Taller Práctico: Iluminando el Busto 3D

### Paso a Paso en Unreal Engine 5:
1. **Crear Nivel Vacío**: `File -> New Level -> Empty Level`. Añadir un plano de suelo y el busto en el centro.
2. **Paso 1 (Key Light)**: Colocar una Spot/Point Light a 45° lateral y 45° elevada. Ajustar hasta obtener una sombra marcada.
3. **Paso 2 (Fill Light)**: Añadir una luz en el lado opuesto al 30% de intensidad sin proyectar sombras duras.
4. **Paso 3 (Rim Light)**: Añadir una luz detrás del busto para generar el filo brillante que lo separa del fondo negro.

---

## ☀️ 2. Iluminando el Exterior: Sol y Cielo

* **Directional Light (Luz Solar)**: Emite rayos 100% paralelos desde el infinito. Solo importa su **rotación** (atajo: `Ctrl + L` + mover ratón).
* **Sky Light (Luz de Cielo)**: Captura la cúpula celeste para rellenar las sombras con luz difusa azulada, **impidiendo que las sombras sean negras puras**.

---

## ⚙️ 3. Movilidad de Luces (Arte vs. Rendimiento)

| Movilidad | Método de Cálculo | Coste GPU | Cuándo Usarla |
| :--- | :--- | :--- | :--- |
| **Static** | 100% Horneada en Lightmaps | Cero en runtime | VR a 90 FPS, móviles, niveles fijos |
| **Stationary** | Híbrida: Directa dinámica + Indirecta baked | Medio | Consolas/PC. Permite variar color/intensidad |
| **Movable** | 100% Tiempo real cuadro a cuadro | Alto continuo | UE5 con Lumen, linternas, ciclos día/noche |

> **🚨 Alerta de Rendimiento**: En Unreal clásico no puedes solapar más de 4 luces *Stationary* con sombras en el mismo espacio (canales RGBA). Una 5ª luz se marcará con `❌` roja y pasará a *Movable*, duplicando el coste.

---

## 🎮 4. Casos de Estudio en la Industria

* [The Last of Us Part I/II (Naughty Dog)](https://www.youtube.com/watch?v=R9_mD4oI6fU): Baking de máxima precisión para fotorrealismo en interiores desolados + linterna dinámica en combate.
* [Cyberpunk 2077 (CD Projekt RED)](https://www.youtube.com/watch?v=a3YxH_xK004): Iluminación 100% dinámica y Ray Tracing por la densidad de neones emisivos y clima variable.
* [Zelda: Tears of the Kingdom (Nintendo)](https://www.nintendo.com/games/detail/the-legend-of-zelda-tears-of-the-kingdom-switch/): Directional + Sky estilizado con cel-shading en Nintendo Switch.
* [Resident Evil 4 Remake (Capcom)](https://www.residentevil.com/re4/): Ausencia de sol; atmósfera de terror creada con linterna y niebla volumétrica.
