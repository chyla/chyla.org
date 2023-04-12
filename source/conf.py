# -- Path setup --------------------------------------------------------------

import os
import sys
sys.path.append(os.path.abspath("./_ext"))


# -- Project information -----------------------------------------------------

project = 'chyla.org'
copyright = 'Adam Chyła'
author = 'Adam Chyła'
language = 'pl'


# -- General configuration ---------------------------------------------------

master_doc = "content"

extensions = [
    'pdfobject',
]

templates_path = ['_templates']

exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

html_theme = 'chyla'
html_theme_path = ['_themes']
html_logo = '_static/logo-45x45.png'
html_favicon = html_logo
html_copy_source = False
html_show_sphinx = False

html_static_path = ['_static']
html_extra_path = ['_extra']

html_context = {
	'extra_scripts': '''
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-DKEWN50PZG"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-DKEWN50PZG');
</script>
''',

	'footer_infos': '''
<h5>Adam Chyła</h5>
<p>Specjalista ds. Rozwoju Oprogramowania</p>
''',

	'footer_social_list': '''
<li><a href="https://github.com/chyla" target="_blank"><i class="bi bi-github"></i></a></li>
''',

	'footer_law': '''
<p>Witryna prywatna. Każda opinia wyrażona w tej wirtynie jest wyłącznie moją opinią (nie jest to opinia mojego pracodawcy).<br/>
   Private website. All opinions expressed here are only mine (not of my employer).</p>

<p><a href="/law/nota_prawna.html">Zapoznaj się z notą prawną dotyczącą treści i funkcjonowania portalu</a> oraz <a href="/law/polityka_prywatnosci_i_plikow_cookies.html">polityką prywatności i plików cookie</a>.</p>
''',
}

html_additional_pages = {
    'index': 'index.html',
    'blog/index': 'blog/index.html',
    'blog/Linux_-_Core_dump/index': 'blog/Linux_-_Core_dump/index.html',
    'blog/Podstawy_GDB/index': 'blog/Podstawy_GDB/index.html',
    'blog/Python_and_virtualenv/index': 'blog/Python_and_virtualenv/index.html',
    'blog/Python_-_Dekoratory/index': 'blog/Python_-_Dekoratory/index.html',
    'blog/Python_-_Generatory/index': 'blog/Python_-_Generatory/index.html',
    'blog/Zapomniane_haslo_zaszyfrowanego_dysku/index': 'blog/Zapomniane_haslo_zaszyfrowanego_dysku/index.html',
    'blog/Zmienne-srodowiskowe-w-systemie-Linux/index': 'blog/Zmienne-srodowiskowe-w-systemie-Linux/index.html',
	's/index': 's/index.html',
	's/twitch/index': 's/twitch/index.html',
}
