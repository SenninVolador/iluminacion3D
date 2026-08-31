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

Los Shaders son esencialmente álgebra vectorial y operaciones matemáticas aplicadas en paralelo por píxel y por vértice. Conocer los 5 operadores maestros te permite crear casi cualquier efecto visual en tiempo real.

---

## 1. El Efecto Fresnel (Fresnel / Dot Product)

El **Fresnel** describe un fenómeno físico: toda superficie se vuelve mucho más reflectante y brillante cuando se mira en un ángulo rasante (casi paralelo a la superficie) que cuando se mira perpendicularmente de frente.

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
$$\text{Fresnel} = 1.0 - (\vec{N} \cdot \vec{V})$$
Donde:
* $\vec{N}$ = Vector normal de la superficie (hacia dónde apunta la cara).
* $\vec{V}$ = Vector de vista de la cámara (hacia dónde mira el jugador).

### Usos en Videojuegos:
- **Efecto de escudo de energía o campo de fuerza**: Borde brillante alrededor de la silueta.
- **Bordes de terciopelo / tela (Fuzz effect)**.
- **Reflexión de agua y cristales**: Transparentes en el centro, reflectantes en las orillas.

---

## 2. LERP (Linear Interpolation / Interpolación Lineal)

El nodo más utilizado en cualquier Shader Graph. Mezcla dos valores o texturas ($A$ y $B$) basándose en una máscara de control ($Alpha$):

$$\text{Resultado} = A \times (1 - Alpha) + B \times Alpha$$

```
   Entrada A (Piedra limpia) ──┐
                               ├──► [ LERP ] ──► Superficie final
   Entrada B (Musgo verde)   ──┤         ▲
                                         │
                   Máscara Alpha (0 = A, 1 = B)
```

### Casos de uso típicos:
- **Pintura de vértices (Vertex Painting)**: Mezclar asfalto seco con charcos de agua o barro.
- **Daño progresivo / Desgaste**: Transicionar de pintura nueva a metal oxidado.
- **Efectos de disolución**: Usar una textura de ruido como Alpha para desintegrar un personaje.

---

## 3. Panner (Animación de Coordenadas UV)

El nodo **Panner** suma un valor dependiente del tiempo a las coordenadas UV de una textura:

$$\text{UV}_{\text{final}} = \text{UV} + (\vec{\text{Speed}} \times \text{Time})$$

* **Usos**: Ríos y cascadas de agua en movimiento, lava deslizándose, nubes en el cielo, cintas transportadoras, hologramas parpadeantes.

---

## 4. World Position Offset (WPO - Animación por Vértices)

Permite desplazar la posición geométrica de los vértices directamente en la GPU sin usar esqueletos ni huesos:

* **Vegetación y Viento**: Mover las puntas de las ramas y hojas usando una función seno ($\sin(\text{Time})$) multiplicada por los colores de vértice (*Vertex Color*).
* **Olas de Mar**: Generar ondulaciones en planos gigantes de agua.

---
**Notas relacionadas**:
- [[Fundamentos PBR y Mapas de Textura]]
- [[Anatomía del Shader Graph en Unreal (Master Materials e Instances)]]
- [[Modelos de Sombreado (Shading Models)]]
