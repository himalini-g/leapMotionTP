


class Gun(object):
    def __init__(self, width, height, name,  gap, ammo, reloadTime, price, damage, bulletScale, scalars, noiseList = []):
        self.name = name
        self.cx = width // 2
        self.cy = height + 30
        self.shootGap = gap
        self.capacity = ammo
        self.ammo = ammo
        self.reloadTime = reloadTime
        self.price = price
        self.damage = damage
        self.bulletScale = bulletScale
        self.scalars = scalars
        self.colorList = ['grey78', 'grey98']
        self.noiseList = noiseList
        self.scale = 200
        self.d = 1
        self.counter = 0
        self.firing = self.getFiringFrames(0, self.d)
        self.timePassed = 0

    def getBullet(self):
        pass
    def scaleBullet(self):
        pass
    def getFiringFrames(self, scalar, d):
        scale, cx, cy = self.scale * scalar, self.cx, self.cy
        innerScale = self.scale * scalar // 2
        return [[(cx, cy), (cx - d * (scale * 5 // 6), cy - (scale // 3)),  (cx - d * (scale // 3), cy - (scale // 4)),
                 (cx - d * (scale // 1.3), cy - (scale // 1.3)), (cx - d * (scale // 3.4), cy -  (scale // 1.8)),
                 (cx - d * (scale // 3.4), cy - (scale // 1.3)), (cx - d * (scale // 5), cy - (scale // 1.8)),
                 (cx - d * (scale // 5), cy - (scale)),  (cx, cy - (scale // 2 - (scale // 5))),
                 (cx, cy),
                 (cx + d * (scale * 5 // 6), cy),  (cx + d * (scale // 3), cy - (scale // 4)),
                 (cx + d * (scale), cy - scale // 2), (cx + d * (scale // 3), cy - (scale // 2)),
                 (cx + d * (scale // 2), cy - (scale)),  (cx, cy - (scale // 2 - (scale // 5)))],

                 [(cx, cy),(cx - d * (innerScale * 5 // 6), cy),  (cx - d * (innerScale // 3), cy - (innerScale // 4)),
                 (cx - d * (innerScale), cy - innerScale // 2), (cx - d * (innerScale // 3), cy - (innerScale // 2)),
                 (cx - d * (innerScale // 2), cy - (innerScale)),  (cx, cy - (innerScale // 2 + (innerScale // 5))),
                 (cx, cy ),
                 (cx + d * (innerScale * 5 // 6), cy),  (cx + d * (innerScale // 3), cy - (innerScale // 4)),
                 (cx + d * (innerScale), cy - innerScale // 2), (cx + d * (innerScale // 3), cy - (innerScale // 2)),
                 (cx + d * (innerScale // 2), cy - (innerScale)),  (cx, cy - (innerScale // 2 + (innerScale // 5)))] 
               ]
    def animateFiring(self):
        self.counter += 1
        self.d *= -1
        self.firing = self.getFiringFrames(self.scalars[self.counter % len(self.scalars)], self.d)
    def getAmmoFrame(self, cx, cy, ):
         scale = self.bulletScale
         return [(cx, cy), (cx + scale * 3, cy), (cx + scale * 4, cy - scale), 
                (cx + scale * 3, cy - scale * 2),(cx, cy - scale * 2), (cx, cy) ]

class MachineGun(Gun):
    def __init__(self, width, height):
        super(MachineGun, self).__init__(width, height, 'MACHINE GUN', 0, 100, 5, 100, 5, 3, [0.15, 0.2, 0.3, 0.4], ['handGunShot1.wav', 'handGunShot2.wav', 'handGunShot3.wav'])
        self.purchaseBox = [(width * 0.10784313725, height * 0.69607843137 + 12), \
                        (width * 0.10784313725 + 180, height * 0.69607843137 - 30)]
        self.txtCenter = (width // 2 - width // 2.2 + 200, height // 2)
        self.boxColor = 'yellow'
class ShotGun(Gun):
    def __init__(self, width, height):
   
        super(ShotGun, self).__init__(width, height, 'SHOT GUN', 0.5, 5, 4, 70, 50, 20, [0.2, 1.2, 1.4, 1.6],  ['handGunShot1.wav', 'handGunShot2.wav', 'handGunShot3.wav'])
        self.purchaseBox = [(width * 0.10784313725 + 400, height * 0.69607843137 + 12), \
                        (width * 0.10784313725 + 180 + 400, height * 0.69607843137 - 30)]
        self.txtCenter = (width // 2 - width // 2.2  + 400 + 200 , height // 2)
        self.boxColor = 'orange'
  
class HandGun(Gun):
    def __init__(self, width, height):
        super(HandGun, self).__init__(width, height, 'HAND GUN', 0.1, 18, 2, 100, 7, 10, [0.2, 0.4, 0.5, 0.8], ['handGunShot1.wav', 'handGunShot2.wav', 'handGunShot3.wav'])
class Revolver(Gun):
    def __init__(self, width, height):
        super(Revolver, self).__init__(width, height, 'REVOLVER', 0.05, 6, 2, 30, 7, 10, [0.2, 0.4, 0.5, 0.8], ['handGunShot1.wav', 'handGunShot2.wav', 'handGunShot3.wav'])
        self.purchaseBox = [(width * 0.10784313725 + 800, height * 0.69607843137 + 12), \
                        (width * 0.10784313725 + 180 + 800, height * 0.69607843137 - 30)]
        self.txtCenter = (width // 2 - width // 2.2  + 800 + 200, height // 2)
        self.boxColor = 'red'

def initialized(data):
    data.gun = HandGun(width, height)
    data.bulletX = width // 2
    data.bulletY = height // 2
    data.hitX = 100
    data.hitY = 300
def drawAmmoBox(canvas, data):
    startX = 35
    startY = data.height - 150
    increment = - (data.gun.bulletScale * 3)
    for bullet in range(data.gun.ammo):
        points = data.gun.getAmmoFrame(startX, startY)
        canvas.create_polygon(points, fill = 'white')
        startY += increment

def drawGunFire(canvas, data):
    if(data.firing):
        for val in data.gun.scalars:
            data.gun.animateFiring()
            counter = 0
            for lst in data.gun.firing:
                canvas.create_polygon(lst, fill = data.gun.colorList[counter])
                counter += 1
        data.firing = False
def drawFingerLines(canvas, data):
    for key, val in data.fingerPoints.items():
        canvas.create_line(val[0], 300 - val[2], val[3], 300 - val[5], fill = data.trigger)
def drawScreenIntersect(canvas,data):
    canvas.create_oval(data.intersect[0] - 5, data.intersect[1] - 5, data.intersect[0] + 5, data.intersect[1] + 5, fill = data.trigger)
def redrawAll(canvas, data):
    drawScreenIntersect(canvas, data)
    drawGunFire(canvas, data)
    drawAmmoBox(canvas, data)

