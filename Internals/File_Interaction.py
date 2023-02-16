import os
import base64
from Utilities import constant as const


def limit_len_upload_primitive(file_path):
    if os.path.getsize(file_path) > 20990034:
        return False
    else:
        return True


def read_file_byte(file_path):
    with open(file_path, "rb") as f:
        contents = f.read()

    return contents


def write_file_byte(task_result):
    file_path = const.DOWNLOAD_FOLDER + str(task_result).split(":")[0]
    base64_content = task_result.split(":")[1]

    with open(file_path, "wb") as f:
        f.write(decode(base64_content))

    if os.path.exists(file_path):
        print("[+] " + file_path + " have been Download\n")


def encode(file_path):
    string_to_encode = read_file_byte(file_path)
    encoded_file = base64.b64encode(string_to_encode)
    return encoded_file.decode('utf-8')


def decode(file_content):
    decoded = base64.b64decode(file_content)
    return decoded
