const loadingTextElement = document.getElementById('loadingText');
let dotCount = 0;
const maxDots = 3; 

function animateDots() {
    let dots = '';
    for (let i = 0; i < dotCount; i++) {
        dots += '.';
    }
    loadingTextElement.textContent = 'В Разработке' + dots;

    dotCount = (dotCount + 1) % (maxDots + 1); 

    setTimeout(animateDots, 500); 
}

document.addEventListener('DOMContentLoaded', animateDots);