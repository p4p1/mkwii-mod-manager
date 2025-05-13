#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Made by papi
# Created on: Tue 13 May 2025 03:02:16 PM IST
# gif_extractor.py
# Description:

from PIL import Image
import sys, os

gif = Image.open(sys.argv[1])
frame_folder = sys.argv[2]
os.makedirs(frame_folder, exist_ok=True)

for i in range(gif.n_frames):
    gif.seek(i)
    gif.save(f"{frame_folder}/frame_{i}.png")
