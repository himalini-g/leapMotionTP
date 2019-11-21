
import os, sys, inspect, thread, time, random
sys.path.insert(0, "/Users/hima/Desktop/Leap/LeapSDK/lib/gun.py")
import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import numpy as np
from Tkinter import *

####################################
# customize these functions
####################################
class Dot():
    def __init__(self, width, height):
        self.x = random.randint(width // 3, width - width // 3)
        self.y = random.randint(height // 3, height - height // 3 )
        self.r = 20
    def gotHit(self, x, y, aimR):
        print(x, y )
        print(self.x, self.y)
        distance = (((self.x - x)**2)+ ((self.y - y)**2)**0.5)
        if((self.r + aimR + 5) > distance):
            return True
        return False
def init(data):
    data.controller = Leap.Controller()
    data.frame = data.controller.frame()
    data.fingerNames = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    data.boneNames = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    data.fingerPoints = {}
    data.dist = 0
    data.distA = []
    data.distB = []
    data.fingerWidth = [0, 0, 0, 0, 0]
    data.trigger = 'black'
    data.intersect = [0, 0]
    data.correctedPoint = [0, 0]
    data.scalar =  2.83464566929 #root.winfo_fpixels('1m') is how I came to the number, but I can't use this in the constructor
    newDot = Dot(data.width, data.height)
    data.target = newDot
    print(data.target.x, data.target.y)
    data.points = 0
def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    print('target made')
    makeNewTarget(data)
def timerFired(data):
    updateLeapMotionData(data)
    printLeapMotionData(data)
    getHit(data)

def updateLeapMotionData(data):
    data.frame = data.controller.frame()
def printLeapMotionData(data):
    frame = data.frame
    for hand in frame.hands:
        handType = "Left hand" if hand.is_left else "Right hand"
        for finger in hand.fingers:
            data.fingerWidth[finger.type] = finger.width
            for b in range(0, 4):
                bone = finger.bone(b)
                name = data.fingerNames[finger.type] + data.boneNames[bone.type]
                if(name == 'IndexDistal'):
                    data.indexDir = bone.direction
                data.fingerPoints[name] = []
                for joint in [bone.prev_joint, bone.next_joint]:
                    data.fingerPoints[name].extend([joint[0], joint[1], joint[2]])
    getTrigger(data)
    getAim(data)
def makeNewTarget(data):
    newDot = Dot(canvas.width, canvas.height)
    data.target = newDot
def getTrigger(data):
    if('ThumbDistal' in data.fingerPoints and 'IndexMetacarpal' in data.fingerPoints):
        a0 = np.array(data.fingerPoints['ThumbDistal'][:3])
        a1 = np.array(data.fingerPoints['ThumbDistal'][3:])
        b0 = np.array(data.fingerPoints['IndexMetacarpal'][:3])
        b1 = np.array(data.fingerPoints['IndexMetacarpal'][3:])
        data.distA, data.distB, data.dist= getTriggerDistance(a0,a1,b0,b1,True)
        if(data.dist < data.fingerWidth[0] + data.fingerWidth[1] - 7):
            data.trigger = 'green'
        else:
            data.trigger = 'black'
def getAim(data):
    if('IndexDistal' in data.fingerPoints):
        fingerTip = data.fingerPoints['IndexDistal'][3:]
        fingerDirection = [data.indexDir[0], data.indexDir[1], data.indexDir[2]]
        planePoint =  [0, 0, -212] #hardcoded to my computer width, but could take input later
        planeNormal = [0, 0, 1] #hardcoded to my computer angle, which is 90 deg, but could take input later
        data.intersect = list(planeIntersection(data, planeNormal, planePoint, fingerDirection, fingerTip))
        corner = [-152, 212, -212] 
        data.intersect = [data.scalar * abs(corner[0] - data.intersect[0]), data.scalar * (corner[1] - data.intersect[1])]
def planeIntersection(data, planeNormal, planePoint, rayDirection, rayPoint):
    epsilon=1e-6
    planeNormal = np.array(planeNormal)
    planePoint = np.array(planePoint)
    #Define ray
    rayDirection = np.array(rayDirection)
    rayPoint = np.array(rayPoint) #Any point along the ray
    ndotu = planeNormal.dot(rayDirection) 

    if abs(ndotu) < epsilon: #line and plane are parallel
        return None 
    else:
        w = rayPoint - planePoint
        si = -planeNormal.dot(w) / ndotu
        Psi = w + si * rayDirection + planePoint
        return Psi
def getHit(data):
    if(data.target.gotHit(data.intersect[0], data.intersect[1], 5) and data.trigger == 'green'):
        newDot = Dot(data.width, data.height)
        data.target = newDot
        data.points += 1
def drawFingerLines(canvas, data):
    for key, val in data.fingerPoints.items():
        canvas.create_line(val[0], 300 - val[2], val[3], 300 - val[5], fill = data.trigger)
    if(len(data.distA) > 2 and len(data.distB) > 2):
        canvas.create_line(data.distA[0], 3000 - data.distA[2], data.distB[0], 3000 - data.distB[2], fill = data.trigger)
def drawScreenIntersect(canvas,data):
    getHit(data)
    txt = str(int(data.intersect[0])) + ' , ' + str(int(data.intersect[1]))
    canvas.create_oval(data.intersect[0] - 5, data.intersect[1] - 5, data.intersect[0] + 5, data.intersect[1] + 5, fill = data.trigger)
    canvas.create_text(data.intersect[0], data.intersect[1], text = txt)
def drawTarget(canvas, data):
    canvas.create_oval(data.target.x - data.target.r, data.target.y - data.target.r, data.target.x + data.target.r, data.target.y + data.target.r, fill = 'red')
    txt = str(data.target.x) + ' , ' + str(data.target.y)
    canvas.create_text(data.target.x, data.target.y, text = txt)
def getTriggerDistance(data, a0,a1,b0,b1,clampAll=False,clampA0=False,clampA1=False,clampB0=False,clampB1=False):

    ''' Given two lines defined by numpy.array pairs (a0,a1,b0,b1)
        Return the closest points on each segment and their distance
    '''

    # If clampAll=True, set all clamps to True
    if clampAll:
        clampA0=True
        clampA1=True
        clampB0=True
        clampB1=True


    # Calculate denomitator
    A = a1 - a0

    B = b1 - b0
  
    magA = np.linalg.norm(A)
    magB = np.linalg.norm(B)

    _A = A / magA
    _B = B / magB

    cross = np.cross(_A, _B);

    denom = np.linalg.norm(cross)**2


    # If lines are parallel (denom=0) test if lines overlap.
    # If they don't overlap then there is a closest point solution.
    # If they do overlap, there are infinite closest positions, but there is a closest distance
    if not denom:
        d0 = np.dot(_A,(b0-a0))

        # Overlap only possible with clamping
        if clampA0 or clampA1 or clampB0 or clampB1:
            d1 = np.dot(_A,(b1-a0))

            # Is segment B before A?
            if d0 <= 0 >= d1:
                if clampA0 and clampB1:
                    if np.absolute(d0) < np.absolute(d1):
                        return a0,b0,np.linalg.norm(a0-b0)
                    return list(a0),list(b1),np.linalg.norm(a0-b1)


            # Is segment B after A?
            elif d0 >= magA <= d1:
                if clampA1 and clampB0:
                    if np.absolute(d0) < np.absolute(d1):
                        return list(a1),list(b0),np.linalg.norm(a1-b0)
                    return list(a1),list(b1),np.linalg.norm(a1-b1)

        # Segments overlap, return distance between parallel segments
        return None,None,np.linalg.norm(((d0*_A)+a0)-b0)



    # Lines criss-cross: Calculate the projected closest points
    t = (b0 - a0);
    detA = np.linalg.det([t, _B, cross])
    detB = np.linalg.det([t, _A, cross])

    t0 = detA/denom;
    t1 = detB/denom;

    pA = a0 + (_A * t0) # Projected closest point on segment A
    pB = b0 + (_B * t1) # Projected closest point on segment B


    # Clamp projections
    if clampA0 or clampA1 or clampB0 or clampB1:
        if clampA0 and t0 < 0:
            pA = a0
        elif clampA1 and t0 > magA:
            pA = a1

        if clampB0 and t1 < 0:
            pB = b0
        elif clampB1 and t1 > magB:
            pB = b1

        # Clamp projection A
        if (clampA0 and t0 < 0) or (clampA1 and t0 > magA):
            dot = np.dot(_B,(pA-b0))
            if clampB0 and dot < 0:
                dot = 0
            elif clampB1 and dot > magB:
                dot = magB
            pB = b0 + (_B * dot)

        # Clamp projection B
        if (clampB0 and t1 < 0) or (clampB1 and t1 > magB):
            dot = np.dot(_A,(pB-a0))
            if clampA0 and dot < 0:
                dot = 0
            elif clampA1 and dot > magA:
                dot = magA
            pA = a0 + (_A * dot)


    return list(pA),list(pB),np.linalg.norm(pA-pB)
def redrawAll(canvas, data):
    drawTarget(canvas, data)
    drawFingerLines(canvas, data)
    drawScreenIntersect(canvas,data)
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
    data.timerDelay = 20 # milliseconds
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

run(2000, 1000)

