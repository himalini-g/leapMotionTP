

def timerFired(data):
    pass
def changeModes(data):
    if((data.pauseBox[0][0] < data.mouseX < data.pauseBox[1][0]) and \
            (data.pauseBox[0][1] < data.mouseY < data.pauseBox[1][1])):
        data.mode = 'Paused'
    elif((data.helpBox[0][0] < data.mouseX < data.helpBox[1][0]) and \
            (data.helpBox[0][1] < data.mouseY < data.helpBox[1][1])):
        data.mode = 'Help'
    elif((data.storeBox[0][0] < data.mouseX <data.helpBox[1][0]) and \
        (data.storeBox[0][1] < data.mouseY < data.storeBox [1][1])):
        data.mode = 'gunStore'
    elif((data.mode == 'gameOver')):
        data.mode = 'restart'
def drawOverlay(canvas, data):
   
    txt = 'AMMO: [%d]' %(data.gun.ammo)
    canvas.create_text(30, data.height - 100, anchor = 'sw', text = txt, font = ('Fixedsys', 30, 'bold'), fill = data.fontFill)
    txt = 'GUN EQUIPED: [%s]' %(data.gun.name)
    canvas.create_text(30, data.height - 60,  anchor = 'sw', text = txt, font = ('', 30, 'bold'),  fill = data.fontFill)
    txt = 'GUNS PURCHASED: ' + ', '.join([gun.name for gun in data.gunsPurchased if gun.name != data.gun.name])
    canvas.create_text(30, data.height - 20,  anchor = 'sw', text = txt,font = ('', 30, 'bold'), fill =  data.fontFill)


   
    txt = 'PAUSE'
    canvas.create_text(data.width - 30, 50, anchor = 'se', text = txt, font = ('Fixedsys', 30, 'bold'), fill = data.fontFill)
    txt = 'HELP'
    canvas.create_text(data.width - 30, 90, anchor = 'se', text = txt, font = ('', 30, 'bold'), fill =  data.fontFill)
    txt = 'STORE'
    canvas.create_text(data.width - 30, 130, anchor = 'se', text = txt, font = ('', 30, 'bold'), fill =  data.fontFill)
    txt = 'MONEY: %s $' %(data.currency)
    canvas.create_text(data.width // 2, 50,  anchor = 's', text = txt,font =  ('Fixedsys', 30, 'bold'), fill = data.fontFill)
    txt = 'SCORE: [%d]' %(data.score)
    canvas.create_text(data.width // 2, 90,  anchor = 's', text = txt,font =  ('Fixedsys', 30, 'bold'), fill = data.fontFill)
    txt = 'HEALTH: [%s]' %(data.health)
    canvas.create_text(data.width // 2, 130,  anchor = 's', text = txt,font =  ('Fixedsys', 30, 'bold'), fill = data.fontFill)
def gameOverScreen(canvas, data):
    canvas.create_rectangle(0,0, data.width, data.height, fill = 'grey12')
    txt = 'GAME OVER'
    canvas.create_text(data.width // 2, data.height // 2 - 50, text = txt,font =  ('Fixedsys', 60, 'bold'), fill = data.fontFill)
    txt = 'FINAL SCORE: [%d]' %(data.score)
    canvas.create_text(data.width // 2, data.height // 2, text = txt,font =  ('Fixedsys', 60, 'bold'), fill = data.fontFill)
    txt = 'CLICK ANYWHERE TO REPLAY'
    canvas.create_text(data.width // 2, data.height // 2 + 50,  text = txt,font =  ('Fixedsys', 40, 'bold'), fill = data.fontFill)
def redrawAll(canvas, data):
    drawOverlay(canvas, data)

