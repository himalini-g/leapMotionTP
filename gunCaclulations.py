
################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################
from Tkinter import *
import Leap, sys, thread, time
import numpy as np
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import gunGraphics
from thread import start_new_thread

def init(data):
    data.controller = Leap.Controller()
    data.frame = data.controller.frame()
    data.fingerNames = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    data.boneNames = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    data.fingerPoints = {}
    data.dist = 0
    data.fingerWidth = [0, 0, 0, 0, 0]
    data.trigger = 'black'
    data.intersect = [0, 0]
    data.mode = ['gunGraphics']
    data.scalar =  2.83464566929  #root.winfo_fpixels('1m') is how I came to the number, but I can't use this in the constructor
def updateLeapMotionData(data):
    data.frame = data.controller.frame()
def getLeapMotionData(data):
    # Get the most recent frame and report some basic information
    frame = data.frame
    # Get hands
    for hand in frame.hands:
        for finger in hand.fingers:
            data.fingerWidth[finger.type] = finger.width
            # Get bones
            for b in range(0, 4):
                bone = finger.bone(b)
                name = data.fingerNames[finger.type] + data.boneNames[bone.type]
                if(name == 'IndexDistal'):
                    data.indexDir = bone.direction
                data.fingerPoints[name] = []
                for joint in [bone.prev_joint, bone.next_joint]:
                    data.fingerPoints[name].extend([joint[0], joint[1], joint[2]])
    
def getTrigger(data):
    if('ThumbDistal' in data.fingerPoints and 'IndexMetacarpal' in data.fingerPoints):
        a0 = np.array(data.fingerPoints['ThumbDistal'][:3])
        a1 = np.array(data.fingerPoints['ThumbDistal'][3:])
        b0 = np.array(data.fingerPoints['IndexMetacarpal'][:3])
        b1 = np.array(data.fingerPoints['IndexMetacarpal'][3:])
        distA, distB, data.dist = getTriggerDistance(data, a0,a1,b0,b1)
        if(data.dist < data.fingerWidth[0] + data.fingerWidth[1] - 7):
            data.trigger = 'green'
        else:
            data.trigger = 'black'
#Code for plane intersection from: https://stackoverflow.com/questions/5666222/3d-line-plane-intersection
#user who posted it: https://stackoverflow.com/users/4288232/timsc
def getAim(data):
    if('IndexDistal' in data.fingerPoints):
        fingerTip = data.fingerPoints['IndexDistal'][3:]
        fingerDirection = [data.indexDir[0], data.indexDir[1], data.indexDir[2]]
        planePoint =  [0, 0, -212] #hardcoded to my computer width, but could take input later
        planeNormal = [0, 0, 1] #hardcoded to my computer angle, which is 90 deg, but could take input later
        data.intersect = list(planeIntersection(data, planeNormal, planePoint, fingerDirection, fingerTip))
        corner = [-152, 212, -212]
        data.intersect = [data.scalar * abs(corner[0] - data.intersect[0]), data.scalar * (corner[1] - data.intersect[1])]
#got this off of stack overflow from this user: https://stackoverflow.com/users/4288232/timsc
# on this post: #https://stackoverflow.com/questions/5666222/3d-line-plane-intersection
#Based on http://geomalgorithms.com/a05-_intersect-1.html
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
#from stack overflow user: https://stackoverflow.com/users/1429402/fnord
#on this post: https://stackoverflow.com/questions/2824478/shortest-distance-between-two-line-segments
def getTriggerDistance(data, a0,a1,b0,b1):
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
        d1 = np.dot(_A,(b1-a0))
            # Is segment B before A?
        if d0 <= 0 >= d1:
            if np.absolute(d0) < np.absolute(d1):
                return a0,b0,np.linalg.norm(a0-b0)
            return a0,b1,np.linalg.norm(a0-b1)
        # Is segment B after A?
        elif d0 >= magA <= d1:
            if np.absolute(d0) < np.absolute(d1):
                return a1,b0,np.linalg.norm(a1-b0)
            return a1,b1,np.linalg.norm(a1-b1)


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
    if t0 < 0:
        pA = a0
    elif t0 > magA:
        pA = a1

    if t1 < 0:
        pB = b0
    elif t1 > magB:
        pB = b1

    # Clamp projection A
    if (t0 < 0) or (t0 > magA):
        dot = np.dot(_B,(pA-b0))
        if dot < 0:
            dot = 0
        elif dot > magB:
            dot = magB
        pB = b0 + (_B * dot)

    # Clamp projection B
    if (t1 < 0) or (t1 > magB):
        dot = np.dot(_A,(pB-a0))
        if dot < 0:
            dot = 0
        elif dot > magA:
            dot = magA
        pA = a0 + (_A * dot)
    return list(pA),list(pB),np.linalg.norm(pA-pB)
def timerFired(data):
    updateLeapMotionData(data)
    getLeapMotionData(data)
    getTrigger(data)
    getAim(data)
    if('gunGraphics' in data.mode):
        gunGraphics.timerFired
def redrawAll(canvas, data):
    gunGraphics.redrawAll(canvas, data)
def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

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
    # create the root and the canvas
    root = Tk()
    init(data)
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")
run(1200, 600)
