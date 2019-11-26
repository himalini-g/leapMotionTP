from Tkinter import *



####################################
# customize these functions
####################################

def timerFired(data):
    pass
def drawFingerLines(canvas, data):
    for key, val in data.fingerPoints.items():
        canvas.create_line(val[0], 300 - val[2], val[3], 300 - val[5], fill = data.trigger)
    # if(len(data.distA) > 2 and len(data.distB) > 2):
    #     canvas.create_line(data.distA[0], 3000 - data.distA[2], data.distB[0], 3000 - data.distB[2], fill = data.trigger)
def drawScreenIntersect(canvas,data):
    txt = str(int(data.intersect[0])) + ' , ' + str(int(data.intersect[1]))
    canvas.create_oval(data.intersect[0] - 5, data.intersect[1] - 5, data.intersect[0] + 5, data.intersect[1] + 5, fill = data.trigger)
    canvas.create_text(data.intersect[0], data.intersect[1], text = txt)
def drawTarget(canvas, data):
    canvas.create_oval(data.target.x - data.target.r, data.target.y - data.target.r, data.target.x + data.target.r, data.target.y + data.target.r, fill = 'red')
    txt = str(data.target.x) + ' , ' + str(data.target.y)
    canvas.create_text(data.target.x, data.target.y, text = txt)
def redrawAll(canvas, data):
    drawScreenIntersect(canvas,data)
    drawFingerLines(canvas, data)
    drawTarget(canvas, data)

####################################
# use the run function as-is
####################################

