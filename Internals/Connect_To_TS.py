from Utilities import constant as const
import requests


def test_ts_connexion():
    try:
        req = requests.get("http://" + const.TEAMSERVER_IP + ":" + const.TEAMSERVER_PORT + "/listeners")

        if req.status_code == 200:
            const.success_message("TeamServer Is Online\n")
            status = True

        else:
            const.warning_message("TeamServer Is Not Online\n")
            status = False

        return status

    except:
        const.warning_message("TeamServer Is Not Online\n")


def save_ts_configuration(local_ip, local_port):
    const.TEAMSERVER_IP = local_ip
    const.TEAMSERVER_PORT = local_port


def set_ts_configuration():
    const.information_message("Enter TeamServer configuration")
    local_ip = input("\t[ TeamServer IP ] : ")
    local_port = input("\t[ TeamServer PORT ] : ")

    save_ts_configuration(local_ip, local_port)
    test_ts_connexion()