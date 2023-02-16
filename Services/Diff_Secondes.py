from datetime import datetime


def secdiff(arg1, arg2):
    a = datetime.strptime(arg1, '%Y-%m-%d %H:%M:%S')
    b = datetime.strptime(arg2, '%Y-%m-%d %H:%M:%S')

    diff = (a - b).total_seconds()

    if diff < 5:
        return True

    else:
        return False
