// Navigation & Animations
document.addEventListener('DOMContentLoaded', function() {
    console.log('Main JS loaded');
    
    // Add smooth scrolling
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
    
    // Add animation on page load
    const navbar = document.getElementById('navbar');
    if (navbar) {
        navbar.style.animation = 'slideDown 0.5s ease-out';
    }
});

// Slide down animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideDown {
        from {
            transform: translateY(-100%);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);
