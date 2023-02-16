import requests

import Utilities.constant as const


def delete_listener(name):
    url = 'http://%s:%s/Listeners/%s' % (const.TEAMSERVER_IP, const.TEAMSERVER_PORT, name)

    requests.delete(url)


def delete_implant(implant_id):
    url = "http://%s:%s/Implants/%s" % (const.TEAMSERVER_IP, const.TEAMSERVER_PORT, implant_id)
    req = requests.delete(url)
    const.success_message(req.text)
