---
tags:
  - shaders
  - unreal-engine
  - master-materials
  - material-instances
  - tech-art
date: 2026-08-18
---

# Anatomía del Shader Graph en Unreal: Master Materials e Instances

En la producción profesional de videojuegos, **nunca se crea un Material nuevo desde cero para cada objeto**. En su lugar, se diseña un **Master Material (Material Maestro)** flexible y se crean **Material Instances (Instancias de Material)** para cada prop, personaje o superficie del juego.

---

## 1. El Pipeline Profesional: Master Material vs. Material Instance

```
                  ┌────────────────────────────────────────┐
                  │          MASTER MATERIAL (M_Base)      │
                  │  • Contiene la lógica matemática       │
                  │  • Requiere compilación de shaders     │
                  │  • Define los parámetros editables     │
                  └───────────────────┬────────────────────┘
                                      │
                   Herencia instantánea sin recompilar
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          ▼                           ▼                           ▼
┌──────────────────┐        ┌──────────────────┐        ┌──────────────────┐
│  MI_WoodProp_01  │        │  MI_MetalBox_01  │        │  MI_ConcreteWall │
│ • Textura madera │        │ • Textura metal  │        │ • Textura piedra │
│ • Roughness: 0.8 │        │ • Roughness: 0.2 │        │ • Roughness: 0.9 │
│ • Tiling UV: 1.0 │        │ • Metallic: 1.0  │        │ • Tiling UV: 4.0 │
└──────────────────┘        └──────────────────┘        └──────────────────┘
```

### ¿Por qué este sistema es fundamental?
1. **Iteración en tiempo real**: Cambiar un parámetro en un *Material Instance* se actualiza al instante en la pantalla **sin esperar a que Unreal recompile miles de shaders**.
2. **Optimización de memoria y llamadas de dibujado (Draw Calls)**: Los objetos que comparten el mismo Master Material pueden agruparse de forma más eficiente en GPU.
3. **Escalabilidad**: Si necesitas corregir un bug o añadir una función a todo el juego (por ejemplo, efecto de nieve o lluvia), lo modificas en el Master Material y todos los props se actualizan automáticamente.

---

## 2. Tipos de Parámetros en el Shader Graph

Para convertir un valor fijo en una propiedad configurable dentro de una instancia, se debe convertir en un **Parámetro** (clic derecho sobre el nodo $\rightarrow$ *Convert to Parameter*):

* **Scalar Parameter (Parámetro Escalar)**: Un único número flotante.
  * *Usos*: Multiplicador de rugosidad, intensidad emisiva, escala de UV (Tiling), contraste.
* **Vector Parameter (Parámetro Vectorial / 4 Canales RGBA)**:
  * *Usos*: Tinte de color base, color emisivo, tintes de suciedad.
* **Texture Sample Parameter 2D**:
  * *Usos*: Slots para intercambiar las texturas de *BaseColor*, *NormalMap* y *ORM*.
* **Static Switch Parameter (Interruptor Estático)**:
  * Activa o desactiva ramas completas de código del shader (por ejemplo, habilitar o apagar soporte de detalle o emisión).
  * *Nota técnica*: Genera una permutación de shader diferente al compilar.

---

## 3. Estructura de un Master Material PBR Básico

Un Master Material estándar y limpio suele organizar sus nodos en estos bloques funcionales:

```
[ Texture Coordinate ] ──► [ Multiply: Tiling_UV ] ──► UVs de todas las texturas

[ Texture_BaseColor ] ───► [ Multiply: Tint_Color ] ─────────────► [ BASE COLOR ]

[ Texture_ORM (Canal R) ] ────────────────────────────────────────► [ AMBIENT OCCLUSION ]
[ Texture_ORM (Canal G) ] ──► [ Multiply: Roughness_Scale ] ──────► [ ROUGHNESS ]
[ Texture_ORM (Canal B) ] ──► [ Multiply: Metallic_Scale ] ───────► [ METALLIC ]

[ Texture_Normal ] ───────► [ FlattenNormal: Normal_Strength ] ──► [ NORMAL ]
```

---

## 4. Dynamic Material Instances (MID) en Gameplay

Si necesitas que un material cambie durante la partida mediante código C++ o Blueprints (por ejemplo, un enemigo que se vuelve rojo al recibir daño, un escudo que se disuelve o una barra de vida):

1. En el Blueprint de inicio (`BeginPlay`), se crea una **Dynamic Material Instance**.
2. Durante el juego, se utiliza el nodo **`Set Scalar Parameter Value`** o **`Set Vector Parameter Value`** para animar las propiedades en tiempo real sin coste de compilación.

---
**Notas relacionadas**:
- [[Fundamentos PBR y Mapas de Textura]]
- [[Modelos de Sombreado (Shading Models)]]
- [[Matemáticas de Shaders Esenciales (Fresnel, Lerp y Normales)]]
