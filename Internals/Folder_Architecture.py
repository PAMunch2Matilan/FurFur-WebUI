import os
import shutil


def create_folder():
    folders = ["tmp", "Resources", "Implants", "Downloads"]

    for folder in folders:
        if os.path.exists(folder):
            pass
        else:
            os.mkdir(folder)


def delete_implant_folder():
    folders = ["Resources\\Implant"]

    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)

        else:
            pass
