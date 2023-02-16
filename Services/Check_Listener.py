import json

import requests
from Utilities import constant as const


def check_listener_duplicate(name_check):
    name_list = []

    url = "http://%s:%s/Listeners" % (const.TEAMSERVER_IP, const.TEAMSERVER_PORT)
    req = requests.get(url)
    content = req.text
    json_obj = json.loads(content)
    flag = 0
    result = False

    while flag != len(json_obj):
        name_list.append(json_obj[flag]["name"])
        flag = flag + 1

    for namelist in name_list:
        if namelist == name_check:
            result = True
        else:
            pass

    return result
