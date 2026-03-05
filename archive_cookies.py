from threading import Thread
import time
import os
import requests
from datetime import datetime, timedelta
import json
import csv
import re


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


from config import YOUTUBE_API_KEY as api_key, COOKIE_FILE

cookies = parseCookieFile(COOKIE_FILE)

base_url = "https://www.googleapis.com/youtube/v3/"


def get_html_to_json(path):
    api_url = f"{base_url}{path}&key={api_key}"
    r = requests.get(api_url, cookies=cookies)
    if r.status_code == requests.codes.ok:
        data = r.json()
    else:
        data = None
    return data


def get_video(video_id, part="snippet,statistics,liveStreamingDetails"):
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
    try:
        if "scheduledStartTime" in data_item["liveStreamingDetails"]:
            time_schedule_ = datetime.strptime(
                data_item["liveStreamingDetails"]["scheduledStartTime"],
                "%Y-%m-%dT%H:%M:%SZ",
            )
        else:
            time_schedule_ = None
    except ValueError:
        time_schedule_ = None

    url_ = f"https://www.youtube.com/watch?v={data_item['id']}"

    info = {
        "id": data_item["id"],
        "channel_id": data_item["snippet"]["channelId"],
        "channelTitle": data_item["snippet"]["channelTitle"],
        "publishedAt": time_,
        "video_url": url_,
        "title": data_item["snippet"]["title"],
        "description": data_item["snippet"]["description"],
        "scheduledStartTime": time_schedule_,
    }
    return info


print("Input Youtube livestream URL: ")
url = input()

video_id = url.split("&")[0].split("=")[-1].split("/")[-1]
url = "https://www.youtube.com/watch?v=" + video_id
video_info = get_video(video_id)
if video_info["scheduledStartTime"] == None:
    date = datetime.strftime(video_info["publishedAt"] + timedelta(hours=8), "%Y%m%d")

else:
    date = datetime.strftime(
        video_info["scheduledStartTime"] + timedelta(hours=8), "%Y%m%d"
    )

# print(video_info['scheduledStartTime']+timedelta(hours=8))
# print(date)
title = video_info["title"]
# print(video_info['id'])
# print(video_info['channelTitle'])

filename_txt = date + "[" + video_id + "].txt"
filename_csv = date + "[" + video_id + "].csv"
filename_json = date + "[" + video_id + "].json"


def ytdlp_td():
    os.system(
        "yt-dlp.exe --cookies-from-browser edge --skip-download --wait-for-video 15 "
        + url
    )


def ytarchive_td():
    os.system("ytarchive.exe --cookies ../cookies.txt --wait " + url + " best")


def chatdownloader_txt_td(date, video_id, url):
    os.system(
        "chat_downloader --cookies ../cookies.txt --quiet --message_group all -o "
        + date
        + "["
        + video_id
        + "].txt "
        + url
    )


def chatdownloader_csv_td(date, video_id, url):
    os.system(
        "chat_downloader --cookies ../cookies.txt --quiet  --message_group all --quiet -o "
        + date
        + "["
        + video_id
        + "].csv "
        + url
    )


def chatdownloader_json_td(date, video_id, url):
    os.system(
        "chat_downloader --cookies ../cookies.txt  --message_group superchat -o "
        + date
        + "["
        + video_id
        + "].json "
        + url
    )


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
os.chdir(date + " " + title)


td0 = Thread(target=ytdlp_td)
td1 = Thread(target=ytarchive_td)
td2 = Thread(
    target=chatdownloader_txt_td, args=[date, video_id, video_info["video_url"]]
)
td3 = Thread(
    target=chatdownloader_csv_td, args=[date, video_id, video_info["video_url"]]
)
td4 = Thread(
    target=chatdownloader_json_td, args=[date, video_id, video_info["video_url"]]
)

td0.start()
time.sleep(1)
td1.start()
time.sleep(1)
td2.start()
time.sleep(1)
td3.start()
time.sleep(1)
td4.start()

td0.join()
td1.join()
td2.join()
td3.join()
td4.join()

# flag_is_madoka = video_info['channel_id'] == 'UCBhhDcVyOAhmUERi1PsQ4Rw'
flag_is_hachi = video_info["channel_id"] == "UC7XCjKxBEct0uAukpQXNFPw"
# flag_is_sola = video_info['channel_id'] == 'UC23wZiGcf1ZlmTRZDfkagew'

# if(flag_is_madoka):
# os.system('copy ' + filename_json + ' ..\\00_madoka_sc')
if flag_is_hachi:
    os.system("copy " + filename_json + " ..\\00_hachi_sc")
# if(flag_is_sola):
# os.system('copy ' + filename_json + ' ..\\00_sola_sc')
