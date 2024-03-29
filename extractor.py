import re
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


def get_best_source(sources: list) -> str:
    source_ord = ["1080 P", "720 P", "480 P", "360 P", "Auto"]
    source_data = {}

    for source in sources:
        source_data[source['label']] = source

    for ord in source_ord:
        if ord in source_data.keys():
            return source_data[ord]['file']

    return


def download_file(url, filename="", dest="downloads"):
    if not os.path.isdir(dest):
        os.mkdirs(dest)

    obj = SmartDL(url, dest=f"{dest}/{filename}")
    obj.start()


def main():
    url = "https://gogoplay.io/videos/shaonian-ge-xing-feng-hua-xue-yue-pian-episode-19"
    video_id = extract_id(url)
    video_id = "MTgwNDAy"
    data_url = generate_hashed_url(video_id)
    video_source = get_download_url(data_url)
    download_url = get_best_source(video_source)
    print(download_url)


if __name__ == "__main__":
    main()
