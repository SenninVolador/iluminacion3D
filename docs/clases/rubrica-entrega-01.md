# Rúbrica de Evaluación: Entrega N°1

Cátedra de Iluminación 3D · Docente Daniel Rojas (UNIACC)

Estudio de Iluminación de 3 Puntos y Shader Paramétrico PBR en Unreal Engine 5.

---

## Información General de la Evaluación

* **Puntaje Total**: 60 puntos
* **Escala de Calificación**: 1.0 a 7.0 (Exigencia del 60% para nota 4.0 = 36 puntos)
* **Software Requerido**: Unreal Engine 5
* **Documento para Descarga**: [Descargar Rúbrica Oficial en PDF](/Rubrica_Entrega_01.pdf)

---

## 🎯 Descripción del Encargo

El estudiante debe configurar un **estudio de iluminación de 3 puntos (Key, Fill, Rim)** sobre un elemento central (busto o prop 3D) dentro de un nivel vacío en Unreal Engine 5. 

Adicionalmente, deberá construir y asignar un **Master Material PBR** que disponga de al menos **tres (3) parámetros expuestos** en una **Instancia de Material (`MI_...`)**, demostrando control sobre la respuesta física de la superficie y la jerarquía lumínica.

---

## 📦 Requisitos de Entrega

1. **Escena en Unreal Engine 5**: Nivel limpio con fondo neutro o ciclorama oscuro y cámara encuadrada.
2. **Esquema de 3 Puntos**: Tres emisores configurados con roles claros (Key Light, Fill Light y Rim Light).
3. **Shader PBR Parametrizado**:
   * Master Material (`M_Master_...`) estructurado con texturas asignadas.
   * Instancia de Material (`MI_...`) asignada a la malla con al menos 3 parámetros editables en tiempo real (ej. Rugosidad, Tinte de Color, Fuerza de Normales o UV Tiling).
4. **Entregables**:
   * Proyecto o nivel de Unreal Engine (`.uproject` o carpeta del mapa con assets).
   * Tres (3) capturas de pantalla en alta resolución:
     1. Render final con las 3 luces activas.
     2. Render en modo *Unlit* o vista del Shader Graph en el editor.
     3. Captura del panel de detalles de la Instancia de Material mostrando los parámetros expuestos.

---

## 📊 Matriz de Evaluación Detallada (60 Puntos)

| Criterio | Excelente (100%) | Bueno (75%) | Suficiente (50%) | Insuficiente (0-25%) | Puntaje |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **1. Key Light (Luz Principal)** | Posicionada a ~45° lateral y ~45° cenital. Define claramente el modelado volumétrico, contraste y dirección de las sombras principales sin sobreexponer. | Posicionada adecuadamente pero con leve descalibración de intensidad (zonas ligeramente quemadas o sombra poco definida). | Ubicación incorrecta o intensidad muy baja/alta, afectando la lectura del volumen del objeto. | Luz ausente, mal orientada o que no cumple el rol de emisor dominante. | **/ 7 pts** |
| **2. Fill Light (Luz de Relleno)** | Ubicada en el flanco opuesto. Intensidad calibrada (25-40% de la Key). Suaviza las sombras duras rescatando información sin generar sombras cruzadas evidentes. | Ubicada correctamente pero su intensidad compite con la Key Light (>50%) o es demasiado débil (<15%). | Genera sombras cruzadas notorias o no logra levantar la penumbra del lado oscuro. | Ausente o colocada en una posición errónea que anula el contraste del esquema. | **/ 7 pts** |
| **3. Rim Light (Contraluz / Contorno)** | Ubicada detrás del sujeto. Dibuja un filete brillante limpio y continuo en bordes y hombros, logrando una separación perfecta del fondo oscuro. | Presente y bien ubicada, pero con intensidad algo excesiva (quema el contorno) o tenue. | Posición deficiente; solo ilumina una fracción menor del borde sin lograr despegar el modelo. | Ausente o no genera contraste de silueta respecto al fondo. | **/ 6 pts** |
| **4. Material PBR y Texturizado** | Mapas de textura (BaseColor, Normal, ORM/Roughness/Metallic) asignados correctamente. Respuesta física coherente y verosímil según el tipo de material. | Texturas bien asignadas pero con leves desajustes en el balance de rugosidad o fuerza de normales. | Errores en la asignación de canales (ej. Normal Map invertido o rugosidad no calibrada). | Material plano sin mapas PBR o texturas con sombras pintadas a mano que rompen el PBR. | **/ 15 pts** |
| **5. Arquitectura del Shader e Instanciación** | Construcción correcta de Master Material (`M_...`) y derivación a Instancia (`MI_...`). Presenta **3 o más parámetros expuestos** y funcionales en tiempo real. | Presenta Master Material e Instancia, pero solo 2 parámetros funcionan correctamente o su nomenclatura es genérica. | Material con solo 1 parámetro expuesto o no utiliza el flujo de instancias (modifica el shader base). | No utiliza instancias de material ni expone parámetros escalares/vectoriales. | **/ 15 pts** |
| **6. Nomenclatura, Orden y Presentación** | Proyecto ordenado con nomenclatura estándar de la industria (`M_`, `MI_`, `T_`, `SM_`, `L_`). Outliner limpio con carpetas. Renders nítidos y bien encuadrados. | Proyecto comprensible pero con descuidos menores en nomenclatura o carpetas. | Desorden evidente en el árbol de contenido o nombres por defecto (`NewMaterial`, `PointLight1`). | Proyecto desorganizado, archivos rotos o faltan capturas solicitadas. | **/ 10 pts** |

---

## 📈 Tabla de Conversión de Puntaje a Nota (Escala 1.0 – 7.0 al 60%)

| Puntaje | Nota | Nivel de Desempeño |
| :---: | :---: | :--- |
| **60** | **7.0** | Sobresaliente: Dominio técnico impecable y acabado profesional. |
| **56 – 59** | **6.5 – 6.9** | Muy Bueno: Excelente ejecución con observaciones mínimas. |
| **50 – 55** | **5.8 – 6.4** | Bueno: Cumplimiento sólido de todos los requerimientos. |
| **44 – 49** | **5.0 – 5.6** | Aceptable: Cumple los requisitos con detalles de calibración. |
| **36 – 43** | **4.0 – 4.9** | Aprobado: Cumplimiento básico de los objetivos mínimos. |
| **28 – 35** | **3.3 – 3.9** | Reprobado: Falencias notorias en el esquema de luces o shader. |
| **18 – 27** | **2.5 – 3.2** | Insuficiente: Incumplimiento grave de los requisitos de entrega. |
| **0 – 17** | **1.0 – 2.4** | No evaluable: Entrega incompleta o fuera de plazo sin justificación. |
