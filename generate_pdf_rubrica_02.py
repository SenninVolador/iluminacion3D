import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

PDF_PATH = r"c:\Users\danie\OneDrive\Escritorio\Iluminacion3D\Rubrica_Entrega_02.pdf"

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

    # Typography Styles
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
        alignment=1, # Center
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
            Paragraph(f"EVALUACIÓN N° 02 — PÁGINA {page_num} DE 2", meta_right)
        ]]
        t = Table(header_data, colWidths=[300, 207])
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
            Paragraph("Rúbrica de Evaluación Oficial · Entrega 2: Iluminación de Interior", footer_right)
        ]]
        t = Table(foot_data, colWidths=[320, 187])
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

    story.append(Paragraph("Rúbrica de Evaluación: Iluminación de Interiores, Moodboard y Réplica", h1_style))
    story.append(Paragraph("Evaluación de iluminación interior en Unreal Engine 5 basada en la metodología de Chris Brejon. Analiza referencias visuales de cine o videojuegos, justificación física/narrativa de emisores y tratamiento de luz indirecta (Lumen).", desc_style))

    # Info summary table
    info_data = [
        [
            Paragraph("<b>Puntaje Total:</b> 60 Puntos<br/><b>Exigencia:</b> 60% (Nota 4.0 = 36 pts)", body_style),
            Paragraph("<b>Escala:</b> 1.0 a 7.0<br/><b>Moodboard:</b> 15% (9 Puntos)", body_style),
            Paragraph("<b>Entregables:</b> Lámina Moodboard/Análisis + Nivel UE5 + 4 Capturas HD (Lit, Comparativa, Detail, Outliner)", body_style)
        ]
    ]
    t_info = Table(info_data, colWidths=[150, 140, 217])
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

    story.append(Paragraph("1. Ponderación General de Criterios (Total 100% = 60 Puntos)", h2_style))

    ponderacion_data = [
        [
            Paragraph("<b>Criterio</b>", table_header_style),
            Paragraph("<b>Ponderación</b>", table_header_style),
            Paragraph("<b>Puntaje</b>", table_header_style),
            Paragraph("<b>Foco Formativo y Descripción</b>", table_header_style)
        ],
        [
            Paragraph("1. Referencias y Moodboard", table_cell_style),
            Paragraph("<b>15%</b>", table_score_style),
            Paragraph("<b>9 pts</b>", table_score_style),
            Paragraph("Recopilación estructurada de referencias de cine/videojuegos AAA y desglose analítico de fuentes.", table_cell_style)
        ],
        [
            Paragraph("2. Iluminación Interior y Espacialidad", table_cell_style),
            Paragraph("<b>25%</b>", table_score_style),
            Paragraph("<b>15 pts</b>", table_score_style),
            Paragraph("Lectura volumétrica del recinto, profundidad de planos, luz motivada exterior y rebotes GI/Lumen.", table_cell_style)
        ],
        [
            Paragraph("3. Uso Correcto de Fuentes de Luz", table_cell_style),
            Paragraph("<b>30%</b>", table_score_style),
            Paragraph("<b>18 pts</b>", table_score_style),
            Paragraph("Emisores idóneos (Rect/Point/Spot), jerarquía Brejon, intensidades físicas, penumbras y Kelvin.", table_cell_style)
        ],
        [
            Paragraph("4. Intención Narrativa y Atmósfera", table_cell_style),
            Paragraph("<b>20%</b>", table_score_style),
            Paragraph("<b>12 pts</b>", table_score_style),
            Paragraph("Atmósfera dramática definida, dirección intencionada de la mirada al punto focal y niebla coherente.", table_cell_style)
        ],
        [
            Paragraph("5. Nomenclatura, Orden y Entregables", table_cell_style),
            Paragraph("<b>10%</b>", table_score_style),
            Paragraph("<b>6 pts</b>", table_score_style),
            Paragraph("Nomenclatura técnica oficial Epic Games, Outliner en carpetas, PPV calibrado y 4 capturas HD.", table_cell_style)
        ]
    ]

    t_pond = Table(ponderacion_data, colWidths=[130, 60, 47, 270])
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
    story.append(Spacer(1, 10))

    story.append(Paragraph("2. Criterios de Referencias y Espacialidad Interior (24 Puntos)", h2_style))

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
            Paragraph("<b>1. Referencias y Moodboard</b><br/>(15% del total)", table_cell_style),
            Paragraph("Moodboard estructurado con referencias de alta calidad. Desglose riguroso de fuentes, temperatura Kelvin y clave tonal. La escena 3D refleja fielmente la dirección visual propuesta.", table_cell_style),
            Paragraph("Moodboard completo pero con desglose técnico elemental o leve discrepancia en la traslación de la paleta y contrastes a la escena 3D.", table_cell_style),
            Paragraph("Moodboard escaso o desorganizado; recopilación de imágenes aisladas sin análisis de fuentes ni intención clara.", table_cell_style),
            Paragraph("No presenta moodboard o incluye imágenes no pertinentes sin relación con la escena desarrollada.", table_cell_style),
            Paragraph("<b>/ 9</b>", table_score_style)
        ],
        [
            Paragraph("<b>2. Iluminación Interior</b><br/>(25% del total)", table_cell_style),
            Paragraph("Recinto con excelente lectura volumétrica y planos de profundidad. Luz motivada por aberturas. Rebotes indirectos creíbles (Lumen) sin empastar sombras ni lavar negros.", table_cell_style),
            Paragraph("Espacio bien iluminado con sensación de volumen, aunque con leve aplanamiento en rincones o rebotes ligeramente desbalanceados.", table_cell_style),
            Paragraph("Lectura espacial deficiente; zonas excesivamente oscuras sin detalle o iluminación plana que debilita la tridimensionalidad.", table_cell_style),
            Paragraph("Espacio interior sin profundidad, sobreexpuesto en su totalidad o en penumbra ilegible por falta de rebotes.", table_cell_style),
            Paragraph("<b>/ 15</b>", table_score_style)
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
    story.append(Spacer(1, 14))
    story.append(get_footer(1))

    # ================= PAGE 2 =================
    story.append(PageBreak())
    story.append(get_header(2))
    story.append(Spacer(1, 8))

    story.append(Paragraph("3. Criterios Técnicos, Narrativos y de Estructura (36 Puntos)", h2_style))

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
            Paragraph("<b>3. Uso Correcto de Luces</b><br/>(30% del total)", table_cell_style),
            Paragraph("Emisores idóneos (Rect en vanos, Point/Spot con Source Radius). Jerarquía Brejon clara. Atenuación física realista, sombras calibradas y balance térmico Kelvin impecable.", table_cell_style),
            Paragraph("Tipos de luces adecuados y bien ubicados, pero con desajustes menores en radio de atenuación, sombras algo duras o leve desbalance Kelvin.", table_cell_style),
            Paragraph("Uso incorrecto de tipos de luz (Point en ventanas), sombras con artefactos o intensidades arbitrarias sin jerarquía.", table_cell_style),
            Paragraph("Luces incoherentes, fugas de luz (light leaks) a través de muros o esquema plano sin fuentes justificadas.", table_cell_style),
            Paragraph("<b>/ 18</b>", table_score_style)
        ],
        [
            Paragraph("<b>4. Intención y Atmósfera</b><br/>(20% del total)", table_cell_style),
            Paragraph("Atmósfera dramática definida y envolvente. Punto focal nítido donde la luz guía la mirada de forma orgánica hacia el centro de interés. Niebla volumétrica con sentido estético.", table_cell_style),
            Paragraph("Atmósfera perceptible, pero el punto focal compite con otros brillos secundarios o la niebla satura ligeramente el encuadre.", table_cell_style),
            Paragraph("Intención confusa; la iluminación no transmite un tono emocional claro ni logra conducir la atención hacia un elemento protagónico.", table_cell_style),
            Paragraph("Escena sin atmósfera ni intención narrativa; iluminación puramente utilitaria sin propósito estético ni jerarquía visual.", table_cell_style),
            Paragraph("<b>/ 12</b>", table_score_style)
        ],
        [
            Paragraph("<b>5. Nomenclatura y Orden</b><br/>(10% del total)", table_cell_style),
            Paragraph("Nomenclatura oficial UE5 respetada. Outliner organizado en carpetas temáticas. PPV calibrado sin quemar blancos. Cuatro capturas HD y lámina entregadas impecablemente.", table_cell_style),
            Paragraph("Proyecto ordenado con descuidos menores en nombres de luces o carpetas. Post-Process correcto y capturas completas.", table_cell_style),
            Paragraph("Desorden notorio en Outliner (nombres por defecto PointLight_1), falta una captura solicitada o exposición inestable.", table_cell_style),
            Paragraph("Proyecto desorganizado, archivos faltantes, sin carpetas ni nomenclatura estándar, o faltan entregables clave.", table_cell_style),
            Paragraph("<b>/ 6</b>", table_score_style)
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
    story.append(Spacer(1, 10))

    story.append(Paragraph("4. Escala de Calificación Oficial (Escala 1.0 – 7.0 al 60% de Exigencia)", h2_style))

    escala_data = [
        [
            Paragraph("<b>Puntaje</b>", table_header_style),
            Paragraph("<b>Nota</b>", table_header_style),
            Paragraph("<b>Nivel de Desempeño y Criterio Académico</b>", table_header_style)
        ],
        [
            Paragraph("60 pts", table_cell_style),
            Paragraph("<b>7.0</b>", table_score_style),
            Paragraph("<b>Sobresaliente:</b> Dominio técnico impecable, análisis cinematográfico y ambientación interior profesional.", table_cell_style)
        ],
        [
            Paragraph("54 – 59 pts", table_cell_style),
            Paragraph("<b>6.3 – 6.9</b>", table_score_style),
            Paragraph("<b>Muy Bueno:</b> Excelente réplica de iluminación y moodboard sólido con observaciones mínimas de ajuste.", table_cell_style)
        ],
        [
            Paragraph("48 – 53 pts", table_cell_style),
            Paragraph("<b>5.5 – 6.1</b>", table_score_style),
            Paragraph("<b>Bueno:</b> Cumplimiento consistente de todos los requerimientos de iluminación interior y narrativa.", table_cell_style)
        ],
        [
            Paragraph("42 – 47 pts", table_cell_style),
            Paragraph("<b>4.8 – 5.4</b>", table_score_style),
            Paragraph("<b>Aceptable:</b> Cumple los objetivos básicos pero requiere afinar la calibración de sombras o jerarquía.", table_cell_style)
        ],
        [
            Paragraph("36 – 41 pts", table_cell_style),
            Paragraph("<b>4.0 – 4.6</b>", table_score_style),
            Paragraph("<b>Aprobado (Corte 60%):</b> Cumplimiento mínimo de los aspectos esenciales de la escena y moodboard.", table_cell_style)
        ],
        [
            Paragraph("24 – 35 pts", table_cell_style),
            Paragraph("<b>3.0 – 3.9</b>", table_score_style),
            Paragraph("<b>Reprobado:</b> Falencias graves en la jerarquía lumínica, ausencia de análisis de referencia o espacialidad deficiente.", table_cell_style)
        ],
        [
            Paragraph("0 – 23 pts", table_cell_style),
            Paragraph("<b>1.0 – 2.9</b>", table_score_style),
            Paragraph("<b>Insuficiente:</b> Entrega incompleta, no cumple requisitos mínimos o no fue presentada dentro del plazo.", table_cell_style)
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

    story.append(Spacer(1, 14))
    story.append(get_footer(2))

    doc.build(story)
    print(f"Rubric PDF generated at: {PDF_PATH}")

if __name__ == "__main__":
    create_pdf()
