async function startCountdown() {
    let targetDate;

    try {
        // Hacer petición a la API
        const response = await fetch('/fecha-final');
        const data = await response.json();
        targetDate = new Date(data.fechaFinal); // Ajusta según la estructura de tu API
    } catch (error) {
        console.error('Error al obtener la fecha:', error);
        // Fallback: usar fecha por defecto (ej. +1 mes)
        targetDate = new Date();
        targetDate.setMonth(targetDate.getMonth() + 1);
        targetDate.setHours(0, 0, 0, 0);
    }

    function updateCountdown() {
        const now = new Date();
        const diff = targetDate - now;

        if (diff <= 0) {
            document.getElementById("Day").textContent = "0";
            document.getElementById("Hour").textContent = "00";
            document.getElementById("Minute").textContent = "00";
            document.getElementById("Second").textContent = "00";
            return;
        }

        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((diff % (1000 * 60)) / 1000);

        document.getElementById("Day").textContent = days;
        document.getElementById("Hour").textContent = hours.toString().padStart(2, '0');
        document.getElementById("Minute").textContent = minutes.toString().padStart(2, '0');
        document.getElementById("Second").textContent = seconds.toString().padStart(2, '0');
    }

    updateCountdown();
    setInterval(updateCountdown, 1000);
}

window.onload = startCountdown;   