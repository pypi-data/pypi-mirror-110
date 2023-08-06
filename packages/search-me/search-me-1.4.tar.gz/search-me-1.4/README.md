[![Search Me](https://is.gd/search_me_logo__)](https://is.gd/_pypi)

# Search Me

Search in: **Google**, **Searx**, **Rambler**. Extract data from: **VK, Facebook, Telegram, Twitter, TikTok, Snapchat, Instagram, Tumblr, YouTube**.

[![Version](https://img.shields.io/pypi/v/search-me.svg?style=flat-square&logo=appveyor)](https://pypi.org/project/search-me)
[![License](https://img.shields.io/pypi/l/search-me.svg?style=flat-square&logo=appveyor)](https://pypi.org/project/search-me)
[![Python](https://img.shields.io/pypi/pyversions/search-me.svg?style=flat-square&logo=appveyor)](https://pypi.org/project/search-me)
[![Status](https://img.shields.io/pypi/status/search-me.svg?style=flat-square&logo=appveyor)](https://pypi.org/project/search-me)
[![Downloads](https://static.pepy.tech/personalized-badge/search-me?period=total&units=international_system&left_color=black&right_color=blue&left_text=Downloads)](https://pepy.tech/project/search-me)

## PRE-INSTALLING

- If you want to generate PDF documents (param *pdf_report*), setup [wkhtmltopdf](https://is.gd/html2pdf)
- If you want to download video from youtube (param *socials*), setup [youtube-dl](https://is.gd/youtube_dl)

## INSTALLING

```bash
pip install search-me
```

## USAGE

### Imports

```python
from search_me import Google, Searx, Rambler
```

### Init search engine

```python
engine = Google()
engine = Searx()
engine = Rambler()
```

Parameters:

- *results*: Number of search results on page (*default: 10*)
- *retry*: Number of retries for one query (*default: 10*)
- *show_results*: Show results in table (*default: True*)
- *cache*: Caching searched data after each search query in json file (*default: True*)
- *sleep_min*: Minimum time in seconds to sleep after each query (*default: 0.0*)
- *sleep_max*: Maximum time in seconds to sleep after each query (*default: 1.5*)
- *pdf_report*: Export searched data to pdf-documents (*default: False*)
- *pdf_timeout*: Waiting time in seconds for create pdf-document (*default: 30*)
- *pdf_threads*: Number of threads for generating pdf-documents (*default: multiprocessing.cpu_count()*)
- *pdf_parse*: Parse generated pdf-documents; used, when *pdf_report=True* (*default: False*)
- *pdf_options*: Used, when *pdf_parse=True* (*default: {"text": True, "summary": True, "summary_params": ("ratio", 0.15), "urls": True, "keywords": True}*)
	- *text*: Extract text
	- *summary*: Generate summary from extracted text
	- *summary_params*: Tuple, where first element - type of summarizing ("ratio" or "words"); the second element - value (percent of text or count of words)
	- *urls*: Extract urls
	- *keywords*: Generate keywords from extracted text
- *use_social_search*: Use search across socials (*default: False*)
- *socials*: Tuple with names of social nets (*default: ("vk", "instagram", "telegram", "twitter", "youtube", "facebook", "tumblr", "snapchat", "tiktok")*)
- *social_threads*: Number of threads for social search (*default: multiprocessing.cpu_count()*)
- *social_options*: Used, when *use_social_search=True* (*default: {"posts_limit": 10, "export_data": True, "export_format": "csv", "download_media": True}*)
	- *posts_limit*: Number of posts for VK, Facebook, Telegram, Twitter, Youtube, Snapchat
	- *export_data*: Export data about posts in file
	- *export_format*: Export file format (csv, xls, html, json)
	- *download_media*: Download media from Instagram, Tumblr, Youtube, Snapchat


### Start search

```python
engine.search(items=["query 1", "query 2"])
```

### Access result

```python
print(engine.results)
```

## EXAMPLE USAGE

```python
import logging
log = logging.getLogger().setLevel(logging.DEBUG)

from search_me import Google
g = Google(
	retry=3,
	pdf_report=True,
	pdf_timeout=10,
	cache=True,
	use_social_search=True,
	pdf_parse=True,
	socials=("vk", "telegram", "twitter", "youtube", "facebook")
	)
g.search(items=["社會信用體系", "0x0007ee", "журнал медуза"])
for search_result in g.search_results:
	print(f"Item: {search_result['item']}")
	print("Links:")
	print("\n".join(search_result['links']))
	print("Socials:")
	for social, social_v in search_result['socials'].items():
		print(f"{social} {social_v}")
	for pdf in search_result['pdf']:
		print(f"Path: {pdf['path']}\nText: {pdf['text']}\nSummary: {pdf['summary']}")
		print("Urls:")
		print("\n".join(list(pdf['urls'])))
		print("Keywords:")
		print("\n".join(list(pdf['keywords'])))
		print()
	print("=" * 40)
```

## LINKS
- [Search Language Codes](https://is.gd/lang_codes)
- [List of Google domains](https://is.gd/domains_list)

## SUPPORT

[![PayPal](https://is.gd/search_me_paypal_)](https://is.gd/mypaypal)