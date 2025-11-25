// Auto-hide flash messages setelah 5 detik
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash');
    
    flashMessages.forEach(function(flash) {
        setTimeout(function() {
            flash.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(function() {
                flash.remove();
            }, 300);
        }, 5000);
    });
});

// Animasi slide out untuk flash messages
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

