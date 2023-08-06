import sys
import os
import time
import requests
import zipfile
import json
from ttauto_crawler import utils
from ttauto_crawler import binary
from ttauto_crawler import textUtils
from ttauto_crawler import txt2proj
import logging
import urllib3
import datetime
import shutil
import subprocess
import random
from urllib.parse import *
from PIL import Image
from fake_useragent import UserAgent
import uuid
import calendar
import hashlib
import mutagen
import math

def mergeWithConfig(configPath):
    with open(configPath, 'r') as f:
        data = json.load(f)
    inputDir = data["videoDir"]
    durationFactor = data["videoDurationFactor"]
    durationVolume = data["videoVolume"]
    if len(inputDir) != len(durationFactor) or len(inputDir) != len(durationVolume):
        print('videoDir != videoDurationFactor')
        return
    musicDir = data["music"]
    outputCount = data["outputCount"]
    output = data["output"]
    if os.path.exists(output):
        shutil.rmtree(output)
    os.makedirs(output)

    allTemplate = []
    for i in range(outputCount):
        layers = []
        music = []
        allDuration = 0
        w = 0
        h = 0
        for idx in range(len(inputDir)):
            duration = random.random() * (durationFactor[idx][1] - durationFactor[idx][0]) + durationFactor[idx][0]
            files_idx = os.listdir(inputDir[idx])
            random_file = os.path.join(inputDir[idx], files_idx[random.randint(0, len(files_idx)-1)])
            name = random_file[0:random_file.index(".")].lower()
            ext = random_file[random_file.index("."):].lower()
            if ext in [".jpg",".png",".jpeg"]:
                trace_duration = duration
                for imgidx in range(math.ceil(duration)):
                    ddd = 1
                    if trace_duration < 1:
                        ddd = trace_duration
                    layers.append({
                        "res":os.path.join(inputDir[idx], files_idx[random.randint(0, len(files_idx)-1)]),
                        "type":"image",
                        "duration":ddd,
                        "positionType":"relative",
                        "positionX":0,
                        "positionY":0
                    })
                    if w <=0 or h <=0:
                        img = Image.open(random_file)
                        w = img.width
                        h = img.height
                    trace_duration -=1
            else:
                layers.append({
                    "res":random_file,
                    "type":"video",
                    "duration":duration,
                    "positionType":"relative",
                    "positionX":0,
                    "positionY":0,
                    "params": { "volume": durationVolume[idx] }
                })
                if w <=0 or h <=0:
                    w1,h1,bitrate,fps,video_duration = utils.videoInfo(random_file)
                    w = w1
                    h = h1
            allDuration += duration
            
        musicFiles = os.listdir(musicDir)
        music.append({
            "res":os.path.join(musicDir, musicFiles[random.randint(0, len(musicFiles)-1)]),
            "type":"audio",
            "startTime":0,
            "duration":allDuration,
            "params": { "volume": 1 }
            })
        config = {
            "width": int(w),
            "height": int(h),
            "layer": [
                layers,
                music
            ]
        }
        templateDir = txt2proj.genTemplate(config)
        allTemplate.append(templateDir)
    
    idx = 0
    outDir = output

    templateData = []
    for tp in allTemplate:
        templateData.append({
                "input":[],
                "template": tp,
                "params":{},
                "output": os.path.join(outDir, f"out_{idx}.mp4")})
        idx+=1
    templateDataFile = os.path.join(output, "params.config")
    with open(templateDataFile, 'w') as f:
        json.dump(templateData, f)
    try:
        print(f"template --input {templateDataFile}")
        result = subprocess.run(f"template --input {templateDataFile}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        if result.returncode == 0:
            logging.info(result.stdout.decode(encoding="utf8", errors="ignore"))
            print("=== process success") 
            for tp in allTemplate:
                shutil.rmtree(tp)
            os.remove(templateDataFile)
        else:
            print("====================== script error ======================")
            print(result.stderr.decode(encoding="utf8", errors="ignore"))
            print("======================     end      ======================")
    except subprocess.CalledProcessError as e:
        print("====================== process error ======================")
        print(e)
        print("======================      end      ======================")