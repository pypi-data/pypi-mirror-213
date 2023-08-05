#!python3
from eyes_soatra import eyes
import requests
import json
from lxml.html.clean import Cleaner
from lxml import html
from lxml import etree
import re
import pandas

result = eyes.view_page(
    url='https://www.town.omachi.lg.jp/'
)
