# -*- coding: utf-8 -*-
import requests
import goslate
import urllib
import sys
import datetime

gs = goslate.Goslate()

openmensa = "https://openmensa.org/api/v2"
openmensa_golm = openmensa + "/canteens/61/days/{}".format(datetime.date.today())
openmensa_gsee = openmensa + "/canteens/62/days/{}".format(datetime.date.today())

# if you register a bot at the Slack API, you get a 'secret' URL to send
# the POST requests to. The name of the bot, the channel and the icon
# can be configured directly in Slack and will be used for every
# post that is send to the URL.
url_post = "https://hooks.slack.com/services/X/Y/Z"


def create_menu_text(list_of_items):
    """
    Create the actual text of a post.
    list_of_items: list of the menu item texts.
    """
    def translate_maybe(txt, lang):
        try:
            return gs.translate(txt, lang)
        except Exception:
            return txt

    def create_str_item(item):
        return "{}: {} ({})".format(
            item.get("category").replace("Angebot ", "N°"),
            translate_maybe(item.get("name"), "en"),
            ",".join(item.get("notes"))
        )
    ret = "\n".join(map(create_str_item, list_of_items))
    return ret


def check_page(url):
    if requests.get(url).json().get("closed", False):
        return []
    else:
        return requests.get(url + "/meals").json()


def post(location, items):
    if len(items) > 0:
        # post everything!
        entry = "*Menu for " + location + "*\n" + create_menu_text(items)
        print(entry)
        # requests.post(url_post, json={"text": entry, "mrkdwn": True})
        return True
    return False


if post("Golm", check_page(openmensa_golm)) and post("Gsee", check_page(openmensa_gsee)):
    sys.exit(0)
sys.exit(-1)
