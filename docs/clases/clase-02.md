# Clase 02: Taller de 3 Puntos, Sol, Cielo y Movilidad de Luces

Cátedra de Iluminación 3D y Shaders para Videojuegos · Docente Daniel Rojas (UNIACC)

---

## 1. Taller Práctico: Esquema de Tres Puntos en el Busto 3D

El ejercicio consiste en construir la volumetría de un busto tridimensional partiendo desde la oscuridad absoluta.

<ThreePointLightingViewer />

### Protocolo de Construcción en Unreal Engine 5:
1. **Inicialización**: Crear un nivel vacío (`File -> New Level -> Empty Level`) e insertar un plano de suelo neutro junto al busto en el origen de coordenadas.
2. **Emisor Principal (Key)**: Configurar un foco a $45^\circ$ lateral y $45^\circ$ cenital. Calibrar hasta obtener una penumbra definida.
3. **Emisor de Relleno (Fill)**: Situar una luz difusa en el flanco opuesto sin proyección de sombras duras, a un tercio de la potencia principal.
4. **Emisor Posterior (Rim)**: Posicionar una luz trasera alineada con la silueta para generar la separación tonal respecto al fondo.

---

## 2. Fuentes de Iluminación Exterior: Sol y Atmósfera

* **Directional Light (Luz Solar)**: Modela una fuente situada en el infinito; emite rayos rigurosamente paralelos. La traslación espacial carece de efecto; el cálculo depende exclusivamente del **vector de rotación** (atajo de calibración: `Ctrl + L`).
* **Sky Light (Luz de Cielo / Hemisférica)**: Captura la radiancia difusa de la bóveda celeste para bañar las superficies en sombra, **evitando valores de negro absoluto ($RGB = 0, 0, 0$)**.

---

## 3. Matriz de Movilidad Técnica (Rendimiento vs. Interactividad)

| Movilidad | Método de Cómputo | Coste de GPU en Runtime | Criterio de Selección |
| :--- | :--- | :--- | :--- |
| **Static** | 100% precalculada en mapas de textura (Lightmaps) | Nulo (0 ms) | Realidad virtual (90 FPS), plataformas móviles, geometría estática |
| **Stationary** | Híbrido: Luz directa dinámica + GI precalculada | Moderado | Consolas y PC. Permite modular intensidad y color en ejecución |
| **Movable** | 100% resuelta por fotograma en tiempo real | Alto continuo | UE5 con Lumen, proyectores móviles, linternas, ciclo día/noche |

> **Restricción de Canales (Stationary Overlap)**: En el pipeline diferido clásico de Unreal Engine, no pueden coincidir más de 4 emisores Stationary proyectando sombras sobre una misma superficie (canales RGBA de la máscara de sombras). Un quinto emisor se degrada automáticamente a modo Movable.

---

## 4. Análisis de Casos en la Industria

* **The Last of Us Part I / II (Naughty Dog)**: Precomputación de alta densidad de iluminación indirecta para interiores fotorrealistas combinada con linternas dinámicas.
* **Cyberpunk 2077 (CD Projekt RED)**: Pipeline dinámico integral con trazado de rayos por la alta densidad de emisores de área y ciclo diurno.
* **The Legend of Zelda: Tears of the Kingdom (Nintendo)**: Iluminación solar direccional y cúpula celeste estilizada mediante sombreado no fotorrealista (NPR) optimizado para Nintendo Switch.
* **Resident Evil 4 Remake (Capcom)**: Supresión de luz direccional diurna; construcción de atmósfera mediante niebla volumétrica y conos focales estrechos.
