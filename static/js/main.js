// Reusable function untuk handle image loading dengan instant show jika cached
function handleImageLoad(imgElement) {
    if (!imgElement) return;
    
    // Jika gambar sudah complete/cached, langsung show tanpa fade
    if (imgElement.complete && imgElement.naturalHeight !== 0) {
        imgElement.style.opacity = '1';
        imgElement.style.transition = 'none'; // No transition untuk cached images
        imgElement.classList.add('loaded');
        return;
    }
    
    // Cek cache dengan Image object
    const testImg = new Image();
    testImg.onload = testImg.onerror = function() {
        if (imgElement && testImg.complete) {
            // Gambar cached, langsung show
            imgElement.style.opacity = '1';
            imgElement.style.transition = 'none';
            imgElement.classList.add('loaded');
        }
    };
    testImg.src = imgElement.src;
    
    // Jika belum cached, wait for load dengan fade
    imgElement.addEventListener('load', function() {
        this.style.opacity = '1';
        this.classList.add('loaded');
    }, { once: true });
}

// Handle semua gambar dengan class 'fade-in-on-load' atau 'logo-img'
(function() {
    function initImages() {
        // Handle logo
        const logoImg = document.querySelector('.logo-img');
        if (logoImg) {
            handleImageLoad(logoImg);
        }
        
        // Handle semua gambar dengan class 'fade-in-on-load'
        const fadeImages = document.querySelectorAll('.fade-in-on-load');
        fadeImages.forEach(function(img) {
            handleImageLoad(img);
        });
    }
    
    // Cek segera jika DOM sudah ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initImages);
    } else {
        initImages();
    }
    
    // Cek lagi setelah DOM ready (fallback)
    document.addEventListener('DOMContentLoaded', initImages);
})();

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

