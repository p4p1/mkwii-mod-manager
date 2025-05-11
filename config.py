#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Made by papi
# Created on: Sun 11 May 2025 12:21:26 PM IST
# config.py
# Description:
# Handle the config file things

import json

DOLPHIN_ROOT     = "/userdata/saves/dolphin-emu/Load/Riivolution/"
#DOLPHIN_ROOT = "/home/p4p1/Downloads/roms/wii/"

def load_config(path):
    with open(path, 'r') as fp:
        data = json.load(fp)
    return data

def save_config(path, cfg):
    with open(path, 'w') as fp:
        json.dump(cfg, fp, indent=4)

def generate_config():
    cfg={
        'dolphin_path': DOLPHIN_ROOT,
        'menu_select': 0,
        'loading': False,
        'action_thread': None
    }
    with open("./config.json", 'w') as fp:
        json.dump(cfg, fp, indent=4)

if __name__ == "__main__":
    generate_config()
