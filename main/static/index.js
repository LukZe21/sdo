console.log('Started')
searchBtn = document.getElementById('search_input')


function slide(direction, containerId) {
    const sliderItemWidth = document.querySelector('.slider-item').offsetWidth + 20; // Including margin
    const sliderContainer = document.getElementById(containerId);
    const slider = sliderContainer.querySelector('.slider'); // Assuming the slider has this class

    if (direction === 'prev') {
        slider.scrollLeft -= sliderItemWidth;
    } else if (direction === 'next') {
        slider.scrollLeft += sliderItemWidth;
    }
}


const carousel = document.querySelector('.carousels');
const pointsContainer = document.querySelector('.points');
const images = document.querySelectorAll('.carousel-img');
const numImages = images.length;
let currentImageIndex = 0;

for (let i = 0; i < numImages; i++) {
  const point = document.createElement('div');
  point.classList.add('point');
  pointsContainer.appendChild(point);
  point.addEventListener('click', () => {
    goToImage(i);
  });
}
function highlightPoint(index) {
  const points = document.querySelectorAll('.point');
  points.forEach((point, i) => {
    if (i === index) {
      point.classList.add('active');
    } else {
      point.classList.remove('active');
    }
  });
}
function goToImage(index) {
  if (index >= 0 && index < numImages) {
    carousel.style.transform = `translateX(-${index * 100}%)`;
    currentImageIndex = index;
    highlightPoint(index);
  }
}
function nextImage() {
  currentImageIndex = (currentImageIndex + 1) % numImages;
  goToImage(currentImageIndex);
}
setInterval(nextImage, 5000);
highlightPoint(0);



document.addEventListener("DOMContentLoaded", function () {
  const nextButton = document.getElementById("nextButton");
  const prevButton = document.getElementById("prevButton");
  const cardsContainer = document.querySelector(".cards");
  const cards = document.querySelectorAll(".card");
  const cardWidth = cards[0].offsetWidth + 0;
  const visibleCardCount = 4;
  const autoMoveInterval = 5000;
  let isTransitioning = false; 
  let currentIndex = 0;
  let autoMoveTimer;
  function moveForward() {
    if (!isTransitioning) {
      isTransitioning = true;
      currentIndex++;
      if (currentIndex >= cards.length) {
        currentIndex = 0;
      }
      const offset = -currentIndex * cardWidth;
      cardsContainer.style.transition = "transform 0.5s ease";
      cardsContainer.style.transform = `translateX(${offset}px)`;
      setTimeout(() => {
        isTransitioning = false;
      }, 500);
    }
  }
  function moveBackward() {
    if (!isTransitioning) {
      isTransitioning = true;
      currentIndex--;
      if (currentIndex < 0) {
        currentIndex = cards.length - 1;
      }
      const offset = -currentIndex * cardWidth;
      cardsContainer.style.transition = "transform 0.5s ease";
      cardsContainer.style.transform = `translateX(${offset}px)`;
      setTimeout(() => {
        isTransitioning = false;
      }, 500);
    }
  }
  function startAutoMove() {
    autoMoveTimer = setInterval(moveForward, autoMoveInterval);
  }
  function stopAutoMove() {
    clearInterval(autoMoveTimer);
  }
  startAutoMove();
  cardsContainer.addEventListener("mouseover", stopAutoMove);
  cardsContainer.addEventListener("mouseout", startAutoMove);
  nextButton.addEventListener("click", moveForward);
  prevButton.addEventListener("click", moveBackward);
});