        const slider = document.getElementById("slider");
        const prev = document.getElementById("prev-slide");
        const next = document.getElementById("next-slide");

        let currentIndex = 0;

        // Обработчик для кнопки "вперёд"
        next.addEventListener("click", () => {
            const slideWidth = slider.firstElementChild.clientWidth;
            currentIndex++;
            if (currentIndex >= slider.children.length) currentIndex = 0; // Циклический переход
            slider.style.transform = `translateX(-${currentIndex * slideWidth}px)`;
        });

        // Обработчик для кнопки "назад"
        prev.addEventListener("click", () => {
            const slideWidth = slider.firstElementChild.clientWidth;
            currentIndex--;
            if (currentIndex < 0) currentIndex = slider.children.length - 1; // Циклический переход
            slider.style.transform = `translateX(-${currentIndex * slideWidth}px)`;
        });





        const sliderEvents = document.getElementById("sliderEvents");
        const prevEvents = document.getElementById("prev");
        const nextEvents = document.getElementById("next");

        let currentIndexEvents = 0;

        prevEvents.onclick = () => {
            currentIndexEvents = (currentIndexEvents === 0) ? sliderEvents.children.length - 1 : currentIndexEvents - 1;
            updateSliderPosition();
        };

        nextEvents.onclick = () => {
            currentIndexEvents = (currentIndexEvents === sliderEvents.children.length - 1) ? 0 : currentIndexEvents + 1;
            updateSliderPosition();
        };

        function updateSliderPosition() {
            const width = sliderEvents.clientWidth;
            sliderEvents.style.transform = `translateX(-${currentIndexEvents * width}px)`;
        }