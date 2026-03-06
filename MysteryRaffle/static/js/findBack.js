async function startCountdown() {
    let targetDate = new Date("2026-03-06T23:59:59Z");
    let intervalId;

    function updateCountdown() {
        const now = new Date();
        const diff = targetDate - now;

        if (diff <= 0) {
            clearInterval(intervalId);

            // Eliminar el botón de acceso anticipado
            const button = document.getElementById("OpenModal");
            if (button) {
                button.style.backgroundColor = "#ccc";
                button.style.color = "#666";
                button.style.textDecoration = "line-through";
                button.style.cursor = "not-allowed";
                button.style.pointerEvents = "none";
                button.id = "acceso-anticipado-inactivo";
            }   

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
    intervalId = setInterval(updateCountdown, 1000);
}

window.onload = startCountdown;   