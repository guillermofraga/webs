function crearModalRifa() {
    // Crear el contenedor del modal
    const modal = document.createElement('div');
    modal.id = 'modalRaffle';
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(8px);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.3s ease;
    `;

    // Contenido del modal
    modal.innerHTML = `
        <div style="
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            padding: 2rem;
            width: 90%;
            max-width: 400px;
            color: white;
            font-family: system-ui, sans-serif;
            transform: scale(0.9);
            transition: transform 0.3s ease;
        ">
            <h3 style="margin: 0 0 1.5rem; text-align: center; font-weight: bold;">
                Vota en la Rifa
            </h3>
            <form id="formRaffle" method="post" action="/raffle/vote" style="display: flex; flex-direction: column; gap: 1rem;">
                <input
                    name="email" 
                    type="email" 
                    placeholder="Tu correo electrónico" 
                    required 
                    style="
                        padding: 0.75rem;
                        border: 1px solid rgba(255, 255, 255, 0.3);
                        background: rgba(255, 255, 255, 0.1);
                        border-radius: 6px;
                        color: white;
                        outline: none;
                    "
                />
                <select 
                    name="precio_rifa"
                    required 
                    style="
                        padding: 0.75rem;
                        border: 1px solid rgba(255, 255, 255, 0.3);
                        background: rgba(255, 255, 255, 0.1);
                        border-radius: 6px;
                        color: #ffffff;
                        outline: none;
                    "
                >
                    <option value="" disabled selected>Selecciona precio de la rifa</option>
                    <option style="color: #000" value="2">2€</option>
                    <option style="color: #000" value="3">3€</option>
                    <option style="color: #000" value="5">5€</option>
                </select>
                
                <p style="
                    font-size: 0.8rem;
                    color: #fff;
                    text-align: center;
                    margin-top: 1rem;
                    font-weight: 500;
                    opacity: 0.9;
                ">
                    <span style="color: #FAD201; font-weight: bold">Aviso:</span> El precio de la rifa más votado será el seleccionado para la compra.
                </p>   

                <button 
                    type="submit"
                    style="
                        background: #00c4c7;
                        color: white;
                        border: none;
                        padding: 0.75rem;
                        border-radius: 6px;
                        font-weight: bold;
                        cursor: pointer;
                        transition: transform 0.2s;
                    "
                    onmouseover="this.style.transform='scale(1.02)'"
                    onmouseout="this.style.transform='scale(1)'"
                >
                    Confirmar Votación
                </button>
            </form>
            <button 
                id="closeModal"
                style="
                    position: absolute;
                    top: 1rem;
                    right: 1rem;
                    background: none;
                    border: none;
                    color: white;
                    font-size: 1.5rem;
                    cursor: pointer;
                "
            >&times;</button>
        </div>
    `;

    // Añadir al body
    document.body.appendChild(modal);

    // Animar aparición
    setTimeout(() => {
        modal.style.opacity = '1';
        modal.style.pointerEvents = 'auto';
        modal.querySelector('div').style.transform = 'scale(1)';
    }, 10);

    // Cerrar con X
    modal.querySelector('#closeModal').onclick = () => cerrarModal();

    // Cerrar al hacer clic fuera
    modal.onclick = (e) => {
        if (e.target === modal) cerrarModal();
    };

    // Cerrar con ESC
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') cerrarModal();
    });

    function cerrarModal() {
        modal.style.opacity = '0';
        modal.style.pointerEvents = 'none';
        modal.querySelector('div').style.transform = 'scale(0.9)';
        setTimeout(() => modal.remove(), 300);
    }

    document.getElementById('formRaffle').onsubmit = (e) => {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);

    const boton = e.target.querySelector("button[type='submit']");
    boton.textContent = "Procesando voto...";
    boton.disabled = true;

    fetch(form.action, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then((data) => {  // ✅ Correcto
    if (data.success) {
        modal.innerHTML = `
            <div style="text-align: center; color: white;">
                <h3>✅ Éxito</h3>
                <p>${data.message}</p>
            </div>
        `;
    } else {
        modal.innerHTML = `
            <div style="text-align: center; color: white;">
                <h3>❌ Error</h3>
                <p>${data.message}</p>
            </div>
        `;
    }
})
    .catch((err) => {  // ✅ Correcto
        modal.innerHTML = `
            <div style="text-align: center; color: white;">
                <h3>❌ Error</h3>
                <p>No se pudo conectar con el servidor.</p>
            </div>
        `;
    });   
};   

}

// Abrir modal al hacer clic en el botón de la rifa
document.getElementById('OpenModal')?.addEventListener('click', crearModalRifa);   