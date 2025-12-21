document.addEventListener('DOMContentLoaded', () => {
    cargarHistorias();
});

async function cargarHistorias() {
    try {
        const response = await fetch('/api/relatos');
        const relatos = await response.json();

        const listaMitos = document.getElementById('lista-mitos');
        const listaCuentos = document.getElementById('lista-cuentos');

        if(listaMitos) listaMitos.innerHTML = '';
        if(listaCuentos) listaCuentos.innerHTML = '';

        relatos.forEach(relato => {
            const li = document.createElement('li');
            li.innerHTML = `<strong>${relato.titulo}</strong> – ${relato.autor}`;

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