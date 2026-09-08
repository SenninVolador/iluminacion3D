---
layout: doc
---

# Iluminación 3D

Docente: Daniel Rojas (UNIACC)

Plataforma técnica de la asignatura de **Iluminación 3D y Shaders para Videojuegos**. Recursos de cátedra, fundamentación física PBR, laboratorios de iluminación en Unreal Engine 5 y simuladores interactivos en tiempo real.

---

## Programa de Clases y Sesiones Prácticas

<div style="display: flex; flex-direction: column; gap: 14px; margin-bottom: 28px;">

<div class="class-item" style="border: 1px solid #d1d5db; border-radius: 4px; padding: 14px 18px; background: #ffffff;">
<div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 4px;">
<h3 style="font-size: 15px; font-weight: 700; margin: 0;"><a href="/iluminacion3D/clases/clase-01" style="color: #111827; text-decoration: none;">Clase 01: Fundamentos de la Luz y Esquema de 3 Puntos</a></h3>
<span style="font-size: 11px; color: #6b7280; font-family: monospace;">Sesión 01</span>
</div>
<p style="font-size: 12.5px; color: #4b5563; margin: 0 0 8px 0; line-height: 1.45;">
Introducción a la luz digital en tiempo real vs. cine, tiempo de fotograma (frametime), el esquema de 3 puntos (Key, Fill, Rim) y concepto fundamental de Shaders PBR.
</p>
<div style="font-size: 11px; color: #111827; font-weight: 600;">
Conceptos: <span style="font-weight: normal; color: #4b5563;">Frametime · 3-Point Lighting · Key Light · Fill Light · Rim Light · PBR</span>
</div>
</div>

<div class="class-item" style="border: 1px solid #d1d5db; border-radius: 4px; padding: 14px 18px; background: #ffffff;">
<div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 4px;">
<h3 style="font-size: 15px; font-weight: 700; margin: 0;"><a href="/iluminacion3D/clases/clase-02" style="color: #111827; text-decoration: none;">Clase 02: Taller de 3 Puntos, Luz Solar, Cielo y Movilidad</a></h3>
<span style="font-size: 11px; color: #6b7280; font-family: monospace;">Sesión 02</span>
</div>
<p style="font-size: 12.5px; color: #4b5563; margin: 0 0 8px 0; line-height: 1.45;">
Práctica de iluminación sobre el busto 3D en Unreal Engine 5. Luz solar directa (Directional Light), cielo envolvente (Sky Light), temperatura Kelvin y movilidad técnica (Static, Stationary, Movable).
</p>
<div style="font-size: 11px; color: #111827; font-weight: 600;">
Conceptos: <span style="font-weight: normal; color: #4b5563;">Directional Light · Sky Light · Grados Kelvin · Movilidad Técnica · Regla de los 4 Canales</span>
</div>
</div>

<div class="class-item" style="border: 1px solid #d1d5db; border-radius: 4px; padding: 14px 18px; background: #ffffff;">
<div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 4px;">
<h3 style="font-size: 15px; font-weight: 700; margin: 0;"><a href="/iluminacion3D/clases/clase-03" style="color: #111827; text-decoration: none;">Clase 03: Shaders PBR en el Busto, Sol y Fuentes Locales</a></h3>
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
<h3 style="font-size: 15px; font-weight: 700; margin: 0;"><a href="/iluminacion3D/clases/clase-04" style="color: #111827; text-decoration: none;">Clase 04: Shaders Nodales, Atmósfera y Niebla Volumétrica</a></h3>
<span style="font-size: 11px; color: #6b7280; font-family: monospace;">Sesión 04</span>
</div>
<p style="font-size: 12.5px; color: #4b5563; margin: 0 0 8px 0; line-height: 1.45;">
Taller de corrección y calificación de la Entrega N°1, arquitectura universal de shaders nodales (Utah Teapot), y componentes de atmósfera, cielo y niebla volumétrica (God Rays).
</p>
<div style="font-size: 11px; color: #111827; font-weight: 600;">
Conceptos: <span style="font-weight: normal; color: #4b5563;">Sistemas Nodales · Multiply Tint · SkyAtmosphere · Niebla Volumétrica por Vóxeles · God Rays</span>
</div>
</div>

<div class="class-item" style="border: 1px solid #d1d5db; border-radius: 4px; padding: 14px 18px; background: #ffffff;">
<div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 4px;">
<h3 style="font-size: 15px; font-weight: 700; margin: 0;"><a href="/iluminacion3D/clases/clase-05" style="color: #111827; text-decoration: none;">Clase 05: Iluminación de Interiores, Metodología Brejon y Nomenclatura</a></h3>
<span style="font-size: 11px; color: #6b7280; font-family: monospace;">Sesión 05</span>
</div>
<p style="font-size: 12.5px; color: #4b5563; margin: 0 0 8px 0; line-height: 1.45;">
Iluminación de una escena interior simple: taxonomía de Chris Brejon (Natural, Practical y Dramatic Lights), fuentes locales (Rect, Point, Spot), contraste térmico Kelvin y nomenclatura oficial de Epic Games.
</p>
<div style="font-size: 11px; color: #111827; font-weight: 600;">
Conceptos: <span style="font-weight: normal; color: #4b5563;">Metodología Brejon · Rect Light · Source Radius · Contraste Frío/Cálido · Nomenclatura Epic Games</span>
</div>
</div>

</div>

<div class="academic-nav-grid">
<div class="academic-card">
<h3><a href="/iluminacion3D/glosario">Glosario Interactivo</a></h3>
<p>Definiciones de términos explicados con simuladores 3D interactivos en tiempo real (Temperatura Kelvin, Normal Maps, Atenuación, 3 Puntos, Sol y Sombras).</p>
</div>

<div class="academic-card">
<h3><a href="/iluminacion3D/shaders/01-fundamentos-pbr">Módulo: Shaders y Materiales</a></h3>
<p>Guía técnica sobre modelos de sombreado (Default Lit, SSS, Foliage), matemáticas de shaders (Fresnel, Lerp) y mapas de textura.</p>
</div>

<div class="academic-card">
<h3><a href="/iluminacion3D/recursos/videos">Videos Tutoriales de Apoyo</a></h3>
<p>Serie de cápsulas audiovisuales cortas (máximo 10 min) para repasar ejercicios prácticos en Unreal Engine 5 desde cero hasta la Clase 04.</p>
</div>

<div class="academic-card">
<h3><a href="/iluminacion3D/recursos/shortcuts">Atajos de Teclado y Nodos</a></h3>
<p>Guía rápida de combinaciones de teclas para el Viewport, pilotaje de luces y creación de nodos con 1 click en el Material Editor.</p>
</div>

<div class="academic-card">
<h3><a href="/iluminacion3D/recursos/material-visual">Documentación Técnica (PDF)</a></h3>
<p>Fichas técnicas descargables en formato A4 de 2 páginas con diagramas vectoriales y análisis de videojuegos de la industria.</p>
</div>

<div class="academic-card">
<h3><a href="/iluminacion3D/clases/lenguaje-visual">Guía Visual al Jugador</a></h3>
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
