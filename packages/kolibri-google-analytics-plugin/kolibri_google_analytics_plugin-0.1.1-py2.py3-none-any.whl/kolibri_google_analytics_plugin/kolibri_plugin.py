#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2023 Endless OS Foundation, LLC
# SPDX-License-Identifier: MIT
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from django.template.loader import render_to_string

import logging

from kolibri.core.hooks import FrontEndBaseHeadHook
from kolibri.plugins import KolibriPluginBase
from kolibri.plugins.hooks import register_hook
from kolibri.utils import conf


logger = logging.getLogger(__name__)


class GoogleAnalyticsPlugin(KolibriPluginBase):
    """
    A plugin to configure Google Analytics support for a Kolibri instance.

    TODO: What does it do, what configuration does it need, and how does it
    differ from the inbuilt Kolibri analytics. What are the morals of using it?
    """
    kolibri_options = "options"


@register_hook
class GoogleAnalyticsBaseHeadHook(FrontEndBaseHeadHook):
    @property
    def head_html(self):
        measurement_id = conf.OPTIONS["GoogleAnalytics"]["MEASUREMENT_ID"]
        if not measurement_id:
            logger.info("Google Analytics support enabled but MEASUREMENT_ID not set in options")
            return ""

        return render_to_string("head_snippet.html", {
            "measurement_id": conf.OPTIONS["GoogleAnalytics"]["MEASUREMENT_ID"],
        })
