/* ==================== JavaScript Utilities ==================== */

// Alert auto-dismiss
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        // Auto dismiss after 5 seconds
        setTimeout(() => {
            if (alert.style.display !== 'none') {
                alert.style.display = 'none';
            }
        }, 5000);
    });
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// Add active class to current navigation link
document.addEventListener('DOMContentLoaded', function() {
    const currentLocation = location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentLocation) {
            link.style.color = 'var(--primary-color)';
        }
    });
});

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.addEventListener('submit', function(e) {
            const inputs = form.querySelectorAll('[required]');
            let isValid = true;
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.style.borderColor = 'var(--danger-color)';
                } else {
                    input.style.borderColor = 'var(--border-color)';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields');
            }
        });
    }
}

// File input handling
document.addEventListener('DOMContentLoaded', function() {
    const fileInputs = document.querySelectorAll('.file-input');
    
    fileInputs.forEach(fileInput => {
        const fileLabel = fileInput.parentElement.querySelector('.file-label');
        
        if (fileLabel) {
            // Handle drag and drop
            fileLabel.addEventListener('dragover', (e) => {
                e.preventDefault();
                fileLabel.style.background = 'var(--light-bg)';
            });
            
            fileLabel.addEventListener('dragleave', () => {
                fileLabel.style.background = 'white';
            });
            
            fileLabel.addEventListener('drop', (e) => {
                e.preventDefault();
                fileLabel.style.background = 'white';
                fileInput.files = e.dataTransfer.files;
                updateFileLabel(fileInput, fileLabel);
            });
            
            // Handle file selection
            fileInput.addEventListener('change', () => {
                updateFileLabel(fileInput, fileLabel);
            });
        }
    });
    
    function updateFileLabel(fileInput, fileLabel) {
        if (fileInput.files && fileInput.files.length > 0) {
            const fileName = fileInput.files[0].name;
            const fileText = fileLabel.querySelector('.file-text');
            if (fileText) {
                fileText.textContent = '✓ ' + fileName;
            }
        }
    }
});

// Smooth animations on scroll
function revealOnScroll() {
    const reveals = document.querySelectorAll('.project-card, .service-card, .value-card');
    
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'slideDown 0.6s ease forwards';
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });
    
    reveals.forEach(reveal => observer.observe(reveal));
}

document.addEventListener('DOMContentLoaded', revealOnScroll);

// Counter animation for stats
function animateCounters() {
    const statNumbers = document.querySelectorAll('.stat-number');
    
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = entry.target;
                const finalValue = target.textContent.replace(/[^0-9]/g, '');
                animateValue(target, 0, parseInt(finalValue), 2000);
                observer.unobserve(target);
            }
        });
    }, { threshold: 0.5 });
    
    statNumbers.forEach(stat => observer.observe(stat));
}

function animateValue(element, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const value = Math.floor(progress * (end - start) + start);
        element.textContent = value + '+';
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

document.addEventListener('DOMContentLoaded', animateCounters);

// Toggle mobile menu
function setupMobileMenu() {
    const navbar = document.querySelector('.navbar');
    const navMenu = document.querySelector('.navbar-menu');
    
    if (navbar && navMenu && window.innerWidth <= 768) {
        const menuToggle = document.createElement('button');
        menuToggle.className = 'menu-toggle';
        menuToggle.innerHTML = '☰';
        
        navbar.querySelector('.container').appendChild(menuToggle);
        
        menuToggle.addEventListener('click', () => {
            navMenu.style.display = navMenu.style.display === 'flex' ? 'none' : 'flex';
        });
    }
}

document.addEventListener('DOMContentLoaded', setupMobileMenu);

// Scroll to top button
function setupScrollToTop() {
    const scrollTopBtn = document.createElement('button');
    scrollTopBtn.innerHTML = '↑';
    scrollTopBtn.className = 'scroll-to-top';
    scrollTopBtn.style.cssText = `
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        padding: 0.75rem 1rem;
        background: var(--primary-color);
        color: white;
        border: none;
        border-radius: 50%;
        cursor: pointer;
        display: none;
        font-size: 1.2rem;
        z-index: 999;
        transition: all 0.3s ease;
    `;
    
    document.body.appendChild(scrollTopBtn);
    
    window.addEventListener('scroll', () => {
        scrollTopBtn.style.display = window.scrollY > 300 ? 'block' : 'none';
    });
    
    scrollTopBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

document.addEventListener('DOMContentLoaded', setupScrollToTop);

// Format date inputs
document.addEventListener('DOMContentLoaded', function() {
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        if (input.value) {
            input.style.borderColor = 'var(--success-color)';
        }
    });
});

// Email validation
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Phone validation
function validatePhone(phone) {
    const re = /^[\d\s\-\+\(\)]+$/;
    return re.test(phone);
}

// Export functions for form usage
window.validateForm = validateForm;
window.validateEmail = validateEmail;
window.validatePhone = validatePhone;
