#!/usr/bin/env python3
"""
Sri Bali Agency — build script
Assembles src/ files into index.html.

Usage:
  python3 build.py

Edit src/data/packages.json  to add / change tours, routes, prices.
Edit src/data/markers.json   to add / change map pins.
Edit src/sections/*.html     to change section content.
Then run this script and commit the updated index.html.
"""

import html
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))


# ── Helpers ────────────────────────────────────────────────────────────────────

def read(rel_path):
    with open(os.path.join(BASE, rel_path), encoding='utf-8') as f:
        return f.read()

def load_json(rel_path):
    return json.loads(read(rel_path))

def e(text):
    """HTML-escape a value for safe insertion into HTML."""
    return html.escape(str(text))


# ── Package / Route HTML generation ───────────────────────────────────────────

def build_route_card(route, package_name):
    stops = ''.join(f'\n                      <li>{e(s)}</li>' for s in route['stops'])

    pricing_rows = ''
    for i, p in enumerate(route['pricing']):
        cost = f'<strong>{e(p["cost"])}</strong>' if i == 0 else e(p['cost'])
        pricing_rows += f'\n                      <tr><td>{e(p["item"])}</td><td>{cost}</td></tr>'

    return (
        '          <div class="route-card">\n'
        '            <button class="accordion-header" aria-expanded="false">\n'
        '              <div class="route-meta">\n'
        f'                <span class="route-name">{e(route["name"])}</span>\n'
        f'                <span class="route-duration">⏱ {e(route["duration"])}</span>\n'
        '              </div>\n'
        '              <div class="route-right">\n'
        f'                <span class="route-price">From {e(route["basePrice"])}</span>\n'
        '                <span class="accordion-arrow" aria-hidden="true">›</span>\n'
        '              </div>\n'
        '            </button>\n'
        '            <div class="accordion-body">\n'
        '              <div class="accordion-inner">\n'
        '                <div class="accordion-inner-content">\n'
        '                  <div class="route-stops">\n'
        '                    <h4>Route Stops</h4>\n'
        f'                    <ol>{stops}\n'
        '                    </ol>\n'
        '                  </div>\n'
        '                  <div class="pricing-table">\n'
        '                    <h4>Pricing</h4>\n'
        f'                    <table><tbody>{pricing_rows}\n'
        '                    </tbody></table>\n'
        '                  </div>\n'
        '                  <button class="btn btn-whatsapp wa-book-btn"\n'
        f'                          data-wa-package="{e(package_name)}" data-wa-route="{e(route["name"])}">\n'
        '                    \U0001f4f1 Book via WhatsApp\n'
        '                  </button>\n'
        '                </div>\n'
        '              </div>\n'
        '            </div>\n'
        '          </div>'
    )


def build_packages_section(packages):
    tabs = []
    for i, pkg in enumerate(packages):
        active = ' active' if i == 0 else ''
        selected = 'true' if i == 0 else 'false'
        tabs.append(
            f'        <button class="tab-btn{active}" data-tab="{e(pkg["id"])}" '
            f'role="tab" aria-selected="{selected}" aria-controls="tab-{e(pkg["id"])}">'
            f'{pkg["icon"]} {e(pkg["name"])}</button>'
        )

    panels = []
    for i, pkg in enumerate(packages):
        active = ' active' if i == 0 else ''
        cards = '\n\n'.join(build_route_card(r, pkg['name']) for r in pkg['routes'])
        panels.append(
            f'      <div id="tab-{e(pkg["id"])}" class="tab-panel{active}" role="tabpanel">\n'
            f'        <div class="package-header">\n'
            f'          <h3>{e(pkg["name"])}</h3>\n'
            f'          <p>{e(pkg["tagline"])}</p>\n'
            f'        </div>\n'
            f'        <div class="routes-list">\n'
            f'\n{cards}\n'
            f'        </div>\n'
            f'      </div>'
        )

    return (
        '  <section id="packages" class="packages">\n'
        '    <div class="container">\n'
        '      <span class="section-label">Curated Experiences</span>\n'
        '      <h2 class="section-title">Tour Packages</h2>\n'
        '      <p class="section-subtitle">Five curated experiences, each with multiple route options. '
        'All prices include private car, guide, and fuel.</p>\n'
        '\n'
        '      <div class="tabs" role="tablist" aria-label="Tour packages">\n'
        + '\n'.join(tabs) + '\n'
        '      </div>\n'
        '\n'
        + '\n\n'.join(panels) + '\n'
        '\n'
        '    </div>\n'
        '  </section>'
    )


# ── Static page fragments ──────────────────────────────────────────────────────

HEAD = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Sri Bali Agency — Private car tours in Bali by a Balinese family. Spiritual, Adventure, Cultural, Beach &amp; Nature packages with local guide Sri.">
  <title>Sri Bali Agency — Private Car Tours in Bali</title>

  <!-- Dark mode flash prevention: must run before CSS applies -->
  <script>
    (function () {
      var t = localStorage.getItem('sri-bali-theme') ||
        (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
      document.documentElement.setAttribute('data-theme', t);
    })();
  </script>

  <!-- Leaflet CSS -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.min.css">

  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">

  <!-- Site CSS -->
  <link rel="stylesheet" href="css/base.css">
  <link rel="stylesheet" href="css/components.css">
  <link rel="stylesheet" href="css/nav.css">
  <link rel="stylesheet" href="css/hero.css">
  <link rel="stylesheet" href="css/about.css">
  <link rel="stylesheet" href="css/packages.css">
  <link rel="stylesheet" href="css/map.css">
  <link rel="stylesheet" href="css/contact.css">
</head>"""

NAV = """\
  <header class="site-header">
    <nav class="nav container">
      <a href="#hero" class="nav-logo">
        <span class="logo-icon">\U0001f33a</span>
        <span class="logo-text">Sri Bali Agency</span>
      </a>

      <ul class="nav-links" id="nav-links">
        <li><a href="#about"    class="nav-link">About</a></li>
        <li><a href="#packages" class="nav-link">Packages</a></li>
        <li><a href="#map"      class="nav-link">Map</a></li>
        <li><a href="#contact"  class="nav-link">Contact</a></li>
      </ul>

      <div class="nav-actions">
        <button id="theme-toggle" class="theme-toggle" aria-label="Switch to dark mode">\U0001f319</button>
        <button class="mobile-menu-btn" id="mobile-menu-btn" aria-label="Toggle menu" aria-expanded="false">
          <span></span><span></span><span></span>
        </button>
      </div>
    </nav>
  </header>"""

FAB = """\
  <!-- Floating WhatsApp FAB (visible on mobile) -->
  <a class="fab-whatsapp"
     href="https://wa.me/6281246887673"
     target="_blank" rel="noopener noreferrer"
     aria-label="Chat with Sri on WhatsApp">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
    </svg>
  </a>"""

SCRIPTS = """\
  <!-- Leaflet JS (synchronous — must be defined before deferred site scripts run) -->
  <script src="https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.min.js"></script>

  <!-- Site JS (defer — execute in order after DOM parsed) -->
  <script src="js/theme.js"     defer></script>
  <script src="js/nav.js"       defer></script>
  <script src="js/tabs.js"      defer></script>
  <script src="js/accordion.js" defer></script>
  <script src="js/map.js"       defer></script>
  <script src="js/whatsapp.js"  defer></script>"""


# ── Main build ─────────────────────────────────────────────────────────────────

def build():
    packages = load_json('src/data/packages.json')
    markers  = load_json('src/data/markers.json')

    hero        = read('src/sections/hero.html').rstrip()
    about       = read('src/sections/about.html').rstrip()
    map_section = read('src/sections/map-section.html').rstrip()
    contact     = read('src/sections/contact.html').rstrip()

    packages_html  = build_packages_section(packages)
    markers_json   = json.dumps(markers, ensure_ascii=False, separators=(',', ':'))
    markers_script = f'  <script>window.MAP_MARKERS = {markers_json};</script>'

    parts = [
        HEAD,
        '<body>',
        '',
        NAV,
        '',
        hero,
        '',
        about,
        '',
        packages_html,
        '',
        map_section,
        '',
        contact,
        '',
        FAB,
        '',
        markers_script,
        '',
        SCRIPTS,
        '',
        '</body>',
        '</html>',
        '',
    ]

    page = '\n'.join(parts)

    out_path = os.path.join(BASE, 'index.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(page)

    route_count = sum(len(p['routes']) for p in packages)
    print(f'✓  Built index.html  ({len(page):,} bytes)')
    print(f'   {len(packages)} packages   {route_count} routes   {len(markers)} map markers')


if __name__ == '__main__':
    build()
