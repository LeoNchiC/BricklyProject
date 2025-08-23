(function() { // Открывающая скобка IIFE
  const scrollZone = document.getElementById('scroll-zone-2');
  const scrollTrack = document.getElementById('scroll-track-2');

  let scrollLeft = 0;
  const autoScrollSpeed = 1;
  const scrollInterval = 20;

  let autoScrollDirection = 1;

  function autoScroll() {
    const maxScroll = scrollTrack.scrollWidth - scrollZone.clientWidth;

    if (maxScroll <= 0) {
      return;
    }

    scrollLeft += autoScrollDirection * autoScrollSpeed;

    if (scrollLeft >= maxScroll) {
      scrollLeft = maxScroll;
      autoScrollDirection = -1;
    } else if (scrollLeft <= 0) {
      scrollLeft = 0;
      autoScrollDirection = 1;
    }

    scrollTrack.style.transform = `translateX(-${scrollLeft}px)`;
  }

  setInterval(autoScroll, scrollInterval); 
})(); 

window.addEventListener('scroll', handler, { passive: true });