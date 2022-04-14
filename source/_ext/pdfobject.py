from docutils import nodes
from docutils.parsers.rst import Directive

from sphinx.util.docutils import SphinxDirective
from sphinx.util.osutil import copyfile, ensuredir

import os.path
from pkg_resources import resource_filename

JS_FILE = 'pdfobject.min.js'


class pdfobject(nodes.General, nodes.Element, nodes.Inline):
    def __init__(self, path, node_id):
        super().__init__()
        self.path = path
        self.node_id = node_id


def visit_pdfobject_node(self, node):
    self.body.append(f'''
<div id="{node.node_id}" class="pdfobject-container"></div>
<script>PDFObject.embed("{node.path}", "#{node.node_id}");</script>
''')

def depart_pdfobject_node(self, node):
    pass


class PdfDirective(SphinxDirective):
    has_content = True
    required_arguments = 1

    def run(self):
        targetid = 'pdfobject-%d' % self.env.new_serialno('pdfobject')

        pdf_node = pdfobject(path=self.arguments[0], node_id=targetid)

        return [pdf_node]


def copy_assets(app, exception):
    if app.builder.format == 'html' and not exception:
        staticdir = os.path.join(app.builder.outdir, '_static', 'pdfobject')
        ensuredir(staticdir)

        srcdir = resource_filename("pdfobject", JS_FILE)
        copyfile(srcdir, os.path.join(staticdir, JS_FILE))


def setup(app):
    app.add_node(pdfobject,
                 html=(visit_pdfobject_node, depart_pdfobject_node))

    app.add_directive('pdfobject', PdfDirective)

    app.connect("build-finished", copy_assets)

    app.add_js_file(os.path.join('pdfobject', JS_FILE))

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
