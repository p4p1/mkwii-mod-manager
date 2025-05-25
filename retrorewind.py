#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Made by papi
# Created on: Wed 14 May 2025 04:30:53 PM IST
# RetroRewind.py
# Description:

import os, shutil, io
import zipfile, requests

ZIP_FOLDER       = "/tmp/update/"

class RetroRewind():
    def __init__(self, config):
        self.cfg = config
        self.api_endpoint = "http://update.zplwii.xyz:8000/RetroRewind"
        self.latest = self.getLatestInfo()
        self.current_version = self.getCurrentVerison()
        print(f"Latest Version: {self.latest['version']}")
        print(f"Update URL: {self.latest['url']}")
        print(f"Current Version: {self.current_version}")

    def update_config(self, config):
        self.cfg = config

    def update_version(self):
        self.latest = self.getLatestInfo()
        self.current_version = self.getCurrentVerison()

    def exists(self):
        return os.path.exists(self.cfg["dolphin_path"] + "/RetroRewind6/")

    def getLatestInfo(self):
        try:
            req = requests.get(self.api_endpoint + "/RetroRewindVersion.txt")
            return { 'version': req.text.split('\n')[-1].split(' ')[0], 'url': req.text.split('\n')[-1].split(' ')[1] }
        except:
            return None

    def getCurrentVerison(self):
        try:
            with open(self.cfg['dolphin_path'] + '/RetroRewind6/version.txt', 'r') as fp:
                return fp.read()
        except:
            return None

    def needUpdate(self):
        if self.latest == None or self.current_version == None:
            return False
        if self.latest['version'] != self.current_version:
            return True
        else:
            return False

    def install(self):
        print("installing RR")
        URL = self.api_endpoint + "/zip/RetroRewind.zip"
        extract_to = ZIP_FOLDER
        print("downloading RR")
        res = requests.get(URL)

        res.raise_for_status()
        print("downloaded")
        with zipfile.ZipFile(io.BytesIO(res.content)) as zip_fp:
            os.makedirs(extract_to, exist_ok=True)
            zip_fp.extractall(extract_to)
        print(f"zip extracted at {extract_to}")
        print(f"moving all to {self.cfg['dolphin_path']}")
        if os.path.exists(self.cfg['dolphin_path'] + "/RetroRewind6/"):
            shutil.rmtree(self.cfg['dolphin_path'] + "/RetroRewind6/")
        shutil.move(extract_to + "/RetroRewind6/", self.cfg['dolphin_path'] + "/RetroRewind6/")
        if os.path.exists(self.cfg['dolphin_path'] + "/riivolution/RetroRewind6.xml"):
            os.remove(self.cfg['dolphin_path'] + "/riivolution/RetroRewind6.xml")
        os.makedirs(self.cfg['dolphin_path'] + "/riivolution/", exist_ok=True)
        shutil.move(extract_to + "/riivolution/RetroRewind6.xml", self.cfg['dolphin_path'] + "/riivolution/RetroRewind6.xml")
        print(f"Installed")

    def update(self):
        extract_to=ZIP_FOLDER

        if not os.path.exists(self.cfg['dolphin_path'] + "/RetroRewind6/"):
            return False
        if self.latest == None or self.current_version == None:
            return False
        URL = self.latest['url']
        res = requests.get(URL)
        res.raise_for_status()
        with zipfile.ZipFile(io.BytesIO(res.content)) as zip_fp:
            os.makedirs(extract_to, exist_ok=True)
            zip_fp.extractall(extract_to)
        for item in os.listdir(extract_to):
            src_path = os.path.join(extract_to, item)
            dst_path = os.path.join(self.cfg['dolphin_path'], item)

            # If target exists, remove it first
            if os.path.exists(dst_path):
                if os.path.isdir(dst_path):
                    shutil.rmtree(dst_path)
                else:
                    os.remove(dst_path)
            print(src_path)
            print(dst_path)
            if ".wad" not in src_path or "apps" not in src_path:
                shutil.move(src_path, dst_path)
            # Move the item

        with open(self.cfg['dolphin_path'] + '/RetroRewind6/version.txt', 'w') as fp:
            return fp.write(self.latest['version'])
