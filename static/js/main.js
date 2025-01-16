
const scrollBtn = document.getElementById('scroll-up');

scrollBtn.addEventListener('click', function(e) {
    let ripple = document.createElement('span');
    ripple.classList.add('ripple');
    this.appendChild(ripple);

    let x = e.clientX - e.target.offsetLeft;
    let y = e.clientY - e.target.offsetTop;

    ripple.style.left = `${x}px`;
    ripple.style.top = `${y}px`;

    setTimeout(() => {
        ripple.remove();
    }, 600);

// Smooth scroll to top
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

// Show/hide button based on scroll position
window.addEventListener('scroll', function() {
    if (window.scrollY > 200) {
        scrollBtn.classList.add('visible');
    } else {
        scrollBtn.classList.remove('visible');
    }
});