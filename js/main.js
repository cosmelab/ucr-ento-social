// Mobile Bottom Navigation - REMOVED
// Keeping only the hamburger menu

// Toggle reproducibility story
function toggleReproducibilityStory() {
    const story = document.querySelector('.reproducibility-story');
    const btn = document.querySelector('.reproducibility-btn');

    if (story.style.display === 'none' || story.style.display === '') {
        story.style.display = 'block';
        story.style.marginTop = '20px';
        btn.innerHTML = '<i class="fas fa-times"></i> Close';
    } else {
        story.style.display = 'none';
        btn.innerHTML = '<i class="fas fa-book-open"></i> Learn More';
    }
}

// Floating Mosquito Animation System - DISABLED FOR SOCIAL COMMITTEE SITE
// This was creating the floating blue balls

// CONSOLIDATED DOMContentLoaded - All initialization in one place
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Content Loaded - Initializing...');

    // ===== Gallery Slideshow =====
    const slides = document.querySelectorAll('.hero-gallery-slideshow .slide');
    const indicators = document.querySelectorAll('.gallery-indicators .indicator');

    if (slides.length > 0) {
        let currentSlide = 0;
        const slideInterval = 5000; // Change slide every 5 seconds

        function showSlide(index) {
            // Remove active class from all slides and indicators
            slides.forEach(slide => slide.classList.remove('active'));
            indicators.forEach(indicator => indicator.classList.remove('active'));

            // Add active class to current slide and indicator
            slides[index].classList.add('active');
            if (indicators[index]) {
                indicators[index].classList.add('active');
            }
        }

        function nextSlide() {
            currentSlide = (currentSlide + 1) % slides.length;
            showSlide(currentSlide);
        }

        // Auto-advance slides
        let autoSlideInterval = setInterval(nextSlide, slideInterval);

        // Click on indicators to jump to specific slide
        indicators.forEach((indicator, index) => {
            indicator.addEventListener('click', () => {
                currentSlide = index;
                showSlide(currentSlide);
                // Reset auto-advance timer
                clearInterval(autoSlideInterval);
                autoSlideInterval = setInterval(nextSlide, slideInterval);
            });
        });

        // Pause on hover (optional)
        const slideshow = document.querySelector('.hero-gallery-slideshow');
        if (slideshow) {
            slideshow.addEventListener('mouseenter', () => {
                clearInterval(autoSlideInterval);
            });

            slideshow.addEventListener('mouseleave', () => {
                autoSlideInterval = setInterval(nextSlide, slideInterval);
            });
        }
    }

    // ===== Mobile Navigation Toggle =====
    const navToggle = document.querySelector('.mobile-menu-toggle');
    const navMenu = document.querySelector('.nav-menu');

    console.log('Mobile menu elements found:', !!navToggle, !!navMenu);

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            navMenu.classList.toggle('active');
            navToggle.classList.toggle('active');
            console.log('Menu toggled:', navMenu.classList.contains('active'));
        });

        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
            }
        });

        // Close mobile menu when clicking on a link
        const navLinks = document.querySelectorAll('.nav-menu a');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
            });
        });
    } else {
        console.error('Mobile menu elements not found!');
    }

    // ===== Add active class to current page link =====
    const currentLocation = location.pathname;
    const menuItems = document.querySelectorAll('.nav-menu a');
    menuItems.forEach(item => {
        if(item.getAttribute('href') === currentLocation.split('/').pop() ||
           (currentLocation === '/' && item.getAttribute('href') === 'index.html')) {
            item.classList.add('active');
        }
    });

    // Also add active class to quick links
    const quickLinks = document.querySelectorAll('.quick-links-minimal a');
    quickLinks.forEach(link => {
        if(link.getAttribute('href') === currentLocation.split('/').pop() ||
           (currentLocation === '/' && link.getAttribute('href') === 'index.html') ||
           (currentLocation.endsWith('/') && link.getAttribute('href') === 'index.html')) {
            link.classList.add('active');
        }
    });

    // ===== Fade-in animations =====
    const fadeElements = document.querySelectorAll('.fade-in');
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-visible');

                // Stagger animations for child elements
                const children = entry.target.querySelectorAll('.fade-in-child');
                children.forEach((child, index) => {
                    setTimeout(() => {
                        child.classList.add('fade-in-visible');
                    }, index * 100);
                });
            }
        });
    }, observerOptions);

    fadeElements.forEach(el => observer.observe(el));

    // ===== Parallax effect for images =====
    const parallaxElements = document.querySelectorAll('.parallax-img');

    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;

        parallaxElements.forEach(el => {
            const rate = el.dataset.parallaxRate || 0.5;
            const yPos = -(scrolled * rate);
            el.style.transform = `translateY(${yPos}px)`;
        });
    });

    // ===== Publication Filter Functionality =====
    const filterButtons = document.querySelectorAll('.filter-btn');
    const publicationCards = document.querySelectorAll('.pub-card');

    if (filterButtons.length > 0) {
        filterButtons.forEach(button => {
            button.addEventListener('click', () => {
                // Update active button
                filterButtons.forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');

                const filter = button.getAttribute('data-filter');

                // Filter publications
                publicationCards.forEach(card => {
                    if (filter === 'all') {
                        card.style.display = 'block';
                        card.classList.add('fade-in-visible');
                    } else {
                        const categories = card.getAttribute('data-categories');
                        if (categories && categories.includes(filter)) {
                            card.style.display = 'block';
                            card.classList.add('fade-in-visible');
                        } else {
                            card.style.display = 'none';
                        }
                    }
                });
            });
        });
    }
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add scroll effect to navbar
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(68, 71, 90, 0.95)';
            navbar.style.backdropFilter = 'blur(10px)';
        } else {
            navbar.style.background = '';
            navbar.style.backdropFilter = '';
        }
    }
});
