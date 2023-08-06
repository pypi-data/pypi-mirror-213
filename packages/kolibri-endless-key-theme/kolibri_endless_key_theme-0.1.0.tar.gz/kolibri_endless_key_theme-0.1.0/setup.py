#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2023 Endless OS Foundation, LLC
# SPDX-License-Identifier: MIT
from __future__ import absolute_import, print_function, unicode_literals

from setuptools import setup

import kolibri_endless_key_theme

dist_name = "kolibri_endless_key_theme"
plugin_name = "kolibri_endless_key_theme"
repo_url = "https://github.com/endlessm/kolibri-endless-key-theme"

# Default description of the distributed package
description = """A plugin to define a custom theme for Endless Key for Kolibri"""

long_description = """
A plugin that defines a custom theme to customise the appearance of Kolibri for
Endless Key. See the `Github repo <{repo_url}>`_ for more details.
""".format(
    repo_url=repo_url
)

setup(
    name=dist_name,
    version=kolibri_endless_key_theme.__version__,
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
