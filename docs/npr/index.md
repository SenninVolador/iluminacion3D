# NPR, Geometría de Normales y Vertex Color

**Unidad Técnica Especial — Sombreado No-Fotorrealista (NPR) y Arte Técnico para Videojuegos**  
**Docente:** Daniel Rojas · **Estándar de Producción:** Unity 6 (URP — Universal Render Pipeline) & Unreal Engine 5

---

## 1. De la Física PBR a la Estilización NPR: La Ecuación del Producto Punto

Tanto un motor hiperrealista (como *The Last of Us* o *Alan Wake 2*) como un juego de estética anime o cómic (*Guilty Gear Strive*, *Genshin Impact*, *Zenless Zone Zero*, *Hi-Fi Rush*, *Zelda: Breath of the Wild*) parten exactamente de la misma operación matemática para saber cuánta luz recibe un punto de un modelo: el **Producto Punto (Dot Product)** entre el **Vector Normal de la superficie (`N`)** y el **Vector de Dirección de la Luz (`L`)**:

<div class="formula-card">
  <div class="formula-title">ECUACIÓN FUNDAMENTAL DE ILUMINACIÓN DIRECTA</div>
  <div class="formula-eq">Iluminación Base = dot(N, L) = |N| · |L| · cos(θ)</div>
  <div class="formula-sub">Donde <strong>N</strong> es la Normal del vértice/píxel, <strong>L</strong> es el vector hacia la fuente de luz y <strong>θ</strong> es el ángulo entre ambos.</div>
</div>

* Si la superficie apunta directamente hacia la luz (`θ = 0°`), el producto punto vale **`+1.0`** (luz máxima).
* Si la superficie está a `90°` respecto a la luz, el producto punto vale **`0.0`** (el *Terminator* o frontera exacta donde comienza la sombra).
* Si la superficie da la espalda a la luz (`θ > 90°`), el producto punto cae hacia **`-1.0`** (sombra propia).

La diferencia fundamental entre el **PBR (Physically Based Rendering)** y el **NPR (Non-Photorealistic Rendering)** es qué hacemos con ese número continuo entre `-1.0` y `+1.0`:
1. **En PBR:** Mantenemos el degradado suave continuo (`saturate(dot(N, L))`), permitiendo que la luz decaiga orgánicamente siguiendo la ley del coseno de Lambert.
2. **En NPR (Cel Shading / Toon):** Rompemos el degradado continuo pasando el valor `dot(N, L)` por una función escalonada (`Step`, `Smoothstep` estrecho o una textura **Color Ramp 1D**), convirtiendo la transición suave en bloques sólidos de luz y sombra con bordes nítidos, y reemplazando las sombras negras por colores saturados (violetas, azules fríos o corales cálidos).

<ClientOnly>
  <ToonRampViewer />
</ClientOnly>

---

## 2. Anatomía de las Normales: Face Normal vs. Vertex Normal

Si toda la iluminación depende de `dot(N, L)`, **quien controla el vector Normal (`N`) controla dónde cae la luz y qué forma tiene la sombra**. En una malla poligonal 3D existen tres niveles distintos de normales que todo artista técnico debe dominar:

<div class="pipeline-diagram">
  <div class="pipe-step">
    <span class="pipe-badge">NIVEL 1 · POLÍGONO</span>
    <strong>Face Normal (Normal de Cara)</strong>
    <span>1 vector perpendicular por cada triángulo plano. Define la orientación geométrica bruta.</span>
  </div>
  <div class="pipe-arrow">→</div>
  <div class="pipe-step">
    <span class="pipe-badge">NIVEL 2 · VÉRTICE</span>
    <strong>Vertex Normal (Normal de Vértice)</strong>
    <span>Vectores en las esquinas que la GPU interpola para fingir superficies curvas o bordes duros.</span>
  </div>
  <div class="pipe-arrow">→</div>
  <div class="pipe-step">
    <span class="pipe-badge">NIVEL 3 · TEXTURA UV</span>
    <strong>Normal Map (Tangent Space RGB)</strong>
    <span>Mapa de imagen que desvía la Vertex Normal píxel por píxel para simular micro-relieve.</span>
  </div>
  <div class="pipe-arrow">→</div>
  <div class="pipe-step pipe-step-dark">
    <span class="pipe-badge-dark">SALIDA DE SHADER</span>
    <strong>Producto Punto dot(N, L)</strong>
    <span>Evalúa el corte de luz/sombra (Cel Shading) o el degradado PBR en pantalla.</span>
  </div>
</div>

### 2.1. Face Normal (Normal de Cara o Polígono)
Es el vector perpendicular real y físico de cada triángulo individual. Se calcula mediante el producto cruz (*Cross Product*) de dos de sus aristas:

<div class="formula-card">
  <div class="formula-title">CÁLCULO DE LA NORMAL DE UN TRIÁNGULO (PRODUCTO CRUZ)</div>
  <div class="formula-eq">Normal_Cara = normalize( (V2 − V1) × (V3 − V1) )</div>
  <div class="formula-sub">Donde <strong>V1, V2 y V3</strong> son las coordenadas 3D de los tres vértices que forman el triángulo.</div>
</div>

* **Comportamiento:** Existe **una sola Face Normal por polígono**. Todos los puntos dentro de ese triángulo miran exactamente en la misma dirección matemática.
* **Resultado visual:** Si el motor ilumina usando *Face Normals* puras, cada cara tiene un color plano uniforme y el cambio entre un polígono y el vecino es un salto brusco (**Flat Shading** o estética *Low-Poly* facetada).

### 2.2. Vertex Normal (Normal de Vértice)
Los videojuegos necesitan representar cabezas humanas, esferas, carrocerías y cilindros suaves usando pocos miles de triángulos planos. Para engañar al ojo sin subdividir el modelo en millones de polígonos, las tarjetas gráficas guardan vectores normales **en los vértices**, no en las caras.

* **Interpolación Baricéntrica en el Fragment/Pixel Shader:** Cuando un triángulo tiene tres vértices (`V1`, `V2`, `V3`) con tres *Vertex Normals* apuntando en direcciones ligeramente distintas, la GPU **interpola suavemente** la dirección de la normal píxel por píxel a lo largo del interior del triángulo.
* **El truco óptico:** Aunque el triángulo sigue siendo geométricamente plano como una tabla, el cálculo `dot(N, L)` varía gradualmente de un extremo al otro, haciendo que la luz se curve como si fuera una superficie esférica perfecta.

### 2.3. Hard Edges (Split Normals) vs. Soft Edges (Smooth Normals)
Cuando modelas en Blender, Maya o 3ds Max y eliges entre **Shade Smooth (Suavizado)** y **Shade Flat / Mark Sharp (Borde Duro)**, no estás moviendo ningún vértice de lugar; estás cambiando únicamente sus **Vertex Normals**:

| Propiedad Técnica | Soft Edge (Smooth Vertex Normals) | Hard Edge (Split Vertex Normals) |
| :--- | :--- | :--- |
| **Dirección del Vector en la Esquina** | Las caras vecinas **promedian** sus direcciones en **1 sola Vertex Normal compartida**. | Cada cara impone su propia dirección: el vértice tiene **2, 3 o más Vertex Normals separadas**. |
| **Comportamiento de la Luz** | La luz fluye sin cortes a través de la arista, ocultando la esquina poligonal. | La luz se corta en seco en la arista, marcando un bisel mecánico o esquina dura. |
| **Impacto en Memoria de GPU (Vertex Buffer)** | **Óptimo (1 vértice en GPU):** Como las caras comparten posición y normal, el motor envía un único vértice. | **Mayor costo (Vértices duplicados):** Una GPU no puede asignar dos normales a un mismo índice; un cubo con *Hard Edges* pasa de 8 vértices en Blender/Maya a **24 vértices reales** en Unity/Unreal (`8 × 3` caras). |

---

## 3. El Secreto del NPR Moderno: Normal Transfer e Inverted Hull

En el sombreado realista (PBR), una pequeña desviación en una *Vertex Normal* apenas produce una variación de gris imperceptible. En cambio, en el **Cel Shading (NPR)** usamos un corte binario (`Step`): si `dot(N, L)` baja un milímetro por debajo del umbral (por ejemplo, de `+0.01` a `-0.01`), **el píxel salta instantáneamente de blanco iluminado a sombra oscura**.

Esto genera los dos problemas más famosos del arte 3D estilizado, y sus respectivas soluciones de industria:

### 3.1. Problema 1: El Rostro "Sucio" en Cel Shading y la Técnica de Normal Transfer (Esfera Proxy)
Cuando modelamos la cara de un personaje 3D con buena topología (cuencas de ojos, puente de la nariz, surco nasogeniano, labios y pómulos), las *Vertex Normals* automáticas siguen fielmente cada pequeño hundimiento de la malla.
* **El fallo:** Al aplicar un shader Toon (`Step`), aparecen sombras triangulares rotas en las mejillas, cortes dentados bajo la nariz y manchas oscuras alrededor de la boca cuando la luz gira. El personaje parece una estatua de plástico mal iluminada en lugar de una ilustración 2D.
* **La solución de la industria (*Guilty Gear*, *Genshin Impact*, *Zenless Zone Zero*):** En el dibujado de anime tradicional 2D, los animadores sombrean la cabeza como si fuera un **huevo o esfera simple**, ignorando las micro-arrugas de la mejilla. En 3D logramos exactamente lo mismo mediante **Transferencia de Normales (Normal Transfer / Data Transfer)**:
  1. Se crea una **esfera o cápsula limpia (Proxy Mesh)** envolviendo la cara del personaje.
  2. Se transfieren las direcciones de las *Vertex Normals* de esa esfera hacia los vértices del rostro.
  3. **Resultado:** El modelo conserva el 100% de sus vértices reales (la nariz sigue sobresaliendo en silueta y la boca puede abrirse), pero para el shader de luz la cara reacciona matemáticamente como un elipsoide liso, proyectando una línea de sombra curva e impecable de oreja a mentón.

### 3.2. Problema 2: El Contorno 3D (*Inverted Hull Outline*) y la Rotura de Esquinas
La técnica estándar en videojuegos para dibujar líneas de tinta negra alrededor de un modelo 3D se llama **Inverted Hull (Casco Invertido)**:
1. Se dibuja una segunda pasada del mismo modelo pintada de color de línea (`Unlit`).
2. Se invierte el *Culling* de cámara (`Cull Front` / `Render Face: Back`, mostrando solo las caras traseras).
3. En el *Vertex Shader*, cada vértice se infla hacia afuera empujándolo en la dirección de su **Vertex Normal**:

<div class="formula-card">
  <div class="formula-title">EXTRUSIÓN DE CONTORNO EN EL VERTEX SHADER (INVERTED HULL)</div>
  <div class="formula-eq">Posicion_Outline = Posicion_Original + ( Vertex_Normal × Grosor )</div>
  <div class="formula-sub">En Unity 6 (Shader Graph) se suma a <strong>Position (Object Space)</strong> en el bloque Vertex; en Unreal 5 se conecta a <strong>World Position Offset</strong>.</div>
</div>

* **Por qué se rompe en bordes duros (*Hard Edges*):** Si tienes un cubo, cilindro o espada con *Hard Edges*, en cada esquina hay 3 vértices duplicados cuyas *Vertex Normals* apuntan a `90°` de distancia entre sí. Al empujar cada cara hacia su propia normal, **las caras extruidas se separan dejando un hueco vacío en la esquina** y el contorno negro queda partido.
* **Cómo se repara en producción:** Se guarda una copia **100% suavizada (Soft/Smooth)** de las normales en un canal alternativo de la malla (como `UV3 / TEXCOORD3`, `Tangent` o `Vertex Color`) exclusivamente para que el *Vertex Shader* del contorno infle los vértices unidos sin abrir brechas, mientras la iluminación principal sigue usando las normales originales del modelo.

### 3.3. Laboratorio Interactivo 01: Simulador de Normales, Normal Transfer e Inverted Hull

Experimenta en tiempo real con el **Personaje Anime (Con y Sin Cabello)** y el **Cilindro Biselado**. Usa los tres botones de **Casos de Estudio** superiores para comparar instantáneamente un Cel Shading roto por topología, un *Normal Transfer* limpio estilo anime y un *Inverted Hull Outline* abierto en las esquinas frente a uno sellado:

<ClientOnly>
  <NPRNormalsViewer />
</ClientOnly>

---

## 4. Diferencia entre Vertex Normals, Normal Map (Textura) y Normales 2D

Un error conceptual frecuente es confundir las **normales de la geometría** con el **Normal Map de textura**. La siguiente tabla resume cómo interactúan ambos sistemas en proyectos 3D y 2D:

| Sistema | Dónde vive el dato | Resolución | Qué modifica realmente | Uso clave en Entrega 3 y Examen |
| :--- | :--- | :--- | :--- | :--- |
| **Face Normal** | En el triángulo (calculada por sus 3 vértices). | 1 vector por polígono. | Da la orientación plana bruta de cada cara. | Estética *Low-Poly* facetada intencional o diagnóstico de caras invertidas (*Backfaces*). |
| **Vertex Normal** | Guardada en cada vértice del *Vertex Buffer*. | 1 vector por esquina de vértice. | Controla el suavizado macro de la malla y la dirección hacia donde crece el **Inverted Hull Outline**. | **Fundamental en NPR 3D:** Limpiar sombras en rostros (*Normal Transfer*) y sellar contornos. |
| **Normal Map (Tangent Space)** | En una textura de imagen RGB (`#8080FF`). | Millones de vectores (1 por cada píxel/texel UV). | Perturba la *Vertex Normal* píxel por píxel para fingir poros, tornillos o ladrillos sin añadir polígonos. | Detalle de superficie en 3D, o **trazos de pincel pintados en las normales** (estilo *Arcane* / *Spider-Verse*). |
| **Normal Map en Sprites 2D** | Textura secundaria (`_NormalMap` en Unity URP 2D). | 1 vector por píxel del Sprite. | Como un `Quad` 2D es totalmente plano (`N = (0, 0, 1)`), el Normal Map le inventa volumen esférico o biselado para reaccionar a luces dinámicas `Light 2D`. | **Obligatorio en juegos 2D / HD-2D:** Permite que antorchas y hechizos iluminen el borde derecho o izquierdo de un personaje 2D (*Octopath Traveler*, *Dead Cells*). |

---

## 5. Vertex Color: Pintura en Vértices y Empaquetado de 4 Máscaras (RGBA)

El **Vertex Color (Color de Vértice)** es un atributo adicional guardado directamente dentro de cada vértice de la malla 3D, compuesto por cuatro valores flotantes independientes entre `0.0` y `1.0`:

<div class="formula-card">
  <div class="formula-title">ESTRUCTURA DE DATOS DEL ATRIBUTO VERTEX COLOR</div>
  <div class="formula-eq">VertexColor = vec4( Canal_R, Canal_G, Canal_B, Canal_A )</div>
  <div class="formula-sub">Cada vértice almacena 4 valores de 0.0 (Negro = 0%) a 1.0 (Blanco = 100%) con <strong>0 MB de gasto en texturas de imagen</strong>.</div>
</div>

Al igual que ocurre con las *Vertex Normals*, la tarjeta gráfica **interpola gratuitamente** el color entre un vértice y sus vecinos a través de la superficie del triángulo. Su gran ventaja técnica es que **no consume memoria de texturas adicional** ni depende de que los UVs estén desplegados sin solapamientos.

En la industria de los videojuegos, el *Vertex Color* se utiliza de dos maneras radicalmente distintas: **Uso Artístico Directo** y **Uso Técnico como 4 Máscaras de Datos**.

### 5.1. Uso 1: Vertex Color Artístico (Color Visible y Ambient Occlusion en Vértices)
Es el uso clásico donde el color pintado en los vértices se conecta directamente al **Base Color (Albedo)** del material o se multiplica sobre él:
* **Estética Low-Poly y Estilizada (*Journey*, *Abzû*, *Monument Valley*, *Tunic*):** Modelos sin texturas de imagen donde toda la paleta cromática y los degradados suaves entre la base y la punta de una estructura provienen de los vértices.
* **Baked Vertex Ambient Occlusion (AO):** Se hornea la oclusión ambiental en escala de grises dentro de los vértices (negro `0.0` en grietas profundas e interiores de ropa; blanco `1.0` en zonas expuestas) y se multiplica (`Multiply`) por el color base o la luz ambiental para asentar el modelo sin coste de rendimiento en tiempo real.

### 5.2. Uso 2: Empaquetado de 4 Máscaras Técnicas Independientes (R, G, B, A)
Si abres el modelo 3D de un personaje de *Guilty Gear Strive* o *Genshin Impact*, o un edificio modular de *The Last of Us* en Blender/Maya y activas la vista de *Vertex Color*, verás que el modelo está pintado con un **aspecto de arcoíris técnico (zonas rojas puras, verdes fluorescentes, azules y amarillas)**.

¿Por qué se ve así? Porque el shader **jamás muestra ese color en pantalla**. En lugar de usar `(R, G, B, A)` como un color decorativo, el artista técnico separa los 4 canales en el editor de shaders (`Split` en Unity Shader Graph) para tener **4 mapas de control en blanco y negro (`0.0 = 0%`, `1.0 = 100%`)** dentro del mismo modelo:

<div class="rgba-channels-grid">
  <div class="rgba-card rgba-r">
    <div class="rgba-header"><span class="rgba-pill pill-r">CANAL R</span> <strong>Máscara 1 (0.0 a 1.0)</strong></div>
    <p><strong>En Personajes NPR:</strong> Controla el grosor del <em>Inverted Hull Outline</em> (<code>1.0</code> trazo grueso en hombros/cabello; <code>0.0</code> trazo fino o nulo en ojos, pestañas y nariz).</p>
    <p><strong>En Entornos 3D:</strong> Pin <code>T / Alpha</code> del primer <code>Lerp</code> para mezclar Piedra Base con Musgo o Nieve.</p>
  </div>
  <div class="rgba-card rgba-g">
    <div class="rgba-header"><span class="rgba-pill pill-g">CANAL G</span> <strong>Máscara 2 (0.0 a 1.0)</strong></div>
    <p><strong>En Personajes NPR:</strong> Desplaza el umbral <code>dot(N, L)</code> para forzar <em>Sombra Permanente</em> bajo el mentón, cuello alto y bajo el flequillo.</p>
    <p><strong>En Entornos 3D:</strong> Pin <code>T / Alpha</code> del segundo <code>Lerp</code> para revelar grietas, ladrillo roto o desgaste de bordes.</p>
  </div>
  <div class="rgba-card rgba-b">
    <div class="rgba-header"><span class="rgba-pill pill-b">CANAL B</span> <strong>Máscara 3 (0.0 a 1.0)</strong></div>
    <p><strong>En Personajes NPR:</strong> Máscara de <em>Rim Light / Specular</em> (permite brillo de borde en el cabello y lo bloquea en zonas internas).</p>
    <p><strong>En Entornos 3D:</strong> Máscara de humedad y charcos (oscurece el Albedo y sube el <em>Smoothness</em> a <code>0.95</code> en Unity).</p>
  </div>
  <div class="rgba-card rgba-a">
    <div class="rgba-header"><span class="rgba-pill pill-a">CANAL A</span> <strong>Máscara 4 (0.0 a 1.0)</strong></div>
    <p><strong>En Personajes NPR:</strong> Controla el tinte cálido interior (<em>Subsurface / Rubor</em>) en mejillas y puente nasal.</p>
    <p><strong>En Entornos 3D:</strong> Peso de animación de <em>Viento (Vertex Position)</em>: <code>0.0</code> ancla la raíz al muro/suelo y <code>1.0</code> mueve las puntas.</p>
  </div>
</div>

### 5.3. Laboratorio Interactivo 02: Simulador de Vertex Color y Máscaras RGBA

Alterna entre el **Caso A (Personaje Anime NPR)** y el **Caso B (Entorno 3D con Viento WPO)**. Utiliza la barra **Vista de Diagnóstico** para inspeccionar el mapa `Vertex Color RGB (Raw)` (el aspecto "arcoíris" de producción) y cada uno de los 4 canales en escala de grises (`R`, `G`, `B`, `A`), ajustando su influencia con los controles deslizantes:

<ClientOnly>
  <VertexColorViewer />
</ClientOnly>

---

## 6. Implementación Estándar de Industria en Unity 6 (URP — Universal Render Pipeline)

En **Unity 6 (`6000.x`)**, el pipeline estándar para proyectos estilizados 3D y 2D es **URP (Universal Render Pipeline)** apoyado en **Shader Graph** y el nuevo **Render Graph API**. A continuación se detalla el flujo exacto utilizado en la industria para implementar todas las técnicas anteriores sin romper el *SRP Batcher* ni perder sombras dinámicas.

### 6.1. Preparación en Blender e Importación FBX en Unity 6
1. **En Blender (Antes de exportar el `.FBX`):**
   * Transfiere las normales faciales desde una esfera limpia usando el modificador **Data Transfer** → activar **Face Corner Data → Custom Normals** (restringido al *Vertex Group* de la cara).
   * En modo **Vertex Paint**, pinta tus máscaras en el atributo de color (`Color`) usando canales puros: Rojo `(1,0,0)` para grosor de outline, Verde `(0,1,0)` para umbral de sombra fija y Azul `(0,0,1)` para máscara de Rim/Specular.
2. **En Unity 6 (Ventana *Inspector* del archivo `.FBX` → Pestaña `Model`):**
   * En la sección **Geometry**, asegúrate de configurar:
     * **`Normals`: `Import`** (Crítico: si lo dejas en *Calculate*, Unity recalculará las normales geométricas y destruirá tu *Normal Transfer* de Blender).
     * **`Tangents`: `Calculate Mikktspace`**.
     * **`Weld Vertices`: Activado (`True`)**.
   * Unity importa automáticamente los colores de vértice en `Mesh.colors32`, los cuales quedan listos para leerse en **Shader Graph** con el nodo **`Vertex Color`**.

---

### 6.2. El Estándar para Cel Shading en Unity 6 URP: Nodo `Custom Function` (`GetMainLight`)
En **URP Shader Graph**, el target **Lit** aplica las ecuaciones PBR de forma cerrada (ocultando el vector de la luz principal), mientras que el target **Unlit** no tiene un nodo nativo para consultar la dirección ni las sombras del sol (`Directional Light`).

Por ello, **el estándar de la industria en Unity URP** consiste en crear un **Shader Graph Unlit** (o un Sub-Graph reutilizable llamado `SG_MainLight`) que incluye un nodo **`Custom Function`** con unas pocas líneas de HLSL para llamar a `GetMainLight()` directamente desde el motor URP:

#### Paso A: Crear el archivo `CustomLightingURP.hlsl` en tu proyecto de Unity 6
Crea un archivo de texto con extensión `.hlsl` en tu carpeta `Assets/Shaders/` y pega el siguiente código oficial compatible con **Unity 6 (`Forward` y `Forward+`)**:

```hlsl
#ifndef CUSTOM_LIGHTING_URP_INCLUDED
#define CUSTOM_LIGHTING_URP_INCLUDED

void GetMainLightWithShadows_float(
    float3 WorldPos,
    out float3 Direction,
    out float3 Color,
    out float DistanceAtten,
    out float ShadowAtten)
{
#if defined(SHADERGRAPH_PREVIEW)
    // Valores de previsualización dentro de la ventana de Shader Graph
    Direction = normalize(float3(0.5, 0.5, 0.25));
    Color = float3(1.0, 1.0, 1.0);
    DistanceAtten = 1.0;
    ShadowAtten = 1.0;
#else
    // 1. Calcular coordenadas del Shadow Map (Cascades o Screen Space Shadows)
    #if SHADOWS_SCREEN
        float4 clipPos = TransformWorldToHClip(WorldPos);
        float4 shadowCoord = ComputeScreenPos(clipPos);
    #else
        float4 shadowCoord = TransformWorldToShadowCoord(WorldPos);
    #endif

    // 2. Consultar la luz direccional principal de URP en Unity 6
    Light mainLight = GetMainLight(shadowCoord, WorldPos, half4(1, 1, 1, 1));

    Direction = mainLight.direction;
    Color = mainLight.color;
    DistanceAtten = mainLight.distanceAttenuation;
    ShadowAtten = mainLight.shadowAttenuation;
#endif
}

#endif
```

#### Paso B: Configurar el Nodo y las 3 Keywords de Sombra en Shader Graph
1. En tu **Shader Graph** (`Create → Shader Graph → URP → Unlit Shader Graph`), haz clic derecho → **Create Node → Custom Function**.
2. En el *Node Settings* (dentro del *Graph Inspector*):
   * **Type:** `File` → selecciona tu archivo `CustomLightingURP.hlsl`.
   * **Name:** `GetMainLightWithShadows` (sin el sufijo `_float`, Shader Graph lo añade automáticamente).
   * **Inputs:** añade `WorldPos` (`Vector3`) y conéctale un nodo **`Position` (`Space: World`)**.
   * **Outputs:** añade `Direction` (`Vector3`), `Color` (`Vector3`), `DistanceAtten` (`Float`) y `ShadowAtten` (`Float`).
3. **Requisito Crítico para Sombras Arrojadas en Unity 6:** Para que `ShadowAtten` reciba las sombras proyectadas por otros objetos y no devuelva siempre `1.0`, abre el **Blackboard** de tu Shader Graph, pulsa **`+` → `Keyword` → `Boolean`** y agrega estas tres *Keywords* exactas del pipeline URP (con **`Scope: Global`** y **`Definition: Multi Compile`**):
   * `_MAIN_LIGHT_SHADOWS`
   * `_MAIN_LIGHT_SHADOWS_CASCADE`
   * `_SHADOWS_SOFT`

---

### 6.3. Grafo Completo en Unity 6 Shader Graph: Cel Shading + Vertex Color RGBA

Una vez que tienes tu nodo `GetMainLightWithShadows`, la conexión de nodos dentro de **Unity 6 Shader Graph** para replicar el **Laboratorio 02** es directa:

<div class="pipeline-diagram">
  <div class="pipe-step">
    <span class="pipe-badge">1. PRODUCTO PUNTO</span>
    <strong>Normal Vector (World) · Direction</strong>
    <span>Se conectan a un nodo <code>Dot Product</code> para obtener la luz cruda entre -1 y +1.</span>
  </div>
  <div class="pipe-arrow">→</div>
  <div class="pipe-step">
    <span class="pipe-badge">2. CANAL G (SOMBRA FIJA)</span>
    <strong>Add ( Dot + (VertexColor.G − 1.0) )</strong>
    <span>Extrae <code>G</code> con un nodo <code>Split</code>. Donde G es 0 (mentón), empuja el valor a sombra.</span>
  </div>
  <div class="pipe-arrow">→</div>
  <div class="pipe-step">
    <span class="pipe-badge">3. CORTE Y SOMBRA CAST</span>
    <strong>Smoothstep × ShadowAtten</strong>
    <span>Cuantiza el borde Toon y lo multiplica por <code>ShadowAtten</code> de la luz principal.</span>
  </div>
  <div class="pipe-arrow">→</div>
  <div class="pipe-step pipe-step-dark">
    <span class="pipe-badge-dark">4. SALIDA FRAGMENT</span>
    <strong>Lerp (ColorSombra, ColorLuz, Cel)</strong>
    <span>Mezcla paleta de sombra y luz, suma <code>Fresnel × VertexColor.B</code> y va a <code>Base Color</code>.</span>
  </div>
</div>

* **Tip de Industria en Unity (Rampa 1D vs. Smoothstep):** Si tu estilo artístico tiene más de 2 tonos o una transición cálida en el borde (como *Genshin Impact*), en lugar de usar un nodo `Smoothstep`, toma el resultado de `(Dot * 0.5 + 0.5)` y conéctalo a la entrada **`UV`** de un nodo **`Sample Texture 2D`** que lea una textura **Toon Ramp 1D** (importada en Unity con **`Wrap Mode: Clamp`** para que los extremos nunca se filtren entre sí).

---

### 6.4. Contorno *Inverted Hull Outline* en Unity 6 URP (`Render Objects` + `AssetPostprocessor`)

En **Unity 6 URP**, los shaders multipase manuales rompen la facilidad de uso de **Shader Graph**. El estándar de producción en estudios que usan URP consiste en combinar un **Shader Graph de Contorno (`Render Face: Back`)** con la característica nativa **`Render Objects` (Renderer Feature)** del *Universal Renderer Data*:

#### Paso 1: Crear el Shader Graph del Contorno (`SG_Outline_URP`)
1. Crea un nuevo **`URP Unlit Shader Graph`**.
2. Abre el **Graph Inspector → Graph Settings → Universal** y cambia **`Render Face`** a **`Back`** (esto activa `Cull Front`: oculta las caras delanteras del modelo y dibuja únicamente el interior de las caras traseras).
3. En el contexto **Vertex** (arriba a la derecha del Master Stack):
   * Crea un nodo **`Position`** configurado en **`Space: Object`**.
   * Crea un nodo **`Normal Vector`** configurado en **`Space: Object`** (o lee las normales suavizadas desde **`UV3`** si usas el script de abajo).
   * Crea un nodo **`Vertex Color`** → **`Split`** y toma el canal **`R` (Rojo)**.
   * Multiplica: `Normal (Object) × OutlineWidth (Float Parameter) × VertexColor.R`.
   * Suma (`Add`) ese desplazamiento a `Position (Object)` y conéctalo a la entrada **`Position`** del bloque **Vertex**.
4. En el contexto **Fragment**, conecta un parámetro **`Outline Color`** al bloque **`Base Color`**.

#### Paso 2: Inyectar el Pase de Contorno con `Render Objects` (Sin duplicar mallas en la escena)
Para que Unity 6 dibuje automáticamente la pasada de contorno sobre todos tus personajes sin tener que duplicar GameObjects:
1. Selecciona tu objeto o personaje en la escena y asígnale una capa dedicada (por ejemplo, `Layer: CharacterNPR`).
2. Busca en tu carpeta `Assets/Settings/` el archivo **`Universal Renderer Data`** (por defecto llamado `PC_RPAsset_Renderer` o `UniversalRenderer`).
3. En la parte inferior del *Inspector*, haz clic en **`Add Renderer Feature` → `Render Objects`**:
   * **Name:** `Outline_InvertedHull_Pass`
   * **Event:** `AfterRenderingOpaques`
   * **Filters → Queue:** `Opaque`
   * **Filters → Layer Mask:** marca únicamente `CharacterNPR`.
   * **Overrides → Material:** arrastra tu material `M_Outline_URP` creado con el Shader Graph del Paso 1.
   * **Overrides → Depth:** marca *Write Depth = Off* y *Depth Test = Less Equal*.

#### Paso 3: Script `AssetPostprocessor` para Hornear Normales Suavizadas en `UV3` (Sellar Esquinas Duras)
Como vimos en el **Laboratorio 01**, si un modelo tiene bordes duros (*Hard Edges*), el contorno *Inverted Hull* se abre en las esquinas. Y si ya estás usando el `Vertex Color (RGBA)` para tus 4 máscaras del shader, **¿dónde guardas las normales suavizadas para el contorno?**

El estándar en la industria con Unity es colocar este pequeño script de C# dentro de una carpeta **`Assets/Editor/SmoothNormalBaker.cs`**. Cada vez que importes un `.FBX` cuyo nombre contenga `_NPR`, Unity calculará automáticamente las normales promediadas sin costuras y las guardará en el canal **`UV3` (`TEXCOORD3`)**, dejando libre tu `Vertex Color`:

```csharp
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;

public class SmoothNormalBaker : AssetPostprocessor
{
    void OnPostprocessModel(GameObject root)
    {
        // Se ejecuta automáticamente en cualquier modelo cuyo archivo contenga "_NPR"
        if (!assetPath.Contains("_NPR")) return;

        foreach (var mf in root.GetComponentsInChildren<MeshFilter>())
            if (mf.sharedMesh != null) BakeSmoothNormalsToUV3(mf.sharedMesh);

        foreach (var smr in root.GetComponentsInChildren<SkinnedMeshRenderer>())
            if (smr.sharedMesh != null) BakeSmoothNormalsToUV3(smr.sharedMesh);
    }

    private void BakeSmoothNormalsToUV3(Mesh mesh)
    {
        Vector3[] verts = mesh.vertices;
        Vector3[] norms = mesh.normals;
        var avgNormals = new Dictionary<Vector3, Vector3>();

        // 1. Promediar todas las normales de los vértices que comparten la misma posición 3D
        for (int i = 0; i < verts.Length; i++)
        {
            if (!avgNormals.TryGetValue(verts[i], out Vector3 acc))
                avgNormals[verts[i]] = norms[i];
            else
                avgNormals[verts[i]] = (acc + norms[i]).normalized;
        }

        // 2. Guardar la normal suavizada en Object Space dentro del canal UV3 (índice 3)
        var uv3 = new List<Vector3>(verts.Length);
        for (int i = 0; i < verts.Length; i++)
            uv3.Add(avgNormals[verts[i]].normalized);

        mesh.SetUVs(3, uv3);
    }
}
```
> En tu **Shader Graph de Contorno**, simplemente añade un nodo **`UV`** configurado en **`Channel: UV3`**, pásalo por un nodo **`Split` / `Combine` (XYZ)** y úsalo en lugar del nodo `Normal Vector` para inflar el contorno sin una sola grieta.

---

### 6.5. Juegos 2D y HD-2D en Unity 6 URP (`2D Renderer` + `Secondary Textures`)

Para los equipos cuyo proyecto de Examen Final sea **2D o 2.5D (HD-2D)** en Unity 6, el pipeline 2D de URP permite aplicar exactamente los mismos principios de **Normal Maps** y **Máscaras por Canal** sobre Sprites:

1. **Activar el Renderer 2D:** Asegúrate de que tu *URP Asset* utilice un **`2D Renderer Data`** y añade componentes **`Light 2D`** en tu escena (`Global Light 2D` para ambiente y `Point / Spot / Freeform Light 2D` para antorchas, proyectiles y focos).
2. **Importar el Mapa de Normales y la Máscara del Sprite:**
   * Selecciona la textura de normales de tu Sprite (`Personaje_N.png`) y en el *Inspector* cambia **`Texture Type: Normal Map`** (desmarcando *sRGB*).
   * Selecciona tu textura de máscara (`Personaje_Mask.png`, donde puedes usar R, G, B para brillo especular o *Rim Light*) y déjala en **`Texture Type: Default`** (desmarcando *sRGB*).
3. **Vincular `Secondary Textures` en el Sprite Editor (Paso Clave en Unity 6):**
   * Selecciona el Sprite principal (`Personaje_Albedo.png`) y haz clic en el botón **`Open Sprite Editor`**.
   * En la esquina superior izquierda del *Sprite Editor*, cambia el menú desplegable de *Sprite Editor* a **`Secondary Textures`**.
   * Haz clic en **`+`** abajo a la derecha y agrega los **dos nombres reservados obligatorios del estándar URP 2D**:
     * Entry 1 → **Name:** **`_NormalMap`** | **Texture:** tu mapa de normales.
     * Entry 2 → **Name:** **`_MaskTex`** | **Texture:** tu mapa de máscaras.
   * Pulsa **Apply**.
4. **Shader Graph 2D Estilizado:**
   * Puedes usar el material nativo `Sprites-Lit-Default` o crear tu propio shader personalizado en **`Create → Shader Graph → URP → Sprite Lit Shader Graph`**, leyendo `_NormalMap` y `_MaskTex` mediante nodos `Sample Texture 2D` con esas referencias exactas en el *Blackboard*.

---

## 7. Equivalencia Rápida: Unity 6 (URP) vs. Unreal Engine 5

Si trabajas en **Unreal Engine 5** o estás migrando conceptos entre ambos motores, esta tabla resume las equivalencias exactas de producción:

| Operación Técnica | En Unity 6 (URP + Shader Graph) | En Unreal Engine 5 (Material Editor) |
| :--- | :--- | :--- |
| **Preservar Normales Transferidas al Importar FBX** | Inspector del FBX → Pestaña *Model* → **`Normals: Import`** | Ventana *FBX Import Options* → **`Normal Import Method: Import Normals and Tangents`** |
| **Importar Colores de Vértice (RGBA)** | Automático al importar el FBX (`Mesh.colors32`). | *FBX Import Options* → **`Vertex Color Import Option: Replace`** |
| **Leer Dirección de la Luz Principal (Sol)** | Nodo **`Custom Function`** llamando a `GetMainLight(shadowCoord, WorldPos)` en HLSL. | Nodo directo **`SkyAtmosphereLightDirection`** (o `AtmosphereSunLightVector`). |
| **Leer Normal del Vértice en el Shader** | Nodo **`Normal Vector`** (`Space: World` para luz; `Space: Object` para extrusión). | Nodo **`VertexNormalWS`** (Espacio de Mundo). |
| **Separar Canales RGBA del Vertex Color** | Nodo **`Vertex Color`** conectado a un nodo **`Split`** (`R, G, B, A`). | Nodo **`Vertex Color`** (expone los pines blanco, rojo, verde, azul y alfa directamente). |
| **Desplazar Vértices (Outline o Viento)** | Conectar la operación a la entrada **`Position (Object Space)`** del bloque **Vertex**. | Conectar el desplazamiento al pin **`World Position Offset`** del nodo principal. |
| **Invertir Caras para Contorno (`Inverted Hull`)** | *Graph Settings* → **`Render Face: Back`** + inyección vía **`Render Objects` (Renderer Feature)**. | Material con `Two Sided` o malla duplicada filtrando con el nodo **`TwoSidedSign`**. |

---

## 8. Referencias Vinculadas en la Plataforma

* [Rúbrica Entrega N°3: Avance de Examen — LookDev, NPR y Banco de Pruebas](/clases/rubrica-entrega-03)
* [Rúbrica Examen Final: Integración en Videojuego y Breakdown Técnico (80.lv)](/clases/rubrica-examen)
* [04. Matemáticas de Shaders: Producto Punto, Fresnel, Lerp y Normales](/shaders/04-matematicas-shaders)
* [03. Modelos de Sombreado (Default Lit, Unlit, Subsurface, Foliage)](/shaders/03-shading-models)

<style scoped>
.formula-card {
  border: 1px solid #d1d5db;
  border-left: 4px solid #111827;
  background: #f9fafb;
  padding: 12px 16px;
  border-radius: 4px;
  margin: 16px 0;
}

.formula-title {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  font-weight: 700;
  color: #6b7280;
  letter-spacing: 0.5px;
  margin-bottom: 4px;
}

.formula-eq {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 4px;
}

.formula-sub {
  font-size: 12px;
  color: #4b5563;
}

.pipeline-diagram {
  display: flex;
  align-items: stretch;
  gap: 8px;
  margin: 18px 0;
  flex-wrap: wrap;
}

.pipe-step {
  flex: 1;
  min-width: 150px;
  border: 1px solid #d1d5db;
  background: #f9fafb;
  border-radius: 4px;
  padding: 10px 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.pipe-step-dark {
  background: #111827;
  border-color: #111827;
  color: #ffffff;
}

.pipe-badge {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9.5px;
  font-weight: 700;
  color: #4b5563;
}

.pipe-badge-dark {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9.5px;
  font-weight: 700;
  color: #9ca3af;
}

.pipe-step strong {
  font-size: 12.5px;
  color: #111827;
}

.pipe-step-dark strong {
  color: #ffffff;
}

.pipe-step span:last-child {
  font-size: 11.5px;
  color: #4b5563;
  line-height: 1.35;
}

.pipe-step-dark span:last-child {
  color: #d1d5db;
}

.pipe-arrow {
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: #6b7280;
  font-size: 16px;
  padding: 0 2px;
}

.rgba-channels-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin: 16px 0;
}

.rgba-card {
  border: 1px solid #d1d5db;
  border-radius: 4px;
  padding: 12px 14px;
  background: #fafafa;
}

.rgba-card p {
  font-size: 12px;
  color: #374151;
  margin: 6px 0 0 0;
  line-height: 1.4;
}

.rgba-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
  font-size: 12.5px;
  color: #111827;
}

.rgba-pill {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  font-weight: 700;
  color: #ffffff;
  padding: 2px 6px;
  border-radius: 2px;
}

.pill-r { background: #dc2626; }
.pill-g { background: #16a34a; }
.pill-b { background: #2563eb; }
.pill-a { background: #374151; }

@media (max-width: 768px) {
  .rgba-channels-grid {
    grid-template-columns: 1fr;
  }
  .pipe-arrow {
    display: none;
  }
}
</style>
