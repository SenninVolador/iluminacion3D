---
tags:
  - iluminacion3d
  - level-design
  - composicion
  - game-art
date: 2026-08-18
---

# 👁️ Lenguaje Visual y Guía al Jugador (Player Guidance)

En el diseño de niveles y arte de videojuegos, la luz no solo sirve para que el escenario sea visible; es la herramienta psicológica y visual más potente para **guiar al jugador de forma intuitiva sin necesidad de interfaces intrusivas (diegetic guidance)**.

---

## 🧭 1. El Ojo Humano y el Principio de Atracción Lumínica

El ojo humano en cualquier encuadre o videojuego siempre busca automáticamente:
1. **El punto de mayor contraste de luminancia** (zona más brillante rodeada de sombra).
2. **El punto de mayor saturación de color** (un foco cálido en un entorno frío).
3. **Líneas de fuga de luz y sombras (Leading Lines)** (haces de luz que apuntan hacia una puerta o escalera).

---

## 🛠️ 2. Técnicas Fundamentales de Guía Visual

### A. El "Efecto Polilla" (Puntos Focales de Salida)
* Ilumina las puertas, pasillos clave o puntos de interés (*Points of Interest - POI*) con una intensidad notablemente superior al resto de la habitación.
* Si el jugador entra a una habitación oscura, correrá instintivamente hacia la fuente de luz.

### B. Contraste de Siluetas (Value Contrast)
* Coloca una fuente de luz brillante justo **detrás** de un objetivo, enemigo o puerta importante.
* Esto genera una **silueta nítida y reconocible** (*Backlighting* o contraluz), facilitando la legibilidad instantánea en mitad de un combate o exploración.

### C. Código de Color y Semiótica (Color Temperature & Meaning)
* **Cálido vs. Frío (Teal & Orange)**:
  * Entorno general en tonos fríos/azules (sensación de peligro, soledad, misterio).
  * Zonas seguras o interactivas (hogueras, palancas, terminales, refugios) en tonos cálidos/ámbar.
* **Luz de Alerta / Peligro**: Rojos y amarillos intermitentes para dirigir la atención hacia amenazas o accesos bloqueados.

### D. Enmarcado por Sombras (Framing)
* Proyecta sombras oscuras en las esquinas y bordes de la pantalla (o usa viñeteado) para "encerrar" la acción principal en el centro del tercio de interés.
* Sombras arquitectónicas (arcos, rejas, vigas) que dibujan un camino natural sobre el suelo.

---

## 🎭 3. Las Tres Funciones de la Iluminación en Juegos

```
           ┌─────────────────────────────────────────┐
           │      FUNCIONES DE LA ILUMINACIÓN        │
           ├────────────────────┬────────────────────┤
           │                    │                    │
     1. READABILITY       2. MOOD & DRAMA      3. NAVIGATION
     (Jugabilidad clara,   (Atmósfera, miedo,   (Dónde ir, qué
     siluetas de combate)  belleza, inmersión)  es interactivo)
```

1. **Readability (Legibilidad)**: El jugador debe entender qué es suelo transitable, qué es obstáculo y dónde están los enemigos.
2. **Mood & Storytelling (Narrativa ambiental)**: Contar historias a través de la luz (un foco roto parpadeando en un hospital abandonado, rayos de sol filtrándose en ruinas antiguas).
3. **Navigation & Affordance (Navegación)**: Resolver el flujo del nivel (*flow*) sin que el jugador se sienta perdido.

---
**Notas relacionadas**:
- [[MOC - Iluminación para Videojuegos]]
- [[Tipos de Luces en Unreal Engine]]
- [[Exposición, Color Grading y ACES en UE5]]
