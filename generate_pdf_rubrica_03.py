import shutil
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

PDF_PATH = r"c:\Users\danie\OneDrive\Escritorio\Iluminacion3D\Rubrica_Entrega_03.pdf"
PUBLIC_PDF_PATH = r"c:\Users\danie\OneDrive\Escritorio\Iluminacion3D\docs\public\Rubrica_Entrega_03.pdf"

def create_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        leftMargin=44,
        rightMargin=44,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Editorial Monochrome Palette
    c_black = colors.HexColor('#111827')
    c_dark = colors.HexColor('#1F2937')
    c_gray_text = colors.HexColor('#4B5563')
    c_gray_light = colors.HexColor('#9CA3AF')
    c_line = colors.HexColor('#E5E7EB')
    c_bg_subtle = colors.HexColor('#F9FAFB')
    c_border_card = colors.HexColor('#D1D5DB')

    h1_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=c_black,
        spaceAfter=3
    )

    desc_style = ParagraphStyle(
        'MainDesc',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=c_gray_text,
        spaceAfter=8
    )

    h2_style = ParagraphStyle(
        'H2Sub',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=c_black,
        spaceBefore=5,
        spaceAfter=3
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10.5,
        textColor=c_dark
    )

    table_header_style = ParagraphStyle(
        'THStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=c_black
    )

    table_cell_style = ParagraphStyle(
        'TDStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.8,
        leading=9,
        textColor=c_dark
    )

    table_score_style = ParagraphStyle(
        'TDScore',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        alignment=1,
        textColor=c_black
    )

    meta_left = ParagraphStyle(
        'MetaL',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=c_black
    )

    meta_right = ParagraphStyle(
        'MetaR',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        alignment=2,
        textColor=c_gray_light
    )

    footer_left = ParagraphStyle(
        'FootL',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=9,
        textColor=c_gray_light
    )

    footer_right = ParagraphStyle(
        'FootR',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=9,
        alignment=2,
        textColor=c_gray_light
    )

    def get_header(page_num):
        header_data = [[
            Paragraph("ILUMINACIÓN 3D · UNIACC", meta_left),
            Paragraph(f"EVALUACIÓN N° 03 (AVANCE DE EXAMEN) — PÁGINA {page_num} DE 2", meta_right)
        ]]
        t = Table(header_data, colWidths=[240, 267])
        t.setStyle(TableStyle([
            ('LINEBELOW', (0,0), (-1,-1), 1.2, c_black),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        return t

    def get_footer(page_num):
        foot_data = [[
            Paragraph("Iluminación 3D · Docente: Daniel Rojas (UNIACC)", footer_left),
            Paragraph("Rúbrica Oficial · Entrega 3: LookDev, NPR y Prototipo de Estilo (3D / 2D)", footer_right)
        ]]
        t = Table(foot_data, colWidths=[250, 257])
        t.setStyle(TableStyle([
            ('LINEABOVE', (0,0), (-1,-1), 0.5, c_line),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        return t

    story = []

    # ================= PAGE 1 =================
    story.append(get_header(1))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Rúbrica Entrega N°3: Prototipo de Estilo (LookDev), NPR y Test de Luz", h1_style))
    story.append(Paragraph("Avance de Examen Final. Evalúa la investigación de referencias (videojuegos y otros medios), la creación del shader/material de estilo (NPR/Estilizado en 3D o 2D) y su prueba de iluminación sobre modelos o sprites de test.", desc_style))

    info_data = [
        [
            Paragraph("<b>Puntaje Total:</b> 60 Puntos<br/><b>Exigencia:</b> 60% (Nota 4.0 = 36 pts)", body_style),
            Paragraph("<b>Escala:</b> 1.0 a 7.0<br/><b>Modalidad:</b> Proyectos 3D y 2D", body_style),
            Paragraph("<b>Entregables:</b> Lámina LookDev Multimedial + Escena Test en Motor + 4 Capturas Técnicas (Render, Comparativa, Grafo, Instancia)", body_style)
        ]
    ]
    t_info = Table(info_data, colWidths=[145, 130, 232])
    t_info.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_subtle),
        ('BOX', (0,0), (-1,-1), 0.7, c_border_card),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_info)
    story.append(Spacer(1, 8))

    story.append(Paragraph("1. Equivalencia Técnica de Evaluación: Proyectos 3D vs. Proyectos 2D", h2_style))

    equiv_data = [
        [
            Paragraph("<b>Componente</b>", table_header_style),
            Paragraph("<b>Proyecto en 3D</b>", table_header_style),
            Paragraph("<b>Proyecto en 2D</b>", table_header_style)
        ],
        [
            Paragraph("<b>Referencias</b>", table_cell_style),
            Paragraph("Shaders 3D, iluminación espacial y otros medios (cine, animación, cómic).", table_cell_style),
            Paragraph("Tratamiento de luz/color 2D, efectos en sprites y otros medios (pintura, animación 2D).", table_cell_style)
        ],
        [
            Paragraph("<b>Shader / Material</b>", table_cell_style),
            Paragraph("Shader NPR o estilizado (Cel Shading, Outline, Fresnel, Hatching, PBR artístico).", table_cell_style),
            Paragraph("Shader en Sprites/Tilemaps (Normal Maps 2D para volumen, emisión, contorno, distorsión).", table_cell_style)
        ],
        [
            Paragraph("<b>Prueba de Luz</b>", table_cell_style),
            Paragraph("Modelos de test bajo esquema de luces (Key/Fill/Rim) probando respuesta del shader.", table_cell_style),
            Paragraph("Sprites/escena de test bajo luces 2D (Light2D, oclusores de sombra 2D y color).", table_cell_style)
        ]
    ]
    t_eq = Table(equiv_data, colWidths=[85, 211, 211])
    t_eq.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_bg_subtle),
        ('GRID', (0,0), (-1,-1), 0.5, c_line),
        ('BOX', (0,0), (-1,-1), 0.8, c_black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_eq)
    story.append(Spacer(1, 8))

    story.append(Paragraph("2. Ponderación General de Criterios (Total 100% = 60 Puntos)", h2_style))

    ponderacion_data = [
        [
            Paragraph("<b>Criterio</b>", table_header_style),
            Paragraph("<b>Pond.</b>", table_header_style),
            Paragraph("<b>Pts</b>", table_header_style),
            Paragraph("<b>Foco Formativo y Alcance</b>", table_header_style)
        ],
        [
            Paragraph("1. Referencias de Shaders, Luz y Otros Medios", table_cell_style),
            Paragraph("<b>20%</b>", table_score_style),
            Paragraph("<b>12 pts</b>", table_score_style),
            Paragraph("Moodboard de videojuegos + otros medios (cine, animación, ilustración) y desglose técnico.", table_cell_style)
        ],
        [
            Paragraph("2. Creación del Shader / Material de Estilo", table_cell_style),
            Paragraph("<b>35%</b>", table_score_style),
            Paragraph("<b>21 pts</b>", table_score_style),
            Paragraph("Construcción del shader NPR/estilizado (3D o 2D) con parámetros expuestos en instancia.", table_cell_style)
        ],
        [
            Paragraph("3. Prueba de Iluminación en Modelos/Sprites Test", table_cell_style),
            Paragraph("<b>30%</b>", table_score_style),
            Paragraph("<b>18 pts</b>", table_score_style),
            Paragraph("Aplicación en escena de laboratorio probando reacción ante dirección, color e intensidad.", table_cell_style)
        ],
        [
            Paragraph("4. Orden del Grafo, Nomenclatura y Presentación", table_cell_style),
            Paragraph("<b>15%</b>", table_score_style),
            Paragraph("<b>9 pts</b>", table_score_style),
            Paragraph("Nodos comentados, nomenclatura estándar de activos y capturas comparativas completas.", table_cell_style)
        ]
    ]

    t_pond = Table(ponderacion_data, colWidths=[150, 45, 42, 270])
    t_pond.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_bg_subtle),
        ('GRID', (0,0), (-1,-1), 0.5, c_line),
        ('BOX', (0,0), (-1,-1), 0.8, c_black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_pond)
    story.append(Spacer(1, 8))

    story.append(Paragraph("3. Matriz de Evaluación — Parte I (33 Puntos)", h2_style))

    criterios_p1 = [
        [
            Paragraph("Criterio", table_header_style),
            Paragraph("Excelente (100%)", table_header_style),
            Paragraph("Bueno (75%)", table_header_style),
            Paragraph("Suficiente (50%)", table_header_style),
            Paragraph("Insuficiente (0-25%)", table_header_style),
            Paragraph("Pts", table_header_style)
        ],
        [
            Paragraph("<b>1. Referencias y Otros Medios</b><br/>(20% del total)", table_cell_style),
            Paragraph("Moodboard completo que integra referencias de shaders, luz y otros medios externos (cine, animación, arte). Explica con claridad qué rasgos técnicos se extraen.", table_cell_style),
            Paragraph("Incluye referencias de juegos y otros medios bien seleccionadas, pero el desglose técnico de cómo traducirlas es general.", table_cell_style),
            Paragraph("Moodboard incompleto (omite otros medios o shaders) o presenta imágenes sueltas sin justificación técnica clara.", table_cell_style),
            Paragraph("No presenta lámina de referencias o las imágenes no guardan relación con el prototipo.", table_cell_style),
            Paragraph("<b>/ 12</b>", table_score_style)
        ],
        [
            Paragraph("<b>2. Creación del Shader / Estilo</b><br/>(35% del total)", table_cell_style),
            Paragraph("Construye un shader NPR o estilizado (3D o 2D) sólido y fiel a la referencia. Expone múltiples parámetros funcionales en instancia para ajustar el estilo en vivo.", table_cell_style),
            Paragraph("El shader logra el estilo propuesto y expone parámetros, pero presenta detalles menores de calibración o poca flexibilidad.", table_cell_style),
            Paragraph("Shader básico o con errores nodales; carece de instancias parametrizadas o no logra reproducir el estilo planteado.", table_cell_style),
            Paragraph("No construye un shader propio (usa material por defecto) o el grafo se encuentra roto.", table_cell_style),
            Paragraph("<b>/ 21</b>", table_score_style)
        ]
    ]

    t_p1 = Table(criterios_p1, colWidths=[70, 110, 105, 105, 90, 27])
    t_p1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_bg_subtle),
        ('GRID', (0,0), (-1,-1), 0.5, c_line),
        ('BOX', (0,0), (-1,-1), 0.8, c_black),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_p1)
    story.append(Spacer(1, 10))
    story.append(get_footer(1))

    # ================= PAGE 2 =================
    story.append(PageBreak())
    story.append(get_header(2))
    story.append(Spacer(1, 8))

    story.append(Paragraph("4. Matriz de Evaluación — Parte II (27 Puntos)", h2_style))

    criterios_p2 = [
        [
            Paragraph("Criterio", table_header_style),
            Paragraph("Excelente (100%)", table_header_style),
            Paragraph("Bueno (75%)", table_header_style),
            Paragraph("Suficiente (50%)", table_header_style),
            Paragraph("Insuficiente (0-25%)", table_header_style),
            Paragraph("Pts", table_header_style)
        ],
        [
            Paragraph("<b>3. Prueba de Luz en Test</b><br/>(30% del total)", table_cell_style),
            Paragraph("Implementa el estilo en uno o varios modelos/sprites de test bajo un esquema de luces intencionado. Demuestra cómo reacciona el shader ante dirección, color e intensidad.", table_cell_style),
            Paragraph("El estilo está aplicado en el modelo/sprite de prueba con iluminación funcional, aunque falta refinar contraste o separación del fondo.", table_cell_style),
            Paragraph("La iluminación de prueba es plana o arbitraria y no permite apreciar bien el comportamiento del shader ni el volumen.", table_cell_style),
            Paragraph("No existe escena de prueba iluminada o las luces destruyen la lectura del material.", table_cell_style),
            Paragraph("<b>/ 18</b>", table_score_style)
        ],
        [
            Paragraph("<b>4. Orden del Grafo y Nomenclatura</b><br/>(15% del total)", table_cell_style),
            Paragraph("Grafo de nodos limpio, alineado y comentado por bloques. Nomenclatura estándar respetada en todos los activos. Entrega todas las capturas comparativas.", table_cell_style),
            Paragraph("Proyecto y grafo comprensibles con descuidos menores en nombres de archivos o falta de comentarios secundarios.", table_cell_style),
            Paragraph("Desorden evidente en el grafo de nodos, nombres por defecto (NewMaterial) o faltan capturas técnicas del desglose.", table_cell_style),
            Paragraph("Proyecto desorganizado, sin convenciones de nombres, archivos rotos o entrega incompleta.", table_cell_style),
            Paragraph("<b>/ 9</b>", table_score_style)
        ]
    ]

    t_p2 = Table(criterios_p2, colWidths=[70, 110, 105, 105, 90, 27])
    t_p2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_bg_subtle),
        ('GRID', (0,0), (-1,-1), 0.5, c_line),
        ('BOX', (0,0), (-1,-1), 0.8, c_black),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_p2)
    story.append(Spacer(1, 12))

    story.append(Paragraph("5. Escala de Calificación Oficial (Escala 1.0 – 7.0 al 60% de Exigencia)", h2_style))

    escala_data = [
        [
            Paragraph("<b>Puntaje</b>", table_header_style),
            Paragraph("<b>Nota</b>", table_header_style),
            Paragraph("<b>Nivel de Desempeño y Criterio Académico</b>", table_header_style)
        ],
        [
            Paragraph("60 pts", table_cell_style),
            Paragraph("<b>7.0</b>", table_score_style),
            Paragraph("<b>Sobresaliente:</b> Investigación visual impecable, shader estilizado robusto y prueba de luz expresiva.", table_cell_style)
        ],
        [
            Paragraph("54 – 59 pts", table_cell_style),
            Paragraph("<b>6.3 – 6.9</b>", table_score_style),
            Paragraph("<b>Muy Bueno:</b> Prototipo de estilo muy bien logrado con observaciones mínimas de ajuste.", table_cell_style)
        ],
        [
            Paragraph("48 – 53 pts", table_cell_style),
            Paragraph("<b>5.5 – 6.1</b>", table_score_style),
            Paragraph("<b>Bueno:</b> Cumplimiento consistente de la dirección de arte técnico, shader funcional y buena luz.", table_cell_style)
        ],
        [
            Paragraph("42 – 47 pts", table_cell_style),
            Paragraph("<b>4.8 – 5.4</b>", table_score_style),
            Paragraph("<b>Aceptable:</b> Cumple los objetivos base pero requiere afinar el shader o la luz para el examen.", table_cell_style)
        ],
        [
            Paragraph("36 – 41 pts", table_cell_style),
            Paragraph("<b>4.0 – 4.6</b>", table_score_style),
            Paragraph("<b>Aprobado (Corte 60%):</b> Cumplimiento mínimo de los aspectos esenciales de referencia, shader y luz.", table_cell_style)
        ],
        [
            Paragraph("24 – 35 pts", table_cell_style),
            Paragraph("<b>3.0 – 3.9</b>", table_score_style),
            Paragraph("<b>Reprobado:</b> Falencias graves en el desarrollo del shader, sin referencias multimediales o prueba deficiente.", table_cell_style)
        ],
        [
            Paragraph("0 – 23 pts", table_cell_style),
            Paragraph("<b>1.0 – 2.9</b>", table_score_style),
            Paragraph("<b>Insuficiente:</b> Entrega incompleta, no cumple requisitos mínimos o fuera de plazo.", table_cell_style)
        ]
    ]

    t_esc = Table(escala_data, colWidths=[65, 45, 397])
    t_esc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_bg_subtle),
        ('GRID', (0,0), (-1,-1), 0.5, c_line),
        ('BOX', (0,0), (-1,-1), 0.8, c_black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_esc)

    story.append(Spacer(1, 16))
    story.append(get_footer(2))

    doc.build(story)
    shutil.copyfile(PDF_PATH, PUBLIC_PDF_PATH)
    print(f"Rubric 03 PDF generated at: {PDF_PATH} and copied to {PUBLIC_PDF_PATH}")

if __name__ == "__main__":
    create_pdf()
