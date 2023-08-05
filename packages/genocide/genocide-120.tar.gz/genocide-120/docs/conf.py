# GENOCIDE - Reconsider OTP-CR-117/19
# -*- coding: utf-8 -*-
#
# pylint: disable=W0012,C0114,C0116,W1514,C0103,W0613,C0209,C0413,R0903,R0913
# pylama: disable=E231


"Reconsider OTP-CR-117/19"


NAME = "genocide"
VERSION = "120"


import doctest
import os
import re
import sys


curdir = os.getcwd()


sys.path.insert(0, os.path.join(curdir, "..", ".."))
sys.path.insert(0, os.path.join(curdir, ".."))
sys.path.insert(0, os.path.join(curdir))


# -- Options for GENERIC output ---------------------------------------------


project = NAME
master_doc = 'index'
version = '%s' % VERSION
release = '%s' % VERSION
language = 'en'
today = ''
today_fmt = '%B %d, %Y'
needs_sphinx='1.7'
exclude_patterns = ['_build', '_templates', '_source', 'Thumbs.db', '.DS_Store']
source_suffix = '.rst'
source_encoding = 'utf-8-sig'
modindex_common_prefix = [""]
keep_warnings = False
templates_path=['_templates']
add_function_parentheses = False
add_module_names = False
show_authors = False
pygments_style = 'colorful'
extensions=[
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
    'sphinx.ext.githubpages'
]


# -- Options for HTML output -------------------------------------------------


html_title = "Reconsider OTP-CR-117/19"
html_style = 'genocide.css'
html_static_path = ["_static"]
html_css_files = ["genocide.css",]
html_short_title = "GENOCIDE %s" % VERSION
html_sidebars = {
    '**': [
        'about.html',
        'searchbox.html',
        'navigation.html',
        'relations.html',
    ]
}
html_theme = "alabaster"
html_theme_options = {
    'github_user': 'bthate',
    'github_repo': NAME,
    'github_button': False,
    'github_banner': False,
    'logo': 'skull.jpg',
    'link': '#000',
    'link_hover': '#000',
    'nosidebar': True,
    'show_powered_by': False,
    'show_relbar_top': False,
    'sidebar_width': 10,
}
html_favicon = "skull.jpg"
html_extra_path = []
html_last_updated_fmt = '%Y-%b-%d'
html_additional_pages = {}
html_domain_indices = False
html_use_index = True
html_split_index = True
html_show_sourcelink = False
html_show_sphinx = False
html_show_copyright = False
html_copy_source = False
html_use_opensearch = 'http://%s.rtfd.io/' % NAME
html_file_suffix = '.html'
htmlhelp_basename = 'testdoc'

intersphinx_mapping = {
                       'python': ('https://docs.python.org/3', 'objects.inv'),
                       'sphinx': ('http://sphinx.pocoo.org/', None),
                      }
intersphinx_cache_limit=1


rst_prolog = '''.. image:: genocide.png
    :width: 100%
    :height: 2.0cm
    :target: index.html

.. raw:: html

    <br>

'''

rst_epilog = '''.. raw:: html

    <br>
    
.. raw:: html

    <center>
    <b>

`home <index.html>`_ - :ref:`about <about>` - :ref:`manual <manual>` - :ref:`source <source>`  - `index <genindex-all.html>`_


.. raw:: html

    </b>
    </center>
    <br>


'''
autosummary_generate=True
autodoc_default_flags=['members', 'undoc-members', 'private-members', "imported-members"]
autodoc_member_order='groupwise'
autodoc_docstring_signature=True
autoclass_content="class"
doctest_global_setup=""
doctest_global_cleanup=""
doctest_test_doctest_blocks="default"
trim_doctest_flags=True
doctest_flags=doctest.REPORT_UDIFF
nitpick_ignore=[
                ('py:class', 'builtins.BaseException'),
               ]


def strip_signatures(app, what, name, obj, options, signature, return_annotation):
    sig = None
    if signature is not None:
        sig = re.sub(r'genocide\.[^.]*\.', '', signature)
    ret = None
    if return_annotation is not None:
        ret = re.sub(r'genocide\.[^.]*\.', '', signature)
    return sig, ret


def setup(app):
    app.connect('autodoc-process-signature', strip_signatures)
