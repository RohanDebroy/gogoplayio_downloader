import re
from tracemalloc import start
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import os
from pySmartDL import SmartDL


def extract_id(url: str) -> str:
    with requests.get(url) as response:
        pattern = r"streaming\.php\?id=([\w]+)"
        a = re.search(pattern, str(response.text))
        return a.groups()[0]


def generate_hashed_url(video_id: str) -> str:
    key = b"25746538592938396764662879833288"
    random_number = b"9900686387599576"

    aes = AES.new(key, AES.MODE_CBC, random_number)
    hashed_id = aes.encrypt(pad(video_id.encode(), 16))
    encoded_hashed_id = base64.b64encode(hashed_id).decode()
    return f'https://gogoplay.io/encrypt-ajax.php?id={encoded_hashed_id}&time=45{random_number.decode()}67'


def get_download_url(data_url: str) -> list:
    headers = {
        "x-requested-with": "XMLHttpRequest"
    }
    with requests.get(data_url, headers=headers) as response:
        response.raise_for_status()
        return response.json()['source']


def get_best_source(sources: list) -> dict:
    source_ord = ["1080 P", "720 P", "480 P", "360 P", "Auto"]
    # source_ord = ["720 P", "480 P", "360 P", "Auto"]
    source_data = {}

    for source in sources:
        source_data[source['label']] = source

    for ord in source_ord:
        if ord in source_data.keys():
            return source_data[ord]

    return


def download_file(url, filename, dest):
    if not os.path.isdir(dest):
        print(f"[Downloader] Creating Folder {dest}")
        os.makedirs(dest)

    request_args = {
        "headers": {
            "referer": "https://gogoplay.io/streaming.php"
        }
    }

    print(f"[Downloader] Download started {filename}")
    obj = SmartDL(url, dest=f"{dest}/{filename}", request_args=request_args)
    obj.start()
    print(f"[Downloader] Download completed {filename}")


def extract_download(url, filename="", dest="downloads"):
    video_id = extract_id(url)
    print("video_id", video_id)
    data_url = generate_hashed_url(video_id)
    print("data_url", data_url)
    video_source = get_download_url(data_url)
    print("video_source", video_source)
    download_source = get_best_source(video_source)
    print("download_source", download_source)
    download_file(
        download_source['file'], f"{filename}.{download_source['type']}", dest=dest)


def main():
    print("Example Full URl: https://gogoplay.io/videos/shaonian-ge-xing-feng-hua-xue-yue-pian-episode-20")
    print("Example Base URl: https://gogoplay.io/videos/shaonian-ge-xing-feng-hua-xue-yue-pian-episode-\n\n")
    base_url = str(input("Enter the base url : "))
    start_episode = input(
        "Enter Starting Episode No (press enter to start from episode 1): ")
    total_episode = int(input("Enter Last episodes No: "))

    if start_episode:
        start_episode = int(start_episode)
    else:
        start_episode = 1

    for i in range(start_episode, total_episode + 1):
        extract_download(f'{base_url}{i}', filename=i)


if __name__ == "__main__":
    main()
