console.log('Hello')

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