#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from setuptools import setup

import kolibri_google_analytics_plugin

dist_name = "kolibri_google_analytics_plugin"
plugin_name = "kolibri_google_analytics_plugin"
repo_url = "https://github.com/endlessm/kolibri-google-analytics-plugin"

# Default description of the distributed package
description = """A plugin to provide Google Analytics support for Kolibri"""

long_description = """
A plugin that provides Google Analytics support for the frontend and backend
of Kolibri. See the `Github repo <{repo_url}>`_ for more details.
""".format(
    repo_url=repo_url
)

setup(
    name=dist_name,
    version=kolibri_google_analytics_plugin.__version__,
    description=description,
    long_description=long_description,
    author="Endless OS Foundation",
    author_email="maintainers@endlessos.org",
    url=repo_url,
    packages=[str(plugin_name)],  # https://github.com/pypa/setuptools/pull/597
    entry_points={
        "kolibri.plugins": "{plugin_name} = {plugin_name}".format(
            plugin_name=plugin_name
        ),
    },
    package_dir={plugin_name: plugin_name},
    include_package_data=True,
    license="MIT",
    zip_safe=False,
    keywords="kolibri",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
