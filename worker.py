#!/usr/bin/python3

import sys

from download import DownloadTester


def main(argv):
    timeout = int(argv[1])
    interval = int(argv[2])
    period = int(argv[3])

    tester = DownloadTester()
    tester.load(['Vultr'])
    tester.schedule(timeout=timeout, interval=interval, period=period)
    tester.run(clear=True)


if __name__ == '__main__':
    main(sys.argv)
