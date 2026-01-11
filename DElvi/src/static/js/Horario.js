const fechaInput = document.getElementById("fecha");
const horaSelect = document.getElementById("hora");


// Cambiar rango según el día
fechaInput.addEventListener("change", async () => {
  const fechaSeleccionada = fechaInput.value;
  horaSelect.innerHTML = '<option value="">Cargando...</option>';

  try {
    const response = await fetch(`/api/disponibilidad/${fechaSeleccionada}`);
    const data = await response.json();

    if (!data.horarios || data.horarios.length === 0) { 
    // Martes cerrado 
    horaSelect.innerHTML = '<option value="">Cerrado</option>'; 
    return; 
    }

    horaSelect.innerHTML = '<option value="">Selecciona una hora</option>';
    data.horarios.forEach(h => {
      const option = document.createElement("option");
      option.value = h.hora;
      option.textContent = h.hora;
      if (!h.disponible) {
        option.disabled = true;
        option.textContent += " (completo)";
      }
      horaSelect.appendChild(option);
    });
  } catch (err) {
    horaSelect.innerHTML = '<option value="">Error al cargar disponibilidad</option>';
  }
});
