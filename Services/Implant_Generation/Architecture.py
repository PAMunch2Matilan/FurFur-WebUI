from colorama import Fore

windows_archs = ["win-x64", "win-x86",
                 "win-arm", "win-arm64", "win7-x64",
                 "win7-x86", "win81-x64",
                 "win81-x86", "win81-arm",
                 "win10-x64", "win10-x86",
                 "win10-arm", "win10-arm64"]

linux_archs = ["linux-x64", "linux-musl-x64",
               "linux-arm", "linux-arm64",
               "rhel-x64", "rhel.6-x64",
               "tizen", "tizen.4.0.0",
               "win81-arm", "tizen.5.0.0"]


def select_windows_arch():
    print("\n[SELECT WINDOWS ARCHITECTURE]")
    count = 0
    for arch in windows_archs:
        print(Fore.LIGHTCYAN_EX + "[%s] " % count + Fore.LIGHTWHITE_EX + "%s" % arch)
        count = count + 1

    select = int(input("\nSelection: "))
    selected = windows_archs[select]

    return selected


def select_linux_arch():
    print("\n[SELECT LINUX ARCHITECTURE]")
    count = 0
    for arch in linux_archs:
        print(Fore.LIGHTCYAN_EX + "[%s] " % count + Fore.LIGHTWHITE_EX + "%s" % arch)
        count = count + 1

    select = int(input("\nSelection: "))
    selected = linux_archs[select]

    return selected
