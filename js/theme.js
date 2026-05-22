(function () {
  var THEME_KEY = 'sri-bali-theme';
  var html = document.documentElement;
  var btn = document.getElementById('theme-toggle');

  function applyTheme(theme) {
    html.setAttribute('data-theme', theme);
    if (btn) {
      btn.textContent = theme === 'dark' ? '☀️' : '🌙';
      btn.setAttribute('aria-label', theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
    }
    localStorage.setItem(THEME_KEY, theme);
  }

  var saved = localStorage.getItem(THEME_KEY)
    || (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  applyTheme(saved);

  if (btn) {
    btn.addEventListener('click', function () {
      applyTheme(html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
    });
  }
})();
