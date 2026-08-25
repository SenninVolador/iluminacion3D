---
tags:
  - presentacion
  - diapositivas
  - clase03
  - shaders
  - master-materials
  - busto3d
  - directional-light
  - sky-light
date: 2026-08-25
---

# 📽️ Presentación: Clase 03 — Shaders PBR en el Busto, Sol, Cielo y Luces Locales

> **Ramo**: Iluminación 3D y Shaders para Videojuegos  
> **Duración estimada**: 60 – 90 minutos  
> **Estructura**: 8 Diapositivas interactivas + Taller en Vivo en Unreal Engine 5  
> **Formato en vivo**: [Presentación en Pantalla / Proyector (HTML)](file:///c:/Users/danie/OneDrive/Escritorio/Iluminacion3D/Presentacion_Clase_03.html)  
> **Ficha Técnica Editorial**: [Material Visual Clase 03 (PDF)](file:///c:/Users/danie/OneDrive/Escritorio/Iluminacion3D/Material_Visual_Clase_03.pdf)

---

## 🗂️ Índice de Diapositivas

```
[ Diapositiva 01 ] ──► Portada: Shaders PBR en el Busto 3D, Sol, Cielo y Luces
[ Diapositiva 02 ] ──► Texturas Empaquetadas ORM para el Busto (AO, Roughness, Metallic)
[ Diapositiva 03 ] ──► Master Material vs. Instancias en el Busto (Piel vs Metal vs Oro)
[ Diapositiva 04 ] ──► El Busto bajo Directional Light (Sol): Relieve y Normales
[ Diapositiva 05 ] ──► El Busto bajo Sky Light (Cielo): Relleno y AO en Cavidades
[ Diapositiva 06 ] ──► Luces Locales de Acento en el Rostro (Point, Spot y Rect)
[ Diapositiva 07 ] ──► Casos Reales: God of War, Horizon, Alan Wake 2, Gears 5
[ Diapositiva 08 ] ──► Desafío Práctico en Clase con el Busto & Próxima Sesión
```

---

## 🎞️ Puntos de Charla y Guión

### 🟢 Diapositiva 01: Portada y Arquitectura
* **Concepto central**: Continuamos con el **busto 3D de la Clase 02**. Hoy lo vestimos con un *Master Material PBR* y evaluamos su respuesta física bajo iluminación solar, de cielo y luces de estudio.

---

### 🟢 Diapositiva 02: Texturas Empaquetadas ORM
* **R (Ambient Occlusion)**: Oclusión en cuencas oculares, nariz y arrugas del busto.
* **G (Roughness)**: Piel mate ($0.75$) vs cromo brillante ($0.10$).
* **B (Metallic)**: Dieléctrico ($0.0$) vs Metal ($1.0$).
* **Ahorro técnico**: 1 sola textura RGB empaquetada ahorra 2 lecturas en GPU (*Texture Samplers*).

---

### 🟢 Diapositiva 03: Master Material vs. Instancias
* **`M_Master_PBR`**: Lógica centralizada con parámetros de rugosidad, metalicidad, tinte y fuerza de normales.
* **Instancias**: `MI_Busto_PielMate`, `MI_Busto_Cromo` y `MI_Busto_Oro`. Cambio instantáneo en el Viewport sin recompilar shaders.

---

### 🟢 Diapositiva 04: Directional Light en el Busto (El Sol)
* Al rotar el sol con <kbd>Ctrl + L</kbd>, el *Normal Map* del busto resalta poros y arrugas bajo luz rasante.
* Búsqueda del ángulo clásico **Rembrandt** (45° lateral) para generar el triángulo luminoso en la mejilla opuesta.

---

### 🟢 Diapositiva 05: Sky Light en el Busto (Cúpula Celeste)
* Baña el lado oscuro del busto con luz difusa ambiental azulada, impidiendo sombras 100% negras.
* Respeta el canal R (Ambient Occlusion) del shader para no aplanar las cuencas oculares.

---

### 🟢 Diapositiva 06: Luces Locales de Acento
* **Point Light**: Chispa o fuego cercano.
* **Spot Light**: Linterna o luz de recorte con perfil IES que crea el brillo en la pupila (*Eye Catchlight*).
* **Rect Light**: Softbox de estudio fotográfico para reflejos suaves en pómulos y frentes pulidas.

---

### 🟢 Diapositiva 07: Casos de Estudio en la Industria (con Enlaces Oficiales)
* 🪓 [God of War Ragnarök (Santa Monica Studio)](https://www.artstation.com/artwork/g8GZ8K): Rostro de Kratos esculpido bajo sol rasante y antorchas mediante Roughness variable.
* 🤖 [Horizon Forbidden West (Guerrilla Games)](https://www.guerrilla-games.com/read/the-technology-of-horizon-forbidden-west): Sol y cielo bañando la piel mate de Aloy y piezas metálicas reflectantes.
* 🔦 [Alan Wake 2 (Remedy Entertainment)](https://www.youtube.com/watch?v=k5lO_68b3cQ): Focos Spot con perfiles IES sobre rostros húmedos con alto contraste de Fresnel.
* ⚙️ [Gears 5 (The Coalition)](https://www.youtube.com/watch?v=J3e2Ea7vJ8Q): Luces de acento para siluetear armaduras metálicas sin sobrecoste de GPU.

---

### 🟢 Diapositiva 08: Desafío en Clase
1. **Misión Shaders**: Crear `M_Master_PBR` con slots para BaseColor, ORM y Normal. Crear 2 instancias (piel mate y metal) y asignarlas al busto.
2. **Misión Iluminación**: Ajustar el sol a 45° (<kbd>Ctrl + L</kbd>), activar Sky Light y añadir una Spot/Rect Light de acento para perfilar el rostro.

---
**Notas relacionadas**:
- [[MOC - Iluminación para Videojuegos]]
- [[Clase 02 - Práctica 3-Point, Luz Solar, Cielo y Movilidad]]
- [[01 - Fundamentos PBR y Mapas de Textura]]
- [[02 - Anatomía del Shader Graph en Unreal (Master Materials e Instances)]]
