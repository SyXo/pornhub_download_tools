#!/usr/bin/env python
#-*- coding:utf-8 -*-
from pymongo import MongoClient as mongoclient
import requests,re,json,time,os
import logging
import sys
logger = logging.getLogger("PornHub Download App")
formatter = logging.Formatter('%(asctime)s %(levelname)-8s:%(message)s')
file_handler = logging.FileHandler("downloading.log")
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter

logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.setLevel(logging.INFO)

dbhost = 'xxx'
dbpass = 'xxx'
dbport = 'xxx'
dbuser = 'xxx'
client = mongoclient(dbhost,dbport)
client.PornHub.authenticate(dbuser,dbpass)
db = client["PornHub"]
coll = db["PhRes"]
try:
                datas = coll.find()
                for data in datas:
                    time.sleep(0.001)
                    if int(data['video_duration']) > 1200:
                            url = data['viewkey']
                            html = requests.get(url).text
                            try:
                                      _ph_info = re.findall('flashvars_.*?=(.*?);\n',html)
                                      _ph_info_json = json.loads(_ph_info[0])
                                      title = _ph_info_json.get('video_title').replace(" ","-")
                                      logger.info(title)
                                      duration = data['video_duration']
                                      logger.info(duration)
                                      media = _ph_info_json.get("mediaDefinitions")
                                      for media_list in media:
                                 	    media_quality = media_list.get("quality")
                                            if int(media_quality) == 720:
                                                 download_url = media_list.get("videoUrl")
                                                 logger.info(download_url)
                                                 '''
                                                 r = requests.get(download_url, stream=True)
						 f = open("/home/thomas/pornhub/"+title+".mp4", "wb")
						 for chunk in r.iter_content(chunk_size=512):
						  if chunk:
        					 		f.write(chunk)
                                                 '''
                                                 check_file = os.system("ls "+"/home/thomas/pornhub/"+title+".mp4")
                                                 if check_file == 0:
                                                           pass
                                                 else:
                                                 	downloading_process = os.popen("axel -n 100 -o "+"/home/thomas/pornhub/"+title+".mp4 "+download_url).read()
                                                 	logger.info(downloading_process)
                            except:
                                      pass
                    else:
                        pass
except:
                print "Error"