import re
import os
import sys
import platform
import search_me
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    requires = f.read()

setup(
    name='search-me',
    version=search_me.__version__,
    packages=['search_me'],
    url='https://is.gd/search_me',
    license=search_me.__license__,
    author=search_me.__author__,
    author_email=search_me.__email__,
    description="Search in Google, Searx, Rambler. Explore VK, Facebook, Telegram, Twitter, TikTok, Snapchat, Instagram, Tumblr, YouTube.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requires.split("\n")[:-1],
    python_requires='>=3.7',
    zip_safe=False,
    keywords=(['google', 'searx', 'rambler', 'search', 'web search', 'web scraper', 'vk', 'telegram', 'instagram', 'youtube', 'twitter', 'facebook', 'tumblr', 'snapchat', 'tik tok', 'tiktok', 'socials', 'downloader', 'parser', 'scraper', 'pdf report', 'pdf parse', 'text summary']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet',
        'Topic :: Sociology',
        'Topic :: Software Development'
    ]
)
