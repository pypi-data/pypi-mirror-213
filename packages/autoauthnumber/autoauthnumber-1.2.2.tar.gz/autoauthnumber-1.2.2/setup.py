# -*- coding: utf-8 -*-

"""
THIS FILE IS PART OF NETWORK FOR MWAFU LIBRARY LOVE BOOK STORE BY MATT BELFAST BROWN
setup.py - The core part of the Author Number library.

Author: Matt Belfast Brown
Creat Date:2021-05-30
Version Date：2023-06-10
Version:1.2.2

THIS PROGRAM IS FREE FOR EVERYONE,IS LICENSED UNDER GPL-3.0
YOU SHOULD HAVE RECEIVED A COPY OF GPL-3.0 LICENSE.

Copyright (C) 2021-2023 Matt Belfast Brown
Copyright (C) 2021-2023 MWAFU LOVE BOOK STORE

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as 
published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty 
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program.  If not, 
see <http://www.gnu.org/licenses/>.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as dest_pimd:
    long_description = dest_pimd.read()

setup(
        name="autoauthnumber",
        version="1.2.2",

        author="Matt Belfast Brown",
        author_email="thedayofthedo@gmail.com",
        license="GPL-3.0 LICENSE",

        description="This is a library about automatic number-taking of 'General Chinese Author Number Table'. At present, "
                    "there is only one way to take the number, that is, directly looking up the table.In the future, "
                    "we will adapt to a variety of author numbering methods, please wait.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        keywords=["auto", "author number"],

        url="https://github.com/thedayofthedoctor/aan",
        project_urls={
            "Documentation": "http://belfast.web3v.work/program/doc/aan/",
            "Bug Tracker": "https://github.com/thedayofthedoctor/aan/issues",
            },

        packages=find_packages(),
        py_modules=["autoauthnumber.mk_Pron", "autoauthnumber.author_number", "autoauthnumber.Translate_API",
                    "autoauthnumber.Translate_API.BaiDu_API", "autoauthnumber.Translate_API.YouDao_API"],
        include_package_data=True,
        zip_safe=True,

        classifiers=[
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            ],
        platforms="any",
        install_requires=["pypinyin", "requests"],
        python_requires=">=3.7,<=3.11"
        )
