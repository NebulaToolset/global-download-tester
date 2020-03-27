from Core.Exceptions import FileDownloadTimeoutException
from Core.Watcher import Watcher
from Core.utils import time_to_string

from urllib.request import urlretrieve

import os
import time
import random
import string
import socket
socket.setdefaulttimeout(5)


class Downloader:
    def __init__(self, remote_url: str):
        self.remote_url = remote_url
        self.dl_tmp_fp = 'tmp/%s.%s.dl.tmp' % (
            remote_url.split('/')[-1],
            ''.join(random.sample(string.ascii_letters + string.digits, 8))
        )
        self.watcher: Watcher or None = None

    def start(self):
        started_at = time.time()
        if self.watcher:
            try:
                urlretrieve(self.remote_url, self.dl_tmp_fp, self.watcher.logger)
            except FileDownloadTimeoutException as e:
                print(e)
                end_at = time.time()
                print('Task from %s to %s, total cost %.2f' % (
                    time_to_string(started_at),
                    time_to_string(end_at),
                    end_at - started_at
                ))
                return
            except Exception as e:
                import traceback
                with open('../downloader.error.log', 'a') as fi:
                    fi.write('\n-----------------------\n')
                    fi.write('%s: %s\n' % (time_to_string(time.time()), e))
                    traceback.print_exc(file=fi)
            return
        raise Exception('Downloader starts with no watcher.')

    def stop_and_clear(self):
        if os.path.exists(self.dl_tmp_fp):
            os.remove(self.dl_tmp_fp)
