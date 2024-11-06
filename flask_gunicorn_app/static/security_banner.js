document.addEventListener('DOMContentLoaded', () => {
    let currentSlide = 0;
    const slides = document.querySelectorAll('.image-container'); // Select the image containers
    const totalSlides = slides.length;

    if (totalSlides === 0) {
        console.error("No slides found. Please check your HTML structure and selectors.");
        return;
    }

    const nextButton = document.getElementById('nextSlide');
    const prevButton = document.getElementById('prevSlide');

    if (nextButton && prevButton) {
        nextButton.addEventListener('click', showNextSlide);
        prevButton.addEventListener('click', showPrevSlide);
    } else {
        console.error("Next or Previous slide buttons not found.");
    }

    function showNextSlide() {
        slides[currentSlide].classList.remove('active');
        currentSlide = (currentSlide + 1) % totalSlides;
        slides[currentSlide].classList.add('active');
    }

    function showPrevSlide() {
        slides[currentSlide].classList.remove('active');
        currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
        slides[currentSlide].classList.add('active');
    }

    // Automatically change slides every 3 seconds
    setInterval(showNextSlide, 3000); // 3000ms = 3 seconds

    // Set the initial active slide
    slides[currentSlide].classList.add('active');
});

