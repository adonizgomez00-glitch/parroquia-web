let records = [];

async function loadRecords(){

    const nombre =
    document.getElementById('searchNombre').value;

    const libro =
    document.getElementById('searchLibro').value;

    const folio =
    document.getElementById('searchFolio').value;

    const response = await fetch(
        `/api/records?nombre=${encodeURIComponent(nombre)}&libro=${encodeURIComponent(libro)}&folio=${encodeURIComponent(folio)}`
    );

    records = await response.json();

    const table =
    document.getElementById('recordsTable');

    table.innerHTML = '';

    records.forEach(record => {

        const row = document.createElement('tr');

        row.innerHTML = `

        <td>${record.id}</td>

        <td>${record.bautizado || ''}</td>

        <td>${record.fecha_bautismo || ''}</td>

        <td>${record.libro || ''}</td>

        <td>${record.folio || ''}</td>

        <td>${record.partida || ''}</td>

        <td>${record.fecha_nacimiento || ''}</td>

        <td>
            ${(record.padres || '').replace(/ y /g,'<br>')}
        </td>

        <td>
            ${(record.padrinos || '').replace(/ y /g,'<br>')}
        </td>

        <td>${record.celebrante || ''}</td>

        <td>

            <a href="/api/certificado/${record.id}"
            target="_blank">

            <button class="small-btn btn-secondary">
            PDF
            </button>

            </a>

        </td>

        <td>

           ${role === 'admin' ? `

<div class="actions">

    <button class="small-btn btn-primary"
    onclick="editRecord(${record.id})">
    Editar
    </button>

    <button class="small-btn btn-danger"
    onclick="deleteRecord(${record.id})">
    Eliminar
    </button>

</div>

` : '<span style="color:#6b7280;">Solo lectura</span>'}
        </td>

        `;

        table.appendChild(row);

    });

}
function editRecord(id){

    if(role !== 'admin'){
        return;
    }

    const r = records.find(x => x.id === id);

    document.getElementById('recordId').value = r.id;
    document.getElementById('bautizado').value = r.bautizado;
    document.getElementById('libro').value = r.libro;
    document.getElementById('folio').value = r.folio;
    document.getElementById('partida').value = r.partida;
    document.getElementById('fecha_bautismo').value = r.fecha_bautismo;
    document.getElementById('fecha_nacimiento').value = r.fecha_nacimiento;
    document.getElementById('padres').value = r.padres;
    document.getElementById('padrinos').value = r.padrinos;
    document.getElementById('celebrante').value = r.celebrante;

}

function resetForm(){

    document.getElementById('recordForm').reset();

    document.getElementById('recordId').value='';

}

async function deleteRecord(id){

    if(role !== 'admin'){
        return;
    }

    if(!confirm('¿Eliminar registro?')) return;

    await fetch(`/api/records/${id}`,{
        method:'DELETE'
    });

    loadRecords();

}

async function mostrarResumen(){

    const response =
    await fetch('/api/resumen-bautizos');

    const data = await response.json();

    let html = `
    <div class="summary-card">

    <h3>📊 Resumen Anual</h3>

    <br>

    <table>

    <thead>

    <tr>
        <th>Año</th>
        <th>Total</th>
    </tr>

    </thead>

    <tbody>
    `;

    data.forEach(item => {

        html += `
        <tr>
            <td>${item.año}</td>
            <td>${item.total}</td>
        </tr>
        `;

    });

    html += `
    </tbody>
    </table>
    </div>
    `;

    document.getElementById('summaryBox').innerHTML = html;

}

document.getElementById('recordForm')
.addEventListener('submit', async(e)=>{

    e.preventDefault();

    const data = {

        bautizado:
        document.getElementById('bautizado').value,

        libro:
        document.getElementById('libro').value,

        folio:
        document.getElementById('folio').value,

        partida:
        document.getElementById('partida').value,

        fecha_bautismo:
        document.getElementById('fecha_bautismo').value,

        fecha_nacimiento:
        document.getElementById('fecha_nacimiento').value,

        padres:
        document.getElementById('padres').value,

        padrinos:
        document.getElementById('padrinos').value,

        celebrante:
        document.getElementById('celebrante').value

    };

    const id =
    document.getElementById('recordId').value;

    if(id){

        await fetch(`/api/records/${id}`,{
            method:'PUT',
            headers:{
                'Content-Type':'application/json'
            },
            body:JSON.stringify(data)
        });

    }else{

        await fetch('/api/records',{
            method:'POST',
            headers:{
                'Content-Type':'application/json'
            },
            body:JSON.stringify(data)
        });

    }

    resetForm();

    loadRecords();

    mostrarResumen();

});

document.getElementById('searchNombre')
.addEventListener('input',loadRecords);

document.getElementById('searchLibro')
.addEventListener('input',loadRecords);

document.getElementById('searchFolio')
.addEventListener('input',loadRecords);

loadRecords();
