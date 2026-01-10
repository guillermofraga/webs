// --- MODAL DE RESERVA ---
const openBtns = document.querySelectorAll(".open-reserve");
const closeBtn = document.getElementById("close-reserve");
const reserveModal = document.getElementById("reserve-modal");

openBtns.forEach((btn) => {
    btn.addEventListener("click", (e) => {
        e.preventDefault();
        reserveModal.classList.remove("hidden");
    });
});

closeBtn.addEventListener("click", () => {
    reserveModal.classList.add("hidden");
});

reserveModal.addEventListener("click", (e) => {
    if (e.target === reserveModal) {
        reserveModal.classList.add("hidden");
    }
});

// --- MODAL DE CONFIRMACIÓN ---
const confirmModal = document.getElementById("confirm-modal");
const closeConfirm = document.getElementById("close-confirm");
const okConfirm = document.getElementById("ok-confirm");

closeConfirm.addEventListener("click", () => {
    confirmModal.classList.add("hidden");
});
okConfirm.addEventListener("click", () => {
    confirmModal.classList.add("hidden");
});

// --- MODAL DE ERROR ---
const errorModal = document.getElementById("error-modal");
const closeError = document.getElementById("close-error");
const okError = document.getElementById("ok-error");
const errorMessage = document.getElementById("error-message");

closeError.addEventListener("click", () => {
    errorModal.classList.add("hidden");
});
okError.addEventListener("click", () => {
    errorModal.classList.add("hidden");
});

// --- FORMULARIO DE RESERVA ---
const reserveForm = document.getElementById("reserve-form");
const btn = document.getElementById("submitBtn");
const text = document.getElementById("btnText");
const spinner = document.getElementById("spinner");

reserveForm.addEventListener("submit", async function (e) {
    e.preventDefault();

    // 🔄 Estado de carga 
    btn.disabled = true;                 // desactiva el botón
    text.textContent = "Procesando Reserva...";  // cambia el texto
    spinner.classList.remove("hidden");  // muestra el spinner

    const data = {
        nombre: document.getElementById("nombre").value,
        telefono: iti.getNumber(), // Obtener el número completo con prefijo
        email: document.getElementById("email").value,
        fecha: document.getElementById("fecha").value,
        hora: document.getElementById("hora").value,
        personas: document.getElementById("personas").value,
    };

    try {
        const response = await fetch("/api/reservas", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });

        const result = await response.json();

        if (response.ok) {
            reserveModal.classList.add("hidden");

            document.getElementById(
                "confirm-details"
            ).innerText = `Nombre: ${data.nombre}\nFecha: ${formatearFecha(data.fecha)} ${data.hora}\nPersonas: ${data.personas}`;

            confirmModal.classList.remove("hidden");

            // 🔄 Reiniciar formulario
            ReiniciarFormulario();

        }
        else {
            reserveModal.classList.add("hidden");

            // Mostrar el mensaje devuelto por el backend 
            errorMessage.innerText = result.error || "Error desconocido";
            errorModal.classList.remove("hidden");

            // 🔄 Reiniciar formulario
            ReiniciarFormulario();
        }
    } catch (err) {
        reserveModal.classList.add("hidden");

        // Mensaje genérico de error
        errorMessage.innerText = "No se pudo hacer la reserva. Inténtalo de nuevo.";
        errorModal.classList.remove("hidden");

        // 🔄 Reiniciar formulario
        ReiniciarFormulario();
    }
    finally{
        // ✅ Restaurar estado del botón
        btn.disabled = false;
        text.textContent = "Confirmar Reserva";
        spinner.classList.add("hidden");
    }
});


function formatearFecha(fechaISO) {
    const [year, month, day] = fechaISO.split("-");
    return `${day}-${month}-${year}`;
}

function ReiniciarFormulario() {
    if (!document.getElementById("save-data").checked) {
        ["nombre", "phone", "email", "fecha", "hora", "personas"].forEach(id => {
        document.getElementById(id).value = "";
        });
    }
    else {
        // Mantener los datos guardados si el checkbox está marcado y borrar solo los no guardados
        ["fecha", "hora", "personas"].forEach(id => {
        document.getElementById(id).value = "";
        });
    }
}