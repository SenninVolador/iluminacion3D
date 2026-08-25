---
layout: page
---

<div class="academic-home">
  <div class="academic-header">
    <h1>Iluminación 3D y Shaders para Videojuegos</h1>
    <div class="meta">
      <strong>Cátedra:</strong> Arte Técnico y Renderizado en Tiempo Real · <strong>Docente:</strong> Daniel Rojas (UNIACC)
    </div>
  </div>

  <p style="font-size: 14px; line-height: 1.6; color: #374151; margin-bottom: 24px;">
    Repositorio académico y base de conocimientos técnicos sobre iluminación digital, sombreadores basados en la física (PBR), optimización de rendimiento en GPU y flujos de trabajo en motores de videojuegos (Unreal Engine).
  </p>

  <div class="academic-nav-grid">
    <div class="academic-card">
      <h3><a href="/clases/clase-01">Unidad 1: Iluminación y Composición</a></h3>
      <p>Fundamentos ópticos, esquemas clásicos de 3 puntos, iluminación solar y de cielo, fuentes locales (Point, Spot, Rect) y movilidad técnica (Static, Stationary, Movable).</p>
    </div>

    <div class="academic-card">
      <h3><a href="/shaders/01-fundamentos-pbr">Unidad 2: Shaders y Materiales PBR</a></h3>
      <p>Conservación de la energía, mapas empaquetados ORM, arquitectura de Master Materials, modelos de sombreado y álgebra vectorial de shaders.</p>
    </div>

    <div class="academic-card">
      <h3><a href="/glosario">Glosario Técnico</a></h3>
      <p>Definiciones conceptuales y técnicas ordenadas cronológicamente clase a clase para consulta rápida durante el semestre.</p>
    </div>

    <div class="academic-card">
      <h3><a href="/recursos/material-visual">Fichas Técnicas (PDF)</a></h3>
      <p>Documentación maquetada en dos páginas por sesión con diagramas vectoriales, matrices de decisión y referencias de la industria.</p>
    </div>
  </div>

  <div style="margin-top: 36px; border-top: 1px solid #e5e7eb; padding-top: 24px;">
    <h2 style="font-size: 16px; font-weight: 700; color: #111827; margin-bottom: 8px;">
      Laboratorio Interactivo: Reflectancia y Rugosidad PBR
    </h2>
    <p style="font-size: 12.5px; color: #6b7280; margin-bottom: 14px;">
      Simulación en tiempo real de la ecuación de microfacetas sobre geometría tridimensional:
    </p>

    <RoughnessViewer />
  </div>
</div>
