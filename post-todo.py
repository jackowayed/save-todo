#!/usr/bin/env python3

import json
import os
import sys
from urllib.request import Request, urlopen

AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")
AIRTABLE_BASE = os.getenv("AIRTABLE_BASE")
AIRTABLE_TABLE = os.getenv("AIRTABLE_TABLE", "Todos")


def create_request(data):
    return Request(
        f"https://api.airtable.com/v0/{AIRTABLE_BASE}/{AIRTABLE_TABLE}",
        data,
        headers={"Authorization": f"Bearer {AIRTABLE_TOKEN}",
                 "Content-Type": "application/json"})


def request_repr(request):
    return (f"{request.get_method()} {request.get_full_url()}\n"
            + repr(request.header_items()))


def add_todo(name, link=None):
    post_data = json.dumps({"fields": {"Name": name}}).encode()
    request = create_request(post_data)
    print(request_repr(request))
    print(post_data)
    with urlopen(request) as response:
        print(response)
        assert response.status == 200, response


add_todo(sys.argv[1])
