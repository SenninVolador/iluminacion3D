# Rúbrica de Evaluación: Entrega N°2

Iluminación 3D · Docente Daniel Rojas (UNIACC)

Proyecto de Iluminación de Interiores: Análisis de Referencia, Moodboard y Réplica en Unreal Engine 5.

---

## Información General de la Evaluación

* **Puntaje Total**: 60 puntos
* **Escala de Calificación**: 1.0 a 7.0 (Exigencia del 60% para nota 4.0 = 36 puntos)
* **Software Requerido**: Unreal Engine 5 (Lumen) + Herramienta de Moodboard (PureRef, Photoshop o Figma)
* **Ponderación Criterio Moodboard**: 15% del total de la evaluación (9 puntos)
* **Documentos de Evaluación**: 
  * [Descargar Rúbrica Oficial en PDF](/Rubrica_Entrega_02.pdf)
  * <a href="/iluminacion3D/Rubrica_Evaluacion_Entrega_02.xlsx" download>Descargar Planilla de Calificación en Formato Excel (.xlsx)</a>

---

## Descripción del Encargo

El estudiante debe diseñar, justificar y construir la **iluminación de un espacio interior** en Unreal Engine 5 a partir de un **análisis riguroso de referencias visuales cinematográficas o de videojuegos AAA**.

El proyecto se sustenta en la metodología de **Chris Brejon (*CG Cinematography*)**, donde cada fuente de luz debe responder a una función clara:
1. **Natural Lights**: Fuentes exteriores que ingresan por aberturas (sol, cielo, luna).
2. **Practical Lights**: Luminarias visibles en la escena (lámparas, ampolletas, monitores, velas).
3. **Dramatic Lights**: Luces de apoyo y modelado fuera de cuadro motivadas por las fuentes del entorno.

La escena debe evidenciar comprensión de la luz indirecta (rebotes Lumen), contraste térmico coherente (Kelvin), jerarquía de intensidades físicas y una clara **intención narrativa** que guíe la mirada del espectador hacia el punto focal.

---

## Requisitos de Entrega

1. **Moodboard y Lámina de Análisis (15%)**:
   * Archivo de imagen o PDF (PureRef / lámina gráfica) con las referencias seleccionadas de cine o videojuegos.
   * Desglose técnico de la referencia principal: identificación de fuentes motivadoras, paleta cromática / temperatura Kelvin, clave tonal (High-Key / Low-Key) e intención narrativa explicada.
2. **Escena de Interior en Unreal Engine 5**:
   * Habitación, pasillo, taller o entorno interior cerrado y ambientado.
   * Iluminación motivada física y narrativamente, evitando iluminación ambiental plana.
   * Manejo de apertura exterior (ventana/puerta/tragaluz) y luminarias prácticas interiores.
3. **Optimización y Post-Processing**:
   * Post-Process Volume no destructivo (`Unbound = True`) con exposición calibrada manualmente.
   * Niebla volumétrica sutil y justificada si la escena lo amerita.
4. **Nomenclatura y Orden del Proyecto**:
   * Outliner organizado por carpetas (`LGT_Natural`, `LGT_Practical`, `LGT_Dramatic`, etc.).
   * Nomenclatura estándar (`L_Directional_...`, `L_Rect_...`, `L_Point_...`, `L_Spot_...`).
5. **Entregables Finales**:
   * Lámina de Moodboard y Referencias (PDF o PNG).
   * Proyecto o nivel de Unreal Engine (`.uproject` o paquete de mapa con assets).
   * Cuatro (4) capturas de pantalla en alta resolución (1920x1080 o superior):
     1. Plano principal (*Hero Shot*) con iluminación final (*Lit*).
     2. Vista comparativa lado a lado: Referencia vs. Réplica 3D.
     3. Vista en modo *Detail Lighting* o *Unlit* para evidenciar modelado lumínico sin la influencia de las texturas.
     4. Captura del Outliner desplegado mostrando la jerarquía de luces y carpetas.

---

## Ponderación General de Criterios

| Criterio de Evaluación | Ponderación (%) | Puntaje Asignado |
| :--- | :---: | :---: |
| **1. Referencias Visuales, Análisis y Moodboard** | **15%** | **9 puntos** |
| **2. Iluminación Interior y Espacialidad** | **25%** | **15 puntos** |
| **3. Uso Correcto y Técnico de Fuentes de Luz** | **30%** | **18 puntos** |
| **4. Intención Narrativa, Atmósfera y Guía Visual** | **20%** | **12 puntos** |
| **5. Nomenclatura, Orden de Escena y Entregables** | **10%** | **6 puntos** |
| **TOTAL** | **100%** | **60 puntos** |

---

## Matriz de Evaluación Detallada (60 Puntos)

| Criterio | Excelente (100%) | Bueno (75%) | Suficiente (50%) | Insuficiente (0-25%) | Puntaje |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **1. Referencias y Moodboard (15%)** | Moodboard estructurado con referencias de alta calidad cinematográfica/videojuegos. Desglose analítico riguroso (fuentes, temperatura Kelvin, contraste). La escena 3D refleja fielmente la dirección visual propuesta. | Moodboard completo pero con desglose técnico elemental o leve discrepancia en la traslación de la paleta y contrastes a la escena 3D. | Moodboard escaso o desorganizado; recopilación de imágenes aisladas sin análisis técnico de fuentes ni intención clara. | No presenta moodboard o incluye imágenes no pertinentes sin ninguna relación con la escena desarrollada. | **/ 9 pts** |
| **2. Iluminación Interior y Espacialidad (25%)** | Recinto con excelente lectura volumétrica y profundidad en planos (primer plano, medio y fondo). Luz motivada por aberturas. Rebotes indirectos creíbles (Lumen) sin empastar sombras ni lavar negros con luz falsa. | Espacio bien iluminado con sensación de volumen, aunque con leve aplanamiento en rincones o rebotes indirectos ligeramente desbalanceados. | Lectura espacial deficiente; zonas excesivamente oscuras sin detalle o iluminación plana que debilita la tridimensionalidad del interior. | Espacio interior sin profundidad, sobreexpuesto en su totalidad o en penumbra ilegible por falta de rebotes. | **/ 15 pts** |
| **3. Uso Correcto de Fuentes de Luz (30%)** | Selección idónea de emisores (Rect Lights en vanos, Point/Spot con Source Radius en bombillas). Jerarquía clara según Brejon. Atenuación física realista, sombras suaves/duras calibradas y contraste térmico impecable (Kelvin). | Tipos de luces adecuados y bien posicionados, pero con desajustes menores en radio de atenuación, sombras ligeramente duras o temperaturas de color desbalanceadas. | Uso incorrecto de tipos de luz (ej. Point Lights en ventanas), sombras con artefactos o valores de intensidad arbitrarios sin jerarquía física. | Luces incoherentes, fugas de luz (*light leaks*) a través de muros o esquema plano sin emisores justificados. | **/ 18 pts** |
| **4. Intención Narrativa y Atmósfera (20%)** | Atmósfera dramática definida y envolvente (tensión, calidez, melancolía, etc.). Punto focal nítido donde la luz guía la mirada de forma orgánica hacia el centro de interés. Niebla volumétrica usada con sentido estético. | Atmósfera presente y perceptible, pero el punto focal compite con otros brillos secundarios o la niebla volumétrica satura ligeramente el encuadre. | Intención confusa; la iluminación no transmite un tono emocional claro ni logra conducir la atención hacia un elemento protagónico. | Escena sin atmósfera ni intención narrativa; iluminación puramente utilitaria sin propósito estético ni jerarquía visual. | **/ 12 pts** |
| **5. Nomenclatura, Orden y Entregables (10%)** | Nomenclatura oficial UE5 respetada en la totalidad de actores. Outliner limpio organizado en carpetas temáticas. Post-Process calibrado sin quemar blancos. Cuatro capturas HD y lámina entregadas impecablemente. | Proyecto ordenado con descuidos menores en nombres de luces o carpetas. Post-Process correcto y capturas completas. | Desorden notorio en Outliner (nombres por defecto `PointLight_1`), falta una captura solicitada o exposición inestable. | Proyecto desorganizado, archivos faltantes, sin carpetas ni nomenclatura estándar, o faltan entregables clave. | **/ 6 pts** |

---

## Tabla de Conversión de Puntaje a Nota (Escala 1.0 – 7.0 al 60% de Exigencia)

| Puntaje | Nota | Nivel de Desempeño y Criterio Académico |
| :---: | :---: | :--- |
| **60** | **7.0** | **Sobresaliente**: Dominio técnico impecable, análisis cinematográfico de referencia y ambientación espacial profesional. |
| **54 – 59** | **6.3 – 6.9** | **Muy Bueno**: Excelente réplica de iluminación y moodboard sólido con observaciones menores de ajuste. |
| **48 – 53** | **5.5 – 6.1** | **Bueno**: Cumplimiento consistente de todos los requerimientos de iluminación interior y narrativa. |
| **42 – 47** | **4.8 – 5.4** | **Aceptable**: Cumple los objetivos básicos pero requiere afinar la calibración de sombras, intensidades o jerarquía. |
| **36 – 41** | **4.0 – 4.6** | **Aprobado (Corte 60%)**: Cumplimiento mínimo de los aspectos esenciales de la escena y moodboard. |
| **24 – 35** | **3.0 – 3.9** | **Reprobado**: Falencias graves en la jerarquía lumínica, ausencia de análisis de referencia o espacialidad deficiente. |
| **0 – 23** | **1.0 – 2.9** | **Insuficiente**: Entrega incompleta, no cumple requisitos mínimos o no fue presentada dentro del plazo. |
