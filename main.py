from graphics import *
import time

data = [[9, 7, 8, 8],
     [5, 5, 1, 6],
     [2, 1, 1, 4],
     [7, 3, 7, 4]]
sumX = [1, 2, 3, 4]
sumY = [6, 7, 8, 9]

def resetColor(rect):
    for i in range(0, len(rect[0])-1):
        for j in range(0, len(rect[0])-1):
                rect[i][j].setFill(color_rgb(0, 100, 255))

def changeColor(rect, wip):
    resetColor(rect)
    for i in range(0, len(rect[0])-1):
        for j in range(0, len(rect[0])-1):
            if wip[i][j] == 1:
                rect[i][j].setFill(color_rgb(0, 220, 220))


def setDefault(win, n, data, sumX, sumY):

    rect = [[0 for x in range(n + 1)] for y in range(n + 1)]

    for x in range(n + 1):
        for y in range(n + 1):
            if x == n and y == n:
                break
            rect[x][y] = Rectangle(Point((y + 1) * 100, (x + 1) * 100), Point((y + 1) * 100 + 100, (x + 1) * 100 + 100))
            if x == n or y == n:
                rect[x][y].setFill(color_rgb(220, 220, 220))

            else:
                rect[x][y].setFill(color_rgb(0, 100, 255))
            rect[x][y].draw(win)

            if x == n:
                txt = Text(Point((y + 1) * 100 + 50, (x + 1) * 100 + 50), sumX[y])
                txt.setTextColor(color_rgb(128, 128, 128))
            elif y == n:
                txt = Text(Point((y + 1) * 100 + 50, (x + 1) * 100 + 50), sumY[x])
                txt.setTextColor(color_rgb(128, 128, 128))
            else:
                txt = Text(Point((y + 1) * 100 + 50, (x + 1) * 100 + 50), data[x][y])
                txt.setTextColor(color_rgb(255, 255, 255))
            txt.setSize(30)
            txt.setStyle('bold')
            txt.draw(win)
    return rect


def createUI(n):
    width = 100*(n+3)
    win = GraphWin("Pluszle", width, width+100)

    return win

def menu(win):
    winWidth = win.getWidth()
    winHeight = win.getHeight()

    logo = Image(Point(winWidth / 2, winHeight / 4), "logo.gif")
    imgMethod = Image(Point(winWidth / 2, winHeight / 4 + 225), "method.gif")
    imgMet1 = Image(Point(winWidth / 2, winHeight / 4 + 300), "met1.gif")
    imgMet2 = Image(Point(winWidth / 2, winHeight / 4 + 350), "met2.gif")

    win.setBackground(color_rgb(255, 255, 255))
    logo.draw(win)
    imgMethod.draw(win)
    imgMet1.draw(win)
    imgMet2.draw(win)

    while True:
        algo = win.getKey()
        if algo == '1' or algo == '2':
            break
    return algo

def clear(win):
    for item in win.items[:]:
        item.undraw()
    win.update()

def main():
    n = 4
    selectedPos = [[0, 0, 1, 0],
           [0, 0, 1, 1],
           [1, 0, 0, 1],
           [1, 0, 1, 0]]

    win = createUI(n)

    algo = menu(win) #string

    clear(win)

    win.setBackground(color_rgb(255, 255, 255))

    problemTable = setDefault(win, n, data, sumX, sumY)
    changeColor(problemTable, selectedPos)

    win.getMouse()
    win.close()

main()


# test
# def line(x1, y1, x2, y2):
#     return Line(Point(x1, y1), Point(x2, y2))
#
# def main():
#     win = GraphWin("Sum Number", 500, 500)
#     win.setBackground(color_rgb(255, 255, 255))
#
#     # pt = Point(250, 250)
#     # cir = Circle(pt, 50)
#     # cir.setFill(color_rgb(100, 255, 50))
#     # cir.draw(win)
#     # pt.setOutline(color_rgb(255, 255, 0))
#     # pt.draw(win)
#
#     # ln = line(250, 250, 250, 350)
#     # ln.setOutline(color_rgb(0, 255, 255))
#     # ln.setWidth(5)
#     # ln.draw(win)
#
#     rect = Rectangle(Point(250, 250), Point(350, 350))
#     rect.setOutline(color_rgb(0, 255, 255))
#     rect.setWidth(5)
#     rect.setFill(color_rgb(0, 100, 255))
#     rect.draw(win)
#
#     cir = Circle(Point(250, 250), 50)
#     cir.setOutline(color_rgb(0, 255, 255))
#     cir.setWidth(5)
#     cir.setFill(color_rgb(0, 100, 255))
#     cir.draw(win)
#
#     # poly = Polygon(Point(40, 40), Point(100, 100),
#     #                Point(40, 100), Point(300, 70),
#     #                Point(450, 70))
#     # poly.setFill(color_rgb(255, 255, 0))
#     # poly.setOutline(color_rgb(0, 255, 255))
#     # poly.setWidth(5)
#     # poly.draw(win)
#
#     # txt = Text(Point(250, 250), "What's up?")
#     # txt.setTextColor(color_rgb(0, 255, 0))
#     # txt.setSize(20)
#     # txt.setFace('courier')
#     # txt.draw(win)
#
#     #Create our objects
#     input_box = Entry(Point(250, 250), 10)
#     input_box.draw(win)
#     txt = Text(Point(250, 280), "")
#     txt.draw(win)
#
#     #Wait to do stuffwith our objects
#     while True:
#         txt.setText(input_box.getText())
#
#     win.getMouse()
#     win.close()
#
# main()
