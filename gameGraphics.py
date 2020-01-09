import random, math, copy, decimal
from Tkinter import *
import backGroundOOP

def init(data):
    backGroundOOP.initialized(data)
def initialized(data):
    backGroundOOP.initialized(data)
def generateEnemies(data):
    enemyLocations = []
    for x in range(2):
        enemyLocationIndex = random.randint(2, len(data.walls[0].stalactites) - 1)
        enemyLocations.append(data.walls[0].stalactites[enemyLocationIndex])
    data.spiderEnemies[data.walls[0].id] = []
    for t in enemyLocations:
        newEnemy = backGroundOOP.Spider(20, t[0], t[1], random.randint(10, 50), data.walls[0].id)
        newEnemy.bodyColor = data.walls[0].color
        data.spiderEnemies[data.walls[0].id].append(newEnemy)
    enemyLocations = [data.walls[0].stalactites[len(data.walls[0].stalactites) * 2 // 3]]
    for x in range(1):
        newPoint = (random.randint(int(enemyLocations[-1][0]) - 100, int(enemyLocations[-1][0]) + 100), random.randint(int(enemyLocations[-1][1]) - 10, int(enemyLocations[-1][1]) + 10))
        enemyLocations.append(newPoint)
    data.batEnemies[data.walls[0].id] = []
    for t in enemyLocations:
        newEnemy = backGroundOOP.Bat(20, t[0], t[1], data.walls[0].id)
       
        newColor = str(random.randint(12, 24 ))
        newEnemy.color = 'grey' + newColor
        data.batEnemies[data.walls[0].id].append(newEnemy)

def drawSpiderEnemies(canvas, data, lst):
    for enemy in lst:
        if(enemy.isDead == True and enemy.color != 'black'):
            enemy.color = 'black'
            enemy.deadSpider(data.width, data.height)
        canvas.create_line(enemy.thread, width = 5, fill = enemy.color) #List[enemy.colorIndex])
        canvas.create_polygon(enemy.bodyFrame, fill = enemy.color) #List[enemy.colorIndex])
        canvas.create_polygon(enemy.headFrame, fill = enemy.color) #List[enemy.colorIndex])
        for leg in enemy.rightLegFrames:
            canvas.create_line(leg, width = 5, fill = enemy.color) #List[enemy.colorIndex])
        for leg in enemy.leftLegFrames:
            canvas.create_line(leg, width = 5, fill = enemy.color) #List[enemy.colorIndex])
        if(enemy.isDead == False):
            for eye in enemy.eyeFrames:
                canvas.create_polygon(eye, fill = 'yellow')
        else:
            for eye in enemy.eyeFrames:
                canvas.create_line(eye, fill = 'yellow', width = 1)

def drawBatEnemies(canvas, data, lst):
    for bat in lst:
        if(bat.isDead and bat.color != 'white'):
            bat.heavenAnimate()
        canvas.create_polygon(bat.bodyFrame, fill = bat.color) #List[bat.colorIndex])
        canvas.create_polygon(bat.leftWingFrame, fill = bat.color) #List[bat.colorIndex])
        canvas.create_polygon(bat.rightWingFrame, fill = bat.color) #List[bat.colorIndex])
        canvas.create_polygon(bat.headFrame, fill = bat.color) #List[bat.colorIndex])
        if(bat.isDead == False):
            canvas.create_polygon(bat.leftEyeFrame, fill = 'yellow')
            canvas.create_polygon(bat.rightEyeFrame, fill = 'yellow')
        elif(bat.isDead):
            for lst in bat.leftEyeFrame:
                canvas.create_line(lst, fill = 'yellow', width = 3)
            for lst in bat.leftEyeFrame:
                canvas.create_line(lst, fill = 'yellow', width = 3)
            canvas.create_oval(bat.halo, fill = '', outline = 'yellow', width = 3)
            
def centerIncrementer(data):
    if(data.center < data.width and data.direction == 1):
        data.center += 10
        
    elif(data.center > data.width):
        data.direction = -1
    if(data.center > 20 and data.direction == -1):
        data.center -= 10
    elif(data.center < 20):
        data.direction = 1
        data.center = 20
def timerFired(data):
 
    counter = 0
    for wall in data.walls:
        if(wall.scaleWall(data.width, data.height)):
            wallID = wall.ID
            data.walls.pop(counter)
            newWall = backGroundOOP.Wall(data.width, data.height, 1)
            data.walls.insert(0, newWall)
            data.walls[0].color = 'grey12'
            generateEnemies(data) 
        counter += 1
    for key, val in data.spiderEnemies.items():
        if(val == []):
            data.spiderEnemies.pop([key], None)
        for spider in val:
            if(spider.scaleSpider(data.width, data.height)):
                val.pop(val.index(spider))

    for key, val in data.batEnemies.items():

        for bat in val:
            bat.scaleBat(data.width, data.height)
            if(bat.counter > 40):
                if(bat.isDead == False):
                    data.health -= 1
                val.pop(val.index(bat))
    
def mousePressed(event, data):
    pass
    #print(event.x, event.y)
def keyPressed(event, data):
    pass
def drawWall(canvas, data):
    canvas.create_rectangle(0,0, data.width, data.height, fill = 'grey12')
    for wall in data.walls:
        if(wall.id in data.spiderEnemies):
            drawSpiderEnemies(canvas, data, data.spiderEnemies[wall.id])
        if(wall.id in data.batEnemies):
            drawBatEnemies(canvas, data, data.batEnemies[wall.id])
        canvas.create_polygon(wall.stalagmites, fill = wall.color)
        canvas.create_polygon(wall.stalactites, fill = wall.color)
        canvas.create_polygon(wall.leftEdge, fill = wall.color)
        canvas.create_polygon(wall.rightEdge, fill = wall.color)
        for light in wall.stalagmiteLight:
            if(light != []):
                canvas.create_polygon(light, fill = 'grey' + str(int(wall.color[4:]) + 1))
        for light in wall.stalactiteLight:
            if(light != []):
                canvas.create_polygon(light, fill = 'grey' + str(int(wall.color[4:]) + 1))
def redrawAll(canvas, data):
    drawWall(canvas, data)
