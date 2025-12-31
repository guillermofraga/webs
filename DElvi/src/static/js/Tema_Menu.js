const themeToggle = document.getElementById("theme-toggle");
      const htmlElement = document.documentElement;
      // Check local storage or preference
      if (
        localStorage.theme === "dark" ||
        (!("theme" in localStorage) &&
          window.matchMedia("(prefers-color-scheme: dark)").matches)
      ) {
        htmlElement.classList.add("dark");
      } else {
        htmlElement.classList.remove("dark");
      }
      themeToggle.addEventListener("click", () => {
        if (htmlElement.classList.contains("dark")) {
          htmlElement.classList.remove("dark");
          localStorage.theme = "light";
        } else {
          htmlElement.classList.add("dark");
          localStorage.theme = "dark";
        }
      });

      // Tema móvil
      const mobileThemeToggle = document.getElementById("mobile-theme-toggle");
      const mobileThemeIcon = document.getElementById("mobile-theme-icon");

      mobileThemeToggle.addEventListener("click", () => {
        if (htmlElement.classList.contains("dark")) {
          htmlElement.classList.remove("dark");
          localStorage.theme = "light";
          mobileThemeIcon.textContent = "dark_mode";
        } else {
          htmlElement.classList.add("dark");
          localStorage.theme = "dark";
          mobileThemeIcon.textContent = "light_mode";
        }
      });

      // menu hamburguesa para móvil
      const mobileBtn = document.getElementById("mobile-menu-btn");
      const mobileMenu = document.getElementById("mobile-menu");
      const mobilePanel = document.getElementById("mobile-panel");
      const mobileBackdrop = document.getElementById("mobile-backdrop");
      const mobileLinks = document.querySelectorAll(".mobile-link");

      function toggleMenu() {
        const isOpen = !mobileMenu.classList.contains("hidden");

        if (isOpen) {
          // cerrar
          mobilePanel.classList.add("translate-x-full");
          setTimeout(() => mobileMenu.classList.add("hidden"), 300);
          document.body.classList.remove("overflow-hidden");
        } else {
          // abrir
          mobileMenu.classList.remove("hidden");
          requestAnimationFrame(() =>
            mobilePanel.classList.remove("translate-x-full")
          );
          document.body.classList.add("overflow-hidden");
        }
      }

      mobileBtn.addEventListener("click", toggleMenu);
      mobileBackdrop.addEventListener("click", toggleMenu);

      mobileLinks.forEach((link) => {
        link.addEventListener("click", toggleMenu);
      });