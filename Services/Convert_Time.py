from datetime import datetime


def convert_time(arg):
    arg2 = arg.split(".")

    return datetime.strptime(arg2[0], '%Y-%m-%dT%H:%M:%S')
