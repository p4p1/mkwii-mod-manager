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
        self.api_endpoint = "http://update.rwfc.net:8000/RetroRewind"
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
        URL = self.api_endpoint + "/zip/RetroRewind.zip"
        extract_to = ZIP_FOLDER
        res = requests.get(URL)

        res.raise_for_status()
        with zipfile.ZipFile(io.BytesIO(res.content)) as zip_fp:
            os.makedirs(extract_to, exist_ok=True)
            zip_fp.extractall(extract_to)
        if os.path.exists(self.cfg['dolphin_path'] + "/RetroRewind6/"):
            shutil.rmtree(self.cfg['dolphin_path'] + "/RetroRewind6/")
        shutil.move(extract_to + "/RetroRewind6/", self.cfg['dolphin_path'] + "/RetroRewind6/")
        if os.path.exists(self.cfg['dolphin_path'] + "/riivolution/RetroRewind6.xml"):
            os.remove(self.cfg['dolphin_path'] + "/riivolution/RetroRewind6.xml")
        os.makedirs(self.cfg['dolphin_path'] + "/riivolution/", exist_ok=True)
        shutil.move(extract_to + "/riivolution/RetroRewind6.xml", self.cfg['dolphin_path'] + "/riivolution/RetroRewind6.xml")

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
        for root, dirs, files in os.walk(extract_to + "/RetroRewind6/"):
            rel_path = os.path.relpath(root, extract_to)
            dest_dir = os.path.join(self.cfg['dolphin_path'], rel_path)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            for file in files:
                shutil.copy2(os.path.join(root, file), os.path.join(dest_dir, file))
        if os.path.exists(extract_to + "/riivolution/RetroRewind6.xml"):
            shutil.move(extract_to + "/riivolution/RetroRewind6.xml", self.cfg['dolphin_path'] + "/riivolution/RetroRewind6.xml")
        with open(self.cfg['dolphin_path'] + '/RetroRewind6/version.txt', 'w') as fp:
            return fp.write(self.latest['version'])

if __name__ == "__main__":
    from config import *

    CONFIG_FILE_PATH = "./config.json"
    config = load_config(CONFIG_FILE_PATH)
    rr_handler = RetroRewind(config)
    print("do you need to update?")
    if rr_handler.needUpdate():
        print("Yes Updating.....")
        rr_handler.update()
    else:
        print("No Installing / Reinstalling.....")
        rr_handler.install()

    print("here")
