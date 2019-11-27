import random, math, copy
from Tkinter import *

class Bat():
    ID = 0
    def __init__(self, scale, cx, cy, iD):
        self.wallID = iD
        self.id = Bat.ID
        Bat.ID += 1
        self.scale = scale
        self.bodyColor = 'grey23'
        self.eyeColor = 'yellow'
        
        self.cx = cx
        self.cy = cy
        
        self.stateIndex = 0 
        self.leftEyeFrame = self.getLeftEyeFrame()
        self.rightEyeFrame = self.getRightEyeFrame()
        self.bodyFrame = self.getBodyFrame()
        self.headFrame = self.getHeadFrame()
        self.heightIncrements = [4, 5, -5, -4, 3]
        self.rightWingStates = self.getRightWingStates()
        self.leftWingStates = self.getLeftWingStates()
        index = random.randint(0, len(self.rightWingStates) - 1)
        self.rightWingFrame = self.rightWingStates[index]
        self.leftWingFrame  = self.leftWingStates[index]
        self.counter = 0
    def getLeftEyeFrame(self):
        cx, cy, scale = self.cx, self.cy , self.scale
        return [(cx - scale  * 0.15, cy - scale * 1.2), (cx - scale * 0.03 , cy - scale * 1.1),
                (cx - scale  * 0.15, cy - scale * 1), (cx - scale  * 0.25, cy - scale * 1.12)]
    def getRightEyeFrame(self):
        cx, cy, scale = self.cx, self.cy , self.scale
        return [(cx + scale  * 0.15, cy - scale * 1.2), (cx + scale * 0.03, cy - scale * 1.1),
                (cx + scale  * 0.15, cy - scale * 1), (cx + scale  * 0.25, cy - scale * 1.12)]
    def getBodyFrame(self):
        cx, cy, scale = self.cx, self.cy , self.scale
        return [(cx, cy + scale), (cx - scale // 5, cy + scale // 2), 
                (cx - scale // 2, cy - scale // 2), (cx , cy - scale),
                (cx + scale // 2, cy - scale // 2), (cx + scale // 5, cy + scale // 2),
                (cx, cy + scale)]
    def getHeadFrame(self):
        cx, cy, scale = self.cx, self.cy , self.scale
        return [(cx, cy - scale // 2), (cx - scale // 3, cy - scale),
                (cx - scale // 3, cy - scale * 1.5), (cx - scale // 6, cy - scale * 1.3),
                (cx + scale // 6, cy - scale * 1.3), (cx + scale // 3, cy - scale * 1.5),
                (cx + scale // 3, cy - scale), (cx, cy - scale // 2)]

    def getRightWingStates(self, indx = None):
        cx, cy, scale = self.cx, self.cy , self.scale
        lst = [[(cx, cy - scale // 2), (cx + scale * 0.9 , cy - scale * 1.3), (cx + scale * 2.6, cy - scale * 2 ), (cx + scale * 2.1, cy - scale * 0.6), 
            (cx + scale * 1, cy - scale * 0.2), (cx, cy - scale // 2)], [(cx, cy - scale // 2), (cx + scale * 0.8 , cy - scale * 1.3),(cx + scale * 1.6, cy - scale * 3 ), (cx + scale * 2.1, cy - scale * 1),
            (cx + scale * 1, cy - scale * 0.2), (cx, cy - scale // 2)],
            [(cx, cy - scale // 2), (cx + scale * 0.9 , cy - scale * 1.3), 
            (cx + scale * 2.6, cy - scale * 2 ), (cx + scale * 2.1, cy - scale * 0.6),
            (cx + scale * 1, cy - scale * 0.2), (cx, cy - scale // 2)],
            [(cx, cy - scale // 2), (cx + scale * 0.9 , cy ),
            (cx + scale * 1.4 , cy + scale * 0.6),
            (cx + scale * 1.7, cy + scale * 1.6 ), (cx + scale * 0.7, cy + scale * 1.3),
            (cx + scale * 0.4, cy + scale * 0.2), (cx, cy - scale // 2)],
            [(cx, cy - scale // 2), (cx + scale * 0.9, cy - scale), 
            (cx + scale * 1.9 , cy - scale * 0.9),
            (cx + scale * 3, cy ), (cx + scale * 2, cy + scale * 0.2),
            (cx + scale * 1, cy + scale * 0.2), (cx, cy - scale // 2)]]

        if(indx == None):
            return lst
        else:
            return lst[indx]
    def getLeftWingStates(self, indx = None):
        cx, cy, scale = self.cx, self.cy, self.scale
        lst = [[(cx, cy - scale // 2), (cx - scale * 0.9 , cy - scale * 1.3), 
            (cx - scale * 2.6, cy - scale * 2 ), (cx - scale * 2.1, cy - scale * 0.6), 
            (cx - scale * 1, cy - scale * 0.2), (cx, cy - scale // 2)], [(cx, cy - scale // 2), 
            (cx - scale * 0.8 , cy - scale * 1.3),(cx - scale * 1.6, cy - scale * 3 ), 
            (cx -scale * 2.1, cy - scale * 1),
            (cx - scale * 1, cy - scale * 0.2), (cx, cy - scale // 2)],
            [(cx, cy - scale // 2), (cx - scale * 0.9 , cy - scale * 1.3), 
            (cx - scale * 2.6, cy - scale * 2 ), (cx - scale * 2.1, cy - scale * 0.6),
            (cx - scale * 1, cy - scale * 0.2), (cx, cy - scale // 2)],
            [(cx, cy - scale // 2), (cx - scale * 0.9 , cy ),
            (cx - scale * 1.4 , cy + scale * 0.6),
            (cx - scale * 1.7, cy + scale * 1.6 ), (cx - scale * 0.7, cy + scale * 1.3),
            (cx - scale * 0.4, cy + scale * 0.2), (cx, cy - scale // 2)],
            [(cx, cy - scale // 2), (cx - scale * 0.9, cy - scale), 
            (cx - scale * 1.9 , cy - scale * 0.9),
            (cx - scale * 3, cy ), (cx - scale * 2, cy + scale * 0.2),
            (cx - scale * 1, cy + scale * 0.2), (cx, cy - scale // 2)]]
        if(indx == None):
            return lst
        else:
            return lst[indx]
    def scaleBat(self, width, height):
        self.counter += 1
        scalar = 0.04
        playerX = width // 2
        playerY = height // 2
        interval = math.sqrt(self.cx**2 + playerX**2) // 20
        self.cx += interval

        self.scale += 2
        self.animate()
    def animate(self):
        self.counter += 1
        self.cy += self.heightIncrements[self.counter % 5]
        
        self.rightWingFrame = self.getRightWingStates(self.counter % 5, )
        self.leftWingFrame = self.getLeftWingStates(self.counter % 5)
        self.bodyFrame = self.getBodyFrame()
        self.headFrame = self.getHeadFrame()
        self.leftEyeFrame = self.getLeftEyeFrame()
        self.rightEyeFrame = self.getRightEyeFrame()
 
    def getPoints(self):
        pass
    def blink(self):
        pass

class Spider():
    ID = 0
    def __init__(self, scale, cx, cy, threadLength, iD):
        self.id = Spider.ID
        self.wallID = iD
        self.scale = scale
        self.bodyColor = 'grey23'
        self.eyeColor = 'yellow'
        self.cx, self.cy = cx, cy
        self.thread = [(self.cx, cy - 3), (self.cx, self.cy + threadLength + 3)]
        cx, cy, s = self.cx, self.cy + threadLength, self.scale
        self.bodyFrame = [(cx, cy ), (cx - s * 2 // 3, cy + s // 2),(cx - s * 2 // 3, cy + s * 3 // 2),
                          (cx, cy + s * 2), (cx + s * 2 // 3, cy + s * 3 // 2),
                          (cx + s * 2 // 3, cy + s // 2), (cx, cy )]
        self.headFrame = [(cx, cy + s * 1.8), (cx - s // 2.7, cy + s * 2),
                         (cx - s // 2.7, cy + s * 2.3), (cx, cy + s * 2.5),
                         (cx + s // 2.7, cy + s * 2.3), (cx + s // 2.7, cy + s * 2),
                         (cx, cy + s * 1.8)]
       
        self.eyeFrames = [[(cx - s  * 0.18 , cy + s * 2.25), (cx - s * 0.13 , cy + s * 2.3),
                        (cx - s  * 0.18, cy + s * 2.35), (cx - s * 0.23, cy + s * 2.3)],
                        [(cx - s  * 0.07 , cy + s * 2.30), (cx - s * 0.02 , cy + s * 2.35),
                        (cx - s  * 0.07, cy + s * 2.40), (cx - s * 0.12, cy + s * 2.35)],
                        [(cx + s  * 0.07 , cy + s * 2.30), (cx + s * 0.02 , cy + s * 2.35),
                        (cx + s  * 0.07, cy + s * 2.40), (cx + s * 0.12, cy + s * 2.35)],
                        [(cx + s  * 0.18 , cy + s * 2.25), (cx + s * 0.13 , cy + s * 2.3),
                        (cx + s  * 0.18, cy + s * 2.35), (cx + s * 0.23, cy + s * 2.3)]]
        
        self.leftLegFrames = [[(cx - s * 0.66, cy + s * 1.4 ), (cx - s * 4 // 3, cy + s * 1.5), (cx - s * 0.9, cy + s * 2 )],
                            [(cx - s * 0.66, cy + s * 1.2 ), (cx - s * 4 // 3, cy + s * 1.1), (cx - s * 1.5, cy + s * 1.7 )],
                            [(cx - s * 0.66, cy + s * 1 ), (cx - s * 4 // 3, cy + s * 0.8), (cx - s * 1.8, cy + s * 1.4 )],
                            [(cx - s * 0.66, cy + s * 0.8 ), (cx - s , cy + s * 0.6), (cx - s * 1.7, cy + s * 1 )]]
        self.rightLegFrames = [[(cx + s * 0.66, cy + s * 1.4 ), (cx + s * 4 // 3, cy + s * 1.5), (cx + s * 0.9, cy + s * 2 )],
                            [(cx + s * 0.66, cy + s * 1.2 ), (cx + s * 4 // 3, cy + s * 1.1), (cx + s * 1.5, cy + s * 1.7 )],
                            [(cx + s * 0.66, cy + s * 1 ), (cx + s * 4 // 3, cy + s * 0.8), (cx + s * 1.8, cy + s * 1.4 )],
                            [(cx + s * 0.66, cy + s * 0.8 ), (cx + s , cy + s * 0.6), (cx + s * 1.7, cy + s * 1 )]]
        self.stateIndex = 0 
        self.counter = 0
        Spider.ID += 1
    def hash(self):
        return hash(self.id)
    def comeDownThread(self, speed):
        self.cy += speed * 5
        cx, cy, s = self.cx, self.cy, self.scale
        self.thread = [(self.cx, 0), (self.cx, self.cy)]
        self.bodyFrame = [(cx, cy ), (cx - s * 2 // 3, cy + s // 2),(cx - s * 2 // 3, cy + s * 3 // 2),
                            (cx, cy + s * 2), (cx + s * 2 // 3, cy + s * 3 // 2),
                            (cx + s * 2 // 3, cy + s // 2), (cx, cy )]
        self.headFrame = [(cx, cy + s * 1.8), (cx - s // 2.7, cy + s * 2),
                            (cx - s // 2.7, cy + s * 2.3), (cx, cy + s * 2.5),
                            (cx + s // 2.7, cy + s * 2.3), (cx + s // 2.7, cy + s * 2),
                            (cx, cy + s * 1.8)]
        self.eyeFrames = [[(cx - s  * 0.18 , cy + s * 2.25), (cx - s * 0.13 , cy + s * 2.3),
                        (cx - s  * 0.18, cy + s * 2.35), (cx - s * 0.23, cy + s * 2.3)],
                        [(cx - s  * 0.07 , cy + s * 2.30), (cx - s * 0.02 , cy + s * 2.35),
                        (cx - s  * 0.07, cy + s * 2.40), (cx - s * 0.12, cy + s * 2.35)],
                        [(cx + s  * 0.07 , cy + s * 2.30), (cx + s * 0.02 , cy + s * 2.35),
                        (cx + s  * 0.07, cy + s * 2.40), (cx + s * 0.12, cy + s * 2.35)],
                        [(cx + s  * 0.18 , cy + s * 2.25), (cx + s * 0.13 , cy + s * 2.3),
                        (cx + s  * 0.18, cy + s * 2.35), (cx + s * 0.23, cy + s * 2.3)]]
        self.leftLegFrames = [[(cx - s * 0.66, cy + s * 1.4 ), (cx - s * 4 // 3, cy + s * 1.5), (cx - s * 0.9, cy + s * 2 )],
                            [(cx - s * 0.66, cy + s * 1.2 ), (cx - s * 4 // 3, cy + s * 1.1), (cx - s * 1.5, cy + s * 1.7 )],
                            [(cx - s * 0.66, cy + s * 1 ), (cx - s * 4 // 3, cy + s * 0.8), (cx - s * 1.8, cy + s * 1.4 )],
                            [(cx - s * 0.66, cy + s * 0.8 ), (cx - s , cy + s * 0.6), (cx - s * 1.7, cy + s * 1 )]]
        self.rightLegFrames = [[(cx + s * 0.66, cy + s * 1.4 ), (cx + s * 4 // 3, cy + s * 1.5), (cx + s * 0.9, cy + s * 2 )],
                            [(cx + s * 0.66, cy + s * 1.2 ), (cx + s * 4 // 3, cy + s * 1.1), (cx + s * 1.5, cy + s * 1.7 )],
                            [(cx + s * 0.66, cy + s * 1 ), (cx + s * 4 // 3, cy + s * 0.8), (cx + s * 1.8, cy + s * 1.4 )],
                            [(cx + s * 0.66, cy + s * 0.8 ), (cx + s , cy + s * 0.6), (cx + s * 1.7, cy + s * 1 )]]
        self.animateEyes()
    def animateEyes(self):

        for eye in self.eyeFrames:
            if(eye[0][1] < eye[2][1]):
                eye[2] = (eye[2][0], eye[2][1] - 1)
            else:
                eye[2] = (eye[2][0], eye[2][1] + 5)
    def scaleColor(self):
        if(self.counter % 2 == 0):
            numColor = int(self.bodyColor[4:])
            numColor += 1
            if(numColor > 98):
                self.bodyColor = 'grey99'
            else: self.bodyColor = 'grey' + str(numColor)
    def scaleSpider(self, width, height):
    
        scalar = 0.04

        self.counter += 1
        newEyes = []
        for eye in self.eyeFrames:
            newEyes.append([])
            for point in eye:
                xNew = (scalar * (point[0] - (width // 2))) + point[0]
                yNew = (scalar * (point[1] - (height // 2))) + point[1]
              
                newEyes[-1].append((xNew, yNew))
        self.eyeFrames= copy.copy(newEyes)
        lgs = []
        for st in [self.leftLegFrames, self.rightLegFrames]:
            newLegs = []
            for leg in st:
                newLegs.append([])
                for point in leg:
                    xNew = (scalar * (point[0] - (width // 2))) + point[0]
                    yNew = (scalar * (point[1] - (height // 2))) + point[1]
                    newLegs[-1].append((xNew, yNew))
            lgs.append(newLegs)
        self.leftLegFrames, self.rightLegFrames = lgs[0], lgs[1]

        newBodyFrame = []
        for point in self.bodyFrame:
            xNew = (scalar * (point[0] - (width // 2))) + point[0]
            yNew = (scalar * (point[1] - (height // 2))) + point[1]
            newBodyFrame.append((xNew, yNew))
        self.bodyFrame = copy.copy(newBodyFrame)
        newHeadFrame = []
        for point in self.headFrame:
            xNew = (scalar * (point[0] - (width // 2))) + point[0]
            yNew = (scalar * (point[1] - (height // 2))) + point[1]
            newHeadFrame.append((xNew, yNew))
        self.headFrame = copy.copy(newHeadFrame)

        newThread = []
        for point in self.thread:
            xNew = (scalar * (point[0] - (width // 2))) + point[0]
            yNew = (scalar * (point[1] - (height // 2))) + point[1]
            newThread.append((xNew, yNew))
        self.thread = copy.copy(newThread)

        self.scaleColor()
        
        if(self.bodyColor == 'grey26'):
            return True
        return False            
class Wall():
    ID = 0
    def __init__(self, width, height, layer):
        self.id = Wall.ID
        self.width = width
        self.height = height
        self.colorChoices = [ 'grey24','grey21', 'grey18', 'grey15', 'grey12']
        self.stalactites = self.generatePoints(width, height, -1, layer)
        self.stalagmites = self.generatePoints(width, height, 1, layer)
        self.color = self.colorChoices[layer]
        self.left, self.right = self.makeEdges(width, height, self.stalactites, self.stalagmites)
        self.layer = layer
        self.counter = 0
        self.generateTexture()
      
        Wall.ID += 1
    def makeEdges(self, width, height, stalactites, stalagmites):
        minX = min(stalactites[2][0], stalagmites[2][0])
        x, x1 = min(stalactites[2][0],stalagmites[2][0]), max(stalactites[2][0],stalagmites[2][0])
        y, y1 = min(stalactites[2][1],stalagmites[2][1]), max(stalactites[2][1],stalagmites[2][1])
        averageX = random.randint(x - 5, x1 + 5)
        averageY = random.randint(y - 5, y1 + 5)
        right = [(stalagmites[2][0], height), stalagmites[2], (averageX, averageY), stalactites[2], (stalactites[2][0], 0), (width, 0), (width, height), (stalagmites[2][0], height)]
        minX = min(stalactites[-3][0], stalagmites[-3][0])
        x, x1 = min(stalactites[-3][0],stalagmites[-3][0]), max(stalactites[-3][0],stalagmites[-3][0])
        y, y1 = min(stalactites[-3][1],stalagmites[-3][1]), max(stalactites[-3][1],stalagmites[-3][1])
        averageX = random.randint(x - 5, x1 + 5)
        averageY = random.randint(y - 5, y1 + 5)

        left = [stalagmites[-3], (averageX, averageY), stalactites[-3], (stalactites[-3][0], 0), (0, 0), (0, height), (stalagmites[-3][0], height),stalagmites[-3] ]
        return left, right

    def generatePoints(self, width, height, d, layer):
        wRange = [(1.3, 1.6 ), (1.1, 1.3), (0.5, 0.8), (0.22, 0.5), (0.1, 0.22)]
        hRange = [(7.6, 9.5), (6.5, 7.5), (5.5, 6.5), (4.5, 5.5), (3.5, 4.5)]
        if(d == 1):
            points = [(width, height)]
        else:
            points = [(width, 0)]

        wd = random.random()*(wRange[layer][1] - wRange[layer][0]) + wRange[layer][0]
        hd = random.random()*(hRange[layer][1] - hRange[layer][0]) + hRange[layer][0]
        
        highLine = lambda w, h, x, d, wd, hd: d * math.sqrt(-wd *((((x - (w // 2))**2) / hd) - 75000)) + h // 2 #don't hardcode
        
        x = int(math.sqrt(75000 * hd) + width // 2) - 3

        high = x
        low = high - (width // 9)
        x = random.randint(low, high)
        points.append((x , int(highLine(width, height, x, d, wd, hd))))

        for i in range(20):
            div = random.randint(5, 15)
            high = points[len(points) - 1][0]
            low = high - (width // div)
            x = int(random.randint(low, high))
            while(x < 0):
                x = int(random.randint(low, high))
            try:
                
                points.append((x, int(highLine(width, height, x, d, wd, hd))))
            except:
           
                points.append(points[-1])
            last = len(points) - 1
            average =  points[last - 1][0] - points[last][0]
            y = (points[last][1] + points[last - 1][1]) // 2
            y += -d * random.randint(int((average * .7)), int((average* 1.3)))

            points.insert(last, (points[last - 1][0] - average // 2, y))
        if(d == 1):
            points.append((0, height))
            points.append((width, height))
        else:
            points.append((0, 0))
            points.append((width, 0))

        return points
    def generateTexture(self):

        texturedStalagmites = [self.stalagmites[0]]
        texturedStalactites = [self.stalactites[0]]

        for indx in range(1, len(self.stalagmites)):
            line = lambda x: (self.stalagmites[indx + 1][1] - self.stalagmites[indx][1])/ (self.stalagmites[indx + 1][0] - self.stalagmites[indx][0]) * (x - self.stalagmites[indx][0]) + self.stalagmites[indx][1]
            texturedStalagmites.append(self.stalagmites[indx])
            if(indx + 1 < len(self.stalagmites) - 3):
                bottomX = self.stalagmites[indx][0]
                bottomY = self.stalagmites[indx][1]
                counter = 0
                r = (self.stalagmites[indx + 1][0] - self.stalagmites[indx][0]) // 20
                delta = (self.stalagmites[indx + 1][1] - self.stalagmites[indx][1])
                for x in range(abs(r)):
                    y = line(bottomX)
                    y = random.randint(y - 5, y + 5)
                    texturedStalagmites.append((bottomX, y))
                    bottomX -= 20

        texturedStalagmites.extend([self.stalagmites[-2], self.stalagmites[-1]])
        self.stalagmites = copy.copy(texturedStalagmites)
        
        
        for indx in range(1, len(self.stalactites) - 2):
            texturedStalactites.append(self.stalactites[indx])
            line = lambda x: (self.stalactites[indx + 1][1] - self.stalactites[indx][1])/ (self.stalactites[indx + 1][0] - self.stalactites[indx][0]) * (x - self.stalactites[indx][0]) + self.stalactites[indx][1]
            bottomX = self.stalactites[indx][0]
            bottomY = self.stalactites[indx][1]
            counter = 0
            r = (self.stalactites[indx + 1][0] - self.stalactites[indx][0]) // 20
            delta = (self.stalactites[indx + 1][1] - self.stalactites[indx][1])
            for x in range(abs(r)):
             
                y = line(bottomX)
                y = random.randint(y - 5, y + 5)
                texturedStalactites.append((bottomX, y))
                bottomX -= 20
        texturedStalactites.extend([self.stalactites[-2], self.stalactites[-1]])
        self.stalactites = copy.copy(texturedStalactites)
    def scaleColor(self):
        if(self.counter % 2 == 0):
            numColor = int(self.color[4:])
            numColor += 1
            if(numColor > 98):
                self.color = 'grey99'
            else: self.color = 'grey' + str(numColor)

    def scaleWall(self, width, height):
        scalar = 0.04

        self.counter += 1
        newStalactites = []
        for point in self.stalactites:
            xNew = (scalar * (point[0] - (width // 2))) + point[0]
            yNew = (scalar * (point[1] - (height // 2))) + point[1]
            newStalactites.append((xNew, yNew))
        self.stalactites= copy.copy(newStalactites)
    
        newStalagmites= []
        for point in self.stalagmites:
            xNew = (scalar * (point[0]  - (width // 2))) + point[0]
            yNew = (scalar * (point[1]  - (height // 2))) + point[1]
            newStalagmites.append((xNew, yNew))
        self.stalagmites = copy.copy(newStalagmites)
        self.scaleColor()
        
        if(self.color == 'grey26'):
            return True
        return False

def init(data):
    data.walls = []
    for num in range(4, -1, -1):
        data.walls.append(Wall(data.width, data.height, num))
   
    data.spiderEnemies = {}
    data.batEnemies = {}
  
def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    pass

def generateEnemies(data):
    enemyLocations = []
    for x in range(5):
        enemyLocationIndex = random.randint(2, len(data.walls[0].stalactites) - 1)
        enemyLocations.append(data.walls[0].stalactites[enemyLocationIndex])
    data.spiderEnemies[data.walls[0].id] = []
    for t in enemyLocations:
        newEnemy = Spider(20, t[0], t[1], random.randint(0, 30), data.walls[0].id)
        newEnemy.bodyColor = data.walls[0].color
        data.spiderEnemies[data.walls[0].id].append(newEnemy)
    enemyLocations = [data.walls[0].stalactites[len(data.walls[0].stalactites) // 3]]
    for x in range(5):
        newPoint = (random.randint(int(enemyLocations[-1][0]) - 100, int(enemyLocations[-1][0]) + 100), random.randint(int(enemyLocations[-1][1]) - 10, int(enemyLocations[-1][1]) + 10))
        enemyLocations.append(newPoint)
    data.batEnemies[data.walls[0].id] = []
    for t in enemyLocations:
        newEnemy = Bat(20, t[0], t[1], data.walls[0].id)
        # newEnemy.bodyColor = data.walls[0].color
        data.batEnemies[data.walls[0].id].append(newEnemy)
def drawSpiderEnemies(canvas, data, lst):
    for enemy in lst:
        canvas.create_line(enemy.thread, width = 5, fill = enemy.bodyColor)
        canvas.create_polygon(enemy.bodyFrame, fill = enemy.bodyColor)
        canvas.create_polygon(enemy.headFrame, fill = enemy.bodyColor)
      
        for leg in enemy.rightLegFrames:
            canvas.create_line(leg, width = 5, fill = enemy.bodyColor)
        for leg in enemy.leftLegFrames:
            canvas.create_line(leg, width = 5, fill = enemy.bodyColor)
        for eye in enemy.eyeFrames:
            canvas.create_polygon(eye, fill = 'yellow')

def drawBatEnemies(canvas, data, lst):
    for bat in lst:
        canvas.create_polygon(bat.bodyFrame, fill = bat.bodyColor)
        canvas.create_polygon(bat.leftWingFrame, fill = bat.bodyColor )
        canvas.create_polygon(bat.rightWingFrame, fill = bat.bodyColor )
        canvas.create_polygon(bat.headFrame, fill = bat.bodyColor)
        canvas.create_polygon(bat.leftEyeFrame, fill = 'yellow')
        canvas.create_polygon(bat.rightEyeFrame, fill = 'yellow')
    
def timerFired(data):
    counter = 0
    for wall in data.walls:
        if(wall.scaleWall(data.width, data.height)):
            data.walls.pop(counter)
            newWall = Wall(data.width, data.height, 1)
            data.walls.insert(0, newWall)
            data.walls[0].color = 'grey12'
            generateEnemies(data)
        counter += 1
    for key, val in data.spiderEnemies.items():
        for spider in val:
            spider.animateEyes()
            if(spider.scaleSpider(data.width, data.height)):
                val.pop(val.index(spider))
    for key, val in data.batEnemies.items():
        for bat in val:
            bat.scaleBat(data.width, data.height)
            if(bat.counter > 30):
                val.pop(val.index(bat))

def drawWall(canvas, data):
    canvas.create_rectangle(0,0, data.width, data.height, fill = 'grey12')
    for wall in data.walls:
        if(wall.id in data.spiderEnemies):
            drawSpiderEnemies(canvas, data, data.spiderEnemies[wall.id])
        if(wall.id in data.batEnemies):
            drawBatEnemies(canvas, data, data.batEnemies[wall.id])
        canvas.create_polygon(wall.stalagmites, fill = wall.color)
        canvas.create_polygon(wall.stalactites, fill = wall.color)
        

def redrawAll(canvas, data):
    drawWall(canvas, data)
  
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
    data.timerDelay = 40 # milliseconds
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

run(1450, 750)

