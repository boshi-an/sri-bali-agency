document.addEventListener('DOMContentLoaded', function () {
  if (typeof L === 'undefined') return;

  var markers = (typeof window.MAP_MARKERS !== 'undefined') ? window.MAP_MARKERS : [];

  var categoryColors = {
    spiritual: '#c8882a',
    adventure: '#e63946',
    cultural:  '#6a4c93',
    beach:     '#2a9d8f',
    nature:    '#2d6a4f'
  };

  var map = L.map('bali-map', {
    center: [-8.5, 115.25],
    zoom: 10,
    scrollWheelZoom: false
  });

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 18
  }).addTo(map);

  markers.forEach(function (m) {
    var circle = L.circleMarker([m.lat, m.lng], {
      radius: 10,
      fillColor: categoryColors[m.category] || '#888',
      color: '#fff',
      weight: 2,
      opacity: 1,
      fillOpacity: 0.88
    }).addTo(map);

    var content =
      '<div class="marker-popup">' +
        '<img src="' + m.photo + '" alt="' + m.name + '" loading="lazy">' +
        '<div class="marker-popup-body">' +
          '<h3>' + m.name + '</h3>' +
          '<p>' + m.description + '</p>' +
          '<span class="category-badge category-' + m.category + '">' + m.category + '</span>' +
        '</div>' +
      '</div>';

    circle.bindPopup(L.popup({ maxWidth: 280, className: 'custom-popup' }).setContent(content));
    circle.on('mouseover', function () { this.openPopup(); });
    circle.on('click', function () { this.openPopup(); });
  });

  var mapEl = document.getElementById('bali-map');
  var resized = false;
  if (mapEl && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      if (entries[0].isIntersecting && !resized) {
        map.invalidateSize();
        resized = true;
      }
    }, { threshold: 0.1 }).observe(mapEl);
  }
});
