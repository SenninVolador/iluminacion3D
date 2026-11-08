---
tags:
  - shaders
  - matematicas
  - fresnel
  - lerp
  - tech-art
date: 2026-08-18
---

# Matemáticas de Shaders Esenciales (Fresnel, Lerp y Normales)

Los Shaders son esencialmente álgebra vectorial y operaciones matemáticas aplicadas en paralelo por píxel y por vértice. Conocer los operadores maestros te permite crear casi cualquier efecto visual en tiempo real.

---

## 1. El Efecto Fresnel

El **efecto Fresnel** describe un fenómeno óptico fundamental: la reflectancia de una superficie aumenta drásticamente a medida que el ángulo de visión se vuelve más rasante (tangente a la superficie).

<ClientOnly>
  <FresnelViewer />
</ClientOnly>

```
       Cámara de Frente (0°)                      Cámara en Ángulo Rasante (90°)
       Menor brillo especular                     Máximo brillo reflectante / Borde
                │                                                /
                ▼                                               /
        ╔═════════════════╗                             ╔═════════════════╗
        ║    SUPERFICIE   ║                             ║    SUPERFICIE   ║
        ╚═════════════════╝                             ╚═════════════════╝
```

### La fórmula matemática básica (Producto Punto):

<div class="formula-card">
  <div class="formula-title">ECUACIÓN DE FRESNEL</div>
  <div class="formula-eq">Fresnel = 1.0 − dot(N, V)</div>
  <div class="formula-sub">Donde <strong>N</strong> es el vector normal de la superficie y <strong>V</strong> es el vector de vista hacia la cámara del jugador.</div>
</div>

### Usos en Videojuegos:
- **Efecto de escudo de energía o campo de fuerza**: Borde brillante alrededor de la silueta.
- **Rim Light estilizada en NPR / Cel Shading**: Recorte de luz automático en hombros y cabello.
- **Reflexión de agua y cristales**: Transparentes al mirarlos desde arriba, reflectantes en las orillas.

---

## 2. LERP (Linear Interpolation / Interpolación Lineal)

El nodo más utilizado en cualquier Shader Graph. Mezcla dos valores o texturas (`A` y `B`) basándose en una máscara de control (`Alpha` de `0.0` a `1.0`):

<div class="formula-card">
  <div class="formula-title">INTERPOLACIÓN LINEAL (NODO LERP)</div>
  <div class="formula-eq">Resultado = A × (1.0 − Alpha) + B × Alpha</div>
  <div class="formula-sub">Cuando <strong>Alpha = 0.0</strong> devuelve 100% de A; cuando <strong>Alpha = 1.0</strong> devuelve 100% de B.</div>
</div>

```
   Entrada A (Piedra limpia) ──┐
                               ├──► [ LERP ] ──► Superficie final
   Entrada B (Musgo verde)   ──┤         ▲
                                         │
                   Máscara Alpha (0 = A, 1 = B)
```

### Casos de uso típicos:
- **Pintura de vértices (Vertex Painting)**: Mezclar asfalto seco con charcos de agua o musgo usando los canales `R, G, B` del Vertex Color.
- **Cortes de Cel Shading**: Mezclar el color de sombra (`A`) y el color iluminado (`B`) usando un nodo `Step` o `SmoothStep` como `Alpha`.
- **Efectos de disolución**: Usar una textura de ruido como `Alpha` para desintegrar un personaje.

---

## 3. Panner (Animación de Coordenadas UV)

El nodo **Panner** suma un valor dependiente del tiempo a las coordenadas UV de una textura:

<div class="formula-card">
  <div class="formula-title">DESPLAZAMIENTO TEMPORAL DE COORDENADAS UV</div>
  <div class="formula-eq">UV_Final = UV_Original + ( Velocidad × Time )</div>
  <div class="formula-sub">Permite animar cascadas, ríos, lava, cintas transportadoras u hologramas sin mover el polígono.</div>
</div>

---

## 4. World Position Offset (WPO - Animación por Vértices)

Permite desplazar la posición geométrica de los vértices directamente en la GPU sin usar esqueletos ni huesos:

* **Vegetación y Viento**: Mover las puntas de las ramas y hojas usando una función seno (`sin(Time)`) multiplicada por el canal Alfa del color de vértice (`VertexColor.A`).
* **Contornos Inverted Hull en NPR**: Inflar la malla trasera a lo largo de su normal (`VertexNormalWS × Grosor`) para crear líneas de tinta alrededor del personaje.

---
**Notas relacionadas**:
- [NPR, Geometría de Normales y Vertex Color](/npr/)
- [Fundamentos PBR y Mapas de Textura](/shaders/01-fundamentos-pbr)
- [Anatomía del Shader Graph en Unreal (Master Materials e Instances)](/shaders/02-master-materials)
- [Modelos de Sombreado (Shading Models)](/shaders/03-shading-models)
