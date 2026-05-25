from flask import (
    request,
    jsonify,
    render_template,
    send_file,
    session,
    redirect
)

from werkzeug.security import (
    check_password_hash
)

from app import app

from auth import (
    USERS,
    login_required,
    admin_required
)

from models import (
    get_records_db,
    create_record_db,
    update_record_db,
    delete_record_db,
    resumen_bautizos_db
)

from reports import (
    generar_reporte_anual_pdf,
    generar_certificado_pdf
)


# =========================
# LOGIN
# =========================

@app.route('/login', methods=['GET', 'POST'])
def login():

    error = ''

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = USERS.get(username)

        if user and check_password_hash(
            user['password'],
            password
        ):

            session.permanent = True

            session['user'] = username
            session['role'] = user['role']

            return redirect('/')

        error = 'Usuario o contraseña incorrectos'

    return render_template(
        'login.html',
        error=error
    )


# =========================
# LOGOUT
# =========================

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/login')


# =========================
# INDEX
# =========================

@app.route('/')
@login_required
def index():

    return render_template(
        'index.html',
        role=session.get('role'),
        session=session
    )


# =========================
# OBTENER REGISTROS
# =========================

@app.route('/api/records', methods=['GET'])
@login_required
def get_records():

    nombre = request.args.get('nombre', '')
    libro = request.args.get('libro', '')
    folio = request.args.get('folio', '')

    records = get_records_db(
        nombre,
        libro,
        folio
    )

    return jsonify(records)


# =========================
# CREAR REGISTRO
# =========================

@app.route('/api/records', methods=['POST'])
@login_required
def create_record():

    data = request.json

    create_record_db(data)

    return jsonify({
        'status': 'created'
    })


# =========================
# ACTUALIZAR REGISTRO
# =========================

@app.route('/api/records/<int:record_id>', methods=['PUT'])
@login_required
@admin_required
def update_record(record_id):

    data = request.json

    update_record_db(
        record_id,
        data
    )

    return jsonify({
        'status': 'updated'
    })


# =========================
# ELIMINAR REGISTRO
# =========================

@app.route('/api/records/<int:record_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_record(record_id):

    delete_record_db(record_id)

    return jsonify({
        'status': 'deleted'
    })


# =========================
# RESUMEN BAUTIZOS
# =========================

@app.route('/api/resumen-bautizos')
@login_required
def resumen_bautizos():

    data = resumen_bautizos_db()

    return jsonify(data)


# =========================
# PDF RESUMEN
# =========================

@app.route('/api/reporte-anual-pdf')
@login_required
def reporte_anual_pdf():

    pdf_path = generar_reporte_anual_pdf()

    return send_file(
        pdf_path,
        as_attachment=False,
        download_name='reporte_anual_bautizos.pdf',
        mimetype='application/pdf'
    )


# =========================
# PDF CERTIFICADO
# =========================

@app.route('/api/certificado/<int:record_id>')
@login_required
def generar_certificado(record_id):

    pdf_path = generar_certificado_pdf(record_id)

    if not pdf_path:
        return 'Registro no encontrado', 404

    return send_file(
        pdf_path,
        as_attachment=False,
        download_name='constancia_bautismo.pdf',
        mimetype='application/pdf'
    )
