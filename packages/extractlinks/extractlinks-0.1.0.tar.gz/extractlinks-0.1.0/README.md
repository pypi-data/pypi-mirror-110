# extractlinks
extract and repair links from Requests objects, including redirects and final landing page

### Installation
```
pip install extractlinks
python3 -m pip install extractlinks
```

### Usage
```
import requests
from extractlinks import ExtractLinks
URL = "http://cnn.com/"
r = requests.get(URL, allow_redirects=True)
e = ExtractLinks(content=r)
print(e.json)
```

### Example Output
```
[
	{
		"@timestamp": "2021-06-26T16:33:20.384Z",
		"url": {
			"full": "https://www.cnn.com/",
			"original": "https://www.cnn.com/",
			"scheme": "https",
			"domain": "www.cnn.com",
			"path": "/"
		},
		"http": {
			"response": {
			"status_code": 200,
			"status_code_reason": "OK",
			"body_bytes": 1110460
		},
		"chainitem": 2,
		"pguid": "1ff26fce-21a0-401a-9d53-1f863c6e3e31",
		"guid": "59dcfa56-b6d2-4924-bae1-70dbcd9d8309"
		"count": 324,
		"types": [
			"a-href",
			"form-action",
			"link-href",
			"meta-content",
			"script-src"
		],
		"tags": [
			"script",
			"meta",
			"a",
			"form",
			"link"
		],
		"attributes": [
			"action",
			"content",
			"src",
			"href"
		],
		"links": [
			"https://www.cnn.com/specials/cnn-investigates",
			"https://www.cnn.com/specials/tech/innovate",
			"https://www.cnn.com/travel/news",
			"https://www.i.cdn.cnn.com/.a/fonts/cnn/3.9.0/cnnsans-italic.woff2"
		...
```

### Objects
```
# primary list-of-dictionaries / JSON dump
# these contain the full link extractions, including items not recognized as URLs or mobile links
output # list of dictionaries
json # JSON string

# lists
links_all # this only contains full links and any relative links "repaired" back to full-link format (ex. /images becomes https://www.cnn.com/images
types_all # ex. "a-href", "img-src", etc
tags_all # ex. "a", "img"
attributes_all # ex. "href", "src"

# generators, if urlbreakdown module is installed; runs URLBreakdown on every link in links_all
urlbreakdown_generator_dict()
urlbreakdown_generator_json()
```

### Notes
- select URL and HTTP output fields align to the Elastic Common Schema
- links_count is not reflective of a unique count, and includes all objects identified including non-URLs in otherwise link-related tag attributes
