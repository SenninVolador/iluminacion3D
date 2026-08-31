---
layout: page
---

<div class="academic-home">
<div class="academic-header">
<h1>Iluminación 3D</h1>
<div class="meta">
<strong>Docente:</strong> Daniel Rojas (UNIACC)
</div>
</div>

<p style="font-size: 14px; line-height: 1.6; color: #374151; margin-bottom: 24px;">
Repositorio académico y base de conocimientos técnicos sobre iluminación digital, sombreadores basados en la física (PBR), optimización de rendimiento en GPU y flujos de trabajo en motores de videojuegos (Unreal Engine).
</p>

<h2 style="font-size: 18px; font-weight: 700; color: #111827; border-bottom: 2px solid #111827; padding-bottom: 6px; margin-bottom: 16px;">
Programa de Clases
</h2>

<div class="class-list" style="display: flex; flex-direction: column; gap: 14px; margin-bottom: 28px;">

<div class="class-item" style="border: 1px solid #d1d5db; border-radius: 4px; padding: 14px 18px; background: #ffffff;">
<div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 4px;">
<h3 style="font-size: 15px; font-weight: 700; margin: 0;"><a href="./clases/clase-01" style="color: #111827; text-decoration: none;">Clase 01: Fundamentos de la Luz, Videojuegos vs. Cine y Shaders</a></h3>
<span style="font-size: 11px; color: #6b7280; font-family: monospace;">Sesión 01</span>
</div>
<p style="font-size: 12.5px; color: #4b5563; margin: 0 0 8px 0; line-height: 1.45;">
Naturaleza del cálculo vectorial de la luz, diferencias entre render en tiempo real y offline (cine), esquema clásico de iluminación de 3 puntos (Key, Fill, Rim) e introducción a los sombreadores PBR.
</p>
<div style="font-size: 11px; color: #111827; font-weight: 600;">
Conceptos: <span style="font-weight: normal; color: #4b5563;">3-Point Lighting · Frametime (16.6 ms) · Albedo · Roughness · Metallic</span>
</div>
</div>

<div class="class-item" style="border: 1px solid #d1d5db; border-radius: 4px; padding: 14px 18px; background: #ffffff;">
<div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 4px;">
<h3 style="font-size: 15px; font-weight: 700; margin: 0;"><a href="./clases/clase-02" style="color: #111827; text-decoration: none;">Clase 02: Taller de 3 Puntos, Sol, Cielo y Movilidad de Luces</a></h3>
<span style="font-size: 11px; color: #6b7280; font-family: monospace;">Sesión 02</span>
</div>
<p style="font-size: 12.5px; color: #4b5563; margin: 0 0 8px 0; line-height: 1.45;">
Taller práctico sobre el busto 3D en Unreal Engine 5, iluminación exterior diurna con Directional Light (Sol) y Sky Light (Cielo), y matriz técnica de movilidad (Static, Stationary, Movable).
</p>
<div style="font-size: 11px; color: #111827; font-weight: 600;">
Conceptos: <span style="font-weight: normal; color: #4b5563;">Directional Light (Ctrl+L) · Sky Light · Lightmaps · Regla de los 4 Canales</span>
</div>
</div>

<div class="class-item" style="border: 1px solid #d1d5db; border-radius: 4px; padding: 14px 18px; background: #ffffff;">
<div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 4px;">
<h3 style="font-size: 15px; font-weight: 700; margin: 0;"><a href="./clases/clase-03" style="color: #111827; text-decoration: none;">Clase 03: Shaders PBR en el Busto, Sol y Fuentes Locales</a></h3>
<span style="font-size: 11px; color: #6b7280; font-family: monospace;">Sesión 03</span>
</div>
<p style="font-size: 12.5px; color: #4b5563; margin: 0 0 8px 0; line-height: 1.45;">
Creación del Master Material PBR y texturas empaquetadas (ORM), respuesta física del busto bajo el sol y cielo, y uso de fuentes locales (Point, Spot, Rect) para acentos y brillo en la mirada.
</p>
<div style="font-size: 11px; color: #111827; font-weight: 600;">
Conceptos: <span style="font-weight: normal; color: #4b5563;">Master Materials · Canales ORM · Normal Map · Radio de Atenuación · Rembrandt</span>
</div>
</div>

<div class="class-item" style="border: 1px solid #d1d5db; border-radius: 4px; padding: 14px 18px; background: #ffffff;">
<div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 4px;">
<h3 style="font-size: 15px; font-weight: 700; margin: 0;"><a href="./clases/clase-04" style="color: #111827; text-decoration: none;">Clase 04: Shaders Nodales, Atmósfera y Niebla Volumétrica</a></h3>
<span style="font-size: 11px; color: #6b7280; font-family: monospace;">Sesión 04</span>
</div>
<p style="font-size: 12.5px; color: #4b5563; margin: 0 0 8px 0; line-height: 1.45;">
Taller de corrección y calificación de la Entrega N°1, arquitectura universal de shaders nodales (Utah Teapot), y componentes de atmósfera, cielo y niebla volumétrica (God Rays).
</p>
<div style="font-size: 11px; color: #111827; font-weight: 600;">
Conceptos: <span style="font-weight: normal; color: #4b5563;">Sistemas Nodales · Multiply Tint · SkyAtmosphere · Niebla Volumétrica por Vóxeles · God Rays</span>
</div>
</div>

</div>

<div class="academic-nav-grid">
<div class="academic-card">
<h3><a href="./glosario">Glosario Interactivo</a></h3>
<p>Definiciones de términos explicados con simuladores 3D interactivos en tiempo real (Temperatura Kelvin, Normal Maps, Atenuación, 3 Puntos, Sol y Sombras).</p>
</div>

<div class="academic-card">
<h3><a href="./shaders/01-fundamentos-pbr">Módulo: Shaders y Materiales</a></h3>
<p>Guía técnica sobre modelos de sombreado (Default Lit, SSS, Foliage), matemáticas de shaders (Fresnel, Lerp) y mapas de textura.</p>
</div>

<div class="academic-card">
<h3><a href="./recursos/material-visual">Documentación Técnica (PDF)</a></h3>
<p>Fichas técnicas descargables en formato A4 de 2 páginas con diagramas vectoriales y análisis de videojuegos de la industria.</p>
</div>

<div class="academic-card">
<h3><a href="./clases/lenguaje-visual">Guía Visual al Jugador</a></h3>
<p>Técnicas de composición e iluminación para guiar la atención del jugador y construir jerarquía visual en niveles 3D.</p>
</div>
</div>

<div style="margin-top: 36px; border-top: 1px solid #e5e7eb; padding-top: 24px;">
<h2 style="font-size: 16px; font-weight: 700; color: #111827; margin-bottom: 8px;">
Laboratorio Interactivo: Reflectancia y Rugosidad PBR
</h2>
<p style="font-size: 12.5px; color: #6b7280; margin-bottom: 14px;">
Simulación en tiempo real de la ecuación de microfacetas sobre geometría tridimensional:
</p>

<ClientOnly>
  <RoughnessViewer />
</ClientOnly>
</div>
</div>
