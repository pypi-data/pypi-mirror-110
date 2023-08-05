import os

def setup(app):
    app.require_sphinx('2.0')

    # Register the theme that can be referenced without adding a theme path
    app.add_html_theme('sphinx_thunlp_theme', os.path.abspath(os.path.dirname(__file__)))

    # Add Sphinx message catalog for newer versions of Sphinx
    # See http://www.sphinx-doc.org/en/master/extdev/appapi.html#sphinx.application.Sphinx.add_message_catalog
    # rtd_locale_path = path.join(path.abspath(path.dirname(__file__)), 'locale')
    # app.add_message_catalog('sphinx', rtd_locale_path)

    return {'parallel_read_safe': True, 'parallel_write_safe': True}