import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

PDF_PATH = r"c:\Users\danie\OneDrive\Escritorio\Iluminacion3D\Rubrica_Entrega_01.pdf"

def create_pdf():
    # Margins: 48pt left/right, 40pt top/bottom
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        leftMargin=44,
        rightMargin=44,
        topMargin=38,
        bottomMargin=38
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
        fontSize=14,
        leading=18,
        textColor=c_black,
        spaceAfter=3
    )

    desc_style = ParagraphStyle(
        'MainDesc',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=c_gray_text,
        spaceAfter=10
    )

    h2_style = ParagraphStyle(
        'H2Sub',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12.5,
        textColor=c_black,
        spaceBefore=6,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=c_dark
    )

    table_header_style = ParagraphStyle(
        'THStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=c_black
    )

    table_cell_style = ParagraphStyle(
        'TDStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=9.5,
        textColor=c_dark
    )

    table_score_style = ParagraphStyle(
        'TDScore',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
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
            Paragraph(f"EVALUACIÓN N° 01 — PÁGINA {page_num} DE 2", meta_right)
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
            Paragraph("Rúbrica de Evaluación Oficial · Unreal Engine 5", footer_right)
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
    story.append(Spacer(1, 10))

    story.append(Paragraph("Rúbrica de Evaluación: Estudio 3-Point Lighting y Shader Paramétrico", h1_style))
    story.append(Paragraph("Evaluación práctica de estudio de iluminación de tres puntos, modelado de volumen, asignación de texturas PBR y parametrización de Master Materials e Instancias en Unreal Engine 5.", desc_style))

    # Info summary table
    info_data = [
        [
            Paragraph("<b>Puntaje Total:</b> 60 Puntos<br/><b>Exigencia:</b> 60% (Nota 4.0 = 36 pts)", body_style),
            Paragraph("<b>Escala:</b> 1.0 a 7.0<br/><b>Motor:</b> Unreal Engine 5", body_style),
            Paragraph("<b>Entregables:</b> Proyecto / Mapa limpio + 3 Capturas HD (Render final, Unlit/Shader, Panel MI)", body_style)
        ]
    ]
    t_info = Table(info_data, colWidths=[160, 140, 207])
    t_info.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_subtle),
        ('BOX', (0,0), (-1,-1), 0.7, c_border_card),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_info)
    story.append(Spacer(1, 10))

    story.append(Paragraph("1. Criterios de Iluminación de Tres Puntos (20 Puntos)", h2_style))

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
            Paragraph("<b>Key Light</b><br/>(Luz Principal)", table_cell_style),
            Paragraph("Ubicada a ~45° lateral y ~45° cenital. Define claramente el modelado volumétrico, contraste y dirección de sombras sin sobreexponer.", table_cell_style),
            Paragraph("Posicionada adecuadamente pero con leve descalibración de intensidad (zonas ligeramente quemadas o sombras débiles).", table_cell_style),
            Paragraph("Ubicación incorrecta o intensidad muy baja/alta, afectando la lectura del volumen del modelo 3D.", table_cell_style),
            Paragraph("Luz ausente, mal orientada o que no cumple el rol de emisor dominante del esquema.", table_cell_style),
            Paragraph("<b>/ 7</b>", table_score_style)
        ],
        [
            Paragraph("<b>Fill Light</b><br/>(Luz de Relleno)", table_cell_style),
            Paragraph("Ubicada en el flanco opuesto. Intensidad calibrada (25-40% de Key). Suaviza penumbras rescatando detalle sin sombras cruzadas.", table_cell_style),
            Paragraph("Ubicada correctamente pero su intensidad compite con Key (>50%) o es demasiado débil (<15%).", table_cell_style),
            Paragraph("Genera sombras cruzadas notorias o no logra levantar la penumbra del lado en sombra.", table_cell_style),
            Paragraph("Ausente o colocada en posición errónea que anula el contraste del esquema.", table_cell_style),
            Paragraph("<b>/ 7</b>", table_score_style)
        ],
        [
            Paragraph("<b>Rim Light</b><br/>(Contraluz)", table_cell_style),
            Paragraph("Ubicada detrás del sujeto. Dibuja un filete brillante limpio en bordes y hombros, logrando separación nítida del fondo oscuro.", table_cell_style),
            Paragraph("Presente y bien ubicada, pero con intensidad algo excesiva (quema el borde) o tenue.", table_cell_style),
            Paragraph("Posición deficiente; solo ilumina una fracción menor del contorno sin lograr despegar el modelo.", table_cell_style),
            Paragraph("Ausente o no genera contraste de silueta respecto al fondo de la escena.", table_cell_style),
            Paragraph("<b>/ 6</b>", table_score_style)
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

    story.append(Paragraph("2. Resumen de Requisitos Técnicos Obligatorios", h2_style))
    reqs_text = """
    • <b>Escena:</b> Nivel limpio en Unreal Engine 5 con cámara encuadrada fija en el sujeto.<br/>
    • <b>Material PBR:</b> Master Material estructurado con BaseColor, Normal Map y Rugosidad/Metalicidad (ORM).<br/>
    • <b>Instancia Parametrizada:</b> Asignación de <code>MI_...</code> con al menos <b>3 parámetros expuestos</b> editables en tiempo real.
    """
    story.append(Paragraph(reqs_text, body_style))

    story.append(Spacer(1, 18))
    story.append(get_footer(1))

    # ================= PAGE 2 =================
    story.append(PageBreak())
    story.append(get_header(2))
    story.append(Spacer(1, 10))

    story.append(Paragraph("3. Criterios de Materiales, Shaders y Estructura (40 Puntos)", h2_style))

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
            Paragraph("<b>Material PBR y Texturizado</b>", table_cell_style),
            Paragraph("Mapas de textura (BaseColor, Normal, ORM) asignados correctamente. Respuesta física coherente y verosímil según el material.", table_cell_style),
            Paragraph("Texturas bien asignadas pero con leves desajustes en el balance de rugosidad o fuerza de normales.", table_cell_style),
            Paragraph("Errores en asignación de canales (Normal invertido, rugosidad no calibrada o mapa ausente).", table_cell_style),
            Paragraph("Material plano sin mapas PBR o texturas con sombras pintadas a mano que rompen el PBR.", table_cell_style),
            Paragraph("<b>/ 15</b>", table_score_style)
        ],
        [
            Paragraph("<b>Shader e Instancia (3+ Parámetros)</b>", table_cell_style),
            Paragraph("Master Material (<code>M_</code>) estructurado y derivado a Instancia (<code>MI_</code>). Presenta <b>3 o más parámetros expuestos</b> y funcionales.", table_cell_style),
            Paragraph("Master Material e Instancia correctos, pero solo 2 parámetros funcionan o nomenclatura genérica.", table_cell_style),
            Paragraph("Material con solo 1 parámetro expuesto o modifica el shader base sin usar el flujo de instancias.", table_cell_style),
            Paragraph("No utiliza instancias de material ni expone parámetros escalares/vectoriales funcionales.", table_cell_style),
            Paragraph("<b>/ 15</b>", table_score_style)
        ],
        [
            Paragraph("<b>Nomenclatura y Presentación</b>", table_cell_style),
            Paragraph("Nomenclatura estándar (<code>M_</code>, <code>MI_</code>, <code>T_</code>, <code>SM_</code>, <code>L_</code>). Outliner ordenado en carpetas. Renders nítidos y bien encuadrados.", table_cell_style),
            Paragraph("Proyecto comprensible pero con descuidos menores en nomenclatura o carpetas de contenido.", table_cell_style),
            Paragraph("Desorden evidente en el árbol de contenido o nombres por defecto (<code>NewMaterial</code>, <code>PointLight1</code>).", table_cell_style),
            Paragraph("Proyecto desorganizado, archivos rotos o faltan capturas solicitadas en la entrega.", table_cell_style),
            Paragraph("<b>/ 10</b>", table_score_style)
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
    story.append(Spacer(1, 14))

    story.append(Paragraph("4. Escala de Calificación (Escala 1.0 – 7.0 al 60% de Exigencia)", h2_style))

    escala_data = [
        [
            Paragraph("<b>Puntaje</b>", table_header_style),
            Paragraph("<b>Nota</b>", table_header_style),
            Paragraph("<b>Nivel de Desempeño y Criterio Académico</b>", table_header_style)
        ],
        [
            Paragraph("60 pts", table_cell_style),
            Paragraph("<b>7.0</b>", table_score_style),
            Paragraph("<b>Sobresaliente:</b> Dominio técnico impecable, calibración lumínica y shader profesional.", table_cell_style)
        ],
        [
            Paragraph("54 – 59 pts", table_cell_style),
            Paragraph("<b>6.3 – 6.9</b>", table_score_style),
            Paragraph("<b>Muy Bueno:</b> Excelente ejecución técnica con observaciones mínimas de ajuste.", table_cell_style)
        ],
        [
            Paragraph("48 – 53 pts", table_cell_style),
            Paragraph("<b>5.5 – 6.1</b>", table_score_style),
            Paragraph("<b>Bueno:</b> Cumplimiento sólido de todos los requerimientos de entrega.", table_cell_style)
        ],
        [
            Paragraph("42 – 47 pts", table_cell_style),
            Paragraph("<b>4.8 – 5.4</b>", table_score_style),
            Paragraph("<b>Aceptable:</b> Cumple requisitos mínimos con detalles de calibración en luces o shader.", table_cell_style)
        ],
        [
            Paragraph("36 – 41 pts", table_cell_style),
            Paragraph("<b>4.0 – 4.6</b>", table_score_style),
            Paragraph("<b>Aprobado (Corte 60%):</b> Cumplimiento básico de los objetivos formativos.", table_cell_style)
        ],
        [
            Paragraph("24 – 35 pts", table_cell_style),
            Paragraph("<b>3.0 – 3.9</b>", table_score_style),
            Paragraph("<b>Reprobado:</b> Falencias notorias en el esquema de 3 puntos o shader no parametrizado.", table_cell_style)
        ],
        [
            Paragraph("0 – 23 pts", table_cell_style),
            Paragraph("<b>1.0 – 2.9</b>", table_score_style),
            Paragraph("<b>Insuficiente:</b> Entrega incompleta, no funcional o fuera de plazo.", table_cell_style)
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
    print(f"Rubric PDF generated at: {PDF_PATH}")

if __name__ == "__main__":
    create_pdf()
