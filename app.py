import re
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import os
from pySmartDL import SmartDL
import json
import cloudscraper

id_encrypt_key = b"93106165734640459728346589106791"
iv = b"8244002440089157"
video_response_decryption_key = b"97952160493714852094564712118349"
scraper = cloudscraper.create_scraper()


def extract_id(url: str) -> str:
    with scraper.get(url) as response:
        pattern = r"streaming\.php\?id=([\w]+)"
        a = re.search(pattern, str(response.text))
        return a.groups()[0]


def generate_hashed_url(video_id: str) -> str:
    aes = AES.new(id_encrypt_key, AES.MODE_CBC, iv)
    hashed_id = aes.encrypt(pad(video_id.encode(), 16))
    encoded_hashed_id = base64.b64encode(hashed_id).decode()
    return f'https://goload.pro/encrypt-ajax.php?id={encoded_hashed_id}&alias={video_id}'


def decrypt_response(encrypted_data) -> dict:
    def unpad(s): return s[:-ord(s[len(s) - 1:])]
    aes = AES.new(video_response_decryption_key, AES.MODE_CBC, iv)
    decrypted = unpad(aes.decrypt(base64.b64decode(encrypted_data))).decode()
    return json.loads(decrypted)['source']


def get_download_url(data_url: str) -> list:
    headers = {
        "x-requested-with": "XMLHttpRequest"
    }
    with requests.get(data_url, headers=headers) as response:
        response.raise_for_status()

    return decrypt_response(response.json()["data"])


def get_best_source(sources: list) -> dict:
    source_ord = ["1080 P", "720 P", "480 P", "360 P", "hls P", "Auto"]
    # source_ord = ["720 P", "480 P", "360 P", "Auto"]
    source_data = {}

    for source in sources:
        source_data[source['label']] = source

    for ord in source_ord:
        if ord in source_data.keys():
            return source_data[ord]

    return


def download_m3u8(url, filename, dest,  cli="utils\m3u8dl_cli.exe"):
    COMMAND = f'{cli} "{url}" --enableDelAfterDone --saveName "{filename}" --retryCount "3" --workDir "{dest}"'
    print(COMMAND)
    os.system(COMMAND)


def download_file(url, filename, dest):
    if not os.path.isdir(dest):
        print(f"[Downloader] Creating Folder {dest}")
        os.makedirs(dest)

    if "m3u8" in url:
        download_m3u8(url, filename, dest)
        return

    request_args = {
        "headers": {
            "referer": "https://gogoplay4.com/streaming.php"
        }
    }

    print(f"[Downloader] Download started {filename}")
    obj = SmartDL(url, dest=f"{dest}/{filename}", request_args=request_args)
    obj.start()
    print(f"[Downloader] Download completed {filename}")


def extract_download(url, filename="", dest="downloads"):
    video_id = extract_id(url)
    # print("video_id", video_id)
    data_url = generate_hashed_url(video_id)
    # print("data_url", data_url)
    video_source = get_download_url(data_url)
    # print("video_source", video_source)
    download_source = get_best_source(video_source)
    # print("download_source", download_source)
    download_file(
        download_source['file'], f"{filename}.{download_source['type']}", dest=dest)


def main():
    print("Example Full URl: https://gogoplay.io/videos/shaonian-ge-xing-feng-hua-xue-yue-pian-episode-20")
    print("Example Base URl: https://gogoplay.io/videos/shaonian-ge-xing-feng-hua-xue-yue-pian-episode-\n\n")
    base_url = str(input("Enter the base url : "))
    start_episode = input(
        "Enter Starting Episode No (press enter to start from episode 1): ")
    total_episode = int(input("Enter Last episodes No: "))
    series_name = str(input("Enter the name of the series: "))

    if start_episode:
        start_episode = int(start_episode)
    else:
        start_episode = 1

    for i in range(start_episode, total_episode + 1):
        extract_download(f'{base_url}{i}', filename=i,
                         dest=f"downloads/{series_name}")


if __name__ == "__main__":
    main()
