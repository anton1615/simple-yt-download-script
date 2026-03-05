from threading import Thread
import time
import os
import requests
from datetime import datetime
import json
import csv
import re

from config import YOUTUBE_API_KEY as api_key, COOKIE_FILE

base_url = "https://www.googleapis.com/youtube/v3/"


def parseCookieFile(cookiefile):
    """Parse a cookies.txt file and return a dictionary of key value pairs
    compatible with requests."""

    cookies = {}
    with open(cookiefile, "r") as fp:
        for line in fp:
            if line != "\n" and not re.match(r"^\#", line):
                lineFields = line.strip().split("\t")
                # print(lineFields)
                cookies[lineFields[5]] = lineFields[6]
    return cookies


cookies = parseCookieFile(COOKIE_FILE)


def get_html_to_json(path):
    api_url = f"{base_url}{path}&key={api_key}"
    r = requests.get(api_url, cookies=cookies)
    if r.status_code == requests.codes.ok:
        data = r.json()
    else:
        data = None
    return data


def get_video(video_id, part="snippet,statistics"):
    path = f"videos?part={part}&id={video_id}"
    data = get_html_to_json(path)
    if not data:
        return {}
    data_item = data["items"][0]
    # print(data_item)

    try:
        time_ = datetime.strptime(
            data_item["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%SZ"
        )
    except ValueError:
        time_ = None

    url_ = f"https://www.youtube.com/watch?v={data_item['id']}"

    info = {
        "id": data_item["id"],
        "channel_id": data_item["snippet"]["channelId"],
        "channelTitle": data_item["snippet"]["channelTitle"],
        "publishedAt": time_,
        "video_url": url_,
        "title": data_item["snippet"]["title"],
        "description": data_item["snippet"]["description"],
    }
    return info


print("Input Youtube livestream URL: ")
url = input()

video_id = url.split("&")[0].split("=")[-1].split("/")[-1]
video_info = get_video(video_id)
date = datetime.strftime(video_info["publishedAt"], "%Y%m%d")
title = video_info["title"]
# print(video_info['id'])
# print(video_info['channelTitle'])

filename_txt = date + "[" + video_id + "].txt"
filename_csv = date + "[" + video_id + "].csv"
filename_json = date + "[" + video_id + "].json"

title = (
    title.replace("\\", chr(65340))
    .replace("/", chr(65295))
    .replace(":", chr(65306))
    .replace("*", chr(65290))
    .replace("?", chr(65311))
    .replace('"', chr(65282))
    .replace("<", chr(65308))
    .replace(">", chr(65310))
    .replace("|", chr(65372))
)
# print(title)
os.makedirs(date + " " + title)
time.sleep(1)
os.chdir(date + " " + title)
time.sleep(1)
os.system("yt-dlp.exe --cookies-from-browser edge -F " + url)
print("Input video/audio format (-f ___): ")
format = input()
os.system("yt-dlp.exe --cookies-from-browser edge -f " + format + " " + url)
