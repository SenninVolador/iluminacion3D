# Rúbrica de Evaluación: Entrega N°3 (Avance de Examen)

Iluminación 3D · Docente Daniel Rojas (UNIACC)

Prototipo de Estilo Visual (*LookDev*), Shaders NPR / Estilizados y Prueba de Iluminación (Proyectos 3D y 2D).

---

## Información General de la Evaluación

* **Puntaje Total**: 60 puntos
* **Escala de Calificación**: 1.0 a 7.0 (Exigencia del 60% para nota 4.0 = 36 puntos)
* **Modalidad**: Aplicable a proyectos 3D y 2D (vinculado al proyecto de juego desarrollado transversalmente en otros ramos)
* **Documentos de Evaluación**: 
  * [Descargar Rúbrica Oficial en PDF](/Rubrica_Entrega_03.pdf)
  * <a href="/iluminacion3D/Rubrica_Evaluacion_Entrega_03.xlsx" download>Descargar Planilla de Calificación en Formato Excel (.xlsx)</a>

---

## Descripción del Encargo

La **Entrega N°3** constituye el **avance técnico y estético directo hacia el Examen Final**. Su propósito es definir, construir y validar la identidad visual del videojuego que el estudiante o equipo se encuentra desarrollando en paralelo con otras asignaturas, mediante una etapa formal de ***Look Development (LookDev)* y prototipado de estilo (NPR / Estilizado)**.

En lugar de exigir el nivel completo terminado, el estudiante debe presentar:
1. **Una investigación de referencias multimediales**: Referentes de shaders e iluminación en videojuegos, sumados obligatoriamente a **referencias de otros medios** (cine, animación tradicional o 3D, cómic, ilustración, pintura o fotografía) explicando qué rasgo visual buscan extraer.
2. **La creación e implementación del estilo en uno o varios modelos/sprites de prueba (*Test Bench*)**: Construir el shader principal (ej. *Cel Shading*, *Outline*, tramas *Halftone/Hatching*, *Fresnel* estilizado en 3D; o *Normal Maps 2D*, emisión, contorno y reacción lumínica en 2D) y someterlo a un esquema de luces controlado para comprobar cómo se comporta antes de propagarlo al juego final.

---

## Equivalencia Técnica: Proyectos 3D vs. Proyectos 2D

| Componente | Proyecto 3D | Proyecto 2D |
| :--- | :--- | :--- |
| **1. Referencias y Moodboard** | Referencias de shaders 3D, iluminación espacial y medios externos (cine, animación, ilustración, cómic). | Referencias de tratamiento de color y luz en 2D, efectos sobre sprites y medios externos (animación 2D, pintura, grabado, vitrales). |
| **2. Creación de Shaders / Materiales** | Shader NPR o estilizado (ej. *Cel Shading* con rampa de corte, *Outlines*, *Fresnel*, achurado *Hatching*, *Subsurface* artístico o PBR estilizado parametrizado). | Shader aplicado a Sprites/Tilemaps (ej. mapas de normales 2D para reacción volumétrica a la luz, contornos, emisión dinámica, agua/distorsión o paletas indexadas). |
| **3. Prueba de Iluminación en Test** | Escena de laboratorio con 1 o más modelos 3D donde se pruebe la respuesta del shader ante cambios de dirección, color (Kelvin) e intensidad de luces (Key, Fill, Rim). | Escena de laboratorio con sprites/escenario de prueba donde se valide la reacción a luces 2D (`Light2D` / `Point` / `Spot`), sombras 2D (*Light Occluders*) y contraste cromático. |

---

## Requisitos de Entrega

1. **Lámina o Documento de LookDev y Referencias (20%)**:
   * Moodboard estructurado en tres bloques claros:
     1. Referencias de **Shaders / Materiales** en videojuegos.
     2. Referencias de **Iluminación y Atmósfera** en videojuegos.
     3. Referencias de **Otros Medios** (cine, animación, pintura, cómic, ilustración), indicando explícitamente qué característica técnica se busca traducir al motor.
2. **Creación del Shader / Material de Estilo (35%)**:
   * Grafo nodal funcional (Master Material e Instancia) con **parámetros expuestos** que permitan ajustar el estilo en tiempo real (ej. dureza del corte de sombra, color de la penumbra, grosor de línea, intensidad de contorno o relieve del mapa normal).
3. **Escena de Prueba (*Test Bench*) con Iluminación (30%)**:
   * Uno o varios modelos 3D (o sprites/escena 2D) dispuestos en un entorno de prueba dentro del motor.
   * Esquema de iluminación configurado para demostrar cómo responde el material ante luces principales, de relleno y de contorno/acento.
4. **Orden Técnico, Nomenclatura y Presentación (15%)**:
   * Nodos del shader ordenados y comentados por bloques lógicos.
   * Nomenclatura correcta de archivos y carpetas en el motor.
5. **Entregables Finales**:
   * Lámina de Referencias y LookDev (PDF o PNG en alta resolución).
   * Proyecto ejecutable en el motor abierto durante la revisión en sala (más respaldo empaquetado).
   * Tres (3) a cuatro (4) capturas técnicas en alta resolución:
     1. Render del modelo o sprite de prueba con el estilo final e iluminación activa.
     2. Comparativa del mismo modelo/sprite con material básico por defecto vs. con el shader NPR/estilizado aplicado.
     3. Captura legible del grafo de nodos del Shader mostrando sus bloques comentados.
     4. Captura del panel de la Instancia de Material mostrando los parámetros expuestos.

---

## Ponderación General de Criterios

| Criterio de Evaluación | Ponderación (%) | Puntaje Asignado |
| :--- | :---: | :---: |
| **1. Referencias de Shaders, Luz y Otros Medios** | **20%** | **12 puntos** |
| **2. Creación del Shader / Material de Estilo (NPR / 2D / 3D)** | **35%** | **21 puntos** |
| **3. Prueba de Iluminación sobre Modelos / Sprites de Test** | **30%** | **18 puntos** |
| **4. Orden del Grafo, Nomenclatura y Presentación** | **15%** | **9 puntos** |
| **TOTAL** | **100%** | **60 puntos** |

---

## Matriz de Evaluación Detallada (60 Puntos)

| Criterio | Excelente (100%) | Bueno (75%) | Suficiente (50%) | Insuficiente (0-25%) | Puntaje |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **1. Referencias de Shaders, Luz y Otros Medios (20%)** | Moodboard completo y riguroso que integra referencias de shaders, iluminación y **otros medios externos** (cine, animación, arte). Explica con claridad qué rasgos técnicos y estéticos se extraen hacia el prototipo. | Incluye referencias de videojuegos y de otros medios bien seleccionadas, pero el desglose técnico de cómo traducirlas al motor es general o poco específico. | Moodboard incompleto (omite referencias de otros medios o de shaders) o presenta imágenes sueltas sin justificación ni conexión clara con el estilo buscado. | No presenta lámina de referencias o las imágenes no guardan relación alguna con el prototipo presentado. | **/ 12 pts** |
| **2. Creación del Shader / Material de Estilo (35%)** | Construye un shader NPR o estilizado (3D o 2D) sólido, bien resuelto matemáticamente y coherente con la referencia. Expone múltiples parámetros funcionales en instancia para controlar el estilo en tiempo real. | El shader logra el estilo propuesto y cuenta con parámetros expuestos, pero presenta detalles menores de calibración visual o poca flexibilidad en sus controles. | Shader demasiado básico o con errores de construcción nodal; carece de instancias parametrizadas o no logra reproducir el estilo planteado en las referencias. | No construye un shader propio (utiliza materiales por defecto sin trabajar) o el grafo se encuentra roto/no funcional. | **/ 21 pts** |
| **3. Prueba de Iluminación en Modelos/Sprites de Test (30%)** | Implementa el estilo en uno o varios modelos/sprites de test bajo un esquema de luces intencionado. Demuestra con éxito cómo reacciona el shader ante la dirección, intensidad y temperatura de color de las fuentes. | El estilo está aplicado en el modelo/sprite de prueba con una iluminación funcional, aunque falta refinar el contraste de sombras o la separación respecto al fondo. | La iluminación de prueba es plana o arbitraria y no permite apreciar correctamente el comportamiento del shader ni el volumen del modelo/sprite. | No existe escena de prueba iluminada o las luces destruyen por completo la lectura del material (sobreexposición o penumbra total). | **/ 18 pts** |
| **4. Orden del Grafo, Nomenclatura y Presentación (15%)** | Grafo de nodos limpio, alineado y documentado con cajas de comentario. Nomenclatura estándar respetada en todos los activos. Entrega todas las capturas comparativas requeridas. | Proyecto y grafo comprensibles con descuidos menores en los nombres de algunos archivos o falta de comentarios en secciones secundarias del nodo. | Desorden evidente en el grafo de nodos ("espagueti" sin comentar), nombres por defecto (`NewMaterial`) o faltan capturas técnicas del desglose. | Proyecto desorganizado, sin convenciones de nombres, archivos rotos o entrega incompleta de respaldos visuales. | **/ 9 pts** |

---

## Tabla de Conversión de Puntaje a Nota (Escala 1.0 – 7.0 al 60% de Exigencia)

| Puntaje | Nota | Nivel de Desempeño y Criterio Académico |
| :---: | :---: | :--- |
| **60** | **7.0** | **Sobresaliente**: Investigación visual impecable, shader estilizado robusto y prueba de iluminación altamente expresiva. |
| **54 – 59** | **6.3 – 6.9** | **Muy Bueno**: Prototipo de estilo muy bien logrado con observaciones mínimas de ajuste en parámetros o luces. |
| **48 – 53** | **5.5 – 6.1** | **Bueno**: Cumplimiento consistente de la dirección de arte técnico, shader funcional y buena respuesta lumínica. |
| **42 – 47** | **4.8 – 5.4** | **Aceptable**: Cumple los objetivos base del prototipo pero requiere afinar la construcción del shader o la luz para el examen. |
| **36 – 41** | **4.0 – 4.6** | **Aprobado (Corte 60%)**: Cumplimiento mínimo de los aspectos esenciales de referencia, material y prueba de luz. |
| **24 – 35** | **3.0 – 3.9** | **Reprobado**: Falencias graves en el desarrollo del shader, ausencia de referencias multimediales o prueba lumínica deficiente. |
| **0 – 23** | **1.0 – 2.9** | **Insuficiente**: Entrega incompleta, no cumple requisitos mínimos o no fue presentada dentro del plazo. |
