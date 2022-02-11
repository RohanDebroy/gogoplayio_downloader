import re
import requests


def extract_id(url: str) -> str:
    with requests.get(url) as response:
        pattern = r"streaming\.php\?id=([\w]+)"
        a = re.search(pattern, str(response.text))
        return a.groups()[0]


def scrape_cipher(id: str):
    pattern_meta_crypto = r'<meta name="crypto" content="([\w\d\+\/]+)">'
    pattern_script_crypto = r'data-name="crypto" data-value="([\d\w\/\+]+)">'
    pattern_script_ts = r'data-name="ts" data-value="([\d\w\/\+]+)">'

    with requests.get(f'https://gogoplay.io/streaming.php?id={id}') as response:
        pass


def main():
    url = "https://gogoplay.io/videos/shaonian-ge-xing-feng-hua-xue-yue-pian-episode-20"
    id = extract_id(url)


if __name__ == "__main__":
    main()
