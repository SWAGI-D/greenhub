// script.js

// Auto-dismiss alerts after 5 seconds
setTimeout(() => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        alert.style.transition = 'opacity 0.5s ease';
        alert.style.opacity = 0;
        setTimeout(() => alert.remove(), 500);
    });
}, 5000);

// Like button toggle (if not using AJAX)
document.addEventListener('DOMContentLoaded', () => {
    const likeButtons = document.querySelectorAll('.like-btn');
    likeButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            btn.classList.toggle('liked');
        });
    });

    // Toggle comment form
    const toggleCommentBtns = document.querySelectorAll('.toggle-comment-form');
    toggleCommentBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const form = btn.nextElementSibling;
            form.classList.toggle('d-none');
        });
    });
});
