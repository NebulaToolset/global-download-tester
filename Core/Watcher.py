from Core.Exceptions import FileDownloadTimeoutException
from Core.utils import time_to_string, speed_human_readable

import sys
import time


class Watcher:
    def __init__(self, log_fp, tmp_fp):
        self.log_fp = log_fp
        self.tmp_fp = tmp_fp
        self.last_time = 0
        self.accumulate = 1
        self.accuracy = 100
        self.started_at = 0
        self.timeout = 0
        self.downloader = None
        self.increased_log = {}

        self.traffic = 0

    def logger(self, block_num, block_size, total_size):
        _current = time.time()
        if not self.started_at:
            self.started_at = _current
            line = '=========%s==========' % time_to_string(_current)
            with open(self.log_fp, 'a') as fi:
                fi.write('%s\n' % line)
        # Stop download by raise an exception
        if self.timeout and self.timeout + self.started_at < _current:
            raise FileDownloadTimeoutException('Downloader timeout')
        current = int(_current * self.accuracy)
        if current == self.last_time:
            self.accumulate += 1
            return

        # Downloaded increase bytes
        dl_increase = self.accumulate * block_size
        self.traffic += dl_increase
        # Instantaneous Speed (1s / accuracy)
        dl_speed = self.accuracy * dl_increase / (current - self.last_time)
        # Speed in 2s
        window_size = 2  # In seconds
        self.increased_log[_current] = dl_increase
        self.increased_log = {
            t: v
            for t, v in self.increased_log.items()
            if t > _current - window_size
        }
        window_dl_speed = sum(self.increased_log.values()) / window_size
        # Reset the accumulate
        self.accumulate = 1

        line = '\t'.join(list(map(
            str,
            [
                int(1000 * _current),
                speed_human_readable(dl_speed), speed_human_readable(window_dl_speed),
                block_num, '%.2f%%' % (100 * self.traffic / total_size)]
        )))
        time_str = time_to_string(_current)
        print('\r%s: %s' % (time_str, line), end='')
        # Log data
        with open(self.log_fp, 'a') as fi:
            fi.write('%s\n' % line)

        # Update time
        self.last_time = current

    def bind(self, downloader):
        self.downloader = downloader
        downloader.watcher = self

    def born(self, timeout=0):
        self.timeout = timeout
        self.downloader.start()
        self.downloader.stop_and_clear()

    def suicide(self):
        self.downloader.stop_and_clear()
