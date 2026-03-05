import os
import requests
from datetime import datetime
import subprocess
import time
from random import randint
from threading import Thread
import json
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


def get_channel_uploads_id(channel_id, part="contentDetails"):
    path = f"channels?part={part}&id={channel_id}"
    data = get_html_to_json(path)
    try:
        uploads_id = data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    except KeyError:
        uploads_id = None
    return uploads_id


def get_playlist(playlist_id, page_token="", part="contentDetails", max_results=10):
    path = f"playlistItems?part={part}&playlistId={playlist_id}&maxResults={max_results}&pageToken={page_token}"
    data = get_html_to_json(path)
    if not data:
        return [], ""

    next_page_token = data.get("nextPageToken", "")
    video_ids = []
    for data_item in data["items"]:
        video_ids.append(data_item["contentDetails"]["videoId"])
    return video_ids, next_page_token


def get_video(video_id, part="snippet,statistics"):
    path = f"videos?part={part}&id={video_id}"
    data = get_html_to_json(path)
    if not data:
        return {}
    data_item = data["items"][0]

    try:
        time_ = datetime.strptime(
            data_item["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%SZ"
        )
    except ValueError:
        time_ = None

    url_ = f"https://www.youtube.com/watch?v={data_item['id']}"

    info = {
        "id": data_item["id"],
        "channelTitle": data_item["snippet"]["channelTitle"],
        "publishedAt": time_,
        "video_url": url_,
        "title": data_item["snippet"]["title"],
        "description": data_item["snippet"]["description"],
    }
    return info


def chatdownloader_txt_td(date, video_id, url):
    os.system(
        "chat_downloader --cookies youtube.com_cookies.txt --message_group all -o "
        + date
        + "["
        + video_id
        + "].txt "
        + url
    )


def chatdownloader_csv_td(date, video_id, url):
    os.system(
        "chat_downloader --cookies youtube.com_cookies.txt  --message_group all --quiet -o "
        + date
        + "["
        + video_id
        + "].csv "
        + url
    )


def chatdownloader_json_td(date, video_id, url):
    os.system(
        "chat_downloader --cookies youtube.com_cookies.txt  --message_group superchat -o "
        + date
        + "["
        + video_id
        + "].json "
        + url
    )


"""
f = open('download.txt', 'r')
for url_nl in f.readlines():
	url = url_nl.rstrip('\n')
	video_id = url.split('=')[1]
	video_info = get_video(video_id)
	date = datetime.strftime(video_info['publishedAt'], '%Y%m%d')
	os.system('chat_downloader --quiet --message_group superchat -o ' + date +'json ' + url)
"""

print("Input Youtube livestream URL: ")
url = input()
video_id = url.split("&")[0].split("=")[-1].split("/")[-1]

# print("----------------------")
video_info = get_video(video_id)
# print(video_info)
date = datetime.strftime(video_info["publishedAt"], "%Y%m%d")
print(date + "_" + video_id)
# chatdownloader_txt_td(date,video_id,video_info['video_url'])
# chatdownloader_csv_td(date,video_id,video_info['video_url'])
# chatdownloader_json_td(date,video_id,video_info['video_url'])

td2 = Thread(
    target=chatdownloader_txt_td, args=[date, video_id, video_info["video_url"]]
)
td3 = Thread(
    target=chatdownloader_csv_td, args=[date, video_id, video_info["video_url"]]
)
td4 = Thread(
    target=chatdownloader_json_td, args=[date, video_id, video_info["video_url"]]
)

td2.start()
time.sleep(1)
td3.start()
time.sleep(1)
td4.start()

td2.join()
td3.join()
td4.join()
