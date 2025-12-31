const fechaInput = document.getElementById("fecha");
const horaSelect = document.getElementById("hora");

// Obtener fecha actual en formato YYYY-MM-DD
const hoy = new Date();
const yyyy = hoy.getFullYear();
const mm = String(hoy.getMonth() + 1).padStart(2, "0");
const dd = String(hoy.getDate()).padStart(2, "0");
const fechaHoy = `${yyyy}-${mm}-${dd}`;

// Asignar como mínimo
fechaInput.min = fechaHoy;

// Función para generar opciones de 30 min
function generarHoras(min, max) {
  horaSelect.innerHTML = '<option value="">Selecciona una hora</option>';
  let [minH, minM] = min.split(":").map(Number);
  let [maxH, maxM] = max.split(":").map(Number);

  let current = new Date();
  current.setHours(minH, minM, 0, 0);

  let end = new Date();
  end.setHours(maxH, maxM, 0, 0);

  while (current <= end) {
    let h = String(current.getHours()).padStart(2, "0");
    let m = String(current.getMinutes()).padStart(2, "0");
    let timeStr = `${h}:${m}`;
    let option = document.createElement("option");
    option.value = timeStr;
    option.textContent = timeStr;
    horaSelect.appendChild(option);

    // avanzar 30 min
    current.setMinutes(current.getMinutes() + 30);
  }
}

// Cambiar rango según el día
fechaInput.addEventListener("change", () => {
  const fechaSeleccionada = new Date(fechaInput.value);
  const diaSemana = fechaSeleccionada.getDay(); // 0=domingo, 6=sábado

  if (diaSemana === 5 || diaSemana === 6 || diaSemana === 0) {
    // viernes, sábado, domingo: 12:00 - 23:30
    generarHoras("12:00", "23:30");
  }
  else if (diaSemana === 2) {
    // Martes: Cerrado
    horaSelect.innerHTML = '<option value="">Cerrado</option>';
  }
  else if (diaSemana === 1 || diaSemana === 3 || diaSemana === 4) {
    // Lunes, Miércoles, Jueves: 12:00 - 18:00
    generarHoras("12:00", "18:00");
  }
});