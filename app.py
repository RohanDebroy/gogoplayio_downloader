from pySmartDL import SmartDL
import requests

# download video
url = "https://vidstreamingcdn.com/cdn33/e91fb74f3f6a7033f024be131aaae542/EP.20.v1.1644590642.720p.mp4?mac=NURuFV7O0%2BRrQtsg3voSTEyscilgaXdFmRd42VdpHQI%3D&vip=117.205.178.116&expiry=1644599859685"
url = "https://vidstreamingcdn.com/cdn33/e91fb74f3f6a7033f024be131aaae542/EP.20.v1.1644590642.1080p.mp4?mac=HDK0fnjBI8XZaOkBNG%2BVQ16e%2F1K0%2F1LMLyTNK9S4ocU%3D&vip=206.189.205.251&expiry=1644602295253"

obj = SmartDL(url, dest="downloads")
obj.start()


# Fetch the json
url = "https://gogoplay.io/encrypt-ajax.php?id=r+mV06RiLSP0lwrA1tRa/Q==&time=98714738999384908221"

headers = {
    "x-requested-with": "XMLHttpRequest"
}

resp = requests.get(url, headers=headers)

print(resp.status_code)
