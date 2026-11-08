# Rúbrica de Evaluación: Examen Final

Iluminación 3D · Docente Daniel Rojas (UNIACC)

Implementación de Shaders, Materiales e Iluminación en el Proyecto de Juego (3D / 2D) y Artículo Técnico Estilo *80 Level (80.lv)*.

---

## Información General de la Evaluación

* **Puntaje Total**: 60 puntos
* **Escala de Calificación**: 1.0 a 7.0 (Exigencia del 60% para nota 4.0 = 36 puntos)
* **Modalidad**: Integración en el videojuego desarrollado transversalmente con otras asignaturas (3D o 2D)
* **Documentos de Evaluación**: 
  * [Descargar Rúbrica Oficial de Examen en PDF](/Rubrica_Examen_Final.pdf)
  * <a href="/iluminacion3D/Rubrica_Evaluacion_Examen_Final.xlsx" download>Descargar Planilla de Calificación en Formato Excel (.xlsx)</a>

---

## Descripción del Encargo

El **Examen Final** evalúa la culminación e integración en producción (*In-Game*) de todos los contenidos de la asignatura dentro del videojuego que los estudiantes desarrollan transversalmente con otros ramos del semestre.

A partir del prototipo de estilo (*LookDev* / NPR) validado en la Entrega N°3, el estudiante o equipo debe:
1. **Implementar los shaders y materiales definitivos** a lo largo de los personajes, elementos interactivos y escenarios del juego (tanto si el proyecto es **3D** como si es **2D**).
2. **Construir la iluminación completa del nivel jugable**, aplicando intención dramática, separación de planos de profundidad y **guía visual al jugador** (*Visual Leading*).
3. **Redactar un Artículo / Breakdown Técnico breve estilo *80 Level (80.lv)*** (de 2 a 3 páginas o formato post web), documentando visualmente cómo llegaron a su resultado final paso a paso.

---

## Estructura del Artículo / Breakdown Técnico Estilo *80.lv* (20%)

El documento técnico debe ser visual, directo y conciso (no un informe extenso de texto plano, sino una pieza de portafolio profesional donde las capturas comparativas expliquen el proceso). Debe incluir exactamente estas **4 secciones**:

1. **Dirección Visual y Referencias (El Punto de Partida)**
   * 1 párrafo introductorio + el Moodboard definitivo (videojuegos + cine/animación/ilustración).
   * Explicar qué rasgos estéticos y técnicos definieron la identidad visual del juego.
2. **Desglose de Shaders y Materiales (*Shader Breakdown*)**
   * Captura nítida del grafo de nodos con etiquetas indicando qué hace cada bloque clave (ej. *"Rampa de Cel Shading"*, *"Borde Fresnel"*, *"Normal Map 2D en Sprite"*).
   * Comparativa visual: **Asset con material base por defecto vs. Asset con el shader final aplicado** e instancias parametrizadas.
3. **Desglose de Iluminación Paso a Paso (*Lighting Passes*)**
   * Secuencia de 3 a 4 capturas desde el mismo encuadre del nivel mostrando cómo se construye la luz por capas:
     * **Paso 1**: Vista *Unlit* (solo color base / texturas sin luz).
     * **Paso 2**: Luz principal o ambiental base (*Natural / Key Light*).
     * **Paso 3**: Luces prácticas y de acento (lámparas, antorchas, neones, pantallas).
     * **Paso 4**: Toma final con atmósfera, niebla y *Post-Processing*.
4. **Guía al Jugador y Resolución de Problemas**
   * 1 párrafo breve explicando cómo utilizaron el contraste y el color para guiar al jugador por el nivel, y qué desafío técnico resolvieron durante la integración.

---

## Equivalencia de Evaluación en el Juego: 3D vs. 2D

| Aspecto Evaluado en el Examen | Proyecto de Juego 3D | Proyecto de Juego 2D |
| :--- | :--- | :--- |
| **1. Shaders y Materiales en el Nivel** | Aplicación del sistema de Master Materials e instancias (NPR / Cel Shading / PBR estilizado) en personajes, props y arquitectura del nivel sin materiales rotos ni por defecto. | Aplicación consistente de shaders 2D (mapas de normales 2D sobre sprites/tilemaps, shaders de agua/fuego, contornos, emisión o distorsión) integrados en la escena jugable. |
| **2. Iluminación e Intención en Juego** | Esquema de iluminación 3D (Natural, Practical, Dramatic), lectura de volúmenes, sombras calibradas, contraste térmico Kelvin y guía visual hacia objetivos o rutas. | Sistema de iluminación 2D (`Light2D` / luces puntuales y direccionales 2D, oclusores de sombra 2D), separación de capas *Parallax* por valor tonal y focos de atención para el jugador. |
| **3. Post-Procesado y Rendimiento** | *Post-Process Volume* (exposición controlada, *Bloom*, *Color Grading* / LUT), niebla volumétrica/exponencial y desempeño fluido sin sobrecoste de luces solapadas. | Post-procesado 2D (*Bloom* en emisivos, viñeteado, corrección cromática, niebla ambiental por capas), orden de carpetas y ejecución fluida en tiempo real. |

---

## Ponderación General de Criterios

| Criterio de Evaluación | Ponderación (%) | Puntaje Asignado |
| :--- | :---: | :---: |
| **1. Implementación de Shaders y Materiales en el Juego** | **30%** | **18 puntos** |
| **2. Iluminación del Nivel, Atmósfera y Guía al Jugador** | **35%** | **21 puntos** |
| **3. Artículo / Breakdown Técnico Estilo *80.lv*** | **20%** | **12 puntos** |
| **4. Post-Procesado, Coherencia y Orden Técnico** | **15%** | **9 puntos** |
| **TOTAL** | **100%** | **60 puntos** |

---

## Matriz de Evaluación Detallada (60 Puntos)

| Criterio | Excelente (100%) | Bueno (75%) | Suficiente (50%) | Insuficiente (0-25%) | Puntaje |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **1. Shaders y Materiales en el Juego (30%)** | El estilo de shaders y materiales (NPR / estilizado en 3D o 2D) está implementado con total consistencia en el nivel jugable. Uso correcto de instancias parametrizadas para dar variedad visual sin duplicar grafos. | Los shaders principales están bien integrados en el juego y cumplen el estilo propuesto, aunque algunos elementos secundarios del escenario conservan materiales genéricos o poco trabajados. | Implementación parcial; el shader solo se aplicó a un objeto aislado sin integrarse al resto del nivel, o presenta errores visuales notorios durante la ejecución. | No se implementaron shaders propios en el juego o los materiales están rotos/ausentes en la escena final. | **/ 18 pts** |
| **2. Iluminación del Nivel y Guía al Jugador (35%)** | Iluminación del nivel sobresaliente (3D o 2D). Construye una atmósfera envolvente, separa planos de profundidad con claridad y utiliza el contraste/temperatura para **guiar intuitivamente al jugador** en la escena. | Buena iluminación general y atmósfera lograda, pero la jerarquía visual compite en ciertas zonas del nivel o existen áreas puntuales demasiado oscuras/sobreexpuestas. | Iluminación plana o meramente utilitaria; ilumina el nivel para que se vea pero carece de intención narrativa, contraste térmico o dirección visual para el jugador. | Nivel sin trabajo de iluminación (luz por defecto del motor), sombras rotas o escena ilegible durante la partida. | **/ 21 pts** |
| **3. Breakdown Técnico Estilo *80.lv* (20%)** | Artículo visual impecable, claro y conciso. Incluye las 4 secciones completas: referencias multimediales, explicación del grafo del shader, secuencia paso a paso de capas de luz (*Lighting Passes*) y conclusión técnica. | Artículo completo y bien estructurado que explica cómo llegaron al resultado, aunque le falta mayor detalle en el desglose de nodos o en alguna captura intermedia de las capas de luz. | Documento incompleto o superficial; muestra capturas finales sin explicar el proceso técnico de cómo construyeron los shaders ni las capas de iluminación. | No entrega el Breakdown técnico o presenta un documento sin capturas del proceso ni explicación propia. | **/ 12 pts** |
| **4. Post-Procesado, Orden y Rendimiento (15%)** | Acabado final pulido mediante Post-Processing (color, exposición, *Bloom* y niebla controlada). Proyecto perfectamente ordenado con nomenclatura estándar y rendimiento fluido en tiempo real. | Post-procesado correcto y proyecto ordenado con descuidos menores de nomenclatura o leves caídas de rendimiento en sectores específicos. | Sin ajustes de post-procesado (exposición descontrolada), desorden evidente en las carpetas del motor o problemas de rendimiento por exceso de luces sin optimizar. | Proyecto desorganizado, archivos faltantes, sin post-procesado o el juego no logra ejecutarse de manera estable en la presentación. | **/ 9 pts** |

---

## Tabla de Conversión de Puntaje a Nota (Escala 1.0 – 7.0 al 60% de Exigencia)

| Puntaje | Nota | Nivel de Desempeño y Criterio Académico |
| :---: | :---: | :--- |
| **60** | **7.0** | **Sobresaliente**: Integración visual de nivel profesional en el juego y un Breakdown técnico digno de publicación en portafolio. |
| **54 – 59** | **6.3 – 6.9** | **Muy Bueno**: Excelente acabado de shaders e iluminación en el juego con observaciones mínimas de pulido. |
| **48 – 53** | **5.5 – 6.1** | **Bueno**: Cumplimiento sólido de la identidad visual en el nivel y documentación clara del proceso técnico. |
| **42 – 47** | **4.8 – 5.4** | **Aceptable**: Juego correctamente iluminado y con shaders funcionales, pero con detalles por afinar en guía visual o breakdown. |
| **36 – 41** | **4.0 – 4.6** | **Aprobado (Corte 60%)**: Cumplimiento mínimo de los objetivos de implementación en el juego y explicación del proceso. |
| **24 – 35** | **3.0 – 3.9** | **Reprobado**: Integración incompleta en el juego, ausencia de intención lumínica o falta del desglose técnico. |
| **0 – 23** | **1.0 – 2.9** | **Insuficiente**: Entrega incompleta, no cumple requisitos mínimos o no fue presentada en la instancia de examen. |
