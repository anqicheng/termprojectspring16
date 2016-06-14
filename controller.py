import time
import random
import pdb
from threading import Thread

class Arrow(object):
# State Constants
    WAITING = -1
    APPROACHING = 0
    READY = 1
    HIT = 2
    EXPIRED = 3
# Animation Constants
    timeInterval = 15 # In terms of ms
    baseXs = [22, 160, 270, 365]
    baseY = 520
    verticalMoveStep = -4
    attackableTop = 45
    attackableBottom = 192
            
    def isAttackable(self):
        return self.state == self.READY

    def isTerminated(self):
        return self.state == self.HIT or self.state == self.EXPIRED

    def updateStatus(self):
    # Update the status based on its location, not valid for expired ones
        if self.isTerminated():
            pass
        if self.currentY < self.attackableTop:
            self.state = self.EXPIRED
        elif self.currentY < self.attackableBottom:
            self.state = self.READY

    def animate(self):
        if not self.isTerminated():
            self.currentY += self.verticalMoveStep
            self.updateStatus()
            self.view.moveArrow(self.viewId, 0, self.verticalMoveStep)
            self.view.callback(self.timeInterval, self.animate)
        if self.isTerminated():
            self.view.deleteArrow(self.viewId)
    
    def startAnimation(self):
        self.viewId = self.view.insertArrow(self.direction, self.currentX, self.currentY)
        self.view.callback(self.timeInterval, self.animate)
        self.state = self.APPROACHING
    
    def prepare(self):
        self.view.callback(self.delay, self.startAnimation)

    def __init__(self, view, direction, delay):
        self.view = view
        self.direction = direction
        self.currentX = self.baseXs[direction]
        self.currentY = self.baseY
        self.state = self.WAITING
        self.delay = delay

class Controller(object):

    class Runnable(Thread):
        def __init__(self, exe):
            self.exe = exe
        def run(self):
            self.exe()
# Data fields
    view = None      # Link to view
    model = None     # Link to model


# Message Handlers
    def onMouseClick(self, destination):
        # TO DO: parse the mouse click destination
        if destination == 'game':
            self.goToGame()
        elif destination == 'how':
            pass

    def onKeyStroke(self, key):
        self.keyStroke.add(key)

# Methods
    def __init__(self):
        self.view = None
        self.model = None
        self.keyStroke = set()

    def start(self):
        self.view.drawWelcome()
        self.view.waitUser()

    def linkView(self, view):
        self.view = view

    def linkModel(self, model):
        self.model = model

    def goToGame(self):
        beats = self.model.beatDetect('res/music/cmm.wav')
        self.view.drawGame()
        arrs = []
        last = 2
        for i in beats:
            if random.randint(0, 9) <= 2 + last:
                last = 0
                arrs.append(Arrow(self.view, random.randint(0, 3), int(i * 1000)))
            else:
                last = 2
        for now in arrs:
            self.Runnable(now.prepare).run()
        self.soundDemo()

        
    def respondKeyStroke(self):
    # Returns True if the game should end
        print self.keyStroke
        for key in self.keyStroke:
            if key == 'Escape':
                exiting = True
            else:
                pass
        return exiting

    def soundDemo(self):
        self.model.playSound()
