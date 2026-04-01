// Mobile Menu Toggle
      const hamburgerBtn = document.getElementById('hamburger-btn');
      const mobileMenu = document.getElementById('mobile-menu');
      const menuLinks = mobileMenu.querySelectorAll('.mobile-menu-link, button');

      hamburgerBtn.addEventListener('click', () => {
        hamburgerBtn.classList.toggle('active');
        mobileMenu.classList.toggle('active');
      });

      // Close menu when clicking on a link
      menuLinks.forEach(link => {
        link.addEventListener('click', () => {
          hamburgerBtn.classList.remove('active');
          mobileMenu.classList.remove('active');
        });
      });

      // Close menu when clicking outside
      document.addEventListener('click', (e) => {
        if (!e.target.closest('header')) {
          hamburgerBtn.classList.remove('active');
          mobileMenu.classList.remove('active');
        }
      });

      // Modal Functions
      const contactModal = document.getElementById('contactModal');
      const contactForm = document.getElementById('contactForm');
      const openModalBtns = document.querySelectorAll('.open-modal-btn');
      const cancelBtn = document.querySelector('.modal-cancel');

      function openModal() {
        contactModal.classList.add('active');
        document.body.style.overflow = 'hidden';
        // Limpiar alerta anterior
        const alertElement = document.getElementById('modalAlert');
        alertElement.classList.remove('active');
      }

      function closeModal() {
        contactModal.classList.remove('active');
        document.body.style.overflow = 'auto';
      }

      function showAlert(message, type = 'success') {
        const alertElement = document.getElementById('modalAlert');
        alertElement.textContent = message;
        alertElement.className = `modal-alert ${type} active`;
        
        // Auto-hide después de 5 segundos
        setTimeout(() => {
          alertElement.classList.remove('active');
        }, 5000);
      }

      // Event listeners para los botones de abrir modal
      openModalBtns.forEach(btn => {
        btn.addEventListener('click', openModal);
      });

      // Event listener para el botón de cancelar
      cancelBtn.addEventListener('click', closeModal);

      function handleSubmit(event) {
        event.preventDefault();
        
        const submitBtn = document.getElementById('submitBtn');
        const submitText = document.getElementById('submitText');
        
        // Obtener los valores del formulario
        const asunto = document.getElementById('asunto').value;
        const correo = document.getElementById('correo').value;
        const necesidades = document.getElementById('necesidades').value;
        const observaciones = document.getElementById('observaciones').value;
        
        // Deshabilitar botón y mostrar spinner
        submitBtn.disabled = true;
        submitText.innerHTML = '<span class="spinner"></span>Enviando...';
        
        // Enviar los datos al backend
        fetch('/send-email', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            asunto: asunto,
            correo: correo,
            necesidades: necesidades,
            observaciones: observaciones
          })
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            showAlert('¡Correo enviado exitosamente! Te responderemos pronto.', 'success');
            // Restaurar botón
            submitBtn.disabled = false;
            submitText.innerHTML = 'Enviar';
            contactForm.reset();
            setTimeout(() => {
              closeModal();
            }, 3000);
          } else {
            showAlert('Error al enviar el correo. Por favor, intentalo de nuevo más tarde.', 'error');
            // Restaurar botón en caso de error
            submitBtn.disabled = false;
            submitText.innerHTML = 'Enviar';
          }
        })
        .catch(error => {
          console.error('Error:', error);
          showAlert('Error al enviar el correo. Por favor, intentalo de nuevo más tarde.', 'error');
          // Restaurar botón en caso de error
          submitBtn.disabled = false;
          submitText.innerHTML = 'Enviar';
        });
      }

      // Cerrar modal al hacer click fuera del contenido
      contactModal.addEventListener('click', (e) => {
        if (e.target === contactModal) {
          closeModal();
        }
      });

      // Cerrar modal con tecla Escape
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && contactModal.classList.contains('active')) {
          closeModal();
        }
      });