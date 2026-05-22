document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.accordion-header').forEach(function (header) {
    header.addEventListener('click', function () {
      var body = header.nextElementSibling;
      var isOpen = body.classList.contains('open');
      var panel = header.closest('.routes-list');

      if (panel) {
        panel.querySelectorAll('.accordion-body').forEach(function (b) {
          b.classList.remove('open');
        });
        panel.querySelectorAll('.accordion-header').forEach(function (h) {
          h.setAttribute('aria-expanded', 'false');
        });
      }

      if (!isOpen) {
        body.classList.add('open');
        header.setAttribute('aria-expanded', 'true');
      }
    });
  });
});
