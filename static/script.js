const buttons = document.querySelectorAll("[data-carousel-button]");
let autoSwitchInterval = 7000; 
let autoSwitchTimer;


function switchSlides(offset, slides) {
  const activeSlide = slides.querySelector("[data-active]");
  let newIndex = [...slides.children].indexOf(activeSlide) + offset;
  if (newIndex < 0) newIndex = slides.children.length - 1;
  if (newIndex >= slides.children.length) newIndex = 0;

  slides.children[newIndex].dataset.active = true;
  delete activeSlide.dataset.active;
}


function resetAutoSwitchTimer() {
  clearInterval(autoSwitchTimer);
  autoSwitchTimer = setInterval(autoSwitchSlides, autoSwitchInterval);
}


buttons.forEach(button => {
  button.addEventListener("click", () => {
    const offset = button.dataset.carouselButton === "next" ? 1 : -1;
    const slides = button.closest("[data-carousel]").querySelector("[data-slides]");
    
    switchSlides(offset, slides);
    resetAutoSwitchTimer();
  });
});


function autoSwitchSlides() {
  const carousels = document.querySelectorAll("[data-carousel]");
  carousels.forEach(carousel => {
    const slides = carousel.querySelector("[data-slides]");
    switchSlides(1, slides);
  });
}

autoSwitchTimer = setInterval(autoSwitchSlides, autoSwitchInterval);

document.addEventListener("click", (e) => {
  const isDropdownButton = e.target.matches("[data-dropdown-button]");
  if (!isDropdownButton && e.target.closest("[data-dropdown]") != null) return;

  let currentDropdown;
  if (isDropdownButton) {
    currentDropdown = e.target.closest("[data-dropdown]");
    currentDropdown.classList.toggle("active");
  }

  document.querySelectorAll("[data-dropdown].active").forEach((dropdown) => {
    if (dropdown === currentDropdown) return;
    dropdown.classList.remove("active");
  });
});
