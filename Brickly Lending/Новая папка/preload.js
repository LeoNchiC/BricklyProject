document.addEventListener('DOMContentLoaded', function () {
  const preloader = document.getElementById('preloader');
  const content = document.getElementById('content');

  // Задержка: минимум 2 секунды перед показом контента
  setTimeout(() => {
    preloader.style.opacity = 0;
    setTimeout(() => {
      preloader.style.display = 'none';
      content.style.display = 'block';
    }, 500); // время на плавное скрытие
  }, 2000); // <- здесь задаёшь нужную продолжительность в мс
});
