const scrollZone2 = document.getElementById('scroll-zone');
const scrollTrack2 = document.getElementById('scroll-track');

let scrollLeft = 0;
const autoScrollSpeed = 1;
const scrollInterval = 20; 

let autoScrollDirection = 1; 

function autoScroll() {
  const maxScroll = scrollTrack2.scrollWidth - scrollZone2.clientWidth;

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

  scrollTrack2.style.transform = `translateX(-${scrollLeft}px)`;
}

window.autoScrollIntervalId = setInterval(autoScroll, scrollInterval);