"""
shubhank_utility.
"""

_version_ = "0.0.3"
_author_ = 'Shubhank Singhal'
_credits_ = 'Shubhank Singhal'


import os
import re
import ast
import csv
import sys
import time
import json
import base64
import random
import pymssql
import requests
import dateutil
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
from datetime import datetime
from bs4 import BeautifulSoup
from tldextract import extract
from pymongo import MongoClient
import country_converter as coco
from dateutil.parser import parse
from urllib.parse import urlparse

from user_agent import *

import selenium
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

import logging
logging.basicConfig(level=logging.ERROR)


from shubhank_utility.database import *
from shubhank_utility.fuzzy_match import *
from shubhank_utility.pdf_download import *
from shubhank_utility.utility import *