#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2023 Endless OS Foundation, LLC
# SPDX-License-Identifier: MIT

option_spec = {
    "GoogleAnalytics": {
        "MEASUREMENT_ID": {
            "type": "string",
            "default": "",
            "description": "Measurement ID which identifies this site to Google",
        },
    },
}
