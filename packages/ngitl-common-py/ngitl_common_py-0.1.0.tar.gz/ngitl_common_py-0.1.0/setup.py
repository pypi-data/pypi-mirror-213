#!/usr/bin/env python
# Copyright (C) 2022, NG:ITL
import versioneer
from setuptools import find_packages, setup


setup(
    name="ngitl_common_py",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Helper classes and functions for common python problems",
    author="NG:ITL",
    license="GPLv3",
    author_email="torsten.wylegala@volkswagen.de",
    url="https://github.com/vw-wob-it-edu-ngitl/ngitl_common_py/",
    packages=find_packages("."),
    install_requires=["pywin32==306"],
)
