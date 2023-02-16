import json
import requests
from Utilities import constant as const


def create_listener(name, port):
    url = 'http://%s:%s/Listeners' % (const.TEAMSERVER_IP, const.TEAMSERVER_PORT)
    data = {'name': name, 'bindPort': port}

    requests.post(url, json=data)


def send_simple_task_to_implant(command, implant_id):
    url = "http://%s:%s/Implants/%s" % (const.TEAMSERVER_IP, const.TEAMSERVER_PORT, implant_id)
    data = {"command": command}

    req = requests.post(url, json=data)
    json_obj = json.loads(req.content)
    task_id = json_obj["id"]
    return task_id


def send_cmd_args_task_to_implant(command, args, implant_id):
    url = "http://%s:%s/Implants/%s" % (const.TEAMSERVER_IP, const.TEAMSERVER_PORT, implant_id)
    headers = {"Content-Type": "application/json", "accept": "*/*"}

    data = {
        "command": "%s" % command,
        "arguments": [
            "%s" % args
        ]
    }

    req = requests.post(url, json=data, headers=headers)
    json_obj = json.loads(req.content)
    return json_obj["id"]


def send_cmd_multiple_args_task_to_implant(command, args, args2, implant_id):
    url = "http://%s:%s/Implants/%s" % (const.TEAMSERVER_IP, const.TEAMSERVER_PORT, implant_id)
    headers = {"Content-Type": "application/json", "accept": "*/*"}

    data = {
        "command": "%s" % command,
        "arguments": [
            "%s" % args,
            "%s" % args2
        ]
    }

    req = requests.post(url, json=data, headers=headers)
    json_obj = json.loads(req.content)
    return json_obj["id"]


def send_cmd_three_args_task_to_implant(command, args, args2, args3, implant_id):
    url = "http://%s:%s/Implants/%s" % (const.TEAMSERVER_IP, const.TEAMSERVER_PORT, implant_id)
    headers = {"Content-Type": "application/json", "accept": "*/*"}

    data = {
        "command": "%s" % command,
        "arguments": [
            "%s" % args,
            "%s" % args2,
            "%s" % args3,
        ]
    }

    req = requests.post(url, json=data, headers=headers)
    json_obj = json.loads(req.content)
    return json_obj["id"]


def send_all_param_task_to_implant(command, args, file, implant_id):
    url = "http://%s:%s/Implants/%s" % (const.TEAMSERVER_IP, const.TEAMSERVER_PORT, implant_id)
    data = {
        "command": "%s" % command,
        "arguments": [
            "%s" % args
        ],
        "file": "%s" % file
    }

    req = requests.post(url, json=data)
    json_obj = json.loads(req.content)
    return json_obj["id"]
