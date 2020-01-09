
import copy
def timerFired(data):
    checkBox(data)
def checkBox( data):
    for gun in data.gunsInStore:
        if(gun.purchaseBox[0][0] < data.mouseX < gun.purchaseBox[1][0] and
           gun.purchaseBox[0][1] > data.mouseY > gun.purchaseBox[1][1] and gun.price <= data.currency):
           data.currency = data.currency - gun.price
           data.gunsPurchased.append(data.gunsInStore.pop(data.gunsInStore.index(gun)))
def drawStoreScreen(canvas, data):

    canvas.create_rectangle(0,0, data.width, data.height, fill = 'grey12')
    txt = 'MONEY: %s' %(data.currency)
    canvas.create_text(data.width // 2, 50,  anchor = 's', text = txt,font =  ('Fixedsys', 30, 'bold'), fill = data.fontFill)
    for gun in data.gunsInStore:
        txt = '''

                      %s
                      SPECS:
                      SHOT RELOAD: %.2f SEC
                      AMMO CAPACITY: %d
                      AMMO RELOAD: %d SEC
                      PRICE: %d $ 
                      PURCHASE
                ''' %(gun.name, gun.shootGap, gun.capacity,  gun.reloadTime, gun.price)
        canvas.create_text(gun.txtCenter[0], gun.txtCenter[1] , text = txt,font = ('Fixedsys', 30, 'bold'), fill = data.fontFill)
        canvas.create_rectangle(gun.purchaseBox, fill = '', outline = 'white', width = 3)
    txt = 'PLAY'
    canvas.create_text(data.width - 30, 50, anchor = 'se', text = txt, font = ('Fixedsys', 30, 'bold'), fill = data.fontFill)
def changeModes(data):
    if(data.playBox[0][0] < data.mouseX < data.playBox[1][0] and data.playBox[0][1] < data.mouseY < data.playBox[1][1]):
        data.mode = 'Playing'
def redrawAll(canvas, data):
    drawStoreScreen(canvas, data)
