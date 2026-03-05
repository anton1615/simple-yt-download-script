from threading import Thread
import time
import os
import requests
from datetime import datetime
import json
import csv

from config import YOUTUBE_API_KEY as api_key

base_url = "https://www.googleapis.com/youtube/v3/"


def get_html_to_json(path):
    api_url = f"{base_url}{path}&key={api_key}"
    r = requests.get(api_url)
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


def ytdlp_td(url):
    os.system("yt-dlp.exe -f bv+ba " + url)


def chatdownloader_txt_td(filename, url):
    os.system("chat_downloader --message_group all --quiet -o " + filename + " " + url)


def chatdownloader_csv_td(filename, url):
    os.system("chat_downloader --message_group all --quiet -o " + filename + " " + url)


def chatdownloader_json_td(filename, url):
    os.system(
        "chat_downloader --message_group superchat --quiet -o " + filename + " " + url
    )


file_batch = open("download.txt", "r")
for line in file_batch.readlines():
    if line == "\n":
        continue

    url = line.rstrip("\n")
    video_id = url.split("&")[0].split("=")[-1].split("/")[-1]
    video_info = get_video(video_id)
    date = datetime.strftime(video_info["publishedAt"], "%Y%m%d")
    title = video_info["title"]

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
    os.chdir(date + " " + title)

    td0 = Thread(target=ytdlp_td, args=[url])
    td2 = Thread(target=chatdownloader_txt_td, args=[filename_txt, url])
    td3 = Thread(target=chatdownloader_csv_td, args=[filename_csv, url])
    td4 = Thread(target=chatdownloader_json_td, args=[filename_json, url])

    td0.start()
    time.sleep(1)
    td2.start()
    time.sleep(1)
    td3.start()
    time.sleep(1)
    td4.start()

    td0.join()
    td2.join()
    td3.join()
    td4.join()

    os.chdir("..\\")
