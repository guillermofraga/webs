document.getElementById("miForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const button = document.getElementById("ContactButton");
  
  // Activa el loader
  button.classList.add("loading");
  button.disabled = true;

  const formData = new FormData(e.target);
  const response = await fetch("/contact", { method: "POST", body: formData });
  const result = await response.json();
  mostrarPopup(result.message, result.success);

  // Desactiva el loader
  button.classList.remove("loading");
  button.disabled = false;
});

function mostrarPopup(mensaje, esExito) {
    const popup = document.createElement('div');
    popup.textContent = mensaje;
    popup.style.position = 'fixed';
    popup.style.bottom = '20px';
    popup.style.right = '20px';
    popup.style.padding = '10px 20px';
    popup.style.backgroundColor = esExito ? '#4CAF50' : '#f44336';
    popup.style.color = 'white';
    popup.style.borderRadius = '5px';
    popup.style.zIndex = '1000';
    document.body.appendChild(popup);

    if (esExito) {
      document.getElementById("miForm").reset();
    }

    setTimeout(() => popup.remove(), 3000);
}   