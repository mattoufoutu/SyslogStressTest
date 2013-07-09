__author__ = 'pyt'

from SyslogStressTest.core.Scheduler import Scheduler
from SyslogStressTest.core.Settings import SUPPROCCESS,EPS

# from time import time


if __name__ == "__main__":
    # currtime = time()
    schd = Scheduler()
    try:
        schd.run()
    except KeyboardInterrupt:
        print "KeyboardInterrupt send"
        print "Quit..."
        # print 'Number of parallel process: %s time elapsed: %s at %s EPS' % (SUPPROCCESS, (time() - currtime), EPS)

