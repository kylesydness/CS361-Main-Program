import time
import datetime
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:8463")

class Timer:
    def __init__(self):
        self._total = 0
        self._active = False
        self._start = None
        self._end = None

    def startStop(self):
        """
        Start/stop the timer
        """
        if not self._active:    #start if inactive
            self._start = time.time()
            self._active = True
            return
        if self._active:        #stop if inactive
            self._end = time.time()
            self._active = False
            self._total += self._end - self._start  #add up running total
            return

    def reset(self):
        """
        Reset the timer to 0 seconds
        """
        self._total = 0
        return

    def getTime(self):
        """
        Returns the current time down to microseconds - can be requested while timer is either active or inactive
        """
        if self._active:
            self._end = time.time()
            self._total += self._end - self._start
            self._start = time.time()
        return datetime.timedelta(seconds = self._total)

    def getStatus(self):
        """
        Returns timer's status:
        """
        return self._active

stopwatch = Timer()

"""
stopwatch.startStop() #start timer
time.sleep(60.5)
stopwatch.startStop() #stop timer
print(stopwatch.getTime()) #expect 5ish seconds
time.sleep(2)
stopwatch.startStop() #start timer
time.sleep(30.1)
print(stopwatch.getTime())  #expect 10ish seconds
time.sleep(15.1)
stopwatch.startStop() #stop timer
print(stopwatch.getTime())  #expect 15ish seconds
"""

while True:
    message = socket.recv_string()
    message = message.lower()
    reply = ""

    if message.find("timer") >= 0:
        if message.find("stsp") >= 0:
            stopwatch.startStop()
        if message.find("reset") >= 0:
            stopwatch.reset()
        if message.find("read") >= 0:
            reply += str(stopwatch.getTime())
        if message.find("active") >= 0:
            if len(reply) > 0: reply += ", "
            reply += str(stopwatch.getStatus())

    socket.send_string(str(reply))