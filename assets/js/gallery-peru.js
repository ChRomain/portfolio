// Translations database
const TRANSLATIONS = {
  "fr": {
    "all": "Tout",
    "itinerary_title": "Itinéraire du Voyage au Pérou",
    "play_title": "Lancer le voyage",
    "pause_title": "Pause",
    "intro_hud": "Pérou",
    "hud_sub": "Itinéraire Déroulé",
    "no_photos": "Aucune photo pour cette destination pour le moment.",
    "dest_names": {
      "lima": "Lima",
      "paracas": "Paracas",
      "huacachina": "Oasis de Huacachina",
      "nazca": "Lignes de Nazca",
      "arequipa": "Arequipa",
      "colca_canyon": "Canyon de Colca",
      "sacred_valley": "Vallée Sacrée",
      "salineras_de_maras": "Salines de Maras",
      "rainbow_mountain": "Rainbow Mountain",
      "aguas_calientes": "Aguas Calientes",
      "machu_picchu": "Machu Picchu"
    },
    "dest_dates": {
      "lima": "20-21 Juin & 4-5 Juillet 2026",
      "paracas": "22 Juin 2026",
      "huacachina": "23 Juin 2026",
      "nazca": "24 Juin 2026",
      "arequipa": "25-26 Juin 2026 (Salinas Blancas)",
      "colca_canyon": "27 Juin 2026",
      "sacred_valley": "29 Juin 2026 (Vallée)",
      "salineras_de_maras": "29 Juin 2026 (Salines)",
      "rainbow_mountain": "30 Juin 2026",
      "aguas_calientes": "2 Juillet 2026",
      "machu_picchu": "3 Juillet 2026"
    }
  },
  "en": {
    "all": "All",
    "itinerary_title": "Peru Travel Itinerary",
    "play_title": "Play Journey",
    "pause_title": "Pause",
    "intro_hud": "Peru",
    "hud_sub": "Travel Timeline",
    "no_photos": "No photos for this destination yet.",
    "dest_names": {
      "lima": "Lima",
      "paracas": "Paracas",
      "huacachina": "Huacachina Oasis",
      "nazca": "Nazca Lines",
      "arequipa": "Arequipa",
      "colca_canyon": "Colca Canyon",
      "sacred_valley": "Sacred Valley",
      "salineras_de_maras": "Maras Salt Mines",
      "rainbow_mountain": "Rainbow Mountain",
      "aguas_calientes": "Aguas Calientes",
      "machu_picchu": "Machu Picchu"
    },
    "dest_dates": {
      "lima": "June 20-21 & July 4-5, 2026",
      "paracas": "June 22, 2026",
      "huacachina": "June 23, 2026",
      "nazca": "June 24, 2026",
      "arequipa": "June 25-26, 2026 (Salinas Blancas)",
      "colca_canyon": "June 27, 2026",
      "sacred_valley": "June 29, 2026 (Valley)",
      "salineras_de_maras": "June 29, 2026 (Maras)",
      "rainbow_mountain": "June 30, 2026",
      "aguas_calientes": "July 2, 2026",
      "machu_picchu": "July 3, 2026"
    }
  },
  "es": {
    "all": "Todos",
    "itinerary_title": "Itinerario del Viaje por Perú",
    "play_title": "Iniciar el viaje",
    "pause_title": "Pausa",
    "intro_hud": "Perú",
    "hud_sub": "Ruta de Viaje",
    "no_photos": "No hay fotos para este destino todavía.",
    "dest_names": {
      "lima": "Lima",
      "paracas": "Paracas",
      "huacachina": "Oasis de Huacachina",
      "nazca": "Líneas de Nazca",
      "arequipa": "Arequipa",
      "colca_canyon": "Cañón del Colca",
      "sacred_valley": "Valle Sagrado",
      "salineras_de_maras": "Salineras de Maras",
      "rainbow_mountain": "Montaña de Colores",
      "aguas_calientes": "Aguas Calientes",
      "machu_picchu": "Machu Picchu"
    },
    "dest_dates": {
      "lima": "20-21 de Junio & 4-5 de Julio de 2026",
      "paracas": "22 de Junio de 2026",
      "huacachina": "23 de Junio de 2026",
      "nazca": "24 de Junio de 2026",
      "arequipa": "25-26 de Junio de 2026 (Salinas Blancas)",
      "colca_canyon": "27 de Junio de 2026",
      "sacred_valley": "29 de Junio de 2026",
      "salineras_de_maras": "29 de Junio de 2026",
      "rainbow_mountain": "30 de Junio de 2026",
      "aguas_calientes": "2 de Julio de 2026",
      "machu_picchu": "3 de Julio de 2026"
    }
  }
};

document.addEventListener('DOMContentLoaded', () => {
  // 1. Detect language
  let lang = document.documentElement.lang || 'en';
  if (!TRANSLATIONS[lang]) lang = 'en';

  const t = TRANSLATIONS[lang];

  // Update static translated elements
  document.querySelectorAll('[data-key]').forEach(el => {
    const key = el.getAttribute('data-key');
    if (t[key]) el.textContent = t[key];
  });

  // Update destination button names
  document.querySelectorAll('.dest-btn-name').forEach(el => {
    const destId = el.getAttribute('data-dest-id');
    if (t.dest_names[destId]) el.textContent = t.dest_names[destId];
  });

  // Initialize HUD text
  document.getElementById('peru-current-dest-name').textContent = t.intro_hud;

  // 2. Setup gallery card interaction
  const filterButtons = document.querySelectorAll('.filter-btn');

  function getActiveFilter() {
    const activeBtn = document.querySelector('.filter-btn.active-filter');
    return activeBtn ? activeBtn.getAttribute('data-filter') : 'all';
  }

  function scrollToGrid() {
    const filterContainer = document.querySelector('.peru-filters');
    filterContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  // Filter gallery items (Corrected direct and wrapped child filtering)
  function filterGallery(destId) {
    // Toggle active button class using active-filter CSS style
    filterButtons.forEach(btn => {
      const isActive = btn.getAttribute('data-filter') === destId;
      btn.classList.toggle('active-filter', isActive);
      btn.setAttribute('aria-pressed', isActive ? 'true' : 'false');
    });

    let count = 0;
    const imgs = document.querySelectorAll('.portfolio-grid-final img');
    
    imgs.forEach(img => {
      const cardDest = img.getAttribute('data-destination');
      if (!cardDest) return; // Ignores non-peru images if present
      
      // Get the container element (direct child of .portfolio-grid-final)
      const gridItem = img.closest('.portfolio-grid-final > *') || img;
      
      if (destId === 'all' || cardDest === destId) {
        gridItem.classList.remove('peru-filter-hidden');
        gridItem.style.removeProperty('display');
        count++;
      } else {
        gridItem.classList.add('peru-filter-hidden');
      }
    });

    // Also filter video items
    document.querySelectorAll('.peru-video-item').forEach(item => {
      const dest = item.getAttribute('data-destination');
      if (destId === 'all' || dest === destId) {
        item.classList.remove('peru-filter-hidden');
        count++;
      } else {
        item.classList.add('peru-filter-hidden');
      }
    });

    // Handle empty state (Machu Picchu has no photos yet)
    let emptyStateEl = document.getElementById('peru-empty-state');
    if (count === 0) {
      if (!emptyStateEl) {
        emptyStateEl = document.createElement('div');
        emptyStateEl.id = 'peru-empty-state';
        emptyStateEl.className = 'w-full text-center py-24 text-neutral-500 dark:text-neutral-400 flex flex-col items-center justify-center';
        emptyStateEl.innerHTML = `
          <svg class="h-16 w-16 text-neutral-400 dark:text-neutral-600 mb-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 001.5-1.5V6a1.5 1.5 0 00-1.5-1.5H3.75A1.5 1.5 0 002.25 6v12a1.5 1.5 0 001.5 1.5zm10.5-11.25h.008v.008h-.008V8.25zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z"></path></svg>
          <p class="text-xl font-medium mb-1">${t.no_photos}</p>
        `;
        document.querySelector('.portfolio-grid-final').appendChild(emptyStateEl);
      } else {
        emptyStateEl.style.display = 'flex';
      }
    } else {
      if (emptyStateEl) emptyStateEl.style.display = 'none';
    }

    // Keep map marker states aligned
    updateActiveMapMarker(destId);
    
    // Update timeline bubble states
    updateActiveTimelineBubble(destId);
  }

  // Add filter buttons click events
  filterButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      stopAutopilot();
      const filterValue = btn.getAttribute('data-filter');
      filterGallery(filterValue);
      
      if (filterValue !== 'all') {
        const coords = JSON.parse(btn.getAttribute('data-coords'));
        if (coords) {
          map.flyTo(coords, 9, { duration: 1.5 });
          updateHUD(filterValue);
        }
      } else {
        map.flyTo([-13.5, -73.0], 6.2, { duration: 1.5 });
        resetHUD();
      }
    });
  });


  // 3. Map Setup
  // Itinerary lists coordinates (injected by Hugo via window.PERU_DATA, see peru.html)
  const itinerary = (window.PERU_DATA && window.PERU_DATA.itinerary) || [];
  
  const map = L.map('peru-map', {
    center: [-13.5, -73.0],
    zoom: 6.2,
    minZoom: 5.5,
    maxZoom: 12,
    scrollWheelZoom: false,
    zoomControl: false,
    attributionControl: false
  });

  const darkTilesPeru = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    subdomains: 'abcd',
    maxZoom: 19
  });
  darkTilesPeru.addTo(map);

  const satelliteTilesPeru = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri'
  });

  L.control.zoom({ position: 'bottomright' }).addTo(map);

  // The map now lives inside a collapsed <details> element, so it initializes
  // with a zero-size container; fix its tile grid the first time it's opened.
  const peruItineraryDetails = document.getElementById('peru-itinerary-details');
  if (peruItineraryDetails) {
    peruItineraryDetails.addEventListener('toggle', () => {
      if (peruItineraryDetails.open) {
        setTimeout(() => map.invalidateSize(), 50);
      }
    });
  }

  // Draw itinerary dashed polyline
  const coordsList = itinerary.filter(item => item.coords).map(item => item.coords);
  const polyline = L.polyline(coordsList, {
    color: '#3b82f6',
    weight: 3.5,
    opacity: 0.85,
    dashArray: '8, 12',
    lineCap: 'round'
  }).addTo(map);

  // Create map markers
  const markerGroup = {};

  itinerary.forEach((item, index) => {
    if (!item.coords) return;

    // Custom HTML marker
    const coverImg = item.cover ? item.cover : '';
    const markerHtml = `
      <div class="peru-map-marker ${!coverImg ? 'empty-marker' : ''}" style="background-image: url('${coverImg}');">
        <div class="marker-border"></div>
      </div>
    `;

    const marker = L.marker(item.coords, {
      icon: L.divIcon({
        html: markerHtml,
        className: 'custom-peru-marker',
        iconSize: [36, 36],
        iconAnchor: [18, 18]
      })
    }).addTo(map);

    // Tooltip displaying translated name & dates
    const displayName = t.dest_names[item.id] || item.name;
    const displayDate = t.dest_dates[item.id] || item.date;

    const tooltipContent = `
      <div style="display: flex; flex-direction: column; align-items: center; gap: 4px; min-width: 140px; padding: 4px;">
        ${coverImg ? `<img src="${coverImg}" style="width: 100%; height: 80px; object-fit: cover; border-radius: 4px; box-shadow: 0 2px 5px rgba(0,0,0,0.25);" loading="lazy">` : ''}
        <span style="font-weight: 700; font-size: 0.85rem; letter-spacing: 0.5px; color:#ffffff !important;">${displayName}</span>
        <span style="font-size: 0.65rem; color: #a1a1aa !important; margin-top: 1px;">${displayDate}</span>
      </div>
    `;

    marker.bindTooltip(tooltipContent, {
      direction: 'top',
      className: 'map-tooltip-fancy mini-map-tooltip-container',
      offset: [0, -10],
      interactive: true
    });

    // Clicking marker filters page
    marker.on('click tap', () => {
      stopAutopilot();
      filterGallery(item.id);
      map.flyTo(item.coords, 9, { duration: 1.5 });
      updateHUD(item.id);
      scrollToGrid();
    });

    markerGroup[item.id] = marker;
  });

  // Update highlighted marker
  function updateActiveMapMarker(activeDestId) {
    Object.keys(markerGroup).forEach(id => {
      const markerEl = markerGroup[id].getElement();
      if (markerEl) {
        const innerDiv = markerEl.querySelector('.peru-map-marker');
        if (innerDiv) {
          innerDiv.classList.toggle('active-marker', id === activeDestId);
        }
      }
    });
  }

  // HUD updates
  function updateHUD(destId) {
    const destName = t.dest_names[destId] || destId;
    const destDate = t.dest_dates[destId] || "";
    
    document.getElementById('peru-current-dest-name').textContent = destName;
    document.getElementById('peru-current-dest-date').textContent = destDate.split(" 2026")[0]; // Short date for timeline display
  }

  function resetHUD() {
    document.getElementById('peru-current-dest-name').textContent = t.intro_hud;
    document.getElementById('peru-current-dest-date').textContent = t.hud_sub;
  }


  // 4. Autopilot play timeline engine (bubbles matching the timeline track)
  const playBtn = document.getElementById('peru-play-pause');
  const playIcon = document.getElementById('peru-play-icon');
  const pauseIcon = document.getElementById('peru-pause-icon');
  const timelineTrack = document.getElementById('peru-timeline-track');
  
  let isPlaying = false;
  let autopilotIndex = -1;
  let autopilotTimeout = null;

  // Populate timeline track with clickable bubbles
  itinerary.forEach((item, index) => {
    const bubble = document.createElement('div');
    bubble.className = 'timeline-bubble';
    bubble.setAttribute('data-bubble-id', item.id);
    bubble.title = `${t.dest_names[item.id] || item.name} (${t.dest_dates[item.id] || item.date})`;
    
    bubble.addEventListener('click', (e) => {
      e.stopPropagation();
      stopAutopilot();
      autopilotIndex = index;
      filterGallery(item.id);
      updateHUD(item.id);
      if (item.coords) {
        map.flyTo(item.coords, 9, { duration: 1.5 });
      }
    });
    
    timelineTrack.appendChild(bubble);
  });

  function updateActiveTimelineBubble(activeDestId) {
    const bubbles = document.querySelectorAll('.timeline-bubble');
    let passed = true;
    
    bubbles.forEach(b => {
      const id = b.getAttribute('data-bubble-id');
      b.classList.remove('active', 'passed');
      
      if (id === activeDestId) {
        b.classList.add('active');
        passed = false; // All subsequent bubbles are not passed
      } else if (passed && activeDestId !== 'all') {
        b.classList.add('passed');
      }
    });
  }

  function startAutopilot() {
    isPlaying = true;
    playIcon.classList.add('peru-hidden');
    pauseIcon.classList.remove('peru-hidden');
    
    // Loop back if finished
    if (autopilotIndex >= itinerary.length - 1) {
      autopilotIndex = -1;
    }
    
    autopilotStep();
  }

  function stopAutopilot() {
    isPlaying = false;
    playIcon.classList.remove('peru-hidden');
    pauseIcon.classList.add('peru-hidden');
    if (autopilotTimeout) clearTimeout(autopilotTimeout);
  }

  function autopilotStep() {
    if (!isPlaying) return;
    
    autopilotIndex++;
    if (autopilotIndex >= itinerary.length) {
      // Finished route! Reset.
      stopAutopilot();
      filterGallery('all');
      map.flyTo([-13.5, -73.0], 6.2, { duration: 2.0 });
      resetHUD();
      autopilotIndex = -1;
      return;
    }

    const step = itinerary[autopilotIndex];
    filterGallery(step.id);
    updateHUD(step.id);
    
    if (step.coords) {
      map.flyTo(step.coords, 9, {
        duration: 2.0,
        easeLinearity: 0.25
      });
    }

    // Wait 5 seconds (2s flight + 3s viewing) then step
    autopilotTimeout = setTimeout(autopilotStep, 5000);
  }

  playBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    if (isPlaying) {
      stopAutopilot();
    } else {
      startAutopilot();
    }
  });

  // --- Fullscreen Logic ---
  const peruFsBtn = document.getElementById('peru-fullscreen-toggle');
  const peruFsContainer = document.querySelector('.peru-map-section .map-container-wrapper');
  const peruExpandIcon = document.getElementById('peru-fs-expand-icon');
  const peruCollapseIcon = document.getElementById('peru-fs-collapse-icon');

  const updatePeruFSUI = (isFullscreen) => {
    if (isFullscreen) {
      peruExpandIcon.classList.add('peru-hidden');
      peruCollapseIcon.classList.remove('peru-hidden');
      peruFsContainer.classList.add('peru-is-fullscreen');
      document.body.style.overflow = 'hidden';
    } else {
      peruExpandIcon.classList.remove('peru-hidden');
      peruCollapseIcon.classList.add('peru-hidden');
      peruFsContainer.classList.remove('peru-is-fullscreen');
      peruFsContainer.classList.remove('peru-is-pseudo-fullscreen');
      document.body.style.overflow = '';
    }
    setTimeout(() => map.invalidateSize(), 300);
  };

  const togglePeruFullscreen = () => {
    const fsElement = document.fullscreenElement || document.webkitFullscreenElement;
    const isPseudo = peruFsContainer.classList.contains('peru-is-pseudo-fullscreen');
    if (!fsElement && !isPseudo) {
      if (peruFsContainer.requestFullscreen) {
        peruFsContainer.requestFullscreen();
      } else if (peruFsContainer.webkitRequestFullscreen) {
        peruFsContainer.webkitRequestFullscreen();
      } else {
        peruFsContainer.classList.add('peru-is-pseudo-fullscreen');
        updatePeruFSUI(true);
      }
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen();
      } else if (document.webkitExitFullscreen) {
        document.webkitExitFullscreen();
      } else if (isPseudo) {
        updatePeruFSUI(false);
      }
    }
  };

  peruFsBtn.addEventListener('click', togglePeruFullscreen);

  ['fullscreenchange', 'webkitfullscreenchange'].forEach(evt => {
    document.addEventListener(evt, () => {
      const isFS = !!(document.fullscreenElement || document.webkitFullscreenElement);
      updatePeruFSUI(isFS);
    });
  });

  // --- Satellite Style Toggle ---
  const peruStyleBtn = document.getElementById('peru-style-toggle');
  const peruSatIcon = document.getElementById('peru-style-satellite-icon');
  const peruDarkIcon = document.getElementById('peru-style-dark-icon');

  peruStyleBtn.addEventListener('click', () => {
    const isSatellite = map.hasLayer(satelliteTilesPeru);
    if (!isSatellite) {
      map.removeLayer(darkTilesPeru);
      satelliteTilesPeru.addTo(map);
      satelliteTilesPeru.bringToBack();
      peruSatIcon.classList.add('peru-hidden');
      peruDarkIcon.classList.remove('peru-hidden');
    } else {
      map.removeLayer(satelliteTilesPeru);
      darkTilesPeru.addTo(map);
      darkTilesPeru.bringToBack();
      peruSatIcon.classList.remove('peru-hidden');
      peruDarkIcon.classList.add('peru-hidden');
    }
  });

  // --- Video Controls ---
  document.querySelectorAll('.peru-video-item').forEach(item => {
    const video = item.querySelector('.peru-video-el');
    const playBtn = item.querySelector('.peru-play-btn');
    const playIcon = item.querySelector('.peru-play-icon');
    const pauseIcon = item.querySelector('.peru-pause-icon');
    const muteBtn = item.querySelector('.peru-mute-btn');
    const muteOff = item.querySelector('.peru-mute-off');
    const muteOn = item.querySelector('.peru-mute-on');
    const progBar = item.querySelector('.peru-vprog-bar');

    if (!video) return;

    // Play on hover
    item.addEventListener('mouseenter', () => { video.play().catch(() => {}); });
    item.addEventListener('mouseleave', () => { video.pause(); });

    // Play/Pause button
    playBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      if (video.paused) {
        video.play();
        playIcon.style.display = 'none';
        pauseIcon.style.display = '';
      } else {
        video.pause();
        playIcon.style.display = '';
        pauseIcon.style.display = 'none';
      }
    });

    video.addEventListener('play',  () => { playIcon.style.display = 'none'; pauseIcon.style.display = ''; });
    video.addEventListener('pause', () => { playIcon.style.display = ''; pauseIcon.style.display = 'none'; });

    // Mute button
    muteBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      video.muted = !video.muted;
      muteOff.style.display = video.muted ? 'none' : '';
      muteOn.style.display  = video.muted ? '' : 'none';
    });

    // Progress bar
    video.addEventListener('timeupdate', () => {
      if (video.duration) {
        progBar.style.width = (video.currentTime / video.duration * 100) + '%';
      }
    });
  });
});
