const progressBar = document.getElementById('progress-bar');

function updateProgressBar() {
    const docHeight = document.documentElement.scrollHeight;
    const viewportHeight = document.documentElement.clientHeight;
    const scrollTop = document.documentElement.scrollTop;

    const scrollableDistance = docHeight - viewportHeight;

    let scrollPercentage;
    if (scrollableDistance === 0) {
        scrollPercentage = 100;
    } else {
        scrollPercentage = (scrollTop / scrollableDistance) * 100;
    }

    progressBar.style.width = scrollPercentage + '%';
}

window.addEventListener('scroll', updateProgressBar);

updateProgressBar();