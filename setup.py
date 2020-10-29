"""Setup for engaged_xblock XBlock."""

from __future__ import absolute_import

import os

from setuptools import setup


def package_data(pkg, roots):
    """Generic function to find package_data.

    All of the files under each of the `roots` will be declared as package
    data for package `pkg`.

    """
    data = []
    for root in roots:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name="engaged_xblock-xblock",
    version="1.1.1",
    # TODO: write a better description.
    description="EngagED XBlock to generate Certificates",
    # TODO: choose a license: 'AGPL v3' and 'Apache 2.0' are popular.
    license="AGPL v3",
    packages=["engaged_xblock"],
    install_requires=["XBlock", "requests"],
    entry_points={"xblock.v1": [
        "engaged_xblock = engaged_xblock:EngagEDXBlock", ]},
    package_data=package_data("engaged_xblock", ["static", "public"]),
)
