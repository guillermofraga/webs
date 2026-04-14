// contact-modal.js

(function () {
  // === HTML del Modal ===
  const modalHTML = `
    <div id="contactModal" class="modal" style="
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.7);
      z-index: 1000;
      justify-content: center;
      align-items: center;
      overflow-y: auto;
      padding: 20px;
      backdrop-filter: blur(4px);
    ">
      <div class="modal-content" style="
        background: white;
        border-radius: 16px;
        width: 95%;
        max-width: 520px;
        margin: 40px auto;
        padding: 28px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
        position: relative;
        max-height: 90vh;
        overflow-y: auto;
        animation: fadeIn 0.3s ease-out;
      ">
        <h2 class="modal-header" style="
          margin: 0 0 20px;
          font-size: 1.6em;
          color: #1a1a1a;
          font-weight: 600;
          text-align: center;
          border-bottom: 2px solid #f0f0f0;
          padding-bottom: 12px;
        ">Contactar</h2>
        
        <div id="modalAlert" class="modal-alert" style="
          padding: 12px 16px;
          margin-bottom: 20px;
          border-radius: 8px;
          display: none;
          font-size: 0.95em;
        "></div>
        
        <form id="contactForm" style="
          display: flex;
          flex-direction: column;
          gap: 16px;
        ">
          <div class="form-group">
            <label for="asunto" style="
              font-weight: 600;
              color: #333;
              margin-bottom: 6px;
              display: block;
            ">Asunto:</label>
            <input type="text" id="asunto" name="asunto" required placeholder="Asunto del mensaje" style="
              padding: 12px 14px;
              border: 2px solid #e0e0e0;
              border-radius: 8px;
              font-size: 1em;
              transition: border-color 0.2s ease;
              width: 100%;
            " onfocus="this.style.borderColor='#007BFF'" onblur="this.style.borderColor='#e0e0e0'">
          </div>

          <div class="form-group">
            <label for="correo" style="
              font-weight: 600;
              color: #333;
              margin-bottom: 6px;
              display: block;
            ">Correo:</label>
            <input type="email" id="correo" name="correo" required placeholder="tu@email.com" style="
              padding: 12px 14px;
              border: 2px solid #e0e0e0;
              border-radius: 8px;
              font-size: 1em;
              transition: border-color 0.2s ease;
              width: 100%;
            " onfocus="this.style.borderColor='#007BFF'" onblur="this.style.borderColor='#e0e0e0'">
          </div>

          <div class="form-group">
            <label for="necesidades" style="
              font-weight: 600;
              color: #333;
              margin-bottom: 6px;
              display: block;
            ">Necesidades:</label>
            <textarea id="necesidades" name="necesidades" required placeholder="¿Qué es lo que necesitas?" style="
              padding: 12px 14px;
              border: 2px solid #e0e0e0;
              border-radius: 8px;
              font-size: 1em;
              min-height: 120px;
              resize: vertical;
              transition: border-color 0.2s ease;
              width: 100%;
            " onfocus="this.style.borderColor='#007BFF'" onblur="this.style.borderColor='#e0e0e0'"></textarea>
          </div>

        <div class="modal-buttons" style="
        display: flex;
        justify-content: space-between;
        gap: 12px;
        margin-top: 10px;
        flex-wrap: wrap;
        ">
        <button type="button" class="modal-cancel" style="
            padding: 10px 20px;
            background: #f1f1f1;
            color: #333;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            font-weight: 500;
            transition: all 0.2s ease;
            flex: 1;
            min-width: 120px;
        " onmouseover="this.style.background='#e0e0e0'" onmouseout="this.style.background='#f1f1f1'" onfocus="this.style.outline='2px solid #000'; this.style.outlineOffset='2px'" onblur="this.style.outline='none'">
            Cancelar
        </button>

        <button type="submit" id="submitBtn" class="modal-submit" style="
            padding: 10px 24px;
            background: #000;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            font-weight: 500;
            transition: all 0.2s ease;
            flex: 1;
            min-width: 120px;
        " onmouseover="this.style.background='#555'" onmouseout="this.style.background='#000'" onfocus="this.style.outline='2px solid #555'; this.style.outlineOffset='2px'" onblur="this.style.outline='none'">
            <span id="submitText">Enviar</span>
        </button>
        </div>   
        </form>
      </div>
    </div>`;

  // === Inyectar el modal en el body ===
  document.body.insertAdjacentHTML("beforeend", modalHTML);

  // === Lógica del Modal (tu código original, ajustado) ===
  const contactModal = document.getElementById("contactModal");
  const contactForm = document.getElementById("contactForm");
  const openModalBtns = document.querySelectorAll(".open-modal-btn");
  const cancelBtn = document.querySelector(".modal-cancel");

  function openModal() {
    contactModal.style.display = "flex";
    document.body.style.overflow = "hidden";
    const alertElement = document.getElementById("modalAlert");
    alertElement.classList.remove("active");
    alertElement.style.display = "none";
  }

  function openModalWithCourse(button) {
    const curso = button.getAttribute("data-curso");
    const asuntoField = document.getElementById("asunto");
    if (curso && asuntoField) asuntoField.value = curso;
    openModal();
  }

  function closeModal() {
    contactModal.style.display = "none";
    document.body.style.overflow = "auto";
  }

  function showAlert(message, type = "success") {
    const alertElement = document.getElementById("modalAlert");
    alertElement.textContent = message;
    alertElement.className = `modal-alert ${type}`;
    alertElement.style.display = "block";
    alertElement.style.backgroundColor = type === "success" ? "#d4edda" : "#f8d7da";
    alertElement.style.color = type === "success" ? "#155724" : "#721c24";
    alertElement.style.border = `1px solid ${type === "success" ? "#c3e6cb" : "#f5c6cb"}`;

    setTimeout(() => {
      alertElement.style.display = "none";
    }, 5000);
  }

  openModalBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      if (btn.hasAttribute("data-curso")) {
        openModalWithCourse(btn);
      } else {
        openModal();
      }
    });
  });

  cancelBtn.addEventListener("click", closeModal);

  function handleSubmit(event) {
    event.preventDefault();
    const submitBtn = document.getElementById("submitBtn");
    const submitText = document.getElementById("submitText");

    const formData = {
      asunto: document.getElementById("asunto").value,
      correo: document.getElementById("correo").value,
      necesidades: document.getElementById("necesidades").value,
    };

    submitBtn.disabled = true;
    submitText.innerHTML = '<span class="spinner"></span> Enviando...';

    fetch("/send-email", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          showAlert("¡Correo enviado exitosamente! Te responderemos pronto.", "success");
          submitBtn.disabled = false;
          submitText.textContent = "Enviar";
          contactForm.reset();
          setTimeout(closeModal, 3000);
        } else {
          showAlert("Error al enviar el correo. Inténtalo más tarde.", "error");
          submitBtn.disabled = false;
          submitText.textContent = "Enviar";
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        showAlert("Error al enviar el correo. Inténtalo más tarde.", "error");
        submitBtn.disabled = false;
        submitText.textContent = "Enviar";
      });
  }

  contactForm.onsubmit = handleSubmit;

  contactModal.addEventListener("click", (e) => {
    if (e.target === contactModal) closeModal();
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && contactModal.style.display === "flex") closeModal();
  });

  // === Exponer funciones globales (opcional) ===
  window.ContactModal = {
    open: openModal,
    openWithCourse: openModalWithCourse,
    close: closeModal,
    alert: showAlert,
  };
})();