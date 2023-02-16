from colorama import Fore


def error_message(message):
    print("<p>[!] " + str(message) + "</p>")


def error_exception(message, error):
    print("<p>[!] " + str(message), error, "</p>")


def success_message(message):
    print("<p>[+] " + str(message) + "</p>")


def information_message(message):
    print("<p>[i] " + str(message) + "</p>")


def warning_message(message):
    print("<p>[/!\\] " + str(message) + "</p>")


TEAMSERVER_IP = ""
TEAMSERVER_PORT = ""

DOWNLOAD_FOLDER = "Downloads\\"
TOOLS_FOLDER = "Resources\\tools\\"