# -*- coding: utf-8 -*-
"""widgets to be used in a form"""

import logging

from django.forms import Media

import floppyforms

from . import settings


class BaseInlineHtmlInput(floppyforms.widgets.TextInput):
    """Base class for Inline HtmlInput"""
    clean_value_callbacks = []

    def get_context(self, *args, **kwargs):
        """get context"""
        context = super(BaseInlineHtmlInput, self).get_context(*args, **kwargs)
        context.update({'field_prefix': settings.get_field_prefix()})
        return context

    def value_from_datadict(self, data, files, name):
        """return value"""
        value = super(BaseInlineHtmlInput, self).value_from_datadict(data, files, name)
        return self.clean_value(value)

    def clean_value(self, origin_value):
        """This apply several fixes on the html"""
        return_value = origin_value
        if return_value:  # don't manage None values
            for callback in self.clean_value_callbacks:
                return_value = callback(return_value)
        return return_value


class CkEditorInput(BaseInlineHtmlInput):
    """
    Text widget with CK-Editor html editor
    requires floppyforms to be installed
    """

    template_name = 'html_editor/ckeditor_input.html'

    @property
    def media(self):
        """return code for inserting required js and css files"""
        init_url = settings.init_url()
        try:
            css = {'all': ()}
            js_files = [
                '{0}/ckeditor.js'.format(settings.ckeditor_version()),
                init_url,
            ]
            return Media(css=css, js=js_files)
        except Exception as msg:
            django_logger = logging.getLogger('django')
            django_logger.error(u'CkEditorInput._get_media Error {0}'.format(msg))


def get_inline_html_widget():
    """returns the Input field to use"""
    editor_name = settings.get_html_editor()
    input_class = {
        'ck-editor': CkEditorInput,
    }[editor_name]
    return input_class()
