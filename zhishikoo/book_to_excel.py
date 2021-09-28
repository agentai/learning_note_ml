#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
生成excel
"""
import pandas as pd
import json
import os


base_path = './'
filename = sorted([x for x in os.listdir(base_path) if x.startswith("book_info.json_")])[-1]
print(filename)
with open(filename, "r") as f:
    lines = [json.loads(x) for x in set(f.readlines())]
df = pd.DataFrame(lines)
df.to_excel("books.xlsx", index=False)  # pip install openpyxl