from database import get_db_connection


# =========================
# OBTENER REGISTROS
# =========================

def get_records_db(nombre='', libro='', folio=''):
	
	
    conn = get_db_connection()

    query = '''
    SELECT * FROM bautismos
    WHERE 1=1
    '''

    params = []

    if nombre:
        query += ' AND bautizado LIKE ? '
        params.append(f'%{nombre}%')

    if libro:
        query += ' AND libro = ? '
        params.append(libro)

    if folio:
        query += ' AND folio = ? '
        params.append(folio)

    query += ' ORDER BY id DESC LIMIT 100 '

    rows = conn.execute(query, params).fetchall()

    conn.close()

    return [dict(row) for row in rows]
    
# =========================
# RESUMEN BAUTIZOS
# =========================

def resumen_bautizos_db():

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

    return [
        dict(row)
        for row in rows
    ]
    
# =========================
# ACTUALIZAR REGISTRO
# =========================

def update_record_db(record_id, data):

    conn = get_db_connection()

    fecha_bautismo_iso = ''
    fecha_nacimiento_iso = ''

    if data['fecha_bautismo']:

        partes = data['fecha_bautismo'].split('/')

        if len(partes) == 3:

            year = partes[2]

            if len(year) == 2:

                year = f"20{year}"

            fecha_bautismo_iso = (
                f"{year}-{partes[1]}-{partes[0]}"
            )

    if data['fecha_nacimiento']:

        partes = data['fecha_nacimiento'].split('/')

        if len(partes) == 3:

            year = partes[2]

            if len(year) == 2:

                year = f"20{year}"

            fecha_nacimiento_iso = (
                f"{year}-{partes[1]}-{partes[0]}"
            )

    conn.execute(
        '''
        UPDATE bautismos
        SET
            bautizado=?,
            libro=?,
            folio=?,
            partida=?,
            fecha_bautismo=?,
            fecha_nacimiento=?,
            fecha_bautismo_iso=?,
            fecha_nacimiento_iso=?,
            padres=?,
            padrinos=?,
            celebrante=?
        WHERE id=?
        ''',
        (
            data['bautizado'],
            data['libro'],
            data['folio'],
            data['partida'],
            data['fecha_bautismo'],
            data['fecha_nacimiento'],
            fecha_bautismo_iso,
            fecha_nacimiento_iso,
            data['padres'],
            data['padrinos'],
            data['celebrante'],
            record_id
        )
    )

    conn.commit()

    conn.close()

# =========================
# ELIMINAR REGISTRO
# =========================

def delete_record_db(record_id):

    conn = get_db_connection()

    conn.execute(
        'DELETE FROM bautismos WHERE id=?',
        (record_id,)
    )

    conn.commit()

    conn.close()

# =========================
# CREAR REGISTRO
# =========================

def create_record_db(data):

    conn = get_db_connection()

    fecha_bautismo_iso = ''
    fecha_nacimiento_iso = ''

    if data['fecha_bautismo']:

        partes = data['fecha_bautismo'].split('/')

        if len(partes) == 3:

            year = partes[2]

            if len(year) == 2:

                year = f"20{year}"

            fecha_bautismo_iso = (
                f"{year}-{partes[1]}-{partes[0]}"
            )

    if data['fecha_nacimiento']:

        partes = data['fecha_nacimiento'].split('/')

        if len(partes) == 3:

            year = partes[2]

            if len(year) == 2:

                year = f"20{year}"

            fecha_nacimiento_iso = (
                f"{year}-{partes[1]}-{partes[0]}"
            )

    conn.execute(
        '''
        INSERT INTO bautismos (
            bautizado,
            libro,
            folio,
            partida,
            fecha_bautismo,
            fecha_nacimiento,
            fecha_bautismo_iso,
            fecha_nacimiento_iso,
            padres,
            padrinos,
            celebrante
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        (
            data['bautizado'],
            data['libro'],
            data['folio'],
            data['partida'],
            data['fecha_bautismo'],
            data['fecha_nacimiento'],
            fecha_bautismo_iso,
            fecha_nacimiento_iso,
            data['padres'],
            data['padrinos'],
            data['celebrante']
        )
    )

    conn.commit()

    conn.close()


