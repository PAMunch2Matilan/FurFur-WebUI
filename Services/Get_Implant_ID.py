import json
from Utilities import constant as const
import requests

implant_id_list = []


def get_implant_id(id_tested):
    url = "http://%s:%s/Implants" % (const.TEAMSERVER_IP, const.TEAMSERVER_PORT)
    req = requests.get(url)
    content = req.text

    json_obj = json.loads(content)

    flag = 0

    while flag != len(json_obj):
        implant_id_list.append(json_obj[flag]["metadata"]["id"])
        flag = flag + 1

    for id in implant_id_list:
        if id == id_tested:
            return True
        else:
            pass


def real_get_implant_id():
    implant_id_list = []
    url = "http://%s:%s/Implants" % (const.TEAMSERVER_IP, const.TEAMSERVER_PORT)
    req = requests.get(url)

    content = req.text

    json_obj = json.loads(content)

    flag = 0
    while flag != len(json_obj):
        implant_id_list.append(json_obj[flag]["metadata"]["id"])

        flag = flag + 1

    return implant_id_list
