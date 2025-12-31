// --- SAVE DATA ---
const saveCheckbox = document.getElementById("save-data");
const nombreInput = document.getElementById("nombre");
const telefonoInput = document.getElementById("phone");
const emailInput = document.getElementById("email");

// Al cargar la página, rellenar datos si existen
document.addEventListener("DOMContentLoaded", () => {
  const saved = localStorage.getItem("reservaDatos");
  if (saved) {
    const data = JSON.parse(saved);
    nombreInput.value = data.nombre || "";
    telefonoInput.value = data.telefono || "";
    emailInput.value = data.email || "";
    saveCheckbox.checked = true; // marcar la casilla si ya hay datos guardados
  }
});

// Al marcar o desmarcar el checkbox
saveCheckbox.addEventListener("change", () => {
  if (saveCheckbox.checked) {
    // Guardar datos actuales
    const data = {
      nombre: nombreInput.value,
      telefono: telefonoInput.value,
      email: emailInput.value,
    };
    localStorage.setItem("reservaDatos", JSON.stringify(data));
  } else {
    // Borrar datos guardados
    localStorage.removeItem("reservaDatos");
  }
});

// Opcional: actualizar datos guardados cada vez que el usuario escribe
[nombreInput, telefonoInput, emailInput].forEach((input) => {
  input.addEventListener("input", () => {
    if (saveCheckbox.checked) {
      const data = {
        nombre: nombreInput.value,
        telefono: telefonoInput.value,
        email: emailInput.value,
      };
      localStorage.setItem("reservaDatos", JSON.stringify(data));
    }
  });
});
