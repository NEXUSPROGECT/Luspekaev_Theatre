document.getElementById("menu-button").onclick = function() {
        const mobileMenu = document.getElementById("mobile-menu");
        // Тогглинг видимости меню
        if (mobileMenu.classList.contains("hidden")) {
            mobileMenu.classList.remove("hidden");
            mobileMenu.style.maxHeight = mobileMenu.scrollHeight + "px";
        } else {
            mobileMenu.style.maxHeight = "0";
            setTimeout(() => {
                mobileMenu.classList.add("hidden");
            }, 300); // Убедитесь, что время совпадает с transition duration
        }
};


const profileButton = document.getElementById('profile-button');
        const profileMenu = document.getElementById('profile-menu');
        const closeProfile = document.getElementById('close-profile');

        profileButton.addEventListener('click', () => {
            profileMenu.classList.remove('translate-x-full');
        });

        closeProfile.addEventListener('click', () => {
            profileMenu.classList.add('translate-x-full');
        });

        // Закрытие меню при клике вне его
        window.addEventListener('click', (e) => {
            if (!profileMenu.contains(e.target) && e.target !== profileButton) {
                profileMenu.classList.add('translate-x-full');
            }
        });