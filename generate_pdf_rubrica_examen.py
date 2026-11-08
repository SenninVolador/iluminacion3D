import shutil
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

PDF_PATH = r"c:\Users\danie\OneDrive\Escritorio\Iluminacion3D\Rubrica_Examen_Final.pdf"
PUBLIC_PDF_PATH = r"c:\Users\danie\OneDrive\Escritorio\Iluminacion3D\docs\public\Rubrica_Examen_Final.pdf"

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
            Paragraph(f"EXAMEN FINAL SEMESTRAL — PÁGINA {page_num} DE 2", meta_right)
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
            Paragraph("Rúbrica Oficial · Examen Final: Integración en Juego y Breakdown 80.lv", footer_right)
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

    story.append(Paragraph("Rúbrica Examen Final: Integración en Juego y Breakdown Estilo 80.lv", h1_style))
    story.append(Paragraph("Evaluación de cierre semestral. Evalúa la implementación definitiva de shaders, materiales e iluminación dentro del proyecto de juego transversal (3D o 2D), junto con un artículo visual de desglose técnico estilo 80 Level.", desc_style))

    info_data = [
        [
            Paragraph("<b>Puntaje Total:</b> 60 Puntos<br/><b>Exigencia:</b> 60% (Nota 4.0 = 36 pts)", body_style),
            Paragraph("<b>Escala:</b> 1.0 a 7.0<br/><b>Modalidad:</b> Juego 3D o 2D", body_style),
            Paragraph("<b>Entregables:</b> Nivel Jugable Integrado en Motor + Artículo Breakdown Técnico Estilo 80.lv (2 a 3 páginas / Post visual)", body_style)
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

    story.append(Paragraph("1. Estructura del Artículo / Breakdown Técnico Estilo 80.lv (20% = 12 Puntos)", h2_style))

    breakdown_data = [
        [
            Paragraph("<b>Sección del Artículo</b>", table_header_style),
            Paragraph("<b>Contenido Visual y Explicación Requerida (Breve y al Grano)</b>", table_header_style)
        ],
        [
            Paragraph("<b>1. Dirección Visual y Referencias</b>", table_cell_style),
            Paragraph("1 párrafo + Moodboard definitivo (videojuegos + otros medios), explicando los rasgos estéticos y técnicos elegidos.", table_cell_style)
        ],
        [
            Paragraph("<b>2. Desglose de Shaders (Shader Breakdown)</b>", table_cell_style),
            Paragraph("Captura del grafo con bloques comentados + comparativa visual del asset sin shader vs. con el shader NPR/estilizado final.", table_cell_style)
        ],
        [
            Paragraph("<b>3. Capas de Luz (Lighting Passes)</b>", table_cell_style),
            Paragraph("Secuencia de 3 a 4 capturas del mismo encuadre: 1. Unlit -> 2. Luz Principal -> 3. Luces Prácticas/Acentos -> 4. Final con Post-Process.", table_cell_style)
        ],
        [
            Paragraph("<b>4. Guía al Jugador y Conclusión</b>", table_cell_style),
            Paragraph("1 párrafo explicando cómo la luz guía la mirada del jugador en el nivel y qué desafío técnico resolvieron en el desarrollo.", table_cell_style)
        ]
    ]
    t_bd = Table(breakdown_data, colWidths=[145, 362])
    t_bd.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_bg_subtle),
        ('GRID', (0,0), (-1,-1), 0.5, c_line),
        ('BOX', (0,0), (-1,-1), 0.8, c_black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_bd)
    story.append(Spacer(1, 8))

    story.append(Paragraph("2. Ponderación General de Criterios (Total 100% = 60 Puntos)", h2_style))

    ponderacion_data = [
        [
            Paragraph("<b>Criterio</b>", table_header_style),
            Paragraph("<b>Pond.</b>", table_header_style),
            Paragraph("<b>Pts</b>", table_header_style),
            Paragraph("<b>Foco Formativo y Alcance en Producción</b>", table_header_style)
        ],
        [
            Paragraph("1. Implementación de Shaders en el Juego", table_cell_style),
            Paragraph("<b>30%</b>", table_score_style),
            Paragraph("<b>18 pts</b>", table_score_style),
            Paragraph("Aplicación consistente de shaders e instancias (3D o 2D) en personajes, props y escenario.", table_cell_style)
        ],
        [
            Paragraph("2. Iluminación del Nivel y Guía al Jugador", table_cell_style),
            Paragraph("<b>35%</b>", table_score_style),
            Paragraph("<b>21 pts</b>", table_score_style),
            Paragraph("Atmósfera dramática, separación de planos de profundidad y conducción visual del jugador.", table_cell_style)
        ],
        [
            Paragraph("3. Artículo / Breakdown Técnico Estilo 80.lv", table_cell_style),
            Paragraph("<b>20%</b>", table_score_style),
            Paragraph("<b>12 pts</b>", table_score_style),
            Paragraph("Documento visual paso a paso explicando referencias, nodos del shader y capas de luz.", table_cell_style)
        ],
        [
            Paragraph("4. Post-Procesado, Orden y Rendimiento", table_cell_style),
            Paragraph("<b>15%</b>", table_score_style),
            Paragraph("<b>9 pts</b>", table_score_style),
            Paragraph("Acabado de color/exposición, nomenclatura limpia de proyecto y fluidez en tiempo real.", table_cell_style)
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

    story.append(Paragraph("3. Matriz de Evaluación — Parte I (39 Puntos)", h2_style))

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
            Paragraph("<b>1. Shaders en el Juego</b><br/>(30% del total)", table_cell_style),
            Paragraph("El estilo de shaders y materiales (3D o 2D) está implementado con total consistencia en el nivel jugable. Uso correcto de instancias parametrizadas para dar variedad.", table_cell_style),
            Paragraph("Shaders principales bien integrados en el juego, aunque algunos elementos secundarios conservan materiales genéricos.", table_cell_style),
            Paragraph("Implementación parcial; el shader solo se aplicó a un objeto aislado sin integrarse al nivel, o presenta errores visuales.", table_cell_style),
            Paragraph("No se implementaron shaders propios en el juego o los materiales están rotos/ausentes.", table_cell_style),
            Paragraph("<b>/ 18</b>", table_score_style)
        ],
        [
            Paragraph("<b>2. Iluminación y Guía Visual</b><br/>(35% del total)", table_cell_style),
            Paragraph("Iluminación sobresaliente (3D o 2D). Construye atmósfera envolvente, separa planos de profundidad y usa contraste/temperatura para guiar intuitivamente al jugador.", table_cell_style),
            Paragraph("Buena iluminación general y atmósfera lograda, pero la jerarquía visual compite en ciertas zonas o hay áreas muy oscuras.", table_cell_style),
            Paragraph("Iluminación plana o utilitaria; ilumina para que se vea pero carece de intención narrativa o guía visual al jugador.", table_cell_style),
            Paragraph("Nivel sin trabajo de iluminación (luz por defecto del motor), sombras rotas o escena ilegible.", table_cell_style),
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

    story.append(Paragraph("4. Matriz de Evaluación — Parte II (21 Puntos)", h2_style))

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
            Paragraph("<b>3. Breakdown Estilo 80.lv</b><br/>(20% del total)", table_cell_style),
            Paragraph("Artículo visual impecable, claro y conciso. Incluye las 4 secciones: referencias multimediales, explicación del grafo del shader, secuencia paso a paso de capas de luz y conclusión.", table_cell_style),
            Paragraph("Artículo completo y bien estructurado que explica el proceso, aunque falta mayor detalle en los nodos o en alguna captura intermedia de luz.", table_cell_style),
            Paragraph("Documento incompleto o superficial; muestra capturas finales sin explicar el proceso técnico de cómo construyeron los shaders ni las luces.", table_cell_style),
            Paragraph("No entrega el Breakdown técnico o presenta un documento sin capturas del proceso ni explicación propia.", table_cell_style),
            Paragraph("<b>/ 12</b>", table_score_style)
        ],
        [
            Paragraph("<b>4. Post-Process, Orden y FPS</b><br/>(15% del total)", table_cell_style),
            Paragraph("Acabado pulido con Post-Processing (color, exposición, Bloom y niebla). Proyecto ordenado con nomenclatura estándar y rendimiento fluido en tiempo real.", table_cell_style),
            Paragraph("Post-procesado correcto y proyecto ordenado con descuidos menores de nomenclatura o leves caídas de FPS puntuales.", table_cell_style),
            Paragraph("Sin ajustes de post-procesado, desorden evidente en carpetas del motor o problemas de rendimiento por luces sin optimizar.", table_cell_style),
            Paragraph("Proyecto desorganizado, archivos faltantes, sin post-procesado o el juego no logra ejecutarse de manera estable.", table_cell_style),
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
            Paragraph("<b>Sobresaliente:</b> Integración visual profesional en el juego y Breakdown digno de portafolio.", table_cell_style)
        ],
        [
            Paragraph("54 – 59 pts", table_cell_style),
            Paragraph("<b>6.3 – 6.9</b>", table_score_style),
            Paragraph("<b>Muy Bueno:</b> Excelente acabado de shaders e iluminación en el juego con observaciones mínimas.", table_cell_style)
        ],
        [
            Paragraph("48 – 53 pts", table_cell_style),
            Paragraph("<b>5.5 – 6.1</b>", table_score_style),
            Paragraph("<b>Bueno:</b> Cumplimiento sólido de la identidad visual en el nivel y documentación clara del proceso.", table_cell_style)
        ],
        [
            Paragraph("42 – 47 pts", table_cell_style),
            Paragraph("<b>4.8 – 5.4</b>", table_score_style),
            Paragraph("<b>Aceptable:</b> Juego bien iluminado y con shaders funcionales, con detalles por afinar en guía o breakdown.", table_cell_style)
        ],
        [
            Paragraph("36 – 41 pts", table_cell_style),
            Paragraph("<b>4.0 – 4.6</b>", table_score_style),
            Paragraph("<b>Aprobado (Corte 60%):</b> Cumplimiento mínimo de implementación en el juego y explicación del proceso.", table_cell_style)
        ],
        [
            Paragraph("24 – 35 pts", table_cell_style),
            Paragraph("<b>3.0 – 3.9</b>", table_score_style),
            Paragraph("<b>Reprobado:</b> Integración incompleta en el juego, ausencia de intención lumínica o falta del desglose.", table_cell_style)
        ],
        [
            Paragraph("0 – 23 pts", table_cell_style),
            Paragraph("<b>1.0 – 2.9</b>", table_score_style),
            Paragraph("<b>Insuficiente:</b> Entrega incompleta, no cumple requisitos mínimos o no presentada en el examen.", table_cell_style)
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
    print(f"Exam Rubric PDF generated at: {PDF_PATH} and copied to {PUBLIC_PDF_PATH}")

if __name__ == "__main__":
    create_pdf()
