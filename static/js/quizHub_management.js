// Check if device is mobile
const isMobile = () => window.innerWidth <= 768;

const continue_quiz_btn = document.getElementById('continue-quiz-title-btn');

continue_quiz_btn.addEventListener('click', (e) => {

});




// Toggle quiz content
function toggleQuiz(element) {
    toggleDesktopView(element);
}

// Toggle desktop view
function toggleDesktopView(element) {
    const content = element.closest('.quiz-card').querySelector('.quiz-content');
    const allContents = document.querySelectorAll('.quiz-content');

    // Close all other quiz contents
    allContents.forEach(item => {
        if (item !== content) {
            item.classList.remove('active');
        }
    });

    // Toggle the clicked content
    content.classList.toggle('active');
}



// Handle window resize
window.addEventListener('resize', () => {
    const activeContents = document.querySelectorAll('.quiz-content.active');

    if (!isMobile()) {
        activeContents.forEach(content => {
            content.style.position = 'relative';
            document.body.style.overflow = 'auto';
            const closeButton = content.querySelector('.mobile-close');
            if (closeButton) {
                closeButton.style.display = 'none';
            }
        });
    }
});

// Add search functionality
document.querySelector('.search-input').addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    const quizCards = document.querySelectorAll('.quiz-card');

    quizCards.forEach(card => {
        const title = card.querySelector('.quiz-title').textContent.toLowerCase();
        const status = card.querySelector('.status-badge').textContent.toLowerCase();
        const stats = card.querySelector('.quiz-stats').textContent.toLowerCase();

        if (title.includes(searchTerm) || status.includes(searchTerm) || stats.includes(searchTerm)) {
            card.style.display = '';
        } else {
            card.style.display = 'none';
        }
    });
});