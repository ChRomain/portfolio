document.addEventListener('DOMContentLoaded', () => {
    // --- Parallax & Fading Effect ---
    const carouselContainer = document.getElementById('hero-carousel');
    const heroContent = document.getElementById('hero-content');
    const heroIndicators = document.getElementById('hero-indicators');
    const heroScrollBtn = document.getElementById('hero-scroll-btn');

    window.addEventListener('scroll', () => {
        const scrollY = window.scrollY;
        if (scrollY < 0) return;

        if (carouselContainer) {
            carouselContainer.style.transform = `translate3d(0, ${scrollY * 0.4}px, 0)`;
        }
        
        const opacity = Math.max(0, 1 - scrollY / 350);
        
        if (heroContent) {
            heroContent.style.opacity = opacity;
            heroContent.style.transform = `translate3d(0, ${scrollY * -0.2}px, 0)`;
        }
        if (heroIndicators) {
            heroIndicators.style.opacity = opacity;
            /* Keep the base transform and append the parallax movement */
            heroIndicators.style.transform = `translateX(-50%) translate3d(0, ${scrollY * -0.2}px, 0)`;
        }
        if (heroScrollBtn) {
            heroScrollBtn.style.opacity = opacity;
            heroScrollBtn.style.transform = `translateX(-50%) translate3d(0, ${scrollY * -0.2}px, 0)`;
        }
    }, { passive: true });

    // --- Carousel Logic ---
    const slides = document.querySelectorAll('.carousel-slide');
    const progressBar = document.getElementById('hero-progress-bar');
    const counter = document.getElementById('hero-counter');
    const btnPrev = document.getElementById('hero-prev');
    const btnNext = document.getElementById('hero-next');

    let currentSlide = 0;
    const slideCount = slides.length;
    const intervalTime = 8000;
    let slideTimer;
    let progressInterval;

    const updateCounter = () => {
        if (counter) counter.textContent = `${currentSlide + 1} / ${slideCount}`;
    };

    const startProgress = () => {
        if (!progressBar) return;
        // Reset
        progressBar.style.transition = 'none';
        progressBar.style.width = '0%';
        void progressBar.offsetWidth; // force reflow
        progressBar.style.transition = `width ${intervalTime}ms linear`;
        progressBar.style.width = '100%';
    };

    const showSlide = (n) => {
        if (slideCount === 0) return;
        slides[currentSlide].classList.remove('active', 'opacity-100');
        slides[currentSlide].classList.add('opacity-0');

        currentSlide = (n + slideCount) % slideCount;

        slides[currentSlide].classList.add('active', 'opacity-100');
        slides[currentSlide].classList.remove('opacity-0');

        updateCounter();
        startProgress();

        clearInterval(slideTimer);
        slideTimer = setInterval(() => showSlide(currentSlide + 1), intervalTime);
    };

    if (btnPrev) btnPrev.addEventListener('click', () => showSlide(currentSlide - 1));
    if (btnNext) btnNext.addEventListener('click', () => showSlide(currentSlide + 1));

    if (slideCount > 0) {
        updateCounter();
        startProgress();
        slideTimer = setInterval(() => showSlide(currentSlide + 1), intervalTime);
    }

    // --- Reveal Animations (3D Scroll) ---
    const observerOptions = {
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px"
    };
    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const cards = document.querySelectorAll('.gallery-card');
    cards.forEach((card) => {
        revealObserver.observe(card);

        // Dynamically create glare element
        let glare = card.querySelector('.card-glare');
        if (!glare) {
            glare = document.createElement('div');
            glare.className = 'card-glare';
            card.appendChild(glare);
        }

        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = ((y - centerY) / centerY) * -15; // Sensation de profondeur plus marquée
            const rotateY = ((x - centerX) / centerX) * 15;
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.05, 1.05, 1.05)`;
            
            const percentageX = (x / rect.width) * 100;
            const percentageY = (y / rect.height) * 100;
            glare.style.background = `radial-gradient(circle at ${percentageX}% ${percentageY}%, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0) 80%)`;
            glare.style.opacity = '1';
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)`;
            glare.style.opacity = '0';
        });
    });

    // --- Homepage Mini-Map Logic ---
    const initMiniMap = () => {
        if (typeof L === 'undefined' || typeof L.markerClusterGroup === 'undefined') {
            setTimeout(initMiniMap, 200);
            return;
        }

        const miniMapEl = document.getElementById('mini-map');
        if (!miniMapEl) return;

        const isMobile = window.innerWidth < 768;
        const locations = JSON.parse(miniMapEl.getAttribute('data-locations') || '[]');
        const map = L.map('mini-map', {
            center: isMobile ? [20, 0] : [20, -20],
            zoom: isMobile ? 1.2 : 2.5,
            minZoom: 1,
            scrollWheelZoom: false,
            zoomControl: false,
            attributionControl: false
        });

        // Exact same tiles as main map
        L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png', {
            opacity: 0.5
        }).addTo(map);

        // World Borders (GeoJSON) - Same as main map
        const geoJsonLayer = L.geoJSON(null, {
            style: {
                fillColor: "#353535",
                weight: 0.8,
                color: "#555",
                fillOpacity: 1
            }
        }).addTo(map);

        fetch('/geojson/countries.geojson')
            .then(r => r.json())
            .then(data => {
                geoJsonLayer.addData(data);
                geoJsonLayer.bringToBack();
            });

        const clusterGroup = L.markerClusterGroup({
            showCoverageOnHover: false,
            maxClusterRadius: 45,
            iconCreateFunction: (cluster) => L.divIcon({
                html: `<div class="mini-map-cluster"><span>${cluster.getChildCount()}</span></div>`,
                className: '',
                iconSize: [30, 30]
            })
        });

        locations.forEach(loc => {
            const marker = L.marker(loc.coords, {
                icon: L.divIcon({
                    html: `<div class="home-photo-marker" style="background-image: url('${loc.url}feature.webp');"></div>`,
                    className: '',
                    iconSize: [32, 32]
                })
            });

            const tooltipContent = `
                <div class="mini-map-tooltip">
                    <img src="${loc.url}feature.webp" style="width: 100%; height: 60px; object-fit: cover; border-radius: 4px;">
                    <span style="color: #ffffff !important; font-weight: 900 !important; font-size: 0.85rem !important;">${loc.name}</span>
                </div>
            `;

            marker.bindTooltip(tooltipContent, {
                direction: 'top',
                offset: [0, -10],
                className: 'mini-map-tooltip-container'
            });

            marker.on('click', () => { window.location.href = loc.url; });
            clusterGroup.addLayer(marker);
        });

        map.addLayer(clusterGroup);
        
        // Fly to initial view
        setTimeout(() => {
            const isMobile = window.innerWidth < 768;
            map.flyTo(isMobile ? [20, 0] : [30, -30], isMobile ? 1.5 : 3, { duration: 3, easeLinearity: 0.1 });
        }, 500);
    };

    if (document.getElementById('mini-map')) {
        initMiniMap();
    }

    // --- Travel Dashboard CountUp Logic ---
    const animateCountUp = (el) => {
        const target = parseInt(el.getAttribute('data-target'));
        const duration = 2000; // 2 seconds
        const start = 0;
        const startTime = performance.now();

        const update = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function: easeOutExpo
            const easeOutExpo = (t) => t === 1 ? 1 : 1 - Math.pow(2, -10 * t);
            const currentCount = Math.floor(easeOutExpo(progress) * (target - start) + start);
            
            el.innerText = currentCount;

            if (progress < 1) {
                requestAnimationFrame(update);
            } else {
                el.innerText = target;
            }
        };

        requestAnimationFrame(update);
    };

    const dashboardObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.querySelectorAll('.count-up').forEach(c => animateCountUp(c));
                dashboardObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    const dashboard = document.getElementById('travel-dashboard');
    if (dashboard) dashboardObserver.observe(dashboard);
});
