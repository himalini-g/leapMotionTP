import random, math, copy
from shapely.geometry import *
from Tkinter import *
class Bat():
    def __init__(self, width, height):
        self.scale = 70
        self.bodyColor = 'grey23'
        self.eyeColor = 'yellow'
        self.wingState = 0
        self.cx = width // 2
        self.cy = height // 2
        self.cx, self.cy = self.cx, self.cy
        self.stateIndex = 0 #(self.cx - self.scale // 2, self.cy + self.scale // 2), 
         #(self.cx - (self.scale // 5 + , self.cy + self.scale // 2 + self.scale // 2 * 0.5)
         #(self.cx + self.scale // 2, self.cy + self.scale // 2), 
        self.bodyFrame = [(self.cx, self.cy + self.scale) , (self.cx - self.scale // 5, self.cy + self.scale // 2), \
                         (self.cx - self.scale // 2, self.cy - self.scale // 2), (self.cx, self.cy - self.scale),\
                         (self.cx + self.scale // 2, self.cy - self.scale // 2), (self.cx + self.scale // 5, self.cy + self.scale // 2),  \
                         (self.cx, self.cy + self.scale)]
        self.headFrame = [(self.cx, self.cy + self.scale)
        self.rightWingFrame = [(self.cx, self.cy - self.scale // 2), (self.cx + self.scale * 1.3 , self.cy - self.scale), \
                          (self.cx + self.scale * 3, self.cy ), (self.cx + self.scale * 2, self.cy + self.scale * 0.2), \
                          (self.cx + self.scale * 1, self.cy + self.scale * 0.2), (self.cx, self.cy - self.scale // 2)]
        self.leftWingFrame = [(self.cx, self.cy - self.scale // 2), (self.cx - self.scale * 1.3 , self.cy - self.scale), \
                          (self.cx - self.scale * 3, self.cy ), (self.cx - self.scale * 2, self.cy + self.scale * 0.2), \
                          (self.cx - self.scale * 1, self.cy + self.scale * 0.2), (self.cx, self.cy - self.scale // 2)]
        
        self.counter = 0
    def states(self):
        self.counter += 1

        cx, cy, sc = self.cx, self.cy, self.scale
        if(self.counter % 5 == 0):
            self.rightWingFrame = [(self.cx, self.cy - self.scale // 2), (self.cx + self.scale * 0.9 , self.cy - self.scale * 1.3), \
                            (self.cx + self.scale * 2.6, self.cy - self.scale * 2 ), (self.cx + self.scale * 2.1, self.cy - self.scale * 0.6), \
                            (self.cx + self.scale * 1, self.cy - self.scale * 0.2), (self.cx, self.cy - self.scale // 2)]
        elif(self.counter % 5 == 1):
            self.rightWingFrame = [(self.cx, self.cy - self.scale // 2), (self.cx + self.scale * 0.8 , self.cy - self.scale * 1.3), \
                            (self.cx + self.scale * 1.6, self.cy - self.scale * 3 ), (self.cx + self.scale * 2.1, self.cy - self.scale * 1), \
                            (self.cx + self.scale * 1, self.cy - self.scale * 0.2), (self.cx, self.cy - self.scale // 2)]
        elif(self.counter % 5 == 2):
            self.rightWingFrame = [(self.cx, self.cy - self.scale // 2), (self.cx + self.scale * 0.9 , self.cy - self.scale * 1.3), \
                            (self.cx + self.scale * 2.6, self.cy - self.scale * 2 ), (self.cx + self.scale * 2.1, self.cy - self.scale * 0.6), \
                            (self.cx + self.scale * 1, self.cy - self.scale * 0.2), (self.cx, self.cy - self.scale // 2)]


        elif(self.counter % 5 == 3):
            self.rightWingFrame = [(self.cx, self.cy - self.scale // 2), (self.cx + self.scale * 0.9 , self.cy ), \
                            (self.cx + self.scale * 1.4 , self.cy + self.scale * 0.6),
                            (self.cx + self.scale * 1.7, self.cy + self.scale * 1.6 ), (self.cx + self.scale * 0.7, self.cy + self.scale * 1.3), \
                            (self.cx + self.scale * 0.4, self.cy + self.scale * 0.2), (self.cx, self.cy - self.scale // 2)]

        else:
            self.rightWingFrame = [(self.cx, self.cy - self.scale // 2), (self.cx + self.scale * 0.9, self.cy - self.scale), 
                          (self.cx + self.scale * 1.9 , self.cy - self.scale * 0.9),
                          (self.cx + self.scale * 3, self.cy ), (self.cx + self.scale * 2, self.cy + self.scale * 0.2), \
                          (self.cx + self.scale * 1, self.cy + self.scale * 0.2), (self.cx, self.cy - self.scale // 2)]

    def getPoints(self):
        pass

        
def init(data):
    data.bat = Bat(data.width, data.height)

def drawBat(canvas, data):
    counterBody = 0
    counterWing = 0
    canvas.create_polygon(data.bat.bodyFrame, fill = data.bat.bodyColor)
    canvas.create_polygon(data.bat.leftWingFrame, fill = data.bat.bodyColor )
    canvas.create_polygon(data.bat.rightWingFrame, fill = data.bat.bodyColor )
    for point in data.bat.leftWingFrame:
        canvas.create_oval(point[0] - 5, point[1] - 5, point[0] + 5, point[1] + 5, fill = 'red')
        txt = str(counterWing) + ' ' + str(point[0])+ ' ' +str(point[1])
        canvas.create_text(point[0] - 5, point[1] - 5, text = txt )
        counterWing += 1
    for point in data.bat.rightWingFrame:
        canvas.create_oval(point[0] - 5, point[1] - 5, point[0] + 5, point[1] + 5, fill = 'red')
        txt = str(counterWing) + ' ' + str(point[0])+ ' ' +str(point[1])
        canvas.create_text(point[0] - 5, point[1] - 5, text = txt )
        counterWing += 1
def timerFired(data):
    pass
def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    data.bat.states()
def redrawAll(canvas, data):
    drawBat(canvas, data)
####################################
# use the run function as-is
####################################


def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 1000 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(500, 500)
