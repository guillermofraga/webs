  const form = document.getElementById("reserve-form");
  const btn = document.getElementById("submitBtn");
  const text = document.getElementById("btnText");
  const spinner = document.getElementById("spinner");

  form.addEventListener("submit", () => {
    btn.disabled = true;                 // desactiva el botón
    text.textContent = "Procesando Reserva...";  // cambia el texto
    spinner.classList.remove("hidden");  // muestra el spinner
  });