import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing, Circle, Rect, String, Line

PDF_PATH = r"c:\Users\danie\OneDrive\Escritorio\Iluminacion3D\Material_Visual_Clase_03.pdf"

def create_pdf():
    # Margins: 18mm left/right = ~51pt, 18mm top/bottom = ~51pt
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        leftMargin=48,
        rightMargin=48,
        topMargin=42,
        bottomMargin=42
    )

    styles = getSampleStyleSheet()

    # Editorial Monochrome Palette
    c_black = colors.HexColor('#111827')
    c_dark = colors.HexColor('#1F2937')
    c_gray_text = colors.HexColor('#4B5563')
    c_gray_light = colors.HexColor('#9CA3AF')
    c_line = colors.HexColor('#E5E7EB')
    c_bg_subtle = colors.HexColor('#F9FAFB')
    c_link = colors.HexColor('#1E3A8A')

    # Typography Styles
    h1_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=c_black,
        spaceAfter=4
    )

    desc_style = ParagraphStyle(
        'MainDesc',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=c_gray_text,
        spaceAfter=14
    )

    h2_style = ParagraphStyle(
        'H2Sub',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=c_black,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'BodyClean',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=c_dark
    )

    note_style = ParagraphStyle(
        'NoteText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_dark
    )

    def make_header(page_num):
        t = Table([
            [
                Paragraph("<b>ILUMINACIÓN 3D Y SHADERS PARA VIDEOJUEGOS</b>", ParagraphStyle('HLeft', fontName='Helvetica-Bold', fontSize=8, textColor=c_black)),
                Paragraph(f"Clase 03 · Pág. {page_num} de 2", ParagraphStyle('HRight', fontName='Helvetica', fontSize=8, textColor=c_gray_light, alignment=2))
            ]
        ], colWidths=[350, 149])
        t.setStyle(TableStyle([
            ('LINEBELOW', (0,0), (-1,-1), 0.75, c_black),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('TOPPADDING', (0,0), (-1,-1), 0),
        ]))
        return t

    story = []

    # ==========================================
    # PÁGINA 1: MASTER MATERIALS & BUSTO 3D
    # ==========================================
    story.append(make_header(1))
    story.append(Spacer(1, 14))

    story.append(Paragraph("1. Pipeline PBR: Master Materials e Instancias", h1_style))
    story.append(Paragraph("Construcción de M_Master_PBR para el busto 3D: empaquetado ORM, control de rugosidad, metalicidad y normales.", desc_style))

    # Diagrama Técnico: Master Material -> Instancias del Busto
    d = Drawing(499, 145)
    d.add(Rect(0, 0, 499, 145, fillColor=c_bg_subtle, strokeColor=c_line, strokeWidth=0.75, rx=3, ry=3))

    # Master Material
    d.add(Rect(149, 95, 200, 36, fillColor=colors.white, strokeColor=c_black, strokeWidth=1.2, rx=2, ry=2))
    d.add(String(249, 114, "MASTER MATERIAL (M_Master_PBR)", fontName="Helvetica-Bold", fontSize=8, fillColor=c_black, textAnchor="middle"))
    d.add(String(249, 103, "Lógica de Nodos + Parámetros expuestos", fontName="Helvetica", fontSize=7, fillColor=c_gray_text, textAnchor="middle"))

    # Conexiones
    d.add(Line(249, 95, 249, 75, strokeColor=c_gray_light, strokeWidth=1))
    d.add(Line(80, 75, 420, 75, strokeColor=c_gray_light, strokeWidth=1))
    d.add(Line(80, 75, 80, 58, strokeColor=c_gray_light, strokeWidth=1))
    d.add(Line(249, 75, 249, 58, strokeColor=c_gray_light, strokeWidth=1))
    d.add(Line(420, 75, 420, 58, strokeColor=c_gray_light, strokeWidth=1))

    # Instancias del Busto
    d.add(Rect(15, 12, 130, 46, fillColor=colors.white, strokeColor=c_line, strokeWidth=1, rx=2, ry=2))
    d.add(String(80, 44, "MI_Busto_PielMate", fontName="Helvetica-Bold", fontSize=7.5, fillColor=c_black, textAnchor="middle"))
    d.add(String(80, 32, "Roughness: 0.75", fontName="Helvetica", fontSize=6.5, fillColor=c_gray_text, textAnchor="middle"))
    d.add(String(80, 21, "Metallic: 0.0 (Dieléctrico)", fontName="Helvetica", fontSize=6.5, fillColor=c_gray_text, textAnchor="middle"))

    d.add(Rect(184, 12, 130, 46, fillColor=colors.white, strokeColor=c_line, strokeWidth=1, rx=2, ry=2))
    d.add(String(249, 44, "MI_Busto_Cromo", fontName="Helvetica-Bold", fontSize=7.5, fillColor=c_black, textAnchor="middle"))
    d.add(String(249, 32, "Roughness: 0.10", fontName="Helvetica", fontSize=6.5, fillColor=c_gray_text, textAnchor="middle"))
    d.add(String(249, 21, "Metallic: 1.0 (Metal puro)", fontName="Helvetica", fontSize=6.5, fillColor=c_gray_text, textAnchor="middle"))

    d.add(Rect(354, 12, 130, 46, fillColor=colors.white, strokeColor=c_line, strokeWidth=1, rx=2, ry=2))
    d.add(String(419, 44, "MI_Busto_EstatuaOro", fontName="Helvetica-Bold", fontSize=7.5, fillColor=c_black, textAnchor="middle"))
    d.add(String(419, 32, "Roughness: 0.35", fontName="Helvetica", fontSize=6.5, fillColor=c_gray_text, textAnchor="middle"))
    d.add(String(419, 21, "Metallic: 1.0 · Tinte Oro", fontName="Helvetica", fontSize=6.5, fillColor=c_gray_text, textAnchor="middle"))

    story.append(d)
    story.append(Spacer(1, 16))

    # Bloque 2 Columnas
    mat_content = [
        [
            Paragraph("<b>Master Materials e Instancias</b>", h2_style),
            Paragraph("<b>Texturas Empaquetadas (Canales ORM)</b>", h2_style)
        ],
        [
            Paragraph("• <b>Lógica Centralizada:</b> El Master Material compila la lógica pesada. Las instancias visten el busto en runtime sin tiempos de compilación.<br/>• <b>Parámetros:</b> Expone Roughness, Metallic, Tinte cromático y fuerza de Normal Map con <code>FlattenNormal</code>.", body_style),
            Paragraph("• <b>Canal R:</b> Ambient Occlusion (Cavidades faciales).<br/>• <b>Canal G:</b> Roughness (Dispersión y brillo especular).<br/>• <b>Canal B:</b> Metallic (Dieléctrico vs Conductor).<br/>• <b>Ahorro VRAM:</b> Reduce de 3 lecturas a 1 sola llamada en GPU.", body_style)
        ]
    ]
    mat_table = Table(mat_content, colWidths=[240, 240])
    mat_table.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 0.75, c_line),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(mat_table)
    story.append(Spacer(1, 14))

    # Nota de Taller
    note_t = Table([[
        Paragraph("<b>Metodología de Taller:</b> Asignar <code>M_Master_PBR</code> al busto 3D. Crear una instancia de piel mate y otra metálica reflectante para observar cómo cambia el modelado de volumen bajo diferentes fuentes de luz.", note_style)
    ]], colWidths=[499])
    note_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_subtle),
        ('LINELEFT', (0,0), (-1,-1), 2, c_black),
        ('BOX', (0,0), (-1,-1), 0.5, c_line),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(note_t)

    # ==========================================
    # PÁGINA 2: SOL, CIELO Y LUCES LOCALES
    # ==========================================
    story.append(PageBreak())
    story.append(make_header(2))
    story.append(Spacer(1, 14))

    story.append(Paragraph("2. Iluminación del Busto: Sol, Cielo y Fuentes Locales", h1_style))
    story.append(Paragraph("Interacción del shader del busto bajo la luz solar direccional, la cúpula celeste y luces de acento local.", desc_style))

    # Tabla de Fuentes de Luz
    th_style = ParagraphStyle('THClean', fontName='Helvetica-Bold', fontSize=8, textColor=c_black)
    lights_data = [
        [
            Paragraph("FUENTE DE LUZ", th_style),
            Paragraph("COMPORTAMIENTO FÍSICO", th_style),
            Paragraph("EFECTO EN EL BUSTO", th_style),
            Paragraph("CONTROL CLAVE", th_style)
        ],
        [
            Paragraph("<b>DIRECTIONAL LIGHT</b>", body_style),
            Paragraph("Rayos paralelos desde el infinito (Sol/Luna).", body_style),
            Paragraph("Sombra principal y resalte del Normal Map.", body_style),
            Paragraph("Rotación (<b>Ctrl + L</b>), <code>Atmosphere Sun</code>.", body_style)
        ],
        [
            Paragraph("<b>SKY LIGHT</b>", body_style),
            Paragraph("Cúpula celeste ambiental hemisférica.", body_style),
            Paragraph("Relleno difuso azul en sombras del rostro.", body_style),
            Paragraph("<code>Real Time Capture</code>, <code>Cubemap</code>.", body_style)
        ],
        [
            Paragraph("<b>SPOT / POINT LIGHT</b>", body_style),
            Paragraph("Cono o esfera local de 360°.", body_style),
            Paragraph("Luz de acento, recorte o brillo en ojos.", body_style),
            Paragraph("<code>Attenuation Radius</code>, <code>IES Profile</code>.", body_style)
        ],
        [
            Paragraph("<b>RECT LIGHT</b>", body_style),
            Paragraph("Área plana rectangular (Softbox).", body_style),
            Paragraph("Reflejo suave en pómulos y frentes pulidas.", body_style),
            Paragraph("<code>Source Width / Height</code>.", body_style)
        ]
    ]
    lights_t = Table(lights_data, colWidths=[95, 130, 134, 140])
    lights_t.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,0), 1, c_black),
        ('LINEBELOW', (0,1), (-1,-1), 0.5, c_line),
        ('PADDING', (0,0), (-1,-1), 5.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(lights_t)
    story.append(Spacer(1, 14))

    # Casos de Estudio con Links
    story.append(Paragraph("<b>Casos de Estudio en la Industria (Enlaces a Análisis)</b>", h2_style))
    story.append(Spacer(1, 4))

    games_content = [
        [
            Paragraph("<a href='https://www.artstation.com/artwork/g8GZ8K' color='#1E3A8A'><b><u>God of War Ragnarök (Santa Monica)</u></b></a><br/><b>Estrategia:</b> Shaders de personajes y luz solar.<br/><font color='#4B5563'>Modulan el roughness del rostro de Kratos para que el sol rasante y las antorchas esculpan sus facciones con máxima fuerza.</font>", body_style),
            Paragraph("<a href='https://www.guerrilla-games.com/read/the-technology-of-horizon-forbidden-west' color='#1E3A8A'><b><u>Horizon Forbidden West (Guerrilla)</u></b></a><br/><b>Estrategia:</b> Sol + Cielo sobre piel y metales.<br/><font color='#4B5563'>Aloy combina shaders de piel mate con piezas de armadura metálicas pulidas que reflejan el cielo y sol de forma hiperrealista.</font>", body_style)
        ],
        [
            Paragraph("<a href='https://www.youtube.com/watch?v=k5lO_68b3cQ' color='#1E3A8A'><b><u>Alan Wake 2 (Remedy)</u></b></a><br/><b>Estrategia:</b> Spot Lights, IES y Shaders reflectantes.<br/><font color='#4B5563'>Iluminan los rostros de los personajes con linternas de haz estrecho y perfiles IES reales sobre pieles húmedas con alto Fresnel.</font>", body_style),
            Paragraph("<a href='https://www.youtube.com/watch?v=J3e2Ea7vJ8Q' color='#1E3A8A'><b><u>Gears 5 (The Coalition)</u></b></a><br/><b>Estrategia:</b> Luces de acento en personajes.<br/><font color='#4B5563'>Focos de acento acotados para generar siluetas en cascos y armaduras metálicas sin sobrecargar el presupuesto de GPU.</font>", body_style)
        ]
    ]
    games_t = Table(games_content, colWidths=[240, 240])
    games_t.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 0.75, c_line),
        ('LINEABOVE', (0,1), (-1,1), 0.5, c_line),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(games_t)
    story.append(Spacer(1, 12))

    # Note
    note_t2 = Table([[
        Paragraph("<b>Técnica de Iluminación de Personajes:</b> Al rotar el sol con <b>Ctrl + L</b>, busca un ángulo lateral de 45° que genere una sombra triangular en la mejilla opuesta (iluminación <i>Rembrandt</i>). Usa la Sky Light para controlar el nivel de detalle en la sombra.", note_style)
    ]], colWidths=[499])
    note_t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_subtle),
        ('LINELEFT', (0,0), (-1,-1), 2, c_black),
        ('BOX', (0,0), (-1,-1), 0.5, c_line),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(note_t2)

    doc.build(story)
    print(f"Minimalist PDF for Class 03 (Busto + Sun/Sky + Local) generated at: {PDF_PATH}")

if __name__ == "__main__":
    create_pdf()
