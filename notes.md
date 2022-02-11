# How Gogoplay.io encrypts the id

```
Sample Encrypted url
https://gogoplay.io/encrypt-ajax.php?id=VuqHMpup8jHDen7OfhJLoQ==&time=23990068638759957692

```

## Notes?

This is just notes while I was reversing the encryption algorithm

```
const CryptoJS = require('crypto-js')

const genRandomNumber = (size) => {
  let randomNum = ''
  for (let i = 0; i < size; i++) {
    randomNum += Math.floor(Math.random() * 10)
  }
  return randomNum;
}

// Scraped from the webpage
const meta_crypto =
  'M3fAsKDeCFqG5EiOHC/bb/QTzTQFD9ECnjEc7SrsNRzcxB9CPzO3g2lsbiXxSWLdB7z1oBh/YjZA2xn1R7t5s2ZsYaYXtNeLjHKkIAnrZMDagk7BEj0cYRawsXVuJHn4SQFqJ3gTNOusS/CtKhOy3lv4bFMCAaU6OB5f/2sCvpQKiTZt7U7jn00YtjKyv28iAIMR4bfI3T14rF8BaziXBEcjX2O01J2sCibJ7aR3cYusN/kuEwESk1ZgQWbM3DOtAYTcgVd8JJtpQjM9SbGBxRrvpIHw4pFXa2XF2VrQ4nx3EzMnW0shMQaxIi9rZuYdmDMXr4VayemIw56UuWci8CnONnwtaRQLuujOdxvrPpyeFBEsgajawC5DWJP65slp'
const script_ts = '6107155285081307'
const script_crypto =
  'MlhTqwrX/xQLpqlpFP9cdgXsaTpgD+6nqdHDuoJJzp/ZM1yluhY3YPcMZOkErTs0'

// Function d always return 25746538592938396764662879833288 no matter what the input is it might change in future hence I am keeping the notes
const d = CryptoJS.enc.Utf8.stringify(
  CryptoJS.AES.decrypt(
    script_crypto,
    CryptoJS.enc.Utf8.parse(script_ts + '' + script_ts),
    {
      iv: CryptoJS.enc.Utf8.parse(script_ts),
    },
  ),
)

const e = CryptoJS.AES.decrypt(meta_crypto, CryptoJS.enc.Utf8.parse(d), {
  iv: CryptoJS.enc.Utf8.parse(script_ts),
})

const f = CryptoJS.enc.Utf8.stringify(e)

//MTgwNDAy, basically the video_id
const g = f.substring(0, f.indexOf('&'))

const randomNumber = genRandomNumber(2)

const hashedId = CryptoJS.AES.encrypt(g, CryptoJS.enc.Utf8.parse(d), {
  iv: CryptoJS.enc.Utf8.parse(randomNumber),
})

const time = `12${randomNumber}34`

const final = `https://gogoplay.io/encrypt-ajax.php?id=${hashedId}&time=${time}`

console.log(final)
```
