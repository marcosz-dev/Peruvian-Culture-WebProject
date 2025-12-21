let baseDeDatosRelatos = [];

document.addEventListener('DOMContentLoaded', () => {
    // Detecta si estamos en la página de mitos o de cuentos
    const listaMitos = document.getElementById('lista-mitos');
    const listaCuentos = document.getElementById('lista-cuentos');
    
    // Solo carga si existe alguna de las listas en la página
    if (listaMitos || listaCuentos) {
        cargarHistorias();
    }

    // Configurar cierre del modal (click fuera o en la X)
    const modal = document.getElementById('modal-historia');
    if (modal) {
        window.onclick = function(event) {
            if (event.target == modal) {
                cerrarModal();
            }
        }
    }
});

async function cargarHistorias() {
    try {
        const response = await fetch('/api/relatos');
        baseDeDatosRelatos = await response.json();

        const listaMitos = document.getElementById('lista-mitos');
        const listaCuentos = document.getElementById('lista-cuentos');

        // Limpia listas antes de llenar
        if(listaMitos) listaMitos.innerHTML = '';
        if(listaCuentos) listaCuentos.innerHTML = '';

        baseDeDatosRelatos.forEach((relato, index) => {
            // Crea el elemento de lista
            const li = document.createElement('li');
            li.className = 'item-relato'; // Clase para estilo

            // HTML INTERNO: Título + Autor + BOTÓN LEER
            li.innerHTML = `
                <div class="info-relato">
                    <strong>${relato.titulo}</strong>
                    <span class="autor-relato">Por: ${relato.autor}</span>
                </div>
                <button class="btn-leer" onclick="abrirModal(${index})">Leer Historia</button>
            `;

            // Distribuir en la lista correcta
            if (relato.tipo === 'Mito' || relato.tipo === 'Leyenda') {
                if(listaMitos) listaMitos.appendChild(li);
            } else if (relato.tipo === 'Cuento') {
                if(listaCuentos) listaCuentos.appendChild(li);
            }
        });

    } catch (error) {
        console.error('Error cargando relatos:', error);
    }
}

// Función global para abrir el modal
window.abrirModal = function(index) {
    const relato = baseDeDatosRelatos[index];
    if (!relato) return;

    const modal = document.getElementById('modal-historia');
    if (modal) {
        document.getElementById('m-titulo').innerText = relato.titulo;
        document.getElementById('m-autor').innerText = relato.autor;
        document.getElementById('m-region').innerText = relato.region;
        document.getElementById('m-contenido').innerText = relato.contenido || "Contenido no disponible. Ejecuta setup_db.py nuevamente.";
        
        modal.style.display = 'flex';
    } else {
        console.error("No se encontró el modal en el HTML");
    }
}

window.cerrarModal = function() {
    document.getElementById('modal-historia').style.display = 'none';
}