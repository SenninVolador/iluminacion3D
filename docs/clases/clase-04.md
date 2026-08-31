# Clase 04: Taller de Entrega N°1, Shaders Nodales y Atmósfera Volumétrica

Iluminación 3D · Docente Daniel Rojas (UNIACC)

---

## 1. Bloque 1: Taller de Calificación y Shaders Nodales Universales

La primera parte de la sesión está dedicada al apoyo individual de los estudiantes para pulir la **Entrega N°1 (Estudio de 3 Puntos y Shader Paramétrico)**, la cual se entrega y califica al cierre de la clase mediante la [Rúbrica Oficial de Evaluación](./rubrica-entrega-01).

### Simulador Interactivo: Shader Nodal Paramétrico (Utah Teapot)
Prueba a modificar el tinte de color mediante la operación *Multiply*, la rugosidad, la metalicidad y la fuerza de normales sobre la icónica tetera de Utah:

<ClientOnly>
  <NodeShaderViewer />
</ClientOnly>

### Universalidad de los Sistemas Nodales
Los editores de materiales basados en grafos nodales operan bajo la misma lógica matemática en todos los motores y paquetes 3D de la industria:

* **Unreal Engine**: Material Graph (`Master Material` ──► `Material Instance`).
* **Unity**: Shader Graph (`PBR Master` / `Lit`).
* **Blender**: Shader Editor (`Principled BSDF`).
* **Autodesk Maya**: Hypershade (`Standard Surface`).
* **Godot Engine**: VisualShader.

```
[ Texture Sample: Albedo ] ──┐
                             ├──► [ MULTIPLY ] ──► Base Color (Master Node)
[ Vector Parameter: Tint ] ──┘

[ Scalar Parameter: Roughness ]  ────────────────► Roughness (Master Node)
[ Scalar Parameter: Metallic ]   ────────────────► Metallic (Master Node)

[ Texture Sample: Normal Map ] ──► [ FlattenNormal / Multiply ] ──► Normal
```

---

## 2. Bloque 2: Atmósfera, Cielo y Niebla Volumétrica

Para construir ambientación espacial, perspectiva aérea y **mood (atmósfera narrativa)**, combinamos emisores de luz con componentes de dispersión atmosférica.

### Simulador Interactivo: Niebla Volumétrica y Rayos de Luz (God Rays)
Ajusta la densidad de la niebla, la altura y la hora atmosférica para observar cómo la luz genera rayos crepusculares volumétricos:

<ClientOnly>
  <VolumetricFogViewer />
</ClientOnly>

### Nombres de Componentes: Unreal Engine vs. Términos Genéricos de la Industria

| Unreal Engine 5 | Nombre Genérico en la Industria | Función Técnica |
| :--- | :--- | :--- |
| **Directional Light** | *Sun Light / Infinite Light* | Emisor a distancia infinita con rayos 100% paralelos. |
| **SkyAtmosphere** | *Physical Sky / Atmospheric Scattering* | Dispersión física de luz en gases atmosféricos (Rayleigh y Mie). |
| **Sky Light** | *Ambient Probe / Environment Dome* | Luz difusa envolvente de 360° para bañar las sombras. |
| **Exponential Height Fog** | *Height Fog / Distance Fog* | Niebla analítica por altura y distancia para perspectiva aérea. |
| **Volumetric Fog** | *Media Scatter / Voxel Fog* | Niebla resuelta en grilla 3D de vóxeles que crea **God Rays**. |
| **Volumetric Clouds** | *Procedural Cloud Layer* | Capa de nubes 3D volumétricas con auto-sombreado. |

---

## 3. Principios Ópticos: Dispersión de Rayleigh y Mie

1. **Dispersión de Rayleigh (Moléculas de gas)**:
   * Las partículas gaseosas microscópicas dispersan las longitudes de onda cortas (azul/violeta).
   * Genera el tono azul del cielo diurno y los tonos rojizos/anaranjados del atardecer.
2. **Dispersión de Mie (Polvo, humedad y aerosoles)**:
   * Partículas más grandes generan la bruma del horizonte y el halo brillante alrededor del sol.
3. **Anisotropía de Dispersión ($g$)**:
   * Controla hacia dónde rebota la luz al chocar con la niebla. Valores entre $0.7$ y $0.9$ producen rayos crepusculares marcados (*God Rays*) cuando la cámara mira hacia la fuente luminosa.
