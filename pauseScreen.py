
def drawPauseScreen(canvas, data):
    canvas.create_rectangle(0,0, data.width, data.height, fill = 'grey12')
    txt = 'PAUSED'
    canvas.create_text(data.width // 2 , data.height // 2, text = txt, font = ('Fixedsys', 30, 'bold'),  fill = data.fontFill)
    txt = 'PLAY'
    canvas.create_text(data.width - 30, 50, anchor = 'se', text = txt, font = ('Fixedsys', 30, 'bold'), fill = data.fontFill)
def changeModes(data):
    if(data.playBox[0][0] < data.mouseX < data.playBox[1][0] and data.playBox[0][1] < data.mouseY < data.playBox[1][1]):
        data.mode = 'Playing'
def redrawAll(canvas, data):
    drawPauseScreen(canvas, data)
