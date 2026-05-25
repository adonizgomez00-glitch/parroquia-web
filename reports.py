from reportlab.lib.pagesizes import letter

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

from reportlab.lib import colors

import tempfile

from database import get_db_connection


# =========================
# REPORTE ANUAL PDF
# =========================

def generar_reporte_anual_pdf():

    conn = get_db_connection()

    rows = conn.execute(
        '''
        SELECT
            SUBSTR(fecha_bautismo_iso,1,4) AS año,
            COUNT(*) AS total
        FROM bautismos
        WHERE fecha_bautismo_iso IS NOT NULL
        AND fecha_bautismo_iso != ''
        GROUP BY año
        ORDER BY año ASC
        '''
    ).fetchall()

    conn.close()

    pdfmetrics.registerFont(
        UnicodeCIDFont('HYSMyeongJo-Medium')
    )

    temp_pdf = tempfile.NamedTemporaryFile(
        delete=False,
        suffix='.pdf'
    )

    doc = SimpleDocTemplate(
        temp_pdf.name,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            '<font size=18><b>Reporte Anual de Bautizos</b></font>',
            styles['Title']
        )
    )

    elements.append(Spacer(1,20))

    data = [['Año','Total Bautizos']]

    for row in rows:

        data.append([
            row['año'],
            str(row['total'])
        ])

    table = Table(data, colWidths=[220,220])

    table.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.lightgrey),
        ('GRID',(0,0),(-1,-1),1,colors.black),
        ('BOTTOMPADDING',(0,0),(-1,0),10)
    ]))

    elements.append(table)

    elements.append(Spacer(1,80))

    elements.append(
        Paragraph(
            '''
            <br/><br/><br/>
            _____________________________<br/>
            Firma y sello del párroco
            ''',
            styles['BodyText']
        )
    )

    doc.build(elements)

    return temp_pdf.name


# =========================
# CERTIFICADO PDF
# =========================

def generar_certificado_pdf(record_id):

    conn = get_db_connection()

    row = conn.execute(
        'SELECT * FROM bautismos WHERE id=?',
        (record_id,)
    ).fetchone()

    conn.close()

    if not row:
        return None

    row = dict(row)

    pdfmetrics.registerFont(
        UnicodeCIDFont('HYSMyeongJo-Medium')
    )

    temp_pdf = tempfile.NamedTemporaryFile(
        delete=False,
        suffix='.pdf'
    )

    doc = SimpleDocTemplate(
        temp_pdf.name,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            '<font size=18><b>Constancia de Bautismo</b></font>',
            styles['Title']
        )
    )

    elements.append(Spacer(1,20))

    texto = f'''
    Se hace constar que
    <b>{row['bautizado']}</b>
    se bautizó el día
    <b>{row['fecha_bautismo']}</b>.
    '''

    elements.append(
        Paragraph(texto, styles['BodyText'])
    )

    elements.append(Spacer(1,20))

    data = [

        ['Campo','Valor'],

        ['Libro',row['libro']],
        ['Folio',row['folio']],
        ['Partida',row['partida']],
        ['Nacimiento',row['fecha_nacimiento']],
        ['Padres',row['padres']],
        ['Padrinos',row['padrinos']],
        ['Celebrante',row['celebrante']]

    ]

    table = Table(
        data,
        colWidths=[150,330]
    )

    table.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.lightgrey),
        ('GRID',(0,0),(-1,-1),1,colors.black),
        ('BOTTOMPADDING',(0,0),(-1,0),10)
    ]))

    elements.append(table)

    elements.append(Spacer(1,60))

    elements.append(
        Paragraph(
            '''
            <br/><br/>
            _____________________________<br/>
            Firma y sello parroquial
            ''',
            styles['BodyText']
        )
    )

    doc.build(elements)

    return temp_pdf.name
