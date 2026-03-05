import os
import requests
from datetime import datetime
import subprocess
import time
from random import randint
from threading import Thread

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

from config import YOUTUBE_API_KEY as api_key

headers = requests.utils.default_headers()

base_url = "https://www.googleapis.com/youtube/v3/"
# youtube_channel_id = "UCAWSyEs_Io8MtpY3m-zqILA"


def get_html_to_json(path):
    random_agent = USER_AGENTS[randint(0, len(USER_AGENTS) - 1)]
    headers.update(
        {
            "User-Agent": random_agent,
        }
    )

    api_url = f"{base_url}{path}&key={api_key}"
    r = requests.get(api_url, headers=headers)
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
        "chat_downloader --message_group all -o "
        + date
        + "["
        + video_id
        + "].txt "
        + url
    )


def chatdownloader_csv_td(date, video_id, url):
    os.system(
        "chat_downloader --message_group all --quiet -o "
        + date
        + "["
        + video_id
        + "].csv "
        + url
    )


def chatdownloader_json_td(date, video_id, url):
    os.system(
        "chat_downloader --message_group superchat -o "
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
