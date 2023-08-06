#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 17:51:50 2023

@author: javiera.quiroz
"""

from setuptools import setup

setup(
    name='FlyBaseDownloads',
    version='1.0.1',
    license='MIT',
    author='Javiera Quiroz Olave',
    url= 'https://github.com/JavieraQuirozO/FlyBaseDownloads',
    author_email='javiera.quiroz@biomedica.udec.cl',
    long_description_content_type='text/x-rst',
    long_description= 'The non-official FlyBaseDownload Packege',
    description='Package to download Flybase data in Python, easily and quickly.',
    packages=['FlyBaseDownloads'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
)
