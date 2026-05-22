document.addEventListener('DOMContentLoaded', function () {
  var WA_NUMBER = '6281246887673';

  function buildWhatsAppLink(packageName, routeName) {
    var msg = (packageName && routeName)
      ? 'Hi Sri! I\'m interested in the *' + packageName + '* package (' + routeName + '). Can you share more details and availability?'
      : 'Hi Sri! I\'d like to book a private Bali tour. Can we discuss the options?';
    return 'https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent(msg);
  }

  document.querySelectorAll('.wa-book-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var pkg = btn.getAttribute('data-wa-package') || '';
      var route = btn.getAttribute('data-wa-route') || '';
      window.open(buildWhatsAppLink(pkg, route), '_blank', 'noopener,noreferrer');
    });
  });
});
