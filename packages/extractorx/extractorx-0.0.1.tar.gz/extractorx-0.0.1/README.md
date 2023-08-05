# ExtractorX API

## Installation
Via pip:
```
pip install extractorx
```

### Example Usage:
```
>>> from extractorx.api import ExtractorX
>>> with open("key.txt", "r") as f:
...     key = f.read()
>>> api = ExtractorX(key)
>>> url = "https://www.cnn.com/2023/06/09/investing/bull-market-artificial-intelligence/index.html"
>>> result = api.from_url(url)
>>> result.keys()
dict_keys(['body', 'link', 'metadata', 'title'])
>>> result.get("title")
'How can we possibly be in a bull market now? Two letters: AI | CNN Business'
>>> result.get("body")
'New York (CNN) —— The bear market is over. But the bear economy isn’t. The eurozone has sunk into recession and some economists fear the United States is next...
```