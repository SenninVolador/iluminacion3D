import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

STUDENTS_SEC51 = [
    "JOSE MIGUEL FARFAN CARRASCO",
    "BENJAMIN FERNANDO FIGUEROA GONZALEZ",
    "MATIAS IGNACIO GODOY TIRADO",
    "HENRY ALEXANDER HERNANDEZ PEREZ",
    "GAEL ALBERTO IBARRA MONTECINOS",
    "LUKA PASCAL LATIFE CUEVAS",
    "MEI MALDONADO DUARTE",
    "ELIZABETH FABIOLA MEDRANO MORAN",
    "FREDDY DANILO MONTANARES ROSALES",
    "JOSE FRANCISCO NAVARRETE BARRIOS",
    "NATANIEL ASTRO REYES FLORES",
    "CRISTOBAL NICOLAS VALENZUELA PRESSAC"
]

STUDENTS_SEC52 = [
    "RAUL ELISEO ARROYO VASQUEZ",
    "HORACIO JOAQUIN BASTIAS BARRA",
    "TOMAS ALEJANDRO CARTES GOMEZ",
    "BENJAMIN IGNACIO COLLAO MARDONES",
    "DANA OKINGTHON EISSMANN",
    "JEARIM ANGEL RIVERA MUNOZ"
]

def build_workbook(title_main, subtitle_main, col_headers, rubric_rows, dest_paths):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    f_title = Font(name="Segoe UI", size=13, bold=True, color="111827")
    f_subtitle = Font(name="Segoe UI", size=9.5, italic=True, color="4B5563")
    f_header = Font(name="Segoe UI", size=9, bold=True, color="FFFFFF")
    f_data = Font(name="Segoe UI", size=9, color="1F2937")
    f_bold = Font(name="Segoe UI", size=9, bold=True, color="111827")
    f_kpi_lbl = Font(name="Segoe UI", size=8.5, bold=True, color="374151")
    f_kpi_val = Font(name="Segoe UI", size=11, bold=True, color="111827")

    fill_header_dark = PatternFill(start_color="111827", end_color="111827", fill_type="solid")
    fill_header_light = PatternFill(start_color="E5E7EB", end_color="E5E7EB", fill_type="solid")
    fill_kpi = PatternFill(start_color="F3F4F6", end_color="F3F4F6", fill_type="solid")
    fill_zebra = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")
    fill_nota = PatternFill(start_color="EFF6FF", end_color="EFF6FF", fill_type="solid")

    bd_thin = Side(style='thin', color='D1D5DB')
    bd_thick_bottom = Side(style='medium', color='111827')
    border_cell = Border(left=bd_thin, right=bd_thin, top=bd_thin, bottom=bd_thin)
    border_header = Border(left=bd_thin, right=bd_thin, top=bd_thin, bottom=bd_thick_bottom)

    align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    align_left = Alignment(horizontal="left", vertical="center", wrap_text=True)
    align_right = Alignment(horizontal="right", vertical="center")

    def add_section_sheet(sheet_name, section_label, student_list):
        ws = wb.create_sheet(title=sheet_name)
        ws.views.sheetView[0].showGridLines = True

        ws["A1"] = f"{title_main} — {section_label}"
        ws["A1"].font = f_title
        ws["A2"] = subtitle_main
        ws["A2"].font = f_subtitle

        last_row = 5 + len(student_list)

        # KPIs (Row 4)
        ws["B4"] = "Promedio Curso:"
        ws["B4"].font = f_kpi_lbl
        ws["B4"].alignment = align_right
        ws["C4"] = f"=AVERAGE(H6:H{last_row})"
        ws["C4"].font = f_kpi_val
        ws["C4"].alignment = align_center
        ws["C4"].fill = fill_kpi
        ws["C4"].border = border_cell
        ws["C4"].number_format = "0.0"

        ws["D4"] = "Tasa Aprobación:"
        ws["D4"].font = f_kpi_lbl
        ws["D4"].alignment = align_right
        ws["E4"] = f'=COUNTIF(J6:J{last_row},"APROBADO")/COUNTA(B6:B{last_row})'
        ws["E4"].font = f_kpi_val
        ws["E4"].alignment = align_center
        ws["E4"].fill = fill_kpi
        ws["E4"].border = border_cell
        ws["E4"].number_format = "0.0%"

        ws["F4"] = "Nota Moodle Prom.:"
        ws["F4"].font = f_kpi_lbl
        ws["F4"].alignment = align_right
        ws["G4"] = f"=AVERAGE(I6:I{last_row})"
        ws["G4"].font = f_kpi_val
        ws["G4"].alignment = align_center
        ws["G4"].fill = fill_kpi
        ws["G4"].border = border_cell
        ws["G4"].number_format = "0.0"

        for col_idx, (h_text, width) in enumerate(col_headers, start=1):
            cell = ws.cell(row=5, column=col_idx, value=h_text)
            cell.font = f_header
            cell.fill = fill_header_dark
            cell.alignment = align_center
            cell.border = border_header
            ws.column_dimensions[get_column_letter(col_idx)].width = width

        ws.row_dimensions[5].height = 42

        for idx, name in enumerate(student_list, start=1):
            r = 5 + idx
            ws.row_dimensions[r].height = 24
            zebra = (idx % 2 == 0)

            c_num = ws.cell(row=r, column=1, value=idx)
            c_num.font = f_bold
            c_num.alignment = align_center
            c_num.border = border_cell
            if zebra: c_num.fill = fill_zebra

            c_name = ws.cell(row=r, column=2, value=name)
            c_name.font = f_data
            c_name.alignment = Alignment(horizontal="left", vertical="center")
            c_name.border = border_cell
            if zebra: c_name.fill = fill_zebra

            # 4 Criteria Columns: C, D, E, F
            for c_idx in range(3, 7):
                cell = ws.cell(row=r, column=c_idx)
                cell.font = f_data
                cell.alignment = align_center
                cell.border = border_cell
                if zebra: cell.fill = fill_zebra

            # Col G: Puntaje Total (Máx 60)
            c_tot = ws.cell(row=r, column=7, value=f"=SUM(C{r}:F{r})")
            c_tot.font = f_bold
            c_tot.alignment = align_center
            c_tot.border = border_cell
            if zebra: c_tot.fill = fill_zebra

            # Col H: Nota (1.0 - 7.0)
            c_nota = ws.cell(row=r, column=8, value=f'=IF(G{r}="","",ROUND(IF(G{r}<36, 1 + 3*(G{r}/36), 4 + 3*((G{r}-36)/(60-36))), 1))')
            c_nota.font = f_bold
            c_nota.alignment = align_center
            c_nota.fill = fill_nota
            c_nota.border = border_cell
            c_nota.number_format = "0.0"

            # Col I: Nota e-campus Moodle (10 - 70)
            c_moodle = ws.cell(row=r, column=9, value=f'=IF(H{r}="","",H{r}*10)')
            c_moodle.font = f_bold
            c_moodle.alignment = align_center
            c_moodle.fill = fill_nota
            c_moodle.border = border_cell
            c_moodle.number_format = "0.0"

            # Col J: Estado
            c_est = ws.cell(row=r, column=10, value=f'=IF(H{r}="","",IF(H{r}>=4.0,"APROBADO","REPROBADO"))')
            c_est.font = f_bold
            c_est.alignment = align_center
            c_est.border = border_cell
            if zebra: c_est.fill = fill_zebra

            # Col K: Observaciones
            c_obs = ws.cell(row=r, column=11)
            c_obs.font = f_data
            c_obs.alignment = Alignment(horizontal="left", vertical="center")
            c_obs.border = border_cell
            if zebra: c_obs.fill = fill_zebra

    add_section_sheet("Seccion_Martes", "SECCIÓN 51 (MARTES)", STUDENTS_SEC51)
    add_section_sheet("Seccion_52", "SECCIÓN 52", STUDENTS_SEC52)

    # ================= SHEET 3: Matriz_Rubrica =================
    ws2 = wb.create_sheet(title="Matriz_Rubrica")
    ws2.views.sheetView[0].showGridLines = True

    ws2["A1"] = f"MATRIZ ANALÍTICA — {title_main}"
    ws2["A1"].font = f_title
    ws2["A2"] = "Desglose por niveles de desempeño para cada criterio de evaluación (Total: 60 Puntos = 100%)"
    ws2["A2"].font = f_subtitle

    matriz_headers = [
        ("Criterio y Ponderación", 26),
        ("Excelente (100%)", 32),
        ("Bueno (75%)", 32),
        ("Suficiente (50%)", 32),
        ("Insuficiente (0-25%)", 32),
        ("Pts Máx", 10),
        ("Pond (%)", 10)
    ]

    for col_idx, (h_text, width) in enumerate(matriz_headers, start=1):
        cell = ws2.cell(row=4, column=col_idx, value=h_text)
        cell.font = f_header
        cell.fill = fill_header_dark
        cell.alignment = align_center
        cell.border = border_header
        ws2.column_dimensions[get_column_letter(col_idx)].width = width

    ws2.row_dimensions[4].height = 28

    for idx, (crit, ex, bu, suf, ins, pts, pond) in enumerate(rubric_rows, start=5):
        ws2.row_dimensions[idx].height = 68
        zebra = (idx % 2 == 0)

        c1 = ws2.cell(row=idx, column=1, value=crit)
        c1.font = f_bold
        c1.alignment = align_left
        c1.border = border_cell

        for col_i, text in enumerate([ex, bu, suf, ins], start=2):
            c = ws2.cell(row=idx, column=col_i, value=text)
            c.font = f_data
            c.alignment = align_left
            c.border = border_cell
            if zebra: c.fill = fill_zebra

        c_p = ws2.cell(row=idx, column=6, value=pts)
        c_p.font = f_bold
        c_p.alignment = align_center
        c_p.border = border_cell
        c_p.fill = fill_header_light

        c_po = ws2.cell(row=idx, column=7, value=pond)
        c_po.font = f_bold
        c_po.alignment = align_center
        c_po.border = border_cell
        c_po.fill = fill_header_light

    # ================= SHEET 4: Escala_Conversion =================
    ws3 = wb.create_sheet(title="Escala_Conversion")
    ws3.views.sheetView[0].showGridLines = True

    ws3["A1"] = "TABLA OFICIAL DE CONVERSIÓN: PUNTAJE A NOTA (ESCALA 1.0 - 7.0 Y ESCALA MOODLE 10 - 70)"
    ws3["A1"].font = f_title
    ws3["A2"] = "Puntaje Máximo: 60 Puntos · Puntaje de Aprobación (Nota 4.0 / 40,0): 36 Puntos (60% de Exigencia)"
    ws3["A2"].font = f_subtitle

    scale_headers = [
        ("Puntaje", 12),
        ("Nota (1.0 - 7.0)", 16),
        ("Nota Moodle (10 - 70)", 20),
        ("Estado Académico", 18),
        ("Nivel de Desempeño", 44)
    ]

    for col_idx, (h_text, width) in enumerate(scale_headers, start=1):
        cell = ws3.cell(row=4, column=col_idx, value=h_text)
        cell.font = f_header
        cell.fill = fill_header_dark
        cell.alignment = align_center
        cell.border = border_header
        ws3.column_dimensions[get_column_letter(col_idx)].width = width

    ws3.row_dimensions[4].height = 26

    for p in range(60, -1, -1):
        r = 4 + (60 - p) + 1
        ws3.row_dimensions[r].height = 19
        zebra = ((60 - p) % 2 == 0)

        c_p = ws3.cell(row=r, column=1, value=p)
        c_p.font = f_bold
        c_p.alignment = align_center
        c_p.border = border_cell
        if zebra: c_p.fill = fill_zebra

        if p >= 36:
            grade = round(4.0 + 3.0 * ((p - 36) / (60 - 36)), 1)
            status = "APROBADO"
        else:
            grade = round(1.0 + 3.0 * (p / 36), 1)
            status = "REPROBADO"

        c_g = ws3.cell(row=r, column=2, value=grade)
        c_g.font = f_bold
        c_g.alignment = align_center
        c_g.border = border_cell
        c_g.fill = fill_nota if grade >= 4.0 else fill_zebra
        c_g.number_format = "0.0"

        c_m = ws3.cell(row=r, column=3, value=round(grade * 10, 1))
        c_m.font = f_bold
        c_m.alignment = align_center
        c_m.border = border_cell
        c_m.fill = fill_nota if grade >= 4.0 else fill_zebra
        c_m.number_format = "0.0"

        c_s = ws3.cell(row=r, column=4, value=status)
        c_s.font = f_bold
        c_s.alignment = align_center
        c_s.border = border_cell
        if zebra: c_s.fill = fill_zebra

        if p == 60:
            desc = "Sobresaliente: Dominio técnico e integración visual impecable."
        elif p >= 54:
            desc = "Muy Bueno: Excelente nivel de ejecución con observaciones mínimas."
        elif p >= 48:
            desc = "Bueno: Cumplimiento consistente de todos los requerimientos."
        elif p >= 42:
            desc = "Aceptable: Cumple los requisitos base con detalles de calibración."
        elif p >= 36:
            desc = "Aprobado (Corte 60%): Cumplimiento mínimo de los objetivos formativos."
        elif p >= 24:
            desc = "Reprobado: Falencias importantes en shaders, iluminación o documentación."
        else:
            desc = "Insuficiente: Incumplimiento crítico de los requisitos de entrega."

        c_d = ws3.cell(row=r, column=5, value=desc)
        c_d.font = f_data
        c_d.alignment = Alignment(horizontal="left", vertical="center")
        c_d.border = border_cell
        if zebra: c_d.fill = fill_zebra

    for path in dest_paths:
        wb.save(path)
        print(f"Saved: {path}")


def main():
    # 1. ENTREGA 3
    headers_e3 = [
        ("N°", 5),
        ("Estudiante", 36),
        ("1. Referencias:\nShaders, Luz y Medios\n(Máx 12 pts / 20%)", 19),
        ("2. Creación Shader\n/ Material Estilo\n(Máx 21 pts / 35%)", 19),
        ("3. Prueba de Luz en\nModelos/Sprites Test\n(Máx 18 pts / 30%)", 19),
        ("4. Orden del Grafo\ny Nomenclatura\n(Máx 9 pts / 15%)", 18),
        ("Puntaje\nTotal\n(Máx 60)", 11),
        ("Nota Final\n(1.0 - 7.0)", 12),
        ("Nota Moodle\n(10 - 70)", 13),
        ("Estado\nAcadémico", 13),
        ("Observaciones y Retroalimentación (Para copiar a Moodle)", 44)
    ]

    rows_e3 = [
        (
            "1. Referencias de Shaders, Luz y Otros Medios",
            "Moodboard completo y riguroso que integra referencias de shaders, iluminación y otros medios externos (cine, animación, arte). Explica qué rasgos técnicos se extraen.",
            "Incluye referencias de videojuegos y de otros medios bien seleccionadas, pero el desglose técnico de cómo traducirlas al motor es general.",
            "Moodboard incompleto (omite referencias de otros medios o de shaders) o presenta imágenes sueltas sin justificación ni conexión clara.",
            "No presenta lámina de referencias o las imágenes no guardan relación con el prototipo presentado.",
            12,
            "20%"
        ),
        (
            "2. Creación del Shader / Material de Estilo (NPR / 3D / 2D)",
            "Construye un shader NPR o estilizado (3D o 2D) sólido, bien resuelto y fiel a la referencia. Expone múltiples parámetros funcionales en instancia para ajustar el estilo en vivo.",
            "El shader logra el estilo propuesto y cuenta con parámetros expuestos, pero presenta detalles menores de calibración o poca flexibilidad.",
            "Shader demasiado básico o con errores de construcción nodal; carece de instancias parametrizadas o no logra reproducir el estilo planteado.",
            "No construye un shader propio (utiliza materiales por defecto sin trabajar) o el grafo se encuentra roto.",
            21,
            "35%"
        ),
        (
            "3. Prueba de Iluminación en Modelos/Sprites de Test",
            "Implementa el estilo en uno o varios modelos/sprites de test bajo un esquema de luces intencionado. Demuestra cómo reacciona el shader ante dirección, color e intensidad.",
            "El estilo está aplicado en el modelo/sprite de prueba con iluminación funcional, aunque falta refinar el contraste de sombras o separación del fondo.",
            "La iluminación de prueba es plana o arbitraria y no permite apreciar correctamente el comportamiento del shader ni el volumen.",
            "No existe escena de prueba iluminada o las luces destruyen por completo la lectura del material.",
            18,
            "30%"
        ),
        (
            "4. Orden del Grafo, Nomenclatura y Presentación",
            "Grafo de nodos limpio, alineado y documentado con cajas de comentario. Nomenclatura estándar respetada en todos los activos. Entrega todas las capturas comparativas.",
            "Proyecto y grafo comprensibles con descuidos menores en los nombres de algunos archivos o falta de comentarios en secciones secundarias.",
            "Desorden evidente en el grafo de nodos, nombres por defecto (NewMaterial) o faltan capturas técnicas del desglose.",
            "Proyecto desorganizado, sin convenciones de nombres, archivos rotos o entrega incompleta de respaldos visuales.",
            9,
            "15%"
        )
    ]

    build_workbook(
        title_main="EVALUACIÓN ENTREGA N°3 (AVANCE EXAMEN): LOOKDEV, NPR Y PROTOTIPO DE ESTILO",
        subtitle_main="Asignatura: Iluminación 3D · Docente: Daniel Rojas (UNIACC) · Escala: 1.0 a 7.0 (Moodle 10 a 70) al 60% de Exigencia (36 pts = 4.0)",
        col_headers=headers_e3,
        rubric_rows=rows_e3,
        dest_paths=[
            r"c:\Users\danie\OneDrive\Escritorio\Rubrica_Evaluacion_Entrega_03.xlsx",
            r"c:\Users\danie\OneDrive\Escritorio\Iluminacion3D\docs\public\Rubrica_Evaluacion_Entrega_03.xlsx"
        ]
    )

    # 2. EXAMEN FINAL
    headers_ex = [
        ("N°", 5),
        ("Estudiante", 36),
        ("1. Shaders y Materiales\nen el Juego (3D/2D)\n(Máx 18 pts / 30%)", 19),
        ("2. Iluminación del Nivel\ny Guía al Jugador\n(Máx 21 pts / 35%)", 19),
        ("3. Breakdown Técnico\nEstilo 80.lv\n(Máx 12 pts / 20%)", 19),
        ("4. Post-Procesado,\nOrden y Rendimiento\n(Máx 9 pts / 15%)", 18),
        ("Puntaje\nTotal\n(Máx 60)", 11),
        ("Nota Final\n(1.0 - 7.0)", 12),
        ("Nota Moodle\n(10 - 70)", 13),
        ("Estado\nAcadémico", 13),
        ("Observaciones y Retroalimentación (Para copiar a Moodle)", 44)
    ]

    rows_ex = [
        (
            "1. Implementación de Shaders y Materiales en el Juego",
            "El estilo de shaders y materiales (NPR / estilizado en 3D o 2D) está implementado con total consistencia en el nivel jugable. Uso correcto de instancias parametrizadas.",
            "Los shaders principales están bien integrados en el juego y cumplen el estilo propuesto, aunque algunos elementos secundarios conservan materiales genéricos.",
            "Implementación parcial; el shader solo se aplicó a un objeto aislado sin integrarse al resto del nivel, o presenta errores visuales notorios.",
            "No se implementaron shaders propios en el juego o los materiales están rotos/ausentes en la escena final.",
            18,
            "30%"
        ),
        (
            "2. Iluminación del Nivel, Atmósfera y Guía al Jugador",
            "Iluminación del nivel sobresaliente (3D o 2D). Construye atmósfera envolvente, separa planos de profundidad y usa el contraste/temperatura para guiar intuitivamente al jugador.",
            "Buena iluminación general y atmósfera lograda, pero la jerarquía visual compite en ciertas zonas del nivel o existen áreas muy oscuras/sobreexpuestas.",
            "Iluminación plana o meramente utilitaria; ilumina el nivel para que se vea pero carece de intención narrativa o dirección visual para el jugador.",
            "Nivel sin trabajo de iluminación (luz por defecto del motor), sombras rotas o escena ilegible durante la partida.",
            21,
            "35%"
        ),
        (
            "3. Artículo / Breakdown Técnico Estilo 80.lv",
            "Artículo visual impecable, claro y conciso. Incluye las 4 secciones: referencias multimediales, explicación del grafo del shader, secuencia paso a paso de capas de luz y conclusión.",
            "Artículo completo y bien estructurado que explica cómo llegaron al resultado, aunque le falta mayor detalle en nodos o en alguna captura intermedia de luz.",
            "Documento incompleto o superficial; muestra capturas finales sin explicar el proceso técnico de cómo construyeron los shaders ni las capas de iluminación.",
            "No entrega el Breakdown técnico o presenta un documento sin capturas del proceso ni explicación propia.",
            12,
            "20%"
        ),
        (
            "4. Post-Procesado, Orden del Proyecto y Rendimiento",
            "Acabado final pulido mediante Post-Processing (color, exposición, Bloom y niebla). Proyecto ordenado con nomenclatura estándar y rendimiento fluido en tiempo real.",
            "Post-procesado correcto y proyecto ordenado con descuidos menores de nomenclatura o leves caídas de rendimiento en sectores específicos.",
            "Sin ajustes de post-procesado (exposición descontrolada), desorden evidente en carpetas del motor o problemas de rendimiento por exceso de luces.",
            "Proyecto desorganizado, archivos faltantes, sin post-procesado o el juego no logra ejecutarse de manera estable en la presentación.",
            9,
            "15%"
        )
    ]

    build_workbook(
        title_main="EVALUACIÓN EXAMEN FINAL: INTEGRACIÓN EN JUEGO Y BREAKDOWN 80.LV",
        subtitle_main="Asignatura: Iluminación 3D · Docente: Daniel Rojas (UNIACC) · Escala: 1.0 a 7.0 (Moodle 10 a 70) al 60% de Exigencia (36 pts = 4.0)",
        col_headers=headers_ex,
        rubric_rows=rows_ex,
        dest_paths=[
            r"c:\Users\danie\OneDrive\Escritorio\Rubrica_Evaluacion_Examen_Final.xlsx",
            r"c:\Users\danie\OneDrive\Escritorio\Iluminacion3D\docs\public\Rubrica_Evaluacion_Examen_Final.xlsx"
        ]
    )

if __name__ == "__main__":
    main()
