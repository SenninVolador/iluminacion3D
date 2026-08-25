---
tags:
  - clase
  - clase03
  - shaders
  - master-materials
  - pbr
  - busto3d
  - directional-light
  - sky-light
  - unreal-engine
date: 2026-08-25
---

# 🎓 Clase 03: Shaders PBR en el Busto, Master Materials, Sol, Cielo y Luces Locales

En esta sesión continuamos directamente con el **busto 3D de la Clase 02**: construimos su primer **Master Material PBR** con texturas empaquetadas (ORM), y estudiamos cómo reaccionan sus propiedades físicas al combinarse con **Directional Light (Sol)**, **Sky Light (Cielo)** y luces de acento local (**Point, Spot y Rect Lights**).

---

## 🧱 Bloque 1: Master Material PBR y Texturas ORM para el Busto

En lugar de usar materiales planos, creamos una arquitectura profesional en Unreal Engine 5 para vestir nuestro modelo:

```
                          MAPA DE TEXTURA EMPAQUETADO (ORM)
                         ┌─────────────────────────────────┐
                         │ Canal R ──► Ambient Occlusion   │
                         │ Canal G ──► Roughness (Rugosidad│
                         │ Canal B ──► Metallic (Metalicidad│
                         └─────────────────────────────────┘
```

### Arquitectura de `M_Master_PBR` en el Shader Graph:
* **TexCoord $\times$ Scalar (`Tiling_UV`)**: Control de repetición y escala.
* **Texture Sample (`BaseColor`) $\times$ Vector (`Color_Tint`)** $\rightarrow$ *Base Color*.
* **Texture Sample (`ORM`)**:
  * Pin R $\rightarrow$ *Ambient Occlusion*.
  * Pin G $\times$ Scalar (`Roughness_Multi`) $\rightarrow$ *Roughness*.
  * Pin B $\times$ Scalar (`Metallic_Multi`) $\rightarrow$ *Metallic*.
* **Texture Sample (`Normal`) $\rightarrow$ `FlattenNormal (Strength)`** $\rightarrow$ *Normal*.

### Variación en el Busto mediante Instancias (`Material Instances`):
* `MI_Busto_PielOruga`: Roughness alto ($0.75$), Metallic ($0.0$).
* `MI_Busto_Cromo`: Roughness bajo ($0.1$), Metallic ($1.0$).
* `MI_Busto_EstatuaOro`: Roughness medio ($0.35$), Metallic ($1.0$), Tinte dorado.

---

## ☀️ Bloque 2: El Busto bajo Luz Exterior (Directional + Sky Light)

Colocamos el busto en un entorno abierto para analizar la interacción física de la luz natural con el shader:

```
                ☀️ [ DIRECTIONAL LIGHT ] (Sol)
                Rayos paralelos: genera sombra dura y brillo especular principal
                           │
                           │   ┌───────────────────────────┐
                           │   │  🌌 [ SKY LIGHT ] (Cielo) │
                           │   │  Relleno hemisférico azul │
                           ▼   └─────────────┬─────────────┘
                     ╔═══════════════╗       │
                     ║   BUSTO 3D    ║◄──────┘
                     ╚═══════════════╝
```

1. **Directional Light (Sol)**:
   * Define el contraste dominante. Al rotar el sol con <kbd>Ctrl + L</kbd>, el *Normal Map* del busto revela las arrugas, poros y relieves según el ángulo rasante.
2. **Sky Light (Atmósfera y Cielo)**:
   * Ilumina las zonas en penumbra del rostro del busto con la tonalidad del cielo, impidiendo que el lado opuesto al sol quede en negro carbón.

---

## 💡 Bloque 3: Luces Locales de Acento (Point, Spot y Rect Lights)

Para complementar la luz solar y destacar detalles escultóricos en el busto, sumamos luces locales:

```
┌───────────────┬───────────────────────────────┬────────────────────────────────────────┐
│ TIPO DE LUZ   │ GEOMETRÍA DE EMISIÓN          │ APLICACIÓN EN EL BUSTO                 │
├───────────────┼───────────────────────────────┼────────────────────────────────────────┤
│ 💡 Point Light│ Esfera omnidireccional de 360°│ Luz de antorcha o chispa cercana.      │
│ 🔦 Spot Light │ Cono direccional acotado      │ Foco de acento, recorte o linterna.    │
│ 🔲 Rect Light │ Superficie plana (semiesfera) │ Luz de estudio fotográfico suave.      │
└───────────────┴───────────────────────────────┴────────────────────────────────────────┘
```

* **Attenuation Radius**: Mantener la esfera de influencia ceñida alrededor del busto para optimizar GPU.
* **Source Radius**: Aumentar el tamaño físico del emisor para que los brillos en los ojos y frentes sean suaves y no un punto pixelado.

---

## 🎮 Bloque 4: Casos de Estudio en la Industria

* 🪓 **[God of War Ragnarök (Santa Monica Studio)](https://www.artstation.com/artwork/g8GZ8K)**: Shaders maestros en el busto y rostro de Kratos, adaptando el roughness según sudor, nieve o sangre bajo luz solar y antorchas.
* 🤖 **[Horizon Forbidden West (Guerrilla Games)](https://www.guerrilla-games.com/read/the-technology-of-horizon-forbidden-west)**: Respuesta del sol y luz de cielo sobre la piel de Aloy y las piezas metálicas reflectantes.
* 🔦 **[Alan Wake 2 (Remedy Entertainment)](https://www.youtube.com/watch?v=k5lO_68b3cQ)**: Interacción de focos Spot con perfiles IES sobre personajes con piel y ropa húmeda.
* ⚙️ **[Gears 5 (The Coalition)](https://www.youtube.com/watch?v=J3e2Ea7vJ8Q)**: Optimización de sombras dinámicas sobre personajes y armaduras metálicas bajo luz direccional y puntual.

---

## 🛠️ Taller Práctico para la Clase

1. **Abrir la escena del busto 3D** de la Clase 02.
2. **Crear el Master Material `M_Master_PBR`** con parámetros de *Tiling*, *Tint*, *Roughness* y *Metallic*.
3. **Crear 2 instancias** (una metálica pulida y otra mate no-metálica) y asignarlas al busto.
4. **Configurar el Sol y Cielo**: Ajustar la hora con <kbd>Ctrl + L</kbd> y evaluar cómo el mapa de normales responde a la luz rasante.
5. **Añadir una Spot Light o Rect Light** como luz de acento de estudio para perfilar el rostro.

---
**Notas relacionadas**:
- [[MOC - Iluminación para Videojuegos]]
- [[Clase 02 - Práctica 3-Point, Luz Solar, Cielo y Movilidad]]
- [[01 - Fundamentos PBR y Mapas de Textura]]
- [[02 - Anatomía del Shader Graph en Unreal (Master Materials e Instances)]]
- [[Tipos de Luces en Unreal Engine]]
