
# -*- coding: utf-8 -*-

import threading
import time
from pyping import verbose_ping


class Task:
    def __init__(self):
        self.m_thread = threading.Thread(target=self.task_func, args=())
        self.m_thread.setDaemon(True)
        self.m_thread.start()

    @staticmethod
    def task_func():
        while True:
            verbose_ping("msgo.bandainamco-ol.jp", 2, 1)
            time.sleep(1)
        pass

