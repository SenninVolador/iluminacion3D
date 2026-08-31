---
tags:
  - shaders
  - pbr
  - texturizado
  - materiales
  - gamedev
date: 2026-08-18
---

# Fundamentos PBR y Mapas de Textura

El renderizado basado en la física (**PBR - Physically Based Rendering**) es el estándar moderno en videojuegos para describir cómo los materiales reaccionan a la luz de manera coherente en cualquier condición lumínica (día, noche, interiores o antorchas).

---

## 1. Los Dos Principios Físicos de PBR

1. **Conservación de la Energía**: Una superficie nunca puede reflejar más luz de la que recibe. Si la reflexión especular es muy brillante, la dispersión difusa disminuye.
2. **Microfacetas (Micro-geometría)**: Toda superficie real está compuesta por microscópicos valles y crestas. Cuanto más áspera es la superficie, más se dispersan los rayos de luz en ángulos caóticos (**Roughness alto**); cuanto más pulida, más paralelos rebotan (**Roughness bajo**).

---

## 2. Los Mapas de Textura Esenciales (Pipeline Metálico/Rugosidad)

```
┌─────────────────┬──────────┬────────────────────────────────────────────────────────┐
│ MAPA            │ CANALES  │ DESCRIPCIÓN Y FUNCIÓN EN EL SHADER                     │
├─────────────────┼──────────┼────────────────────────────────────────────────────────┤
│ Base Color      │ RGB      │ Color puro sin sombras ni brillos pintados (Albedo).   │
│ Roughness       │ Escala G │ 0.0 = Espejo pulido / brillo nítido.                   │
│                 │          │ 1.0 = Mate / dispersión difusa total.                  │
│ Metallic        │ Escala G │ 0.0 = Dieléctrico (madera, piel, plástico, tela).      │
│                 │          │ 1.0 = Metal puro (oro, cromo, hierro).                 │
│ Normal Map      │ RGB      │ Simula relieve y detalle geométrico falso en micro-valles.│
│ Ambient Occl.   │ Escala G │ Sombras de contacto en grietas y hendiduras.           │
│ Emissive        │ RGB      │ Luz propia emitida por el material (pantallas, neón).  │
└─────────────────┴──────────┴────────────────────────────────────────────────────────┘
```

---

## 3. Empaquetado de Texturas (Channel Packing / Texturas ORM)

En videojuegos, leer una textura desde la GPU tiene un coste de memoria y ancho de banda. Como los mapas de **Ambient Occlusion**, **Roughness** y **Metallic** son mapas en escala de grises (solo usan 1 canal de información de 8 bits), se empaquetan dentro de una **única textura RGB**:

```
                 TEXTURA EMPAQUETADA: "T_Asset_ORM.png"
               ┌────────────────────────────────────────┐
               │ Canal R (Rojo)  ───► Ambient Occlusion │
               │ Canal G (Verde) ───► Roughness         │
               │ Canal B (Azul)  ───► Metallic          │
               │ Canal A (Alpha) ───► (Opcional: Mask)  │
               └────────────────────────────────────────┘
```

> [!IMPORTANT] Ahorro Crítico en GPU
> Empaquetar en ORM reduce el número de llamadas de muestreo de textura (**Texture Samplers**) de 3 archivos separados a 1 solo, reduciendo la memoria VRAM ocupada a un tercio y acelerando el rendimiento del shader.

---

## 4. Reglas de Oro en PBR para no romper el Shading

- **Metalicidad binaria**: En el mundo real, los materiales son casi siempre **100% metal (1.0)** o **100% no-metal (0.0)**. Los valores intermedios (como 0.5) solo se usan para transiciones sucias como polvo sobre metal oxidado.
- **Sin sombras en el Base Color**: Nunca pintes oaxilas, sombras de pliegues o brillos especulares blancos en la textura de Base Color. Las sombras son trabajo de la luz y del Ambient Occlusion.
- **Valores mínimos de luminosidad**: El negro absoluto ($RGB = 0, 0, 0$) no existe en la naturaleza. El carbón más negro refleja alrededor del $3-4\%$ de la luz ($sRGB \approx 30-50$).

---
**Notas relacionadas**:
- [[Anatomía del Shader Graph en Unreal (Master Materials e Instances)]]
- [[Modelos de Sombreado (Shading Models)]]
- [[Matemáticas de Shaders Esenciales (Fresnel, Lerp y Normales)]]
- [[Glosario de Iluminación 3D]]
