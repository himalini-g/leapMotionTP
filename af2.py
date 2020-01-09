from Tkinter import *
import time

def timerFiredWrapper(timerFired, redrawAll, timerDelay, canvas):
    timerFired()
    canvas.delete(ALL)
    redrawAll(canvas)
    canvas.after(timerDelay, timerFiredWrapper, timerFired, redrawAll, timerDelay, canvas)

def mousePressedWrapper(mousePressed, event, redrawAll, canvas):
    mousePressed(event)
    canvas.delete(ALL)
    redrawAll(canvas)

def keyPressedWrapper(keyPressed, event, redrawAll, canvas):
    keyPressed(event)
    canvas.delete(ALL)
    redrawAll(canvas)

def run(AppClass, width=1000, height=700):
    root = Tk()
    canvas = Canvas(root, width=width, height=height)
    canvas.pack()

    app = AppClass()
    app.timerDelay = 20
    app.width = width
    app.height = height
    app.appStarted()
# set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind('<Key>', lambda e: keyPressedWrapper(app.keyPressed, e, app.redrawAll, canvas))

    timerFiredWrapper(app.timerFired, app.redrawAll, app.timerDelay, canvas)

    root.mainloop()

class App(object):
    def appStarted(app): pass
    def keyPressed(app, event): pass
    def mousePressed(app, event): pass
    def timerFired(app): pass
    def redrawAll(app, canvas): pass


