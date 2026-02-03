async function startCountdown() {
    let targetDate;

        targetDate = new Date("2026-03-06T23:59:59Z");
        //targetDate.setMonth(targetDate.getMonth() + 1); // Example: set to one month from now
        //targetDate.setHours(0, 0, 0, 0);
    

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