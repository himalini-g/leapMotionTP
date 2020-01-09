

def drawHelpScreen(canvas, data):
    canvas.create_rectangle(0,0, data.width, data.height, fill = 'grey12')
    txt = '''
            INSTRUCTIONS:
            - ORIENT LEAP MOTION IN FRONT OF COMPUTER SO THAT
              THE GREEN LIGHT IS FACING YOU AND IT IS CENTERED
              IN FRONT OF THE COMPUTER SCREEN
            - KEEP LAPTOP SCREEN AT 90 DEGREES
            - MAKE SURE LEAP MOTION SENSOR IS NOT SMUDGED
            GAMEPLAY:
            - MAKE A FINGERGUN WITH YOUR RIGHT HAND
            - MAKE SURE PALM IS FACING THE LEAP MOTION
            - SQUEEZE THUMB TO INDEX FINGER TO FIRE GUN
            - USE THE AIM ON SCREEN TO DETERMINE LOCATION OF SHOT
            - CLICK BUTTONS TO PAUSE, PLAY AND ACCESS STORE
            - USE SPACE BAR TO SWITCH BETWEEN WEAPONS
            - EVERY BAT THAT ESCAPES PAST THE SCREEN DECREASES HEALTH
            **IMPORTANT**
            - THE GUN WILL NOT FIRE AGAIN UNTIL THE 'SHOT RELOAD TIME' IS EXHAUSTED,
              EVEN IF LEAP MOTION DETECTS THE PLAYER PULLING THE TRIGGER
            CHEATS: 
            - PRESS 'C' TO GET MORE MONEY
            - PRESS 'L' TO END GAME
            - PRESS 'G' TO GET ALL WEAPONRY
            '''
    canvas.create_text(data.width // 2, data.height // 2, text = txt,font = ('Fixedsys', 25, 'bold'), fill = data.fontFill)
    txt = 'PLAY'
    canvas.create_text(data.width - 30, 50, anchor = 'se', text = txt, font = ('Fixedsys', 30, 'bold'), fill = data.fontFill)
def changeModes(data):
    if(data.playBox[0][0] < data.mouseX < data.playBox[1][0] and data.playBox[0][1] < data.mouseY < data.playBox[1][1]):
        data.mode = 'Playing'
def redrawAll(canvas, data):
    drawHelpScreen(canvas, data)
