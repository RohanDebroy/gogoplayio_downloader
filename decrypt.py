from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64

video_id = "MTgwNDAy"
key = b"25746538592938396764662879833288"
randomNumber = b"9900686387599576"

aes = AES.new(key, AES.MODE_CBC, randomNumber)
hashed_id = aes.encrypt(pad(video_id.encode(), 16))
encoded_hashed_id = base64.b64encode(hashed_id).decode()
