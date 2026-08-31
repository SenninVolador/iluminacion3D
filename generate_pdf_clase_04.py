import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing, Rect, String, Line

PDF_PATH = r"c:\Users\danie\OneDrive\Escritorio\Iluminacion3D\Material_Visual_Clase_04.pdf"

def create_pdf():
    # Margins: 44pt left/right, 38pt top/bottom
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
        fontSize=9,
        leading=12,
        textColor=c_black,
        spaceBefore=6,
        spaceAfter=4
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
            Paragraph("ILUMINACIÓN 3D · FICHA TÉCNICA", meta_left),
            Paragraph(f"SESIÓN 04 — PÁGINA {page_num} DE 2", meta_right)
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
            Paragraph("Ficha de Cátedra N° 04 · Unreal Engine 5", footer_right)
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

    def get_node_diagram():
        d = Drawing(507, 72)
        # Background
        d.add(Rect(0, 0, 507, 72, fillColor=c_bg_subtle, strokeColor=c_border_card, strokeWidth=0.5, rx=3, ry=3))
        
        # Texture Node
        d.add(Rect(10, 36, 110, 28, fillColor=colors.white, strokeColor=c_black, strokeWidth=0.8, rx=2, ry=2))
        d.add(String(65, 52, "Texture Sample (RGB)", fontName="Helvetica-Bold", fontSize=6.5, textAnchor="middle", fillColor=c_black))
        d.add(String(65, 42, "Albedo 2D Base", fontName="Helvetica", fontSize=5.5, textAnchor="middle", fillColor=c_gray_text))

        # Color Tint Node
        d.add(Rect(10, 6, 110, 24, fillColor=colors.white, strokeColor=c_black, strokeWidth=0.8, rx=2, ry=2))
        d.add(String(65, 18, "Color Tint (Vector)", fontName="Helvetica-Bold", fontSize=6.5, textAnchor="middle", fillColor=c_black))
        d.add(String(65, 10, "Parámetro Expuesto", fontName="Helvetica", fontSize=5.5, textAnchor="middle", fillColor=c_gray_text))

        # Multiply Node
        d.add(Rect(150, 22, 85, 28, fillColor=colors.white, strokeColor=c_black, strokeWidth=0.8, rx=2, ry=2))
        d.add(String(192, 38, "MULTIPLY", fontName="Helvetica-Bold", fontSize=7, textAnchor="middle", fillColor=c_black))
        d.add(String(192, 28, "A * B (Tinte)", fontName="Helvetica", fontSize=5.5, textAnchor="middle", fillColor=c_gray_text))

        # Lines to Multiply
        d.add(Line(120, 50, 150, 38, strokeColor=c_black, strokeWidth=0.8))
        d.add(Line(120, 18, 150, 34, strokeColor=c_black, strokeWidth=0.8))

        # Master Node
        d.add(Rect(270, 6, 225, 60, fillColor=c_black, strokeColor=c_black, strokeWidth=1, rx=3, ry=3))
        d.add(String(382, 54, "MASTER PBR NODE (Root)", fontName="Helvetica-Bold", fontSize=7.5, textAnchor="middle", fillColor=colors.white))
        d.add(String(285, 40, "► Base Color (Albedo * Color Tint)", fontName="Courier-Bold", fontSize=6, fillColor=colors.HexColor('#93C5FD')))
        d.add(String(285, 28, "► Metallic / Roughness (Scalar Parameters)", fontName="Courier-Bold", fontSize=6, fillColor=colors.HexColor('#6EE7B7')))
        d.add(String(285, 16, "► Normal Map (Tangent Space Relief)", fontName="Courier-Bold", fontSize=6, fillColor=colors.HexColor('#FCA5A5')))

        # Line Multiply to Master
        d.add(Line(235, 36, 270, 42, strokeColor=c_black, strokeWidth=0.8))

        return d

    story = []

    # ================= PAGE 1 =================
    story.append(get_header(1))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Shaders Nodales Universales y Taller de Entrega N°1", h1_style))
    story.append(Paragraph("Arquitectura modular de sombreadores en la industria de videojuegos, principios nodales genéricos y taller de apoyo presencial con calificación inmediata según rúbrica.", desc_style))

    story.append(Paragraph("1. Lógica Universal de Sistemas Nodales (Shader Graphs)", h2_style))
    story.append(get_node_diagram())
    story.append(Spacer(1, 8))

    table_data_p1 = [
        [
            Paragraph("Motor / Software", table_header_style),
            Paragraph("Editor de Shaders", table_header_style),
            Paragraph("Nodo Maestro de Salida", table_header_style),
            Paragraph("Operador de Tinte", table_header_style)
        ],
        [
            Paragraph("<b>Unreal Engine 5</b>", table_cell_style),
            Paragraph("Material Graph", table_cell_style),
            Paragraph("Master Material (Root Node)", table_cell_style),
            Paragraph("<code>Multiply</code> + Vector Parameter", table_cell_style)
        ],
        [
            Paragraph("<b>Unity (URP / HDRP)</b>", table_cell_style),
            Paragraph("Shader Graph", table_cell_style),
            Paragraph("PBR Master / Lit Master", table_cell_style),
            Paragraph("<code>Multiply</code> + Color Property", table_cell_style)
        ],
        [
            Paragraph("<b>Blender</b>", table_cell_style),
            Paragraph("Shader Editor", table_cell_style),
            Paragraph("Principled BSDF", table_cell_style),
            Paragraph("<code>Mix Color (Multiply)</code>", table_cell_style)
        ],
        [
            Paragraph("<b>Autodesk Maya</b>", table_cell_style),
            Paragraph("Hypershade", table_cell_style),
            Paragraph("Standard Surface (aiStandard)", table_cell_style),
            Paragraph("<code>multiplyDivide</code>", table_cell_style)
        ]
    ]

    t_p1 = Table(table_data_p1, colWidths=[100, 110, 150, 147])
    t_p1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_bg_subtle),
        ('GRID', (0,0), (-1,-1), 0.5, c_line),
        ('BOX', (0,0), (-1,-1), 0.8, c_black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_p1)
    story.append(Spacer(1, 10))

    story.append(Paragraph("2. Taller de Apoyo y Calificación de la Entrega N°1", h2_style))

    taller_cards = [
        [
            Paragraph("<b>Checklist de Iluminación de 3 Puntos:</b><br/>"
                      "• <b>Key Light:</b> 45° lateral/cenital, sombra y contraste dominante.<br/>"
                      "• <b>Fill Light:</b> Lateral opuesto al 30%, rescata penumbras sin sombras cruzadas.<br/>"
                      "• <b>Rim Light:</b> Contraluz trasero que despega la silueta del fondo.", body_style),
            Paragraph("<b>Checklist del Shader Paramétrico:</b><br/>"
                      "• Master Material base compilado una sola vez.<br/>"
                      "• Instancia (<code>MI_...</code>) asignada a la malla.<br/>"
                      "• Al menos 3 parámetros funcionales (Tinte, Rugosidad, Relieve).<br/>"
                      "• Calificación presencial inmediata (Escala 1.0 a 7.0).", body_style)
        ]
    ]
    t_taller = Table(taller_cards, colWidths=[250, 257])
    t_taller.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_subtle),
        ('BOX', (0,0), (-1,-1), 0.7, c_border_card),
        ('GRID', (0,0), (-1,-1), 0.5, c_line),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_taller)

    story.append(Spacer(1, 14))
    story.append(get_footer(1))

    # ================= PAGE 2 =================
    story.append(PageBreak())
    story.append(get_header(2))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Atmósfera, Cielo, Niebla Volumétrica y Mood", h1_style))
    story.append(Paragraph("Principios ópticos ambientales, componentes del stack exterior en la industria y construcción de atmósfera escénica.", desc_style))

    story.append(Paragraph("1. Componentes del Stack Ambiental: Nombres en la Industria", h2_style))

    table_data_p2 = [
        [
            Paragraph("Unreal Engine 5", table_header_style),
            Paragraph("Término Genérico (Industria)", table_header_style),
            Paragraph("Función y Principio Óptico", table_header_style)
        ],
        [
            Paragraph("<b>Directional Light</b>", table_cell_style),
            Paragraph("Sun Light / Infinite Light", table_cell_style),
            Paragraph("Luz a distancia infinita con rayos 100% paralelos. Solo influye su rotación.", table_cell_style)
        ],
        [
            Paragraph("<b>SkyAtmosphere</b>", table_cell_style),
            Paragraph("Physical Sky / Atmos. Scattering", table_cell_style),
            Paragraph("Dispersión física de luz en moléculas de gas (Rayleigh) y aerosoles (Mie).", table_cell_style)
        ],
        [
            Paragraph("<b>Sky Light</b>", table_cell_style),
            Paragraph("Environment Probe / Ambient Dome", table_cell_style),
            Paragraph("Luz difusa envolvente de 360° para bañar sombras y evitar negros absolutos.", table_cell_style)
        ],
        [
            Paragraph("<b>Exponential Height Fog</b>", table_cell_style),
            Paragraph("Height Fog / Distance Fog", table_cell_style),
            Paragraph("Niebla analítica basada en altitud y distancia para aportar perspectiva aérea.", table_cell_style)
        ],
        [
            Paragraph("<b>Volumetric Fog</b>", table_cell_style),
            Paragraph("Media Scatter / Voxel Fog", table_cell_style),
            Paragraph("Niebla 3D en grilla de vóxeles que interactúa con la luz creando <b>God Rays</b>.", table_cell_style)
        ],
        [
            Paragraph("<b>Volumetric Clouds</b>", table_cell_style),
            Paragraph("Procedural Cloud Layer", table_cell_style),
            Paragraph("Nubes 3D volumétricas con auto-sombreado y sombras proyectadas en el terreno.", table_cell_style)
        ]
    ]

    t_p2 = Table(table_data_p2, colWidths=[120, 150, 237])
    t_p2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_bg_subtle),
        ('GRID', (0,0), (-1,-1), 0.5, c_line),
        ('BOX', (0,0), (-1,-1), 0.8, c_black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_p2)
    story.append(Spacer(1, 10))

    story.append(Paragraph("2. Principios Ópticos: Dispersión Atmosférica y Anisotropía", h2_style))

    atmos_cards = [
        [
            Paragraph("<b>Dispersión de Rayleigh (Gases):</b><br/>"
                      "Las moléculas diminutas de gas dispersan más eficientemente las longitudes de onda cortas (azul/violeta). Produce el cielo azul de mediodía y los tonos rojizos cuando el sol está en el horizonte.", body_style),
            Paragraph("<b>Dispersión de Mie (Polvo y Humedad):</b><br/>"
                      "Partículas de mayor tamaño generan la bruma blanquecina del horizonte y el halo luminoso alrededor del sol. Provoca la dispersión hacia adelante (<i>Forward Scattering</i>).", body_style)
        ]
    ]
    t_atmos = Table(atmos_cards, colWidths=[250, 257])
    t_atmos.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_subtle),
        ('BOX', (0,0), (-1,-1), 0.7, c_border_card),
        ('GRID', (0,0), (-1,-1), 0.5, c_line),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_atmos)
    story.append(Spacer(1, 8))

    story.append(Paragraph("3. Niebla Volumétrica y Anisotropía ($g$)", h2_style))
    fog_info = """
    • <b>Cálculo por Vóxeles:</b> El motor subdivide el frustum visual de la cámara en una grilla tridimensional de vóxeles.<br/>
    • <b>Anisotropía de Dispersión ($g$):</b> Controla el ángulo de dispersión. Valores entre <code>0.7</code> y <code>0.85</code> concentran los rayos hacia la cámara generando <b>God Rays (rayos crepusculares)</b> de alto impacto.
    """
    story.append(Paragraph(fog_info, body_style))

    story.append(Spacer(1, 14))
    story.append(get_footer(2))

    doc.build(story)
    print(f"Class 04 PDF generated at: {PDF_PATH}")

if __name__ == "__main__":
    create_pdf()
