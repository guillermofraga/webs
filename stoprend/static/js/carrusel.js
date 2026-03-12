  let currentSlide = 0;
  const slides = document.querySelectorAll('#carousel > div');
  const totalSlides = slides.length;

  function updateCarousel() {
    document.getElementById('carousel').style.transform = `translateX(-${currentSlide * 100}%)`;
    document.querySelectorAll('.opacity-50').forEach((dot, index) => {
      dot.style.opacity = index === currentSlide ? '1' : '0.5';
    });
  }

  function moveSlide(direction) {
    currentSlide = (currentSlide + direction + totalSlides) % totalSlides;
    updateCarousel();
  }

  function goToSlide(index) {
    currentSlide = index;
    updateCarousel();
  }