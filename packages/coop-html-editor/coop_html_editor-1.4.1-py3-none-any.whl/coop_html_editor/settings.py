# -*- coding: utf-8 -*-
"""centralize settings"""

from django.conf import settings as project_settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse


def get_field_prefix():
    """return the prefix to use in form field names"""
    return "html_editor"


def get_html_editor():
    """return the name of the editor to use: aloha or ck-editor"""
    editor_name = getattr(project_settings, 'COOP_HTML_EDITOR', 'ck-editor')
    supported_editors = ('ck-editor', )
    if editor_name not in supported_editors:
        raise ImproperlyConfigured(
            u'Unknown editor {0}. Allowed choices: {1}'.format(editor_name, supported_editors)
        )
    return editor_name


def ckeditor_version():
    """return settings or default"""
    return getattr(project_settings, 'CKEDITOR_VERSION', "ckeditor.4.6.2")


def init_js_template():
    """return settings or default"""
    if get_html_editor() == 'ck-editor':
        return getattr(project_settings, 'CKEDITOR_INIT_JS_TEMPLATE', "html_editor/ckeditor-init.js")


def init_url():
    """return settings or default"""
    url = getattr(project_settings, 'COOP_HTML_EDITOR_INIT_URL', None)
    return url or reverse('html_editor_init')


def plugins():
    """return settings or default"""
    return []


def link_models():
    """return settings or default"""
    return getattr(project_settings, 'HTML_EDITOR_LINK_MODELS', ())


def image_models():
    """return settings or default"""
    return getattr(project_settings, 'HTML_EDITOR_IMAGE_MODELS', ())


def css_classes():
    """return settings or default"""
    if get_html_editor() == 'ck-editor':
        # Example
        # CKEDITOR_CSS_CLASSES = [
        #     "{name: 'Highlight', element: 'span', attributes: {'class': 'highlight'}}",
        #     "{name: 'Red Title', element: 'h3', styles: {color: '#880000'}}",
        # ]
        return getattr(project_settings, 'CKEDITOR_CSS_CLASSES', [])
    return []


def image_default_class():
    if get_html_editor() == 'ck-editor':
        return getattr(project_settings, 'CKEDITOR_IMAGE_DEFAULT_CLASS', '')
