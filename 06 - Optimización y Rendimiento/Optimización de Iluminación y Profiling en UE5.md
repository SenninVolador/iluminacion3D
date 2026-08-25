---
tags:
  - unreal-engine
  - tech-art
  - optimizacion
  - profiling
date: 2026-08-18
---

# ⚡ Optimización de Iluminación y Profiling en UE5

En el desarrollo de videojuegos, la iluminación suele ser uno de los mayores consumidores de tiempo de GPU. Como Lighting Artist o Technical Artist, es fundamental medir, diagnosticar y optimizar el coste de cada luz.

---

## ⏱️ 1. Comandos de Consola y Herramientas de Medición

Para diagnosticar el rendimiento en tiempo real dentro del editor o durante la ejecución:

| Comando / Atajo | ¿Qué mide? | Objetivo |
| :--- | :--- | :--- |
| `stat fps` | Fotogramas por segundo y Frametime total | Mantener $\le 16.6\text{ ms}$ (60 FPS) o $\le 33.3\text{ ms}$ (30 FPS) |
| `stat gpu` | Desglose en milisegundos de cada pase de render en GPU (Lumen, Lights, Shadows, PostProcess) | Identificar si el cuello de botella es sombras o GI |
| `Ctrl + Shift + ,` | **GPU Visualizer**: Captura exacta de un fotograma con gráfico en árbol de milisegundos | Encontrar el actor de luz o pase exacto que más consume |
| `stat scenerendering` | Número de Draw Calls, Luces visibles, Mallas renderizadas | < 2000-3000 Draw Calls en consola/PC |

---

## 🎯 2. Los 4 Grandes Consumidores de Rendimiento en Iluminación

### A. Sombras Dinámicas (Shadow Casting)
Proyectar sombras dinámicas requiere renderizar la geometría de la escena desde el punto de vista de la luz hacia un mapa de sombras (*Shadow Map Pass*).
* **Optimización**:
  * Desactiva `Cast Shadows` en luces decorativas de relleno o fuentes de luz pequeñas.
  * Ajusta `Attenuation Radius`: Cuanto más grande sea la esfera de la luz, más objetos intersecan y más mallas deben dibujarse en el pase de sombras.
  * Si usas **Virtual Shadow Maps (VSM)** en UE5, asegúrate de que los objetos lejanos utilicen LODs o Nanite correctamente para que no colapsen la memoria caché de páginas de sombra.

### B. Solapamiento de Luces (Light Overlap / Light Complexity)
* Presiona `Alt + 8` en el viewport para activar la vista **Light Complexity**:
  * 🟩 **Verde**: 1-2 luces solapadas (Excelente).
  * 🟧 **Naranja**: 3-4 luces solapadas (Aceptable).
  * 🟥 **Rojo / Blanco**: 5+ luces solapadas en el mismo píxel (Sobrecoste severo / Shader Overdraw).

### C. Niebla Volumétrica Excesiva
* La niebla volumétrica renderiza sobre una cuadrícula 3D.
* **Optimización**: Desactiva `Cast Volumetric Shadow` en luces secundarias y usa `Volumetric Scattering Intensity = 0` en luces donde el haz visible no aporte valor narrativo.

### D. Lumen y Reflejos
* Ajusta la calidad de Lumen en el **PostProcessVolume**:
  * `Lumen Scene Lighting Quality` (1.0 por defecto; reducir a 0.5 o 0.75 en plataformas de menor potencia).
  * `Max Trace Distance`: Reduce la distancia máxima que los rayos viajan en exteriores para liberar tiempo de GPU.

---

## 📋 Checklist de Optimización para Escenas

- [ ] ¿Todas las luces que no necesitan proyectar sombras tienen `Cast Shadows = False`?
- [ ] ¿Los radios de atenuación (`Attenuation Radius`) están ajustados al mínimo necesario sin invadir habitaciones contiguas?
- [ ] ¿Has verificado la vista `Alt + 8` (Light Complexity) para evitar zonas en blanco/rojo puro?
- [ ] ¿Las luces estáticas o lejanas usan baking o tienen distancias de apagado (*Max Draw Distance*) configuradas?
- [ ] ¿Has medido con `Ctrl + Shift + ,` que el pase `Lights` o `ShadowDepths` esté dentro de tu budget (generalmente $\le 4-6\text{ ms}$ en total)?

---
**Notas relacionadas**:
- [[Movilidad de Luces (Static, Stationary, Movable)]]
- [[Tipos de Luces en Unreal Engine]]
- [[Lumen vs Baked Lighting (UE5)]]
