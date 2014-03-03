#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import setuptools


setup_params = dict(
    name='transflow',
    author="shellquery",
    author_email="shellquery@gmail.com",
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False)

if __name__ == '__main__':
    setuptools.setup(**setup_params)
