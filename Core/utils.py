import time
import platform


def get_os():
    return platform.system()


def time_to_string(timestamp):
    time_string_format = '%Y-%m-%d %H:%M:%S'
    return time.strftime(time_string_format, time.localtime(timestamp))


def speed_human_readable(speed, is_speed=True):
    if speed >= 1024 * 1024 * 1024:
        text = '%.2f GB' % (speed / 1024 / 1024 / 1024)
    elif speed >= 1024 * 1024:
        text = '%.2f MB' % (speed / 1024 / 1024)
    elif speed >= 1024:
        text = '%.2f KB' % (speed / 1024)
    else:
        text = '%.2f B' % speed
    return text + '/s' if is_speed else text
