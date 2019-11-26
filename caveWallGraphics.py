import random, math, copy
from shapely.geometry import *
from Tkinter import *
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
                print 'ur dumb'
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
    data.c = 0
  
def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    counter = 0
    for wall in data.walls:
        if(wall.scaleWall(data.width, data.height)):
            print(wall.id)
            data.walls.pop(counter)
            newWall = Wall(data.width, data.height, 1)

            data.walls.insert(0, newWall)
            data.walls[0].color = 'grey12'
        counter += 1
def timerFired(data):
    data.c += 1
def moveWall(data):
    pass
def drawWall(canvas, data):
    canvas.create_rectangle(0,0, data.width, data.height, fill = 'grey12')
    
    for wall in data.walls:
        #print(len(data.walls))
        canvas.create_polygon(wall.stalagmites, fill = wall.color)
        canvas.create_polygon(wall.stalactites, fill = wall.color)

    # for wall in [data.walls[2]]:
        # for point in wall.stalactites:
        #     canvas.create_oval(point[0] - 5, point[1] - 5, point[0] + 5, point[1] + 5, fill = 'red')
    #     for point in wall.stalagmites:
    #         canvas.create_oval(point[0] - 5, point[1] - 5, point[0] + 5, point[1] + 5, fill = 'red')
    #     for point in wall.left:
    #         canvas.create_oval(point[0] - 5, point[1] - 5, point[0] + 5, point[1] + 5, fill = 'green')
    
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

run(1450, 750)

