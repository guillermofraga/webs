      const input = document.querySelector("#phone");
      window.intlTelInput(input, {
        initialCountry: "es", // España por defecto
        preferredCountries: ["es", "pt", "fr", "it", "de", "gb"], // países destacados
        utilsScript:
          "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.19/js/utils.js",
      });