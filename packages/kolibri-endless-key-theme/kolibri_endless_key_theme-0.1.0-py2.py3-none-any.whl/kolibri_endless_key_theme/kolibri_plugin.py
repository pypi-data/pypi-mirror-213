#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2023 Endless OS Foundation, LLC
# SPDX-License-Identifier: MIT
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from django.templatetags.static import static

from kolibri.core import theme_hook
from kolibri.plugins import KolibriPluginBase
from kolibri.plugins.hooks import register_hook


class EndlessKeyThemePlugin(KolibriPluginBase):
    pass


@register_hook
class EndlessKeyThemeHook(theme_hook.ThemeHook):
    @property
    def theme(self):
        # There doesn’t seem to be a way to only partially override the default
        # theme, so we have to duplicate it all here.
        return {
            "signIn": {
                "background": static("background.jpg"),
                "backgroundImgCredit": "Thomas Van Den Driessche",
                "topLogo": {
                    "style": "padding-left: 64px; padding-right: 64px; margin-bottom: 8px; margin-top: 8px",
                },
            },
            "logos": [
                {
                    "src": static("favicon.ico"),
                    "content_type": "image/vnd.microsoft.icon",
                    "size": "48x48",
                },
                {
                    "src": static("android-chrome-192x192.png"),
                    "content_type": "image/png",
                    "size": "192x192",
                },
                {
                    "src": static("android-chrome-256x256.png"),
                    "content_type": "image/png",
                    "size": "256x256",
                },
            ],
        }
