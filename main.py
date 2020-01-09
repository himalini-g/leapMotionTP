
################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights rebrved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################
from Tkinter import *
import Leap, sys, time, math, thread
import numpy as np
import gunGraphics
import gameGraphics
import gameElements
import splashScreen
import helpScreen
import pauseScreen
import gunStore
import music

def init(data):
    backGroundMusic = thread(music.play, ('darkAmbient.wav',))
    backGroundMusic.start()
    data.controller = Leap.Controller()
    data.frame = data.controller.frame()
    data.fingerNames = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    data.boneNames = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    data.fingerPoints = {}
    data.dist = 0
    data.fingerWidth = [0, 0, 0, 0, 0]
    data.trigger = 'white'
    data.intersect = [0, 0]
    data.intersectR = 5
    data.mode = 'Splash'
    data.scalar =  2.83464566929  #root.winfo_fpixels('1m') is how I came to the number, but I can't use this in the constructor
    data.gunCounter = 0
    data.fireAngle = 0
    data.gunsPurchased = [gunGraphics.HandGun(data.width, data.height)]
    data.gun = data.gunsPurchased[0]
    data.walls = []
    data.gunsInStore = [gunGraphics.ShotGun(data.width, data.height), gunGraphics.MachineGun(data.width, data.height), gunGraphics.Revolver(data.width, data.height)]
    data.batEnemies = {}
    gameGraphics.initialized(data)
    data.counter = 0
    data.health = 200
    data.score = 0
    data.gameOver = False
    data.firing = False
    data.fontFill = 'white'
    data.playBox = [(data.width - 140, 15), (data.width - 25, 50)] 
    data.helpBox = [(data.width - 140 + 20,  15 + 40), (data.width - 140 + 115, 50 + 40)]
    data.pauseBox = [(data.width - 140, 15), (data.width - 25, 50)]
    data.storeBox = [(data.width - 160 + 25,  15 + 40 + 40), (data.width - 160 + 130, 50 + 40 + 40)]
    data.timeScale = float(data.timerDelay) / 1000
    data.mouseX = 0
    data.mouseY = 0
    data.intersectListX = []
    data.intersectListY = []
    with open('currency.txt', 'rt') as f:
        data.currency =  int(f.read())
def gameOver(data):
    with open('currency.txt', "wt") as f:
        f.write(str(data.currency))
def checkGameOver(data):
    if(data.health < 0):
        gameOver(data)
        data.mode = 'gameOver'
def updateLeapMotionData(data):
    data.frame = data.controller.frame()
def getLeapMotionData(data):
    # Get the most recent frame and report some basic information
    frame = data.frame
    # Get hands
    for hand in frame.hands:
        for finger in [hand.fingers[0], hand.fingers[1]]:
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
            data.trigger = 'white'
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
        data.intersect = [data.scalar * abs(corner[0] - data.intersect[0]), \
                          data.scalar * (corner[1] - data.intersect[1])]
        deltaX =  data.intersect[0] - data.width // 2
        deltaY = data.height -data.intersect[1]
        data.fireAngle = math.atan2(deltaY, deltaX) 
        if(len(data.intersectListX) < 5):
            data.intersectListX.insert(0, data.intersect[0])
            data.intersectListY.insert(0, data.intersect[1])
        else:
            data.intersectListX.insert(0, data.intersect[0])
            data.intersectListY.insert(0, data.intersect[1])
            data.intersectListX.pop()
            data.intersectListY.pop()
            #data.intersect = [sum(data.intersectListX) // 5, sum(data.intersectListY) // 5]
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
def keyPressed(event, data):
    if(event.keysym == 'l'):
        data.gameOver = True
        data.mode = 'gameOver'
        gameOver(data)
    elif(event.keysym == 'c'):
        data.currency += 100
    elif(event.keysym == 'g'):
        data.gunsPurchased.extend(data.gunsInStore)
    elif(event.keysym == 'space'):
        data.gunCounter += 1
        data.gun = data.gunsPurchased[data.gunCounter % len(data.gunsPurchased)]
def mousePressed(event, data):
    data.mouseX = event.x
    data.mouseY = event.y
    if(data.mode == 'Splash'):
        splashScreen.changeModes(data)
    if(data.mode == 'Playing'):
        gameElements.changeModes(data)
    elif(data.mode == 'Paused'):
        pauseScreen.changeModes(data)
    elif(data.mode == 'Help'):
        helpScreen.changeModes(data)
    elif(data.mode == 'gunStore'):
        gunStore.changeModes(data)
    elif(data.mode == 'gameOver'):
        gameElements.changeModes(data)
def timerFired(data):
    if(data.mode == 'Splash'):
        pass
    elif(data.mode == 'Paused'):
        pass
    elif(data.mode == 'Help'):
        pass
    elif(data.mode == 'gunStore'):
        gunStore.timerFired(data)
    elif(data.mode == 'gameOver'):
        pass
    elif(data.mode == 'restart'):
        init(data)
    else:
        data.gun.timePassed += 1
        data.counter += 1
        updateLeapMotionData(data)
        getLeapMotionData(data)
        getTrigger(data)
        getAim(data)
        getEnemyHit(data)
        checkGameOver(data)
        if(data.counter % 2 == 0):
            gameGraphics.timerFired(data)
            
def hitBox(data, enemy):
    for box in enemy.boundingBox:
        if(box[0][0] - data.intersectR < data.intersect[0] < box[1][0] + data.intersectR  and \
            box[0][1] - data.intersectR < data.intersect[1] < box[1][1] + data.intersectR and data.trigger == 'green'):
            return True
    return False
def reloadGun(data):
    data.gun.ammo = data.gun.capacity
    reload = threading.Thread(target=music.play,\
                         args=('handGunReload.wav',))
    
    reload.start()
def getEnemyHit(data):
    if(data.gun.ammo <= 0):
        reloadGun(data)
    for enemy in [data.batEnemies, data.spiderEnemies]:
        for key, lst in enemy.items():
            for enemy in lst:
                if(hitBox(data, enemy) and data.gun.timePassed * data.timeScale > data.gun.shootGap):
                    data.score += 1
                    data.currency += 1
                    data.gun.timePassed = 0
                    enemy.isDead = True
                    data.hitX = data.intersect[0]
                    data.hitY = data.intersect[1]
                    data.firing = True
                    data.gun.ammo -= 1
                    shot = threading.Thread(target=music.play,\
                         args=(data.gun.noiseList[data.gun.counter % len(data.gun.noiseList)],))
                    shot.start()
                    data.gun.counter += 1

def redrawAll(canvas, data):
    if(data.mode == 'Splash'):
        splashScreen.redrawAll(canvas, data)
    elif(data.mode == 'Playing'):
        gameGraphics.redrawAll(canvas, data)
        gameElements.redrawAll(canvas, data)
        gunGraphics.redrawAll(canvas, data)
    elif(data.mode == 'Paused'):
        pauseScreen.redrawAll(canvas, data)
    elif(data.mode == 'gunStore'):
        gunStore.redrawAll(canvas, data)
    elif(data.mode == 'Help'):
        helpScreen.redrawAll(canvas, data)
    elif(data.mode == 'demo'):
        pass
    elif(data.mode == 'gameOver'):
        gameElements.gameOverScreen(canvas, data)
    

#CMU Graphics cite: https://gitlab.com/mattzjack/af2
#it's for the specific graphics framework I'm using for python2
#https://www.cs.cmu.edu/~112/notes/cmu_112_graphics.py


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

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
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
    data.timerDelay = 10 # milliseconds
    # create the root and the canvas
    root = Tk()
    init(data)
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    
    timerFiredWrapper(canvas, data)
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    # and launch the app
    root.mainloop()  # blocks until window is closed
    backGroundMusic.stop()
    print("bye!")
def main():
    
    run(1450, 750)
main()

