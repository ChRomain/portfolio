document.addEventListener('DOMContentLoaded', function () {
  var mapEl = document.getElementById('itinerary-map');
  if (!mapEl || typeof L === 'undefined') return;

  var stops = window.ITINERARY_MAP_DATA || [];
  if (stops.length < 2) return;

  var map = L.map(mapEl, { scrollWheelZoom: false, attributionControl: false });

  L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}', {
    maxZoom: 16
  }).addTo(map);
  L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Reference/MapServer/tile/{z}/{y}/{x}', {
    maxZoom: 16
  }).addTo(map);

  var latlngs = stops.map(function (stop) {
    return [stop.coords[0], stop.coords[1]];
  });

  var markers = stops.map(function (stop, i) {
    return L.circleMarker(latlngs[i], {
      radius: 8,
      fillColor: '#ffffff',
      color: '#3b82f6',
      weight: 2,
      opacity: 1,
      fillOpacity: 1
    })
      .addTo(map)
      .bindPopup('<strong>' + stop.label + '</strong>');
  });

  L.polyline(latlngs, { color: '#3b82f6', weight: 2, dashArray: '6, 8', opacity: 0.7 }).addTo(map);
  map.fitBounds(latlngs, { padding: [30, 30] });

  // The map lives inside a collapsed <details>; fix its tile grid once opened.
  var detailsEl = mapEl.closest('details.itinerary-details');
  if (detailsEl) {
    detailsEl.addEventListener('toggle', function () {
      if (detailsEl.open) {
        setTimeout(function () {
          map.invalidateSize();
          map.fitBounds(latlngs, { padding: [30, 30] });
        }, 50);
      }
    });
  }

  // --- Autoplay through the stops, in order ---
  var playBtn = document.querySelector('.itinerary-play-btn');
  var playIcon = document.querySelector('.itinerary-play-icon');
  var pauseIcon = document.querySelector('.itinerary-pause-icon');
  var track = document.querySelector('.itinerary-timeline-track');
  if (!playBtn || !track) return;

  var progressBar = document.createElement('div');
  progressBar.className = 'itinerary-timeline-progress';
  track.appendChild(progressBar);

  var playing = false;
  var timeoutId = null;
  var stepIndex = 0;
  var STEP_DELAY = 2200;

  var hud = document.getElementById('itinerary-hud');
  var dayEls = Array.prototype.slice.call(document.querySelectorAll('.itinerary-day'));

  function setProgress(index) {
    var pct = ((index + 1) / stops.length) * 100;
    progressBar.style.width = pct + '%';
  }

  // Surligne le jour correspondant dans la liste et le ramène dans la vue, pour que
  // le texte de l'itinéraire suive le déplacement sur la carte.
  function highlightDay(dayIndex, scroll) {
    dayEls.forEach(function (el) {
      el.classList.toggle('is-active', Number(el.dataset.dayIndex) === dayIndex);
    });
    if (!scroll) return;
    var target = dayEls.filter(function (el) {
      return Number(el.dataset.dayIndex) === dayIndex;
    })[0];
    if (!target) return;
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    target.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'nearest' });
  }

  function clearHighlight() {
    dayEls.forEach(function (el) { el.classList.remove('is-active'); });
    if (hud) hud.classList.add('itinerary-hidden');
  }

  function setActiveMarker(index) {
    markers.forEach(function (m, i) {
      m.setStyle({
        radius: i === index ? 11 : 8,
        fillColor: i === index ? '#3b82f6' : '#ffffff',
        color: i === index ? '#ffffff' : '#3b82f6'
      });
    });
  }

  function goToStep(index) {
    var stop = stops[index];
    markers[index].openPopup();
    map.flyTo(latlngs[index], Math.max(map.getZoom(), 10), { duration: 1.2 });
    setProgress(index);
    setActiveMarker(index);
    if (hud) {
      hud.textContent = stop.label;
      hud.classList.remove('itinerary-hidden');
    }
    if (typeof stop.dayIndex === 'number') highlightDay(stop.dayIndex, true);
  }

  // Cliquer un marqueur met en avant son jour, hors lecture automatique.
  markers.forEach(function (m, i) {
    m.on('click', function () {
      var stop = stops[i];
      setActiveMarker(i);
      if (hud) {
        hud.textContent = stop.label;
        hud.classList.remove('itinerary-hidden');
      }
      if (typeof stop.dayIndex === 'number') highlightDay(stop.dayIndex, true);
    });
  });

  function stopAutoplay() {
    playing = false;
    if (timeoutId) clearTimeout(timeoutId);
    timeoutId = null;
    playIcon.classList.remove('itinerary-hidden');
    pauseIcon.classList.add('itinerary-hidden');
  }

  function playStep() {
    if (!playing) return;
    goToStep(stepIndex);
    if (stepIndex >= stops.length - 1) {
      timeoutId = setTimeout(stopAutoplay, STEP_DELAY);
      return;
    }
    stepIndex++;
    timeoutId = setTimeout(playStep, STEP_DELAY);
  }

  function startAutoplay() {
    playing = true;
    stepIndex = 0;
    progressBar.style.width = '0%';
    playIcon.classList.add('itinerary-hidden');
    pauseIcon.classList.remove('itinerary-hidden');
    playStep();
  }

  playBtn.addEventListener('click', function () {
    if (playing) {
      stopAutoplay();
      clearHighlight();
    } else {
      startAutoplay();
    }
  });
});
