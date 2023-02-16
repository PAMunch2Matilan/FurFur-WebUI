from Utilities import constant as const


def write_script():
    script = """
import json
import sys
import time

import requests

implant_name = []


def get_implant_id():
    implant_id_list = []
    url = "http://%s:%s/Implants"
    req = requests.get(url)
    content = req.text

    json_obj = json.loads(content)

    flag = 0
    while flag != len(json_obj):
        implant_id_list.append(json_obj[flag]["metadata"]["id"])
        implant_name.append(json_obj[flag]["metadata"]["username"])

        flag = flag + 1

    return implant_id_list


def search_new_implant(count_implant, path):
    root_path = path

    time.sleep(2)
    if count_implant < len(get_implant_id()):

        print("New implant :" + implant_name[-1] + " connected")

        if sys.getwindowsversion().build > 20000:
            from win11toast import toast
            toast("FurFur", "New Implant: " + implant_name[-1] + " Connected",
                  root_path + "\\Resources\\ico\\ImplantIcon2.ico", audio='ms-winsoundevent:Notification.SMS')

        else:
            from win10toast import ToastNotifier
            w10_toast = ToastNotifier()

            w10_toast.show_toast(
                "Notification",
                "New implant :" + implant_name[-1] + " connected",
                duration=20,
                icon_path=root_path + "\\Resources\\ico\\ImplantIcon2.ico",
                threaded=True,
            )

        count_implant = len(get_implant_id())

    else:
        pass

    search_new_implant(count_implant, path)


if __name__ == '__main__':
    if len(sys.argv[1]) < 0:
        print("Error : check args false")

    else:
        path = sys.argv[1]
        count_implant = 0
        search_new_implant(count_implant, path)
""" % (const.TEAMSERVER_IP, const.TEAMSERVER_PORT)
    file = open("Resources\\Implant_Connection_Detection.py", "w+")
    file.writelines(script)
    file.close()

