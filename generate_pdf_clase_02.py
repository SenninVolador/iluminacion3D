import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing, Circle, Rect, String, Line

PDF_PATH = r"c:\Users\danie\OneDrive\Escritorio\Iluminacion3D\Material_Visual_Clase_02.pdf"

def create_pdf():
    # Generous margins: 18mm left/right = ~51pt, 18mm top/bottom = ~51pt
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

    # Typography
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
                Paragraph(f"Clase 02 · Pág. {page_num} de 2", ParagraphStyle('HRight', fontName='Helvetica', fontSize=8, textColor=c_gray_light, alignment=2))
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
    # PÁGINA 1
    # ==========================================
    story.append(make_header(1))
    story.append(Spacer(1, 14))

    story.append(Paragraph("1. Esquema de Iluminación de 3 Puntos", h1_style))
    story.append(Paragraph("Construcción de volumen, jerarquía de contraste y silueta sobre un sujeto tridimensional a partir de la oscuridad absoluta.", desc_style))

    # Diagrama Técnico Minimalista
    d = Drawing(499, 160)
    d.add(Rect(0, 0, 499, 160, fillColor=c_bg_subtle, strokeColor=c_line, strokeWidth=0.75, rx=3, ry=3))
    
    # Guías técnicas
    d.add(Circle(250, 75, 55, fillColor=None, strokeColor=colors.HexColor('#E5E7EB'), strokeWidth=0.75, strokeDashArray=[3,3]))
    d.add(Line(250, 75, 250, 135, strokeColor=c_gray_light, strokeWidth=1))
    d.add(Line(250, 75, 155, 25, strokeColor=c_gray_light, strokeWidth=1))
    d.add(Line(250, 75, 345, 25, strokeColor=c_gray_light, strokeWidth=1))
    d.add(Line(250, 75, 250, 20, strokeColor=colors.HexColor('#E5E7EB'), strokeWidth=0.75, strokeDashArray=[2,2]))

    # Sujeto
    d.add(Circle(250, 75, 18, fillColor=colors.white, strokeColor=c_black, strokeWidth=1.25))
    d.add(String(250, 72, "SUJETO", fontName="Helvetica-Bold", fontSize=7.5, fillColor=c_black, textAnchor="middle"))

    # Key Light
    d.add(Circle(155, 25, 11, fillColor=c_black, strokeColor=c_black, strokeWidth=1))
    d.add(String(155, 22, "KEY", fontName="Helvetica-Bold", fontSize=7, fillColor=colors.white, textAnchor="middle"))
    d.add(String(155, 7, "Key Light (100%)", fontName="Helvetica-Bold", fontSize=7.5, fillColor=c_black, textAnchor="middle"))
    d.add(String(155, -2, "45° lateral · Sombra principal", fontName="Helvetica", fontSize=6.5, fillColor=c_gray_text, textAnchor="middle"))

    # Fill Light
    d.add(Circle(345, 25, 10, fillColor=colors.white, strokeColor=c_black, strokeWidth=1.25))
    d.add(String(345, 22, "FILL", fontName="Helvetica-Bold", fontSize=6.5, fillColor=c_black, textAnchor="middle"))
    d.add(String(345, 7, "Fill Light (25–40%)", fontName="Helvetica-Bold", fontSize=7.5, fillColor=c_black, textAnchor="middle"))
    d.add(String(345, -2, "Relleno · Suaviza penumbras", fontName="Helvetica", fontSize=6.5, fillColor=c_gray_text, textAnchor="middle"))

    # Rim Light
    d.add(Circle(250, 135, 10, fillColor=colors.white, strokeColor=c_black, strokeWidth=1.25))
    d.add(String(250, 132, "RIM", fontName="Helvetica-Bold", fontSize=6.5, fillColor=c_black, textAnchor="middle"))
    d.add(String(250, 148, "Rim / Back Light (Contraluz)", fontName="Helvetica-Bold", fontSize=7.5, fillColor=c_black, textAnchor="middle"))

    # Cam
    d.add(Rect(237, 12, 26, 14, fillColor=colors.white, strokeColor=c_black, strokeWidth=1, rx=2, ry=2))
    d.add(String(250, 16, "CAM", fontName="Helvetica-Bold", fontSize=6.5, fillColor=c_black, textAnchor="middle"))

    story.append(d)
    story.append(Spacer(1, 16))

    # Bloque 2: Directional + Sky
    ext_content = [
        [
            Paragraph("<b>Directional Light (Luz Solar)</b>", h2_style),
            Paragraph("<b>Sky Light (Luz de Cielo / Ambiente)</b>", h2_style)
        ],
        [
            Paragraph("• <b>Rayos Paralelos:</b> Simula una fuente infinitamente lejana. Solo influye su <b>rotación</b>, no su posición en el mapa.<br/>• <b>Atmosphere Sun Light:</b> Conecta físicamente con la atmósfera de UE5.<br/>• <b>Atajo:</b> <font name='Helvetica-Bold'>Ctrl + L</font> + ratón para mover el sol interactivamente.", body_style),
            Paragraph("• <b>Luz Hemisférica:</b> Captura la cúpula celeste o HDRI para iluminar sombras sin dejarlas en negro absoluto.<br/>• <b>Real Time Capture:</b> Recalcula el rebote ambiental en vivo ante cambios horarios.<br/>• Otorga coherencia lumínica a exteriores.", body_style)
        ]
    ]
    ext_table = Table(ext_content, colWidths=[240, 240])
    ext_table.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 0.75, c_line),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(ext_table)
    story.append(Spacer(1, 14))

    # Note
    note_t = Table([[
        Paragraph("<b>Metodología de Taller:</b> Comenzar siempre en oscuridad total. Añadir primero la <i>Key Light</i> para definir el eje dramático, luego la <i>Fill Light</i> para graduar la penumbra, y finalizar con la <i>Rim Light</i> para siluetear el objeto contra el fondo.", note_style)
    ]], colWidths=[499])
    note_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_subtle),
        ('LINELEFT', (0,0), (-1,-1), 2, c_black),
        ('BOX', (0,0), (-1,-1), 0.5, c_line),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(note_t)

    # ==========================================
    # PÁGINA 2
    # ==========================================
    story.append(PageBreak())
    story.append(make_header(2))
    story.append(Spacer(1, 14))

    story.append(Paragraph("2. Movilidad de Luces y Análisis de Casos", h1_style))
    story.append(Paragraph("Criterios de selección técnica de luces según el presupuesto de renderizado (GPU frametime) y las necesidades de interactividad.", desc_style))

    # Tabla Técnica
    th_style = ParagraphStyle('THClean', fontName='Helvetica-Bold', fontSize=8, textColor=c_black)
    mob_data = [
        [
            Paragraph("MOVILIDAD", th_style),
            Paragraph("MÉTODO DE CÁLCULO", th_style),
            Paragraph("COSTE GPU", th_style),
            Paragraph("APLICACIÓN RECOMENDADA", th_style)
        ],
        [
            Paragraph("<b>STATIC</b>", body_style),
            Paragraph("100% precalculada en mapas de textura (Lightmaps).", body_style),
            Paragraph("Cero coste en runtime", body_style),
            Paragraph("VR (90 FPS), móviles, entornos sin cambios dinámicos.", body_style)
        ],
        [
            Paragraph("<b>STATIONARY</b>", body_style),
            Paragraph("Híbrido: Luz directa dinámica + rebotes indirectos horneados.", body_style),
            Paragraph("Medio (Sombras dinámicas)", body_style),
            Paragraph("Consolas/PC con mapa fijo. Permite variar intensidad y color.", body_style)
        ],
        [
            Paragraph("<b>MOVABLE</b>", body_style),
            Paragraph("100% tiempo real fotograma a fotograma.", body_style),
            Paragraph("Alto continuo", body_style),
            Paragraph("UE5 con Lumen, linternas del jugador, ciclos día/noche.", body_style)
        ]
    ]
    mob_t = Table(mob_data, colWidths=[85, 160, 100, 154])
    mob_t.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,0), 1, c_black),
        ('LINEBELOW', (0,1), (-1,-1), 0.5, c_line),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(mob_t)
    story.append(Spacer(1, 14))

    # Casos de Estudio con Links
    story.append(Paragraph("<b>Casos de Estudio en la Industria (Enlaces a Análisis)</b>", h2_style))
    story.append(Spacer(1, 4))

    games_content = [
        [
            Paragraph("<a href='https://www.youtube.com/watch?v=R9_mD4oI6fU' color='#1E3A8A'><b><u>The Last of Us Part I / II (GDC)</u></b></a><br/><b>Estrategia:</b> Baking de alta precisión + Linternas móviles.<br/><font color='#4B5563'>Precalculan rebotes indirectos para lograr fotorrealismo en interiores sin sobrecargar la GPU, combinando focos dinámicos en combate.</font>", body_style),
            Paragraph("<a href='https://www.youtube.com/watch?v=a3YxH_xK004' color='#1E3A8A'><b><u>Cyberpunk 2077 (RTX / Lumen)</u></b></a><br/><b>Estrategia:</b> Iluminación 100% Dinámica + Ray Tracing.<br/><font color='#4B5563'>Night City integra miles de emisivos, clima y ciclo horario variable. Toda la luz y reflejos se procesan en tiempo real.</font>", body_style)
        ],
        [
            Paragraph("<a href='https://www.nintendo.com/games/detail/the-legend-of-zelda-tears-of-the-kingdom-switch/' color='#1E3A8A'><b><u>Zelda: Tears of the Kingdom</u></b></a><br/><b>Estrategia:</b> Directional + Sky con sombras en cascada.<br/><font color='#4B5563'>Optimiza sombras en cascada para Nintendo Switch, balanceando tonos cálidos solares y sombras frías celestes con un shader nítido.</font>", body_style),
            Paragraph("<a href='https://www.residentevil.com/re4/' color='#1E3A8A'><b><u>Resident Evil 4 Remake (Capcom)</u></b></a><br/><b>Estrategia:</b> Niebla volumétrica y sombras duras.<br/><font color='#4B5563'>Suprime la luz direccional y construye el terror con pequeñas luces puntuales y el haz de la linterna interactuando con partículas.</font>", body_style)
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
        Paragraph("<b>Límite de Canales (Stationary Overlap):</b> En el renderizador clásico de Unreal no pueden solaparse más de 4 luces <i>Stationary</i> con sombra en el mismo espacio (canales RGBA). Una 5ª luz se marcará con cruz roja y pasará a <i>Movable</i>, duplicando el coste.", note_style)
    ]], colWidths=[499])
    note_t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_subtle),
        ('LINELEFT', (0,0), (-1,-1), 2, c_black),
        ('BOX', (0,0), (-1,-1), 0.5, c_line),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(note_t2)

    doc.build(story)
    print(f"Minimalist PDF with links generated at: {PDF_PATH}")

if __name__ == "__main__":
    create_pdf()
