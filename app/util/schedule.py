import threading
import re
from datetime import datetime, timedelta
from calendar import monthrange, isleap
from random import randint
from time import sleep


class ScheduledFun:

    def __init__(self, fun, delay_fun, running=True, *args, **kwargs):
        self.fun = fun
        self.delay_fun = delay_fun
        self.args = args
        self.kwargs = kwargs

        self.timer = None
        self.mutex = threading.Lock()

        if running:
            self.start()

    def __call__(self):
        self.fun(*self.args, **self.kwargs)

    def _loop(self):
        with self.mutex:
            self()
            sleep(1)
            time = self.delay_fun()
            while not time:
                time = self.delay_fun()

            self.timer = threading.Timer(time, self._loop)
            self.timer.start()

    def start(self):
        with self.mutex:
            if self.timer is not None:
                return
            self.timer = threading.Timer(self.delay_fun(), self._loop)
            self.timer.start()

    def stop(self):
        with self.mutex:
            if self.timer is None:
                return
            self.timer.cancel()
            self.timer = None


# time in format HH:MM:SS
def daily(time, run=True, *args, **kwargs):
    def decorator(fun):
        h, m, s = map(int, time.split(':'))

        def delay_fun():
            now = datetime.now()
            then = datetime(now.year, now.month, now.day, h, m, s)
            if then < now:
                then += timedelta(days=1)
            return int((then-now).total_seconds())

        sched_fun = ScheduledFun(fun, delay_fun, run, *args, **kwargs)
        return sched_fun
    return decorator


# time in format DD HH:MM:SS
def monthly(time, run=True, *args, **kwargs):
    def decorator(fun):
        d, h, m, s = map(int, re.split(':| ', time))

        def delay_fun():
            now = datetime.now()
            then = datetime(now.year, now.month, d, h, m, s)
            if then < now:
                days_in_month = monthrange(now.year, now.month)[1]
                then += timedelta(days=days_in_month)
            return int((then-now).total_seconds())

        sched_fun = ScheduledFun(fun, delay_fun, run, *args, **kwargs)
        return sched_fun
    return decorator


# time in format MM-DD HH:MM:SS
def yearly(time, run=True, *args, **kwargs):
    def decorator(fun):
        mo, d, h, mi, s = map(int, re.split('-|:| ', time))

        def delay_fun():
            now = datetime.now()
            then = datetime(now.year, mo, d, h, mi, s)
            if then < now:
                days_in_year = 366 if isleap(now.year) else 365
                then += timedelta(days=days_in_year)
            return int((then-now).total_seconds())

        sched_fun = ScheduledFun(fun, delay_fun, run, *args, **kwargs)
        return sched_fun
    return decorator


# time in format DD HH:MM:SS
def periodically(time, run=True, *args, **kwargs):
    def decorator(fun):
        d, h, m, s = map(int, re.split(':| ', time))

        def delay_fun():
            delta = timedelta(days=d, hours=h, minutes=m, seconds=s)
            return delta.total_seconds()

        sched_fun = ScheduledFun(fun, delay_fun, run, *args, **kwargs)
        return sched_fun
    return decorator


# times in format DD HH:MM:SS
def random_period(min_time, max_time, run=True, *args, **kwargs):
    def decorator(fun):
        d1, h1, m1, s1 = map(int, re.split(':| ', min_time))
        d2, h2, m2, s2 = map(int, re.split(':| ', max_time))

        min_sec = timedelta(days=d1, hours=h1, minutes=m1, seconds=s1).total_seconds()
        max_sec = timedelta(days=d2, hours=h2, minutes=m2, seconds=s2).total_seconds()

        def delay_fun():
            return randint(min_sec, max_sec)

        sched_fun = ScheduledFun(fun, delay_fun, run, *args, **kwargs)
        return sched_fun
    return decorator


# times in format HH:MM:SS
def random_interval(min_time, max_time, run=True, *args, **kwargs):
    def decorator(fun):
        h1, m1, s1 = map(int, min_time.split(':'))
        h2, m2, s2 = map(int, max_time.split(':'))

        d1 = datetime(2000, 1, 1, h1, m1, s1)
        d2 = datetime(2000, 1, 1, h2, m2, s2)
        seconds_between = (d2 - d1).total_seconds()

        now = datetime.now()
        last_invoke = datetime(now.year, now.month, now.day, h1, m1, s1)
        if last_invoke > now:
            last_invoke -= timedelta(days=1)

        def delay_fun():
            nonlocal last_invoke

            last_invoke += timedelta(days=1)
            moment = last_invoke + timedelta(seconds=randint(0, seconds_between))
            print(int((last_invoke - datetime.now()).total_seconds()))
            return int((last_invoke - datetime.now()).total_seconds())

        sched_fun = ScheduledFun(fun, delay_fun, run, *args, **kwargs)
        return sched_fun
    return decorator


if __name__ == '__main__':
    @daily('13:51:00')
    def meow():
        print("dayly")


    @monthly('6 14:03:00')
    def mrr():
        print('monthly')


    @yearly('10-6 14:12:00')
    def wrau():
        print('yearly')


    @periodically('0 0:0:1')
    def miau():
        print('periodically')


    @random_period('0 0:0:1', '0 0:0:10')
    def mrawr():
        print('randomly')


    @random_interval('15:32:0', '15:33:00')
    def sth():
        print('random interval')


    mrawr.stop()
    miau.stop()




