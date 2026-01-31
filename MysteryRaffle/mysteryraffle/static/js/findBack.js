function startCountdown() {
    const now = new Date();
    
    // Sumar 1 mes a la fecha actual
    let targetDate = new Date(now);
    targetDate.setMonth(targetDate.getMonth() + 1);
    targetDate.setHours(0, 0, 0, 0); // Resetear a medianoche

    function updateCountdown() {
        const now = new Date();
        const diff = targetDate - now;

        // Calcular días, horas, minutos y segundos restantes
        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((diff % (1000 * 60)) / 1000);

        // Actualizar el DOM
        document.getElementById("Day").textContent = days;
        document.getElementById("Hour").textContent = hours.toString().padStart(2, '0');
        document.getElementById("Minute").textContent = minutes.toString().padStart(2, '0');
        document.getElementById("Second").textContent = seconds.toString().padStart(2, '0');
    }

    // Actualizar inmediatamente y luego cada segundo
    updateCountdown();
    setInterval(updateCountdown, 1000);
}

// Iniciar la cuenta regresiva cuando la página cargue
window.onload = startCountdown;