import os
import sys
import inspect
import thread
import time
import string
import Leap
import math
from selenium import webdriver
import time

src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
src_dir = string.replace(src_dir, '\\', '/')

arch_dir = 'lib/x64' if sys.maxsize > 2**32 else 'lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))


status = ['pause', 'play']
status_index = 0
src_dir = os.getcwd()
driver = webdriver.PhantomJS('{}\\phantomjs.exe'.format(src_dir))
volume_level = 10


def executeCommand(command):
    print command
    time.sleep(1)
    driver.get(command)


def vlcCommand(key):
    global status, status_index, driver
    print key
    print "\n"
    if key == 'play/pause':
        command = 'http://localhost:8080/requests/status.xml?command=pl_{}'.format(
            status[status_index])
        # print command
        executeCommand(command)
        if status_index == 0:
            status_index = 1
        else:
            status_index = 0
    elif key == 'previous':
        command = 'http://localhost:8080/requests/status.xml?command=pl_{}'.format(
            key)
        executeCommand(command)
    elif key == 'next':
        command = 'http://localhost:8080/requests/status.xml?command=pl_{}'.format(
            key)
        executeCommand(command)
    elif key == 'volume up':
        command = 'http://localhost:8080/requests/status.xml?command=volume&val=+{}'.format(
            volume_level)
        executeCommand(command)
    elif key == 'volume down':
        command = 'http://localhost:8080/requests/status.xml?command=volume&val=-{}'.format(
            volume_level)
        executeCommand(command)


def getDistance(a, b, threshold):
    distance = abs(a-b)
    if a > b:
        if distance > threshold:
            return "previous"
    elif a < b:
        if distance > threshold:
            return "next"

    return None


def check(a, b):
    if a < 0 and b < 0:
        return True
    if a > 0 and b > 0:
        return True
    return False


class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    position1 = None
    position2 = None
    start_frame = None
    prev_angle = None

    def on_connect(self, controller):
        print "Connected"

    def on_frame(self, controller):
        frame = controller.frame()
        hand = frame.hands.rightmost
        direction = hand.direction

        print "no. of hands : {} hands".format(len(frame.hands)),
        print "\n"

        flag = 0
        pinch = hand.pinch_strength

        """Pause and play"""

        if pinch > 0.5 and flag == 0:
            vlcCommand('play/pause')
            flag = 1

        """ Next and previous gesture """
        for gesture in frame.gestures():
            if gesture.type is Leap.Gesture.TYPE_SWIPE:
                swipe = Leap.SwipeGesture(gesture)
                distance = getDistance(
                    swipe.start_position[0], swipe.position[0], 10)
                if flag == 0:
                    vlcCommand(distance)
                    flag = 1

        """Volume up and Down"""
        pitch = int(direction.pitch * Leap.RAD_TO_DEG)
        if pitch <= 80:
            if self.prev_angle == None:
                self.prev_angle = int(pitch)
            else:
                angle = getDistance(int(pitch), self.prev_angle, 20)
                if angle != None and flag == 0:
                    if hand.is_left:
                        vlcCommand('volume down')
                    else:
                        vlcCommand('volume up')
                    flag = 1


def main():

    listener = SampleListener()
    controller = Leap.Controller()

    controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
    controller.config.set("Gesture.Swipe.MinLength", 300.0)
    controller.config.set("Gesture.Swipe.MinVelocity", 1000)
    controller.config.save()

    controller.add_listener(listener)

    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
