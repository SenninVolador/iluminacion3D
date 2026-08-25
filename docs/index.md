---
layout: home

hero:
  name: "Iluminación 3D & Shaders"
  text: "Portal Académico de Videojuegos"
  tagline: "Fundamentos ópticos, pipelines PBR, Unreal Engine 5 y simuladores interactivos en tiempo real."
  actions:
    - theme: brand
      text: "Explorar Clases"
      link: /clases/clase-01
    - theme: alt
      text: "📖 Glosario Clase a Clase"
      link: /glosario
    - theme: alt
      text: "📄 Fichas Técnicas (PDF)"
      link: /recursos/material-visual

features:
  - icon: 💡
    title: "Iluminación en Tiempo Real"
    details: "Esquema de 3 puntos, Directional Light (Sol), Sky Light ambiental, luces locales y movilidad (Static, Stationary, Movable)."
  - icon: 🧱
    title: "Shaders PBR & Master Materials"
    details: "Conservación de energía, mapas ORM empaquetados, instancias en vivo y matemáticas de shaders (Fresnel, Lerp, Normales)."
  - icon: 🎮
    title: "Casos Reales de la Industria"
    details: "Análisis de decisiones técnicas en The Last of Us, Cyberpunk 2077, Zelda: TotK, God of War Ragnarök y Alan Wake 2."
---

<div style="margin-top: 40px;">
  <h2 style="font-size: 20px; font-weight: 800; text-align: center; margin-bottom: 8px;">
    🕹️ Simulador de Shaders PBR en Tiempo Real
  </h2>
  <p style="text-align: center; color: var(--vp-c-text-2); font-size: 13px; margin-bottom: 16px;">
    Prueba cómo reacciona el material 3D en tu navegador ajustando la rugosidad y metalicidad:
  </p>

  <RoughnessViewer />
</div>
