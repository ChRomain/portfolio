document.addEventListener('DOMContentLoaded', function () {
  var mapEl = document.getElementById('itinerary-map');
  if (!mapEl || typeof L === 'undefined') return;

  var stops = window.ITINERARY_MAP_DATA || [];
  if (stops.length < 2) return;

  var map = L.map(mapEl, { scrollWheelZoom: false });

  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    subdomains: 'abcd',
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap contributors &copy; CARTO'
  }).addTo(map);

  var latlngs = stops.map(function (stop) {
    return [stop.coords[0], stop.coords[1]];
  });

  stops.forEach(function (stop, i) {
    L.circleMarker(latlngs[i], {
      radius: 8,
      fillColor: '#ffffff',
      color: '#6366f1',
      weight: 2,
      opacity: 1,
      fillOpacity: 1
    })
      .addTo(map)
      .bindPopup('<strong>' + (i + 1) + '. ' + stop.label + '</strong>');
  });

  L.polyline(latlngs, { color: '#6366f1', weight: 2, dashArray: '6, 8', opacity: 0.7 }).addTo(map);
  map.fitBounds(latlngs, { padding: [30, 30] });
});
