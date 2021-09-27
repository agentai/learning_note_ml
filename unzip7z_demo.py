#!/usr/bin/env python
# -*- coding: utf-8 -*-

import py7zr  # pip install py7zr
import os

"""
7z文件解压
"""

base_path = "/Users/chitao/Downloads/"

for filename in [x for x in os.listdir(base_path) if x.endswith(".7z")]:
    print(filename)
    with py7zr.SevenZipFile(base_path + filename, mode='r', password='zhishikoo.com') as z:
        z.extractall()