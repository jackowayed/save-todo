#!/usr/bin/env python3

import json
import os
import subprocess
import sys
from urllib.request import Request, urlopen


def parse_bool(b):
    """
    Takes a boolean env var arg and makes it a boolean

    False:
    * not present
    * empty string
    * the word false (any case)
    * 0
    """
    if not b:
        return False
    return not (b == "0" or b.lower() == "false")


AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")
AIRTABLE_BASE = os.getenv("AIRTABLE_BASE")
AIRTABLE_TABLE = os.getenv("AIRTABLE_TABLE", "Todos")
INCLUDE_LINK = parse_bool(os.getenv("INCLUDE_CHROME_LINK"))


def create_request(data):
    return Request(
        f"https://api.airtable.com/v0/{AIRTABLE_BASE}/{AIRTABLE_TABLE}",
        data,
        headers={"Authorization": f"Bearer {AIRTABLE_TOKEN}",
                 "Content-Type": "application/json"})


def request_repr(request):
    return (f"{request.get_method()} {request.get_full_url()}\n"
            + repr(request.header_items()))


def get_chrome_tab():
    CHROME_APPLESCRIPT = """
    tell application "Google Chrome" to return URL of active tab of front window
    """
    res = subprocess.run("osascript", text=True,
                         input=CHROME_APPLESCRIPT, capture_output=True)
    if res.returncode != 0:
        print(res.stderr)
    else:
        return res.stdout.strip()


def build_data(name):
    fields = {"Name": name}
    link = None
    if INCLUDE_LINK:
        link = get_chrome_tab()
    if link:
        fields["Link"] = link
    return json.dumps({"fields": fields}).encode()


def add_todo(name):
    post_data = build_data(name)
    request = create_request(post_data)
    print(request_repr(request))
    print(post_data)
    with urlopen(request) as response:
        print(response)
        assert response.status == 200, response


add_todo(sys.argv[1])
