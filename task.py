
# -*- coding: utf-8 -*-

import threading
import time
from pyping import do_ping


class MyThread(threading.Thread):
    def __init__(self, task):
        threading.Thread.__init__(self)
        self.m_task = task

    def run(self):
        import os
        tid = self.m_task.m_tid
        time.sleep(self.m_task.m_init_delay)
        while not self.m_task.m_should_stop:
            delay = do_ping(tid, self.m_task.m_addr, 2)
            self.m_task.add_result(delay)
            time.sleep(1)

        self.m_task.m_thread = None


class Task:
    def __init__(self, tid, addr, init_delay, on_update_task_info):
        self.m_should_stop = False
        self.m_thread = None
        self.m_tid = tid
        self.m_addr = addr
        self.m_init_delay = init_delay
        self.m_on_update_task_info = on_update_task_info

        self.m_total_ping = 0
        self.m_lost_ping = 0
        self.m_total_value = 0

        self.m_current_delay = "-"
        self.m_current_lost = "-"
        self.m_current_average = "-"

    def start(self):
        if self.m_thread:
            return

        self.m_should_stop = False

        self.m_total_ping = 0
        self.m_lost_ping = 0
        self.m_total_value = 0

        self.m_thread = MyThread(self)
        self.m_thread.setDaemon(True)
        self.m_thread.start()

    def stop(self):
        if self.m_thread:
            self.m_should_stop = True

    def is_running(self):
        return self.m_thread != None

    def add_result(self, result):
        self.m_total_ping += 1

        delay = ""
        if result == -1:
            delay = "network error"
            self.m_lost_ping += 1
        elif result == -2:
            delay = "timeout"
            self.m_lost_ping += 1
        else:
            delay = "%d ms" % result
            self.m_total_value += result

        if self.m_total_ping == 0:
            lost = "-"
        elif self.m_lost_ping == 0:
            lost = "0 %"
        else:
            lost = "%.02f %%" % (self.m_lost_ping * 100.0 / self.m_total_ping)

        valid_ping = self.m_total_ping - self.m_lost_ping
        if valid_ping == 0:
            average = "-"
        else:
            average = "%d ms" % int(self.m_total_value * 1.0 / valid_ping)

        self.m_current_delay = delay
        self.m_current_lost = lost
        self.m_current_average = average
        #self.m_on_update_task_info(self, delay, lost, average)

    def get_info(self):
        return self.m_current_delay, self.m_current_lost, self.m_current_average


