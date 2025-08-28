const burgerCheckbox = document.getElementById('burger-checkbox');
const blackBack = document.querySelector('.black-back');

burgerCheckbox.addEventListener('change', function() {
    if (this.checked) {
        // Показываем затемнение
        blackBack.style.opacity = '0';
        blackBack.style.visibility = 'visible';
        requestAnimationFrame(() => {
            blackBack.style.transition = 'opacity 0.3s ease';
            blackBack.style.opacity = '0.5';
        });
        
        // Блокируем скролл
        document.body.style.overflow = 'hidden';
        document.documentElement.style.overflow = 'hidden';
        
    } else {
        // Скрываем затемнение
        blackBack.style.transition = 'opacity 0.3s ease, visibility 0.3s ease';
        blackBack.style.opacity = '0';
        setTimeout(() => {
            blackBack.style.visibility = 'hidden';
        }, 300);
        
        // Разблокируем скролл
        document.body.style.overflow = '';
        document.documentElement.style.overflow = '';
    }
});