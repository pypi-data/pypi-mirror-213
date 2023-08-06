# -*- coding:utf-8 -*-
"""urls"""

from django.urls import path

from .views import html_editor_init, browser_urls, browser_images, ckeditor_config


urlpatterns = [
    path('html-editor-init.js', html_editor_init, name='html_editor_init'),
    path('ckeditor_config.js', ckeditor_config, name='ckeditor_config'),
    path('browser-images.js', browser_images, name='browser_images'),
    path('browser-urls.js', browser_urls, name='browser_urls'),
]
