#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Made by papi
# Created on: Wed 14 May 2025 04:35:49 PM IST
# insanekartwii.py
# Description:

import os, shutil, io
import zipfile, requests

ZIP_FOLDER       = "/tmp/update/"

class InsaneKartWii():
    def __init__(self, config):
        self.download_link = "https://ikw.mwk.li/ikw/Insane%20Kart%20Wii%20v2.0.1.zip"
        self.cfg = config

    def exists(self):
        return os.path.exists(self.cfg['dolphin_path'] + "/IKWv2/")

    def install(self):
        print("instaling IKW")
        extract_to = ZIP_FOLDER
        res = requests.get(self.download_link)

        res.raise_for_status()
        with zipfile.ZipFile(io.BytesIO(res.content)) as zip_fp:
            os.makedirs(extract_to, exist_ok=True)
            zip_fp.extractall(extract_to)
        print(f"zip extracted at {extract_to}")
        print(f"moving all to {self.cfg['dolphin_path']}")
        if os.path.exists(self.cfg['dolphin_path'] + "/IKWv2/"):
            shutil.rmtree(self.cfg['dolphin_path'] + "/IKWv2/")
        shutil.move(extract_to + "/RetroRewind6/", self.cfg['dolphin_path'] + "/IKWv2/")
        if os.path.exists(self.cfg['dolphin_path'] + "/riivolution/IKWv2.xml"):
            os.remove(self.cfg['dolphin_path'] + "/riivolution/IKWv2.xml")
        os.makedirs(self.cfg['dolphin_path'] + "/riivolution/", exist_ok=True)
        shutil.move(extract_to + "/riivolution/IKWv2.xml", self.cfg['dolphin_path'] + "/riivolution/IKWv2.xml")

