
def drawElements(canvas, data):
    txt = 'WELCOME TO'
    canvas.create_text(data.width // 2, data.height // 2 - 90, anchor = 's', text = txt, font = ('Fixedsys', 30, 'bold'), fill = data.fontFill)
    txt = 'CAVE'
    canvas.create_text(data.width // 2, data.height // 2 - 20, text = txt, font = ('Fixedsys', 200, 'bold'), fill = data.fontFill)
    txt = 'CLICK ANYWHERE TO PLAY'
    canvas.create_text(data.width // 2, data.height // 2 + 130, anchor = 's', text = txt, font = ('Fixedsys', 30, 'bold'), fill = data.fontFill)
def drawBackground(canvas, data):
    canvas.create_rectangle(0,0, data.width, data.height, fill = 'grey12')
    for wall in data.walls:
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
def changeModes(data):
    data.mode = 'Playing'
def redrawAll(canvas, data):
    drawBackground(canvas, data)
    drawElements(canvas, data)
