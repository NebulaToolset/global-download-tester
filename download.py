from Core import utils
from Core.Downloader import Downloader
from Core.Watcher import Watcher

from collections import OrderedDict

import re
import os
import time
import random

from Core.utils import time_to_string, speed_human_readable


def first(s):
    """
    Return the first element from an ordered collection
    or an arbitrary element from an unordered collection.
    Raise StopIteration if the collection is empty.
    https://stackoverflow.com/questions/21062781/shortest-way-to-get-first-item-of-ordereddict-in-python-3/27666721
    """
    return next(iter(s))


class DownloadTester:
    def __init__(self):
        self.datafiles = []
        self.fiaddrs = OrderedDict()
        self.scheduled = OrderedDict()

        self.started_at = 0
        self.end_at = 0

        self.traffic_cost = 0
        self.timeout = 0

    def clear_logs(self):
        # Clear history logs.
        old_logs = os.walk('./log')
        for root, _, filenames in old_logs:
            for filename in filenames:
                if filename.endswith('.log'):
                    full_path = os.path.join(root, filename)
                    print('Remove file:', full_path)
                    os.remove(full_path)
        old_dls = os.walk('./tmp')
        for root, _, filenames in old_dls:
            for filename in filenames:
                if filename.endswith('.dl.tmp'):
                    full_path = os.path.join(root, filename)
                    print('Remove file:', full_path)
                    os.remove(full_path)

    def run(self, clear=False):
        started_at_label = time_to_string(self.started_at)
        end_at_label = time_to_string(self.end_at)
        print('The program will start at %s, the last task will be start at %s.' % (
            started_at_label, end_at_label
        ))
        print('Downloader test %d locations, with %d tasks scheduled during at least %d seconds.' % (
            len(self.fiaddrs.keys()), len(self.scheduled), self.end_at - self.started_at
        ))
        print('OS: [%s], press [Enter] to start.' % utils.get_os())
        input()

        if clear:
            self.clear_logs()

        # Do scheduled ping tasks
        while self.scheduled:
            now = int(time.time())
            while self.scheduled and first(self.scheduled) <= now:
                scheduled_time = first(self.scheduled)
                labels = self.scheduled[scheduled_time]
                for label in labels:
                    fi_addrs = self.fiaddrs.get(label)
                    if not fi_addrs:
                        break
                    fi_addr = random.choice(fi_addrs)
                    print('Scheduled download %s at %s...' % (
                        fi_addr, time_to_string(scheduled_time)
                    ))
                    dler = Downloader(fi_addr)
                    watcher = Watcher('./log/%s.log' % label, dler.dl_tmp_fp)
                    watcher.accuracy = 10

                    watcher.bind(dler)
                    watcher.born(self.timeout)

                    self.traffic_cost += watcher.traffic

                del self.scheduled[scheduled_time]
            time.sleep(0.1)
        print('=====================================')
        print('Task finished, cost traffic %s' % speed_human_readable(self.traffic_cost, is_speed=False))

    def schedule(self, timeout, interval, period):
        started_at = int(time.time())

        step = interval / len(self.fiaddrs.keys())
        if step + 1 < timeout:
            raise Exception('Interval too little to test.')
        # step = 1 if interval > len(self.ipaddrs.keys()) else interval / len(self.ipaddrs.keys())
        for _round in range(int(period / interval)):
            offset = 0.
            for fi_addr in self.fiaddrs.keys():
                estimate = int(started_at + _round * interval + offset)
                if estimate not in self.scheduled.keys():
                    self.scheduled[estimate] = []
                self.scheduled[estimate].append(fi_addr)
                offset += step

        self.started_at = started_at
        self.end_at = started_at + period
        self.timeout = timeout

    def load(self, idc: list):
        iter_paths = os.walk('./files_addr')
        for iter_path in iter_paths:
            root, _, file_list = iter_path
            for file in file_list:
                if file.endswith('.fiaddr') and file.split('.')[0] in idc:
                    self.datafiles.append(os.path.join(root, file))

        for datafile in self.datafiles:
            fi = open(datafile)
            for _, line in enumerate(fi):
                line = line.strip()
                if not line or line[0] == '#':
                    continue
                location, url = re.split(':=', line)
                location = location.strip()
                url = url.strip()
                if location not in self.fiaddrs.keys():
                    self.fiaddrs[location] = []
                self.fiaddrs[location].append(url)
            fi.close()

        # Shuffle
        fiaddrs_to_shuffle = list(self.fiaddrs.items())
        random.shuffle(fiaddrs_to_shuffle)
        self.fiaddrs = OrderedDict(fiaddrs_to_shuffle)


def main():
    # dler = Downloader('http://hnd-jp-ping.vultr.com/vultr.com.100MB.bin')
    # url = 'http://sjo-ca-us-ping.vultr.com/vultr.com.1000MB.bin'
    # dler = Downloader(url)
    # watcher = Watcher('./log/%s.log' % url.replace(':', '').replace('/', '-'), dler.dl_tmp_fp)
    # watcher.accuracy = 10
    #
    # watcher.bind(dler)
    # watcher.born(timeout)
    tester = DownloadTester()
    tester.load(['Vultr'])
    tester.schedule(timeout=29, interval=480, period=1000)
    tester.run(clear=True)


if __name__ == '__main__':
    main()
