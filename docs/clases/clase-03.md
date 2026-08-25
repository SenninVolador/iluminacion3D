# Clase 03: Shaders PBR en el Busto, Sol, Cielo y Fuentes Locales

Cátedra de Iluminación 3D y Shaders para Videojuegos · Docente Daniel Rojas (UNIACC)

---

## 1. Respuesta de Superficie PBR e Instanciación Modular

El sombreado basado en la física modela la microestructura del material mediante rugosidad y metalicidad:

<ClientOnly>
  <RoughnessViewer />
</ClientOnly>

### Empaquetado de Canales de Textura (ORM):
A fin de optimizar el ancho de banda de memoria de video (VRAM), se combinan tres mapas escalares de 8 bits en una única textura de tres canales RGB:
* **Canal R (Rojo)**: Ambient Occlusion (Oclusión Ambiental).
* **Canal G (Verde)**: Roughness (Rugosidad / Distribución de microfacetas).
* **Canal B (Azul)**: Metallic (Comportamiento metálico vs. dieléctrico).

### Arquitectura de Shaders en Unreal Engine 5:
* **Master Material (`M_Master_PBR`)**: Contiene las ecuaciones matemáticas y slots de muestreo de texturas. Se compila una sola vez en el proyecto.
* **Material Instances (`MI_Busto`)**: Permiten vestir el busto con distintas respuestas ópticas (piel mate, metal pulido, cerámica) en tiempo real sin tiempos de compilación.

<ClientOnly>
  <NormalMapViewer />
</ClientOnly>

---

## 2. Interacción del Busto bajo Fuentes Naturales (Sol y Cielo)

1. **Directional Light (Sol)**:
   * Al rotar el emisor con `Ctrl + L`, la incidencia rasante revela la microgeometría almacenada en el **Normal Map** del busto.
   * Se busca el esquema clásico de retrato **Rembrandt** (incidencia a $45^\circ$ lateral) para formar el triángulo luminoso característico en la mejilla opuesta.
2. **Sky Light (Bóveda Celeste)**:
   * Proyecta luz ambiental difusa sobre las áreas en sombra, respetando la información del canal R (AO) del shader para preservar la profundidad en cavidades faciales.

---

## 3. Fuentes Lumínicas Locales de Apoyo

| Tipo de Emisor | Geometría de Emisión | Función en el Sujeto | Parámetro Crítico |
| :--- | :--- | :--- | :--- |
| **Point Light** | Esfera omnidireccional ($360^\circ$) | Simulación de fuentes próximas (velas, antorchas) | `Attenuation Radius` |
| **Spot Light** | Cono direccional acotado | Luz de acento y brillo corneal (*Eye Catchlight*) | `Inner/Outer Cone`, `IES` |
| **Rect Light** | Plano rectangular (área) | Luz difusa de estudio para reflejos suaves | `Source Width / Height` |

<ClientOnly>
  <AttenuationViewer />
</ClientOnly>

---

## 4. Análisis de Casos en la Industria

* **God of War Ragnarök (Santa Monica Studio)**: Modelado de shaders faciales en Kratos con modulación de rugosidad para sudor, nieve y sangre bajo luz solar y antorchas.
* **Horizon Forbidden West (Guerrilla Games)**: Integración de piel mate y piezas de aleación reflectante bajo condiciones de iluminación diurna abierta.
* **Alan Wake 2 (Remedy Entertainment)**: Emisores Spot con perfiles fotométricos IES reales sobre superficies húmedas con respuesta de Fresnel pronunciada.
* **Gears 5 (The Coalition)**: Optimización estricta de radios de atenuación en fuentes locales para preservar el presupuesto de fotograma en combate cerrado.
