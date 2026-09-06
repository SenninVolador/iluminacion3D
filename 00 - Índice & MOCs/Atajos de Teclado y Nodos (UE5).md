---
tags:
  - atajos
  - shortcuts
  - unreal-engine
  - shaders
  - workflow
date: 2026-09-06
---

# Atajos de Teclado y Nodos en Unreal Engine 5

Iluminación 3D · Docente Daniel Rojas (UNIACC)

Guía rápida de combinaciones de teclas para optimizar el flujo de trabajo en iluminación, navegación en el Viewport y creación ágil de nodos en el Material Graph.

---

## 1. Atajos Rápidos del Material Editor (Crear Nodos con 1 Click)

| Tecla + Click | Nodo Creado | Función Técnica en Shaders |
| :--- | :--- | :--- |
| **`S + Click`** | **Scalar Parameter** | Parámetro numérico expuesto en la Instancia (ej: `Roughness`, `Metallic`). |
| **`V + Click`** | **Vector Parameter** | Selector cromático RGBA expuesto en la Instancia (ej: `Color_Tint`). |
| **`M + Click`** | **Multiply** | Multiplicador matemático para teñir texturas o escalar intensidades. |
| **`T + Click`** | **Texture Sample** | Muestra de textura 2D (Albedo, mapa ORM o Normal Map). |
| **`1 + Click`** | **Constant (Float)** | Valor numérico fijo de 1 solo canal (ej: 0.0 o 1.0). |
| **`3 + Click`** | **Constant3Vector** | Color RGB estático sin exponer como parámetro. |
| **`L + Click`** | **LinearInterpolate (Lerp)** | Mezcla dos entradas ($A$ y $B$) controladas por una máscara Alpha. |
| **`A + Click`** | **Add** | Suma matemática de dos valores o canales. |
| **`U + Click`** | **TextureCoordinate (TexCoord)** | Control de repetición y escala de coordenadas UV (*Tiling*). |
| **`O + Click`** | **OneMinus** | Invierte un mapa o valor en escala de grises ($1.0 - x$). |

---

## 2. Manipulación de Cables y Organización Nodal

* **Desconectar un pin**: Mantén presionado `Alt + Click Izquierdo` sobre el pin o sobre el cable que deseas cortar.
* **Reubicar una conexión existente**: Mantén presionado `Ctrl + Click Izquierdo` sobre el pin conectado y arrástralo a otro pin sin tener que borrar el cable.
* **Nodo Reroute (Puntos de anclaje)**: Haz **doble click** sobre cualquier cable para crear un punto de pivote y organizar conexiones limpias.
* **Caja de comentarios**: Selecciona un conjunto de nodos y presiona la tecla **`C`**. Genera un recuadro donde puedes documentar el bloque (por ejemplo: *"Tinte de Base Color"* o *"Normal Map"*).
* **Buscador general**: Presiona `Espacio` o haz `Click Derecho` en una zona vacía del editor para buscar cualquier función matemática.

---

## 3. Control de Iluminación en el Viewport 3D

| Atajo | Acción Técnica |
| :--- | :--- |
| **`Ctrl + L` + Mover Mouse** | Rotación interactiva de la **Directional Light** (Sol). Modifica la hora del día en tiempo real. |
| **`Click Derecho > Pilot`** (o `Ctrl + Shift + P`) | **Pilotar la luz**: Controlas la luz seleccionada como si fueras la cámara en primera persona. |
| **`G` (Game View)** | Oculta todos los gizmos, conos y flechas de luces para evaluar la escena limpia. |
| **`End`** | Hace caer el objeto seleccionado directamente sobre la superficie del suelo (*Snap to floor*). |
| **`Alt + Arrastrar Gizmo`** | Duplica el foco de luz o el objeto inmediatamente en el eje seleccionado. |
| **`F` (Focus)** | Centra y enfoca la cámara sobre el objeto o luz seleccionada en el Outliner. |

---

## 4. Navegación de Cámara (Viewport)

| Atajo / Control | Función de Movimiento |
| :--- | :--- |
| **`Click Derecho + W, A, S, D`** | Vuelo libre en primera persona (estilo FPS). |
| **`Click Derecho + Q / E`** | Descender verticalmente (`Q`) o elevarse verticalmente (`E`). |
| **`Rueda del Mouse` (mientras vuelas)** | Ajusta la velocidad de desplazamiento de la cámara en el Viewport. |
| **`Alt + Click Izquierdo`** | Orbitar en 360° alrededor del punto de interés actual. |
| **`Alt + Click Derecho`** | Zoom continuo de aproximación o alejamiento. |
| **`F11`** | Modo inmersivo en pantalla completa. |
