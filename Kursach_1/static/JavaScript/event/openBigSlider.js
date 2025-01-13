document.addEventListener('DOMContentLoaded', () => {
    const lightbox = document.getElementById('lightbox');
    const lightboxSlider = document.getElementById('lightbox-slider');
    const closeLightbox = document.getElementById('close-lightbox');
    const prevSlide = document.getElementById('prev-slide-lightbox');
    const nextSlide = document.getElementById('next-slide-lightbox');
    const images = document.querySelectorAll('.slider-image'); // Получаем все изображения с классом slider-image

    let currentIndex = 0;

    // Открытие слайдера при клике на изображение
    images.forEach((img, index) => {
        img.addEventListener("click", () => {
            currentIndex = index;
            openLightbox();
        });
    });

    // Открыть слайдер
    function openLightbox() {
        updateSlider(); // Обновить слайдер с текущим изображением
        lightbox.classList.remove("hidden"); // Показать слайдер
    }

    // Закрытие модального окна
    closeLightbox.addEventListener('click', () => {
        lightbox.classList.add('hidden');
    });

    // Обновление слайдера
    function updateSlider() {
        const slides = lightboxSlider.children;
        // Скрытие всех слайдов
        for (let i = 0; i < slides.length; i++) {
            slides[i].classList.add('hidden');
        }
        // Показ текущего слайда
        if (slides[currentIndex]) {
            slides[currentIndex].classList.remove('hidden');
        }
    }

    // Переключение на предыдущий слайд
    prevSlide.addEventListener('click', () => {
        if (lightboxSlider.children.length > 0) {
            currentIndex = (currentIndex - 1 + lightboxSlider.children.length) % lightboxSlider.children.length;
            updateSlider();
        }
    });

    // Переключение на следующий слайд
    nextSlide.addEventListener('click', () => {
        if (lightboxSlider.children.length > 0) {
            currentIndex = (currentIndex + 1) % lightboxSlider.children.length;
            updateSlider();
        }
    });
});