from Tkinter import *
from threading import Thread
import pdb
import time


class View(object):
# Constants
    canvasWidth = 800
    canvasHeight = 600
    startPosX = 330
    startPosY = 390
    howPosX = 310
    howPosY = 490
    root = Tk()
    frame = Frame(root)
    canvas = Canvas(root, width = canvasWidth, height = canvasHeight)
    startButton = None
    howButton = None

# Handlers
    def onKeyDown(self, event):
        print 'Keydown: ' + str(event.keysym)
        self.controller.onKeyStroke(event.keysym)
    
    def onMouseClickStart(self, event):
        print 'Clicking Start'
        self.controller.onMouseClick("game")

    def onMouseClickHow(self, event):
        print 'Clicking How'
        self.controller.onMouseClick("how")

    def onMouseMoveStart(self, event):
        print "onMouseMoveStart"
        self.drawStartButton(self.start2)

    def onMouseMoveHow(self, event):
        print "onMouseMoveHow"
        self.drawHowButton(self.how2)

    def onMouseLeaveStart(self, event):
        print "onMouseLeaveStart"
        self.drawStartButton(self.start)

    def onMouseLeaveHow(self, event):
        print "onMouseLeaveHow"
        self.drawHowButton(self.how)

    def onMouseMoveCanvas(self, event):
        print "onMouseMoveCanvas"

    def onMouseLeaveCanvas(self, event):
        print "onMouseLeaveCanvas"

# Methods
    def __init__(self, controller):
        self.controller = controller
        self.frame.pack()
        self.canvas.pack()
        self.linkImage()

# Welcome Page
    def drawStartButton(self, style):
        if self.startButton != None:
            self.canvas.delete(self.startButton)
        self.startButton = self.canvas.create_image(self.startPosX, self.startPosY, image = style, anchor = NW)
        if style == self.start:
            self.canvas.tag_bind(self.startButton, "<Enter>", self.onMouseMoveStart)
        else:
            self.canvas.tag_bind(self.startButton, "<Leave>", self.onMouseLeaveStart)
        self.canvas.tag_bind(self.startButton, "<Button-1>", self.onMouseClickStart)
        
    def drawHowButton(self, style):
        if self.howButton != None:
            self.canvas.delete(self.howButton)
        self.howButton = self.canvas.create_image(self.howPosX, self.howPosY, image = style, anchor = NW)
        if style == self.how:
            self.canvas.tag_bind(self.howButton, "<Enter>", self.onMouseMoveHow)
        else:
            self.canvas.tag_bind(self.howButton, "<Leave>", self.onMouseLeaveHow)
        self.canvas.tag_bind(self.howButton, "<Button-1>", self.onMouseClickHow)


    def drawWelcome(self):
        self.canvas.delete(ALL)
        self.canvas.create_image(0, 0, image = self.welcomeBg, anchor = NW)
        self.canvas.bind("<Enter>", self.onMouseMoveCanvas)
        self.canvas.bind("<Leave>", self.onMouseLeaveCanvas)
        self.root.bind_all("<Key>", self.onKeyDown)
        self.drawStartButton(self.start)
        self.drawHowButton(self.how)
        

    def waitUser(self):
        # Wait for the user to respond
        self.root.mainloop()

# Game Page
    def drawGame(self):
        self.canvas.delete(ALL)
        self.canvas.create_image(0, 0, image = self.gameBg, anchor = NW)
    
    def insertArrow(self, arrowDirection, x, y):
        # Insert a new arrow to the screen with direction given
        # Returns the identifier of the arrow
        return self.canvas.create_image(x, y, image = self.arrows[arrowDirection], anchor = NW)

    def deleteArrow(self, arrow):
        # Eliminate the arrow
        self.canvas.delete(arrow)

    def moveArrow(self, arrow, dx, dy):
        self.canvas.move(arrow, dx, dy)

    def callback(self, time, exe):
        self.canvas.after(time, exe)

    def updateScore(self, score):
        self.canvas.create_text(canvasWidth/2, canvasHeight/10, text = str(score), anchor = CENTER)

# Helper Functions
    def linkImage(self):
        self.welcomeBg = PhotoImage(file = './res/image/welcomeBg.gif')
        self.start = PhotoImage(file = './res/image/start.gif')
        self.how = PhotoImage(file = './res/image/how.gif')
        self.start2 = PhotoImage(file = './res/image/start2.gif')
        self.how2 = PhotoImage(file = './res/image/how2.gif')
        self.gameBg = PhotoImage(file = './res/image/gameBg.gif')
        self.win = PhotoImage(file = './res/image/win.gif')
        self.lose = PhotoImage(file = './res/image/lose.gif')
        self.arrows = [
                        PhotoImage(file = './res/image/left.gif'), 
                        PhotoImage(file = './res/image/down.gif'), 
                        PhotoImage(file = './res/image/up.gif'), 
                        PhotoImage(file = './res/image/right.gif'), 
                      ]
