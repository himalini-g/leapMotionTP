import random, math, copy, decimal

class Stuff():
    def __init__(self):
        self.startColor = (59, 59, 59)
    #http://www.cs.cmu.edu/~112/notes/hw1.html
    def roundHalfUp(self, d):
        # Round to nearest with ties going away from zero.
        rounding = decimal.ROUND_HALF_UP
        # See other rounding options here:
        # https://docs.python.org/3/library/decimal.html#rounding-modes
        return int(decimal.Decimal(d).to_integral_value(rounding=rounding))
    # this is from my homework 1
    def colorBlender(self,  rgb1, rgb2, midpoints):
            colorList = []
            b1 = rgb1[2]
            b2 = rgb2[2]
            g1 = rgb1[1]
            g2 = rgb2[1]
            r1 = rgb1[0]
            r2 = rgb2[0]
            for point in range(midpoints):
                b = self.roundHalfUp(b1 - point*((b1 - b2) / (midpoints + 1)))
                g = self.roundHalfUp(g1 - point*((g1 - g2) / (midpoints + 1)))
                r = self.roundHalfUp(r1 - point*((r1 - r2) / (midpoints + 1)))
                strRGB = '#{:02x}{:02x}{:02x}'.format(r,g,b)
                colorList.append(strRGB)
            return colorList
    def scaleColor(self):
        if(self.counter % 2 == 0):
            numColor = int(self.color[4:])
            numColor += 1
            if(numColor > 98):
                self.color = 'grey99'
            else: self.color = 'grey' + str(numColor)
class Bat(Stuff):
    ID = 0
    def __init__(self, scale, cx, cy, iD):
        self.startColor = (59, 59, 59)
        self.ID = iD
        self.id = Bat.ID
        self.scale = scale
        # self.bodyColor = self.startColor

        # self.colorChoices = [(90, 49, 35), (58, 41, 24), (100, 77, 38), (59, 26, 22), (59, 26, 22)]
        self.colorIndex = 0
        self.color = 'grey23'
        # r = random.randint(0, len(self.colorChoices) -1)
        # self.colorList = self.colorBlender(self.startColor,  self.colorChoices[r], 30)

        self.eyeColor = 'yellow'

        self.cx = cx
        self.cy = cy
        
        self.leftEyeFrame = self.getLeftEyeFrame()
        self.rightEyeFrame = self.getRightEyeFrame()
        self.bodyFrame = self.getBodyFrame()
        self.headFrame = self.getHeadFrame()
        self.heightIncrements = [5, 6, -5, -7, 3]
        self.rightWingStates = self.getRightWingStates()
        self.leftWingStates = self.getLeftWingStates()
        
        index = random.randint(0, len(self.rightWingStates) - 1)
        self.rightWingFrame = self.rightWingStates[index]
        self.leftWingFrame  = self.leftWingStates[index]
        self.counter = 0
        self.halo = self.getHaloFrame()
        self.boundingBox = self.getBoundingBox()
        self.isDead = False
        Bat.ID += 1
    def hash(self):
        return hash(self.id)
        
    def getBoundingBox(self):
        cx, cy, scale = self.cx, self.cy, self.scale
        bodyBox = [(cx - scale // 2, cy - scale // 2),(cx + scale // 2, cy + scale)]
       
        leftXWing = [i[0] for i in self.leftWingFrame]
        leftYWing = [i[1] for i in self.leftWingFrame]
        rightXWing = [i[0] for i in self.rightWingFrame]
        rightYWing = [i[1] for i in self.rightWingFrame]
       
        wingBox = [(min(leftXWing), min(leftYWing)), (max(rightXWing), max(rightYWing))]
        return [bodyBox, wingBox]
    def getDeadLeftEye(self):
        cx, cy, scale = self.cx, self.cy , self.scale
        return [[(cx - scale * 0.03 , cy - scale * 1.2), (cx - scale * 0.25, cy - scale * 1)],
                [(cx - scale * 0.02, cy - scale * 1), (cx - scale * 0.25, cy - scale * 1.2)]]
    def getDeadRightEye(self):
        cx, cy, scale = self.cx, self.cy , self.scale
        return [[(cx + scale * 0.03 , cy - scale * 1.2), (cx + scale * 0.25, cy - scale * 1)],
                [(cx + scale * 0.02, cy - scale * 1), (cx + scale * 0.25, cy - scale * 1.2)]]
    def getHaloFrame(self):
        cx, cy, scale = self.cx, self.cy , self.scale
        return [(cx - scale // 3, cy - scale * 1.7), (cx + scale // 3, cy - scale * 1.5)]
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
        lst = [[(cx, cy - scale // 2), (cx + scale * 0.9 , cy - scale * 1.3), 
            (cx + scale * 2.6, cy - scale * 2 ), (cx + scale * 2.1, cy - scale * 0.6), 
            (cx + scale * 1, cy - scale * 0.2), (cx, cy - scale // 2)], 
            [(cx, cy - scale // 2), (cx + scale * 0.8 , cy - scale * 1.3),
            (cx + scale * 1.6, cy - scale * 3 ), (cx + scale * 2.1, cy - scale * 1),
            (cx + scale * 1, cy - scale * 0.2), (cx, cy - scale // 2)],
            [(cx, cy - scale // 2), (cx + scale * 0.9 , cy - scale * 1.3), 
            (cx + scale * 2.6, cy - scale * 2 ), (cx + scale * 2.1, cy - scale * 0.6),
            (cx + scale * 1, cy - scale * 0.2), (cx, cy - scale // 2)],
            [(cx, cy - scale // 2), (cx + scale * 0.9 , cy),
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
        if(self.isDead == False):
            self.counter += 1
            y = random.randint(height // 2, height)
            intervalX = math.sqrt(self.cx**2) // (40 -self.counter)
            intervalY = math.sqrt(y**2 + self.cy**2) // (40 -self.counter)
            if(0 < self.cx):
                self.cx += intervalX
            if(y < self.cy):
                self.cy -= intervalY
            elif(y > self.cy):
                self.cy += intervalY
            self.scale += 2
            self.animate()
        elif(self.isDead):
            self.counter += 1
            self.color = 'white'
            self.heavenAnimate()
        # if(self.colorIndex > len(self.colorList) - 3):
        #     return True
        # return False
    def heavenAnimate(self):
        self.cy -= 30
        self.headFrame = self.getHeadFrame()
        self.bodyFrame = self.getBodyFrame()
        self.rightWingFrame = self.getRightWingStates(self.counter % 5)
        self.leftWingFrame = self.getLeftWingStates(self.counter % 5)
        self.leftEyeFrame = self.getDeadLeftEye()
        self.rightEyeFrame = self.getDeadRightEye()
        self.halo = self.getHaloFrame()
    def animate(self):
        self.counter += 1
        self.cy += self.heightIncrements[self.counter % 5]
        self.rightWingFrame = self.getRightWingStates(self.counter % 5)
        self.leftWingFrame = self.getLeftWingStates(self.counter % 5)
        self.bodyFrame = self.getBodyFrame()
        self.headFrame = self.getHeadFrame()
        self.leftEyeFrame = self.getLeftEyeFrame()
        self.rightEyeFrame = self.getRightEyeFrame()
        self.boundingBox = self.getBoundingBox()

    def getPoints(self):
        pass
    def blink(self):
        pass

class Spider(Stuff):
    ID = 0
    def __init__(self, scale, cx, cy, threadLength, iD):
        self.startColor = (59, 59, 59)
        self.startAnimate = random.randint(4, 20)
        self.id = Spider.ID
        self.wallID = iD
        self.scale = scale
        # self.colorChoices = [(77, 77, 77), (109, 76, 76), (66, 62, 63)]
        # self.colorIndex = 0
        self.color = 'grey15'
        # r = random.randint(0, len(self.colorChoices) - 1)
        # self.colorList  = self.colorBlender(self.colorChoices[r], self.startColor, 30)
        self.eyeColor = 'yellow'
        self.cx, self.cy = cx, cy
        self.thread = self.getThread()
        self.bodyFrame = self.getBodyFrame()
        self.headFrame = self.getHeadFrame()
        self.eyeFrames = self.getEyeFrames()
        self.leftLegFrames = self.getLeftLegFrames()
        self.rightLegFrames = self.getRightLegFrames()
        self.boundingBox = self.getBoundingBox()
        self.isDead = False
        self.counter = 0
        Spider.ID += 1
    def hash(self):
        return hash(self.id)
 
    def getThread(self):
        return [(self.cx, 0), (self.cx, self.cy)]
    def getRightLegFrames(self):
        cx, cy, s = self.cx, self.cy, self.scale
        lst =  [[(cx + s * 0.66, cy + s * 1.4 ), (cx + s * 4 // 3, cy + s * 1.5), (cx + s * 0.9, cy + s * 2 )],
                            [(cx + s * 0.66, cy + s * 1.2 ), (cx + s * 4 // 3, cy + s * 1.1), (cx + s * 1.5, cy + s * 1.7 )],
                            [(cx + s * 0.66, cy + s * 1 ), (cx + s * 4 // 3, cy + s * 0.8), (cx + s * 1.8, cy + s * 1.4 )],
                            [(cx + s * 0.66, cy + s * 0.8 ), (cx + s , cy + s * 0.6), (cx + s * 1.7, cy + s * 1 )]]
        return lst
    def getLeftLegFrames(self):
        cx, cy, s = self.cx, self.cy, self.scale
        lst = [[(cx - s * 0.66, cy + s * 1.4 ), (cx - s * 4 // 3, cy + s * 1.5), (cx - s * 0.9, cy + s * 2 )],
                            [(cx - s * 0.66, cy + s * 1.2 ), (cx - s * 4 // 3, cy + s * 1.1), (cx - s * 1.5, cy + s * 1.7 )],
                            [(cx - s * 0.66, cy + s * 1 ), (cx - s * 4 // 3, cy + s * 0.8), (cx - s * 1.8, cy + s * 1.4 )],
                            [(cx - s * 0.66, cy + s * 0.8 ), (cx - s , cy + s * 0.6), (cx - s * 1.7, cy + s * 1 )]]
        return lst
    def getEyeFrames(self):
        cx, cy, s = self.cx, self.cy, self.scale
        lst = [[(cx - s  * 0.18 , cy + s * 2.25), (cx - s * 0.13 , cy + s * 2.3),
                        (cx - s  * 0.18, cy + s * 2.35), (cx - s * 0.23, cy + s * 2.3)],
                        [(cx - s  * 0.07 , cy + s * 2.30), (cx - s * 0.02 , cy + s * 2.35),
                        (cx - s  * 0.07, cy + s * 2.40), (cx - s * 0.12, cy + s * 2.35)],
                        [(cx + s  * 0.07 , cy + s * 2.30), (cx + s * 0.02 , cy + s * 2.35),
                        (cx + s  * 0.07, cy + s * 2.40), (cx + s * 0.12, cy + s * 2.35)],
                        [(cx + s  * 0.18 , cy + s * 2.25), (cx + s * 0.13 , cy + s * 2.3),
                        (cx + s  * 0.18, cy + s * 2.35), (cx + s * 0.23, cy + s * 2.3)]]
        return lst
    def getDeadEyeFrames(self):
        cx, cy, s = self.cx, self.cy, self.scale
        lst = [[(cx - s  * 0.19 , cy + s * 2.25), (cx - s  * 0.15, cy + s * 2.35)],
                        [(cx - s * 0.13 , cy + s * 2.27),  (cx - s * 0.23, cy + s * 2.33)],
                        [(cx - s  * 0.1 , cy + s * 2.30), (cx - s  * 0.03, cy + s * 2.40)],
                        [(cx - s * 0.02 , cy + s * 2.3), (cx - s * 0.12, cy + s * 2.38)],
                        [(cx + s  * 0.19 , cy + s * 2.25), (cx + s  * 0.15, cy + s * 2.35)],
                        [(cx + s * 0.13 , cy + s * 2.27),  (cx + s * 0.23, cy + s * 2.33)],
                        [(cx + s  * 0.1 , cy + s * 2.30), (cx + s  * 0.03, cy + s * 2.40)],
                        [(cx + s * 0.02 , cy + s * 2.3), (cx + s * 0.12, cy + s * 2.38)]]
        return lst
    def getHeadFrame(self):
        cx, cy, s = self.cx, self.cy, self.scale
        lst = [(cx, cy + s * 1.8), (cx - s // 2.7, cy + s * 2),
                            (cx - s // 2.7, cy + s * 2.3), (cx, cy + s * 2.5),
                            (cx + s // 2.7, cy + s * 2.3), (cx + s // 2.7, cy + s * 2),
                            (cx, cy + s * 1.8)]
        return lst
    def getBodyFrame(self):
        cx, cy, s = self.cx, self.cy, self.scale
        lst = [(cx, cy ), (cx - s * 2 // 3, cy + s // 2),(cx - s * 2 // 3, cy + s * 3 // 2),
                (cx, cy + s * 2), (cx + s * 2 // 3, cy + s * 3 // 2),
                (cx + s * 2 // 3, cy + s // 2), (cx, cy )]
        return lst
    def getBoundingBox(self):
        cx, cy, s = self.cx, self.cy, self.scale
        return [[(cx - s * 1.8, cy), (cx + s * 1.8, cy + s * 2)], [(cx - s // 2.7,cy + s * 1.8), (cx + s // 2.7, cy + s * 2.5)] ]

    def animateEyes(self):
        for eye in self.eyeFrames:
            if(eye[0][1] < eye[2][1]):
                eye[2] = (eye[2][0], eye[2][1] - 1)
            else:
                eye[2] = (eye[2][0], eye[2][1] + 5)

    # def scaleColor(self):
    #     if(self.counter % 2 == 0 and self.colorIndex + 1  < len(self.colorList) - 1):
    #         self.colorIndex += 1
        
    def scaleSpider(self, width, height):
        if(self.isDead == False):
            if(self.counter > self.startAnimate):
                self.thread[1] = (self.thread[1][0], self.thread[1][1] + 10)
                self.cy += 10
            scalar = 0.04
            self.counter += 1
            
            self.cx = (scalar * (self.cx - (width // 2))) + self.cx
            self.cy = (scalar * (self.cy - (height // 2))) + self.cy
            self.scale += self.scale * 0.04

            self.thread = self.getThread()
            self.bodyFrame = self.getBodyFrame()
            self.headFrame = self.getHeadFrame()
            self.eyeFrames = self.getEyeFrames()
            self.leftLegFrames = self.getLeftLegFrames()
            self.rightLegFrames = self.getRightLegFrames()
            self.boundingBox = self.getBoundingBox()
        
            self.scaleColor()
            if(self.bodyColor == 'grey26'):
                return True
            return False
        else:
            self.counter += 1
            self.color = 'black'
            self.deadSpider(width, height)
    def deadSpider(self, width, height):

        scalar = 0.04
        self.counter += 1
        #self.thread[1] = (self.thread[1][0], self.thread[1][1] + 25)
        self.cy += 20
        self.cx = (scalar * (self.cx - (width // 2))) + self.cx
        self.cy = (scalar * (self.cy - (height // 2))) + self.cy
        self.scale += self.scale * 0.04

        self.thread = self.getThread()
        self.bodyFrame = self.getBodyFrame()
        self.headFrame = self.getHeadFrame()
        self.eyeFrames = self.getDeadEyeFrames()
        self.leftLegFrames = self.getLeftLegFrames()
        self.rightLegFrames = self.getRightLegFrames()

        self.color = 'black'
class Wall(Stuff):
    ID = 0
    def __init__(self, width, height, layer):
        self.startColor = (59, 59, 59)
        self.id = Wall.ID
        self.width = width
        self.height = height
        # self.colorChoices = [(82, 82, 82)]#(41,38,65)]#, (49,49,73), (49,67,67), (46, 32, 62), 
        #                      #(30, 61, 57), (36, 39, 79)]
        self.stalactites = self.generatePoints(width, height, -1, layer)
        self.stalagmites = self.generatePoints(width, height, 1, layer)
        # r = random.randint(0, len(self.colorChoices) - 1)
        self.layer = layer
        # self.colorList = self.colorBlender(self.startColor, self.colorChoices[r], 30)
        # self.colorIndex =  self.layer * 4
        # self.color = self.colorList[self.colorIndex]
        self.colorChoices = [ 'grey24','grey21', 'grey18', 'grey15', 'grey12']
        self.color = self.colorChoices[self.layer]
        self.leftEdge, self.rightEdge = self.makeEdges(width, height, self.stalactites, self.stalagmites)
        self.pointIndex = {}
        self.counter = 0

        self.untexturedStalagmites = copy.copy(self.stalagmites)
        self.untexturedStalactites = copy.copy(self.stalactites)
        self.generateTexture()
        
        self.flickerStalactites = []
        self.flickerStalagmites = []
        self.tempHolderStalagmites = []
        self.tempHolderStalactites = []

        self.stalagmiteLight, self.flickerStalagmites = self.generateLight(1, self.untexturedStalagmites, self.width // 2)
        self.stalactiteLight, self.flickerStalactites = self.generateLight(-1, self.untexturedStalactites, self.width // 2)
        
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
        texturedRock = []
        self.pointIndex = {}
        for lst in [self.stalagmites, self.stalactites]:
            texturedRock.append([])
            for indx in range(1, len(lst)):
                line = lambda x: (lst[indx + 1][1] - lst[indx][1])/ \
                    (lst[indx + 1][0] - lst[indx][0]) * (x - lst[indx][0]) + lst[indx][1]
                texturedRock[-1].append(lst[indx])
                self.pointIndex[lst[indx]] = len(texturedRock[-1]) - 1
                if(indx + 1 < len(lst) - 3):
                    bottomX = lst[indx][0]
                    bottomY = lst[indx][1]
                    r = (lst[indx + 1][0] - lst[indx][0]) // 20
                    for x in range(abs(r)):
                        y = line(bottomX)
                        y = random.randint(y - 5, y + 5)
                        texturedRock[-1].append((bottomX, y))
                        bottomX -= 20
        texturedRock[0].extend([self.stalagmites[-2], self.stalagmites[-1]])
        self.stalagmites = copy.copy(texturedRock[0])
      
        texturedRock[1].extend([self.stalactites[-2], self.stalactites[-1]])
        self.stalactites = copy.copy(texturedRock[1])

    # def scaleColor(self):
    #     if(self.colorIndex + 1 < len(self.colorList)):
    #         self.colorIndex += 1
    #     self.color = self.colorList[self.colorIndex]
       
    def scaleWall(self, width, height):
        scalar = 0.03

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
        newLight = []
        for lst in self.stalactiteLight:
            newLight.append([])
            for point in lst:

                xNew = (scalar * (point[0]  - (width // 2))) + point[0]
                yNew = (scalar * (point[1]  - (height // 2))) + point[1]
                newLight[-1].append((xNew, yNew))
        self.stalactiteLight = copy.copy(newLight)
        newStalagmiteLight = []
        for lst in self.stalagmiteLight:
            newStalagmiteLight.append([])
            for point in lst:

                xNew = (scalar * (point[0]  - (width // 2))) + point[0]
                yNew = (scalar * (point[1]  - (height // 2))) + point[1]
                newStalagmiteLight[-1].append((xNew, yNew))
        self.stalagmiteLight = newStalagmiteLight
        newEdges = []
        for edge in [self.leftEdge, self.rightEdge]:
            newEdges.append([])
            for point in edge:
                xNew = (scalar * (point[0]  - (width // 2))) + point[0]
                yNew = (scalar * (point[1]  - (height // 2))) + point[1]
                newEdges[-1].append((xNew, yNew))
        self.leftEdge = copy.copy(newEdges[0])
        self.rightEdge = copy.copy(newEdges[1])
        
        self.scaleColor()
        # self.flicker(self.stalagmiteLight, 1)
        # self.flicker(self.stalactiteLight,-1)
        # if(self.colorIndex == len(self.colorList) - 2):
        #     return True
        # return False
        if(self.color == 'grey24'):
            return True
        return False
    def generateLight(self, d, lst, center):
        light = []
        if(d == 1):
            rock = self.stalagmites
        else:
            rock = self.stalactites
        flickerIndx = []
        counter = 0
        for indx in range(1, len(lst) - 4, 2):
            flickerIndx.append(0)
            
            light.append([])
            light[-1].append(lst[indx])
            startIndx = self.pointIndex[lst[indx]]
            endIndx = self.pointIndex[lst[indx + 1]]   
            slce = copy.copy(rock[startIndx:endIndx + 1])
            circle = lambda x, r, a, b: (d * math.sqrt(r**2 - (x - b)**2)) + a
            averageY = (lst[indx + 2][1] + lst[indx][1]) // 2
            averageX = (lst[indx + 2][0] + lst[indx][0]) // 2
            startX = lst[indx][0]
            endX = lst[indx + 2][0]
            distX = (lst[indx][0] - lst[indx + 2][0])
            var = 11 - (abs(center - averageX) // (center // 10)) 
            deltaX = abs(lst[indx + 2][0] - lst[indx][0]) // 10
            if(startX > center):
                deltaX *= -1
                light[-1].pop()
                startX = lst[indx + 2][0]
                light[-1].append(lst[indx + 2])
                startIndx = self.pointIndex[lst[indx + 1]]
                endIndx = self.pointIndex[lst[indx + 2]]
                slce = copy.copy(rock[startIndx:endIndx])
            for x in range(var):
                startX -= deltaX
                if(startX > endX):
                    try: 
                        y = circle(startX, abs(distX // 2) + 2, averageY, averageX)
                        light[-1].append((startX, int(y)))
                    except:
                        pass
            flickerIndx[-1] = len(light[-1]) - 1
            light[-1].append(lst[indx + 1])
            light[-1].extend(slce)
        return light, flickerIndx
    def flicker(self, light, d):
        if(d == 1):
            flickerIndx = copy.copy(self.flickerStalagmites)
            tempHolder = copy.copy(self.tempHolderStalagmites)
        else:
            flickerIndx = copy.copy(self.flickerStalactites)
            tempHolder = copy.copy(self.tempHolderStalactites)
        if(self.counter % 2 == 0 ):
            tempHolder = []
            counter = 0
            for l in light:
                tempHolder.append(l.pop(flickerIndx[counter]))
                counter +=1
        elif(tempHolder != []):
            counter = 0
            for l in light:
                l.insert(flickerIndx[counter], tempHolder[counter])
                counter += 1
        if(d == 1):
            self.tempHolderStalagmites = copy.copy(tempHolder)
        else:
            self.tempHolderStalactites = copy.copy(tempHolder)

def initialized(data):
    data.walls = []
    for num in range(4, -1, -1):
        data.walls.append(Wall(data.width, data.height, 0))
    colors = [ 'grey24','grey21', 'grey18', 'grey15', 'grey12']
    counter = 0
    for wall in data.walls:
        wall.color = colors[-1 - counter]
        counter += 1
    data.c = 0
    data.spiderEnemies = {}
    data.batEnemies = {}
    data.direction = 1
    data.center = data.width // 3
