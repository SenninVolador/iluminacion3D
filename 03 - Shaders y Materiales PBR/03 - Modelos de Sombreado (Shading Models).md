---
tags:
  - shaders
  - shading-models
  - subsurface-scattering
  - unreal-engine
date: 2026-08-18
---

# Modelos de Sombreado (Shading Models) en Videojuegos

El **Shading Model (Modelo de Sombreado)** define la fórmula matemática exacta que la GPU utiliza para calcular la interacción entre la luz y el material. En Unreal Engine y motores modernos, no todas las superficies se comportan igual: la piel humana, el cristal de un coche o las hojas de un árbol requieren ecuaciones físicas distintas.

---

## 1. Los Modelos de Sombreado Principales

```
┌───────────────────────────┬────────────────────────────────────────────────────────┐
│ SHADING MODEL             │ COMPORTAMIENTO FÍSICO Y CASOS DE USO PRINCIPALES       │
├───────────────────────────┼────────────────────────────────────────────────────────┤
│ 1. Default Lit            │ El estándar opaco PBR (metales, madera, plásticos,     │
│                           │ piedra, hormigón, ropa normal).                        │
│ 2. Subsurface Scattering  │ Simula cómo la luz entra en el objeto, se dispersa por │
│    (SSS / Subsurface)     │ dentro y sale teñida (piel humana, cera, mármol, jade).│
│ 3. Two Sided Foliage      │ Deja pasar la luz a través de superficies ultrafinas   │
│                           │ de dos caras (hojas de árboles, césped, pétalos).      │
│ 4. Clear Coat             │ Doble capa especular: base mate + laca brillante       │
│                           │ transparente encima (pintura de coches, fibra de carb).│
│ 5. Eye                    │ Específico para ojos humanos: córnea húmeda y refrac-  │
│                           │ ción de la pupila e iris.                              │
│ 6. Hair                   │ Simulación anisotrópica de fibras de pelo y cabello.   │
│ 7. Unlit                  │ Sin cálculo de luz. Solo emite el color puro (UI, VFX, │
│                           │ láseres, fondos de cielo). Cero coste de sombreado.    │
└───────────────────────────┴────────────────────────────────────────────────────────┘
```

---

## 2. Estudio Detallado: Subsurface Scattering (SSS)

En objetos translúcidos u orgánicos, la luz no solo rebota en la superficie exterior; penetra varios milímetros, choca con células o pigmentos (como la hemoglobina de la sangre) y sale por otro punto:

```
               Luz Incidente
                    │
                    ▼
           ────────────────── Superficie de la piel
              \   •    /
               \  •   /   ◄── Dispersión interna y absorción
             ────\───/───────
                  ▼
              Luz Transmitida Rojiza (Orejas/Dedos a contraluz)
```

### Configuración en Unreal Engine:
* **Shading Model**: Cambiar de `Default Lit` a `Subsurface` o `Subsurface Profile`.
* **Subsurface Color**: Tono de color que adquiere la luz al dispersarse (para piel caucásica/humana suele ser un rojo/carmesí intenso).
* **Opacity**: En este modo, no controla la transparencia, sino la **profundidad de penetración** de la luz (valores bajos = mayor dispersión y efecto más lechoso/gomoso).

---

## 3. Two Sided Foliage (Vegetación y Hojas)

Las hojas de árboles, el césped y las cortinas son tan delgadas que cuando el sol les pega por detrás, se iluminan intensamente desde el punto de vista del jugador (*Subsurface Transmission*):

* **Problema con Default Lit**: Si miras una hoja desde el lado opuesto al sol, la cara visible queda completamente oscura.
* **Solución Two Sided Foliage**: Permite conectar un mapa en el canal **`Subsurface Color`** (usualmente un verde brillante amarillento) que se activa cuando la luz incide por la cara posterior.

---

## 4. Clear Coat (Pintura de Automóviles y Laca)

Permite simular materiales de dos capas físicas reales:
1. Una capa inferior con color, escamas metálicas o rugosidad media.
2. Una capa superior transparente, lisa y con alto brillo especular.

* **Parámetros exclusivos**:
  * `Clear Coat`: Intensidad de la capa de barniz ($0.0 - 1.0$).
  * `Clear Coat Roughness`: Rugosidad específica del barniz protector.

---
**Notas relacionadas**:
- [[Fundamentos PBR y Mapas de Textura]]
- [[Anatomía del Shader Graph en Unreal (Master Materials e Instances)]]
- [[Matemáticas de Shaders Esenciales (Fresnel, Lerp y Normales)]]
