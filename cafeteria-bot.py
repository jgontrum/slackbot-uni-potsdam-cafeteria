# -*- coding: utf-8 -*-
import requests
import pytranslate
import urllib
from bs4 import BeautifulSoup
import sys

url_golm = "http://www.studentenwerk-potsdam.de/mensa-golm.html"
url_gsee = "http://www.studentenwerk-potsdam.de/de/mensa-griebnitzsee.html"

# if you register a bot at the Slack API, you get a 'secret' URL to send
# the POST requests to. The name of the bot, the channel and the icon
# can be configured directly in Slack and will be used for every
# post that is send to the URL.
url_post = "https://hooks.slack.com/services/X/Y/Z" 

def clean(text):
	""" 
	Remove stuff that could be in the text.
	"""
	new = text.replace("\r", "")
	new = new.replace("\t", "")
	new = new.replace("\n", "")
	new = new.replace("- ", "-")
	return new

def create_menu_text(list_of_items):
	"""
	Create the actual text of a post. 
	list_of_items: list of the menu item texts. 
	"""
	ret = ""
	for item in list_of_items:
		item = clean(item)
		ret += item + "\n"
		ret += "_" + pytranslate.translate(item, sl='german', tl='english').replace(", ","") + "_\n"
		ret += "\n"
	return ret[:-2] # ignore last newline

def check_page(url):
	page = BeautifulSoup(urllib.urlopen(url).read(), "html.parser")
	items = []
	try:
		# get all four menu options
		items.append(page.find("td", attrs={"class": "text1"}).get_text().strip())
		items.append(page.find("td", attrs={"class": "text2"}).get_text().strip())
		items.append(page.find("td", attrs={"class": "text3"}).get_text().strip())
		items.append(page.find("td", attrs={"class": "text4"}).get_text().strip())
	except Exception, e:
		return []
	return items

def post(location, items):
	if len(items) > 0:
		# post everything!
		entry = "*Menu for " + location + "*\n" + create_menu_text(items)
		requests.post(url_post, json={"text": entry, "mrkdwn": True})
		return True
	return False

if post("Golm", check_page(url_golm)) and post("Griebnitzsee", check_page(url_gsee)):
    sys.exit(0)
sys.exit(-1)
