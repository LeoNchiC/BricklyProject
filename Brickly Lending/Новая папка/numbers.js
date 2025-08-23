document.addEventListener('DOMContentLoaded', () => {
    const animatedNumbers = document.querySelectorAll('.animated-number');

    const animateNumber = (element) => {
        const targetValue = parseInt(element.dataset.value);
        const suffix = element.dataset.suffix || ''; // Получаем суффикс, если есть
        const duration = 2000; // Длительность анимации в мс
        const startValue = 0;
        let startTime = null;

        const step = (currentTime) => {
            if (!startTime) startTime = currentTime;
            const progress = Math.min((currentTime - startTime) / duration, 1);
            const currentValue = Math.floor(progress * (targetValue - startValue) + startValue);

            element.textContent = currentValue + suffix;

            if (progress < 1) {
                requestAnimationFrame(step);
            } else {
                element.textContent = targetValue + suffix; // Убедиться, что конечное значение точно установлено
            }
        };

        requestAnimationFrame(step);
    };

    // Проверяем, когда элемент появляется в видимой области
    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateNumber(entry.target);
                observer.unobserve(entry.target); // Остановить наблюдение после анимации
            }
        });
    }, {
        threshold: 0.5 // Анимировать, когда 50% элемента видно
    });

    animatedNumbers.forEach(number => {
        observer.observe(number);
    });
});