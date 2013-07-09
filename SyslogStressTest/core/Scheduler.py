__author__ = 'pyt'

from SyslogStressTest.core.Settings import SUPPROCCESS, EPS
from SyslogStressTest.core.LogEvent import LogEvent
from SyslogStressTest.core.SocketSyslog import SocketSyslog
from SyslogStressTest.core.Settings import SERVER, PORT
from datetime import datetime

from multiprocessing import Pool, Manager
from threading import Event
from signal import signal,SIGINT,SIG_IGN
# from os import listdir, getpid
from time import time,sleep


def unwrap_self_worker_syslog(queue_worker, queue_result):
    return WorkerSyslog(queue_worker, queue_result).run()


class WorkerSyslog():
    _worker_info = None
    def __init__(self, queue_worker, queue_result):
        self.queue_worker = queue_worker
        self.queue_result = queue_result
        self.socketSyslog = SocketSyslog((SERVER, PORT))
        self._stopevent = Event()
        self.msg = LogEvent()

    @property
    def worker_info(self):
        if self._worker_info is None:
            self._worker_info = self.queue_worker.get()
            print self._worker_info
        return self._worker_info

    def run(self):
        while not self._stopevent.isSet():
            self.ID = self.worker_info.get("ID")
            self.MSG_NUMBER = self.worker_info.get("MSG_NUMBER")
            self.MSG_TIMER = self.worker_info.get("MSG_TIMER")
            self.TIME_EXEC = 0

            currentTime = time()
            for i in xrange(self.MSG_NUMBER):
                #todo change msg syslog
                self.socketSyslog.log(self.msg.rand())
                sleep(self.MSG_TIMER)
            self.TIME_EXEC = time() - currentTime
            self.queue_result.put(
                {
                    "TIME_EXEC": self.TIME_EXEC,
                    "MSG_NUMBER": self.MSG_NUMBER,
                    "MSG_TIMER": self.MSG_TIMER,
                    "ID": self.ID
                }
            )
            self._worker_info = None

    def stopped(self):
        return self._stopevent.isSet()

    def stop(self):
        self._stopevent.set()


def init_worker():
    signal(SIGINT, SIG_IGN)


def ajustSleepTime(queue_result, queue_work):
    while True:
        worker_result = queue_result.get()
        #{'MSG_TIMER': 0.3333333333333333, 'ID': 'ID0', 'TIME_EXEC': 1.001810073852539, 'MSG_NUMBER': 3}
        msg_timer = worker_result.get("MSG_TIMER")
        # worker_id = worker_result.get("ID")
        time_exec = worker_result.get("TIME_EXEC")
        # msg_number = worker_result.get("MSG_NUMBER")
        print worker_result

        if time_exec > 1 and time_exec < 1.1:
            msg_timer -= (0.9/EPS)
        elif time_exec > 1.1:
            msg_timer -= (0.5/EPS)
        elif time_exec < 1 and time_exec > 0.9:
            msg_timer += (0.8/EPS)
        elif time_exec < 0.9:
            msg_timer += (0.5/EPS)

        worker_result["MSG_TIMER"] = msg_timer
        queue_work.put(worker_result)

        sleep(0.1)


class Scheduler():
    """Task scheduler."""
    def __init__(self):
        self.averageTime = 0
        self.averageSendTime = 0
        self.messagePerSubProccess, self.timeSleepPerMessage = self.calculeEPS(EPS, SUPPROCCESS)


    def run(self):
        # oslist = listdir('./sample/')
        # for i in oslist:
        #     new = Random_log(i)
        #     print new

        # if FULLSPEED:
        #     self.timeSleepPerMessage = 0

        po = Pool(initializer=init_worker, processes=SUPPROCCESS)
        manager = Manager()
        self.work = manager.Queue()
        self.result = manager.Queue()
        for i in xrange(SUPPROCCESS):
            worker_param = {
                "ID": "ID%d" % i,
                "MSG_NUMBER": self.messagePerSubProccess,
                "MSG_TIMER": self.timeSleepPerMessage
            }

            self.work.put(worker_param)

            workers = po.apply_async(unwrap_self_worker_syslog, (self.work, self.result))

        po_time = Pool(initializer=init_worker, processes=1)
        time_ajust_worker = po_time.apply_async(ajustSleepTime, (self.result, self.work))

        po.close()
        po.join()

    def calculeEPS(self, numberOfEPS, NumberOfProcess): # 1000, 4
        MessagePerProc = numberOfEPS / NumberOfProcess # 250
        MessageSleepTime = (1. / MessagePerProc) # 0.004
        return (MessagePerProc, MessageSleepTime) # (250, 0.004)
