import pygame
import math

pygame.init()

#initialise layout
screen = pygame.display.set_mode((640, 640))
nodeNum = 6
centerX = 320
centerY = 200
radius = 150
nodeRadius = 15 
presence = 1
edges = 0
showNodeNums = True
showNodeDegrees = False

#initialise node coords
baseAngle = 0
coordsX = []
coordsY = []
def getDefaultCoords():
    global nodeNum, centerX, centerY, radius, baseAngle, coordsX, coordsY
    coordsX = []
    coordsY = []
    for i in range(0, nodeNum):
        coordsX.append(centerX + radius*(math.cos(baseAngle + ((i)*((2*math.pi)/nodeNum)))))
        coordsY.append(centerY - radius*(math.sin(baseAngle + ((i)*((2*math.pi)/nodeNum)))))
getDefaultCoords()

#import graphics
node = pygame.image.load("pygame\\graphoo2\\node.png").convert_alpha()
arrowL = pygame.image.load("pygame\\graphoo2\\left arrow.png").convert_alpha()
arrowL = pygame.transform.scale(arrowL, 
                                 (arrowL.get_width() * 0.5,
                                  arrowL.get_height() * 0.5))
arrowR = pygame.image.load("pygame\\graphoo2\\right arrow.png").convert_alpha()
arrowR = pygame.transform.scale(arrowR, 
                                 (arrowR.get_width() * 0.5,
                                  arrowR.get_height() * 0.5))
fontNode = pygame.font.Font("pygame\\graphoo2\\Code New Roman.otf", size=30)
fontUI = pygame.font.Font("pygame\\graphoo2\\Code New Roman.otf", size=15)

#initialise ui
nodeLand = pygame.Rect(25, 25, 590, 350)
nodeNumCtrlLand = pygame.Rect(25, 400, 215, 35)
edgeChangeLand = pygame.Rect(25, 450, 215, 70)
statsLand = pygame.Rect(265, 400, 350, 120)

nodeNumText = fontUI.render("number of nodes:    " + str(nodeNum), True, (0, 0, 0))
eblText = fontUI.render("blank", True, (255, 255, 255))
eflText = fontUI.render("fill", True, (255, 255, 255))
showNodeNum = fontUI.render("show", True, (255, 255, 255))
hideNodeNum = fontUI.render("hide", True, (255, 255, 255))
showNodeDegree = fontUI.render("show", True, (255, 255, 255))
hideNodeDegree = fontUI.render("hide", True, (255, 255, 255))
bgText = fontUI.render("    /      all edges\n     /      node numbers\n     /      node degrees", True, (0, 0, 0))
statsText = fontUI.render("", True, (0, 0, 0))

#initialise base variables
running = True
x = 0
selectedNode = -1
clock = pygame.time.Clock()
delta_time = 0.01
mlerm = ""

#initialise matrix
edgeMatrix = []
def makeMatrix(present):
    global nodeNum, edgeMatrix
    edgeMatrix = []
    for i in range(0, nodeNum):
        edgeMatrix.append([])
        for j in range(0, nodeNum):
            edgeMatrix[i].append(present)
makeMatrix(presence)

def printMatrix():
    global nodeNum, edgeMatrix
    print("   ", end="")
    for i in range(0, nodeNum):
        print(str(i+1), end="  ")
    print()
    for i in range(0, nodeNum):
        print(str(i+1), edgeMatrix[i])
    print()

#other functions
def drawGraph():
    for i in range(0, nodeNum):
        for j in range(0, nodeNum):
            if edgeMatrix[i][j] == 1:
                pygame.draw.line(screen, (0, 0, 0), (coordsX[i], coordsY[i]), (coordsX[j], coordsY[j]), width=2)

    for i in range(0, nodeNum):
        nodeText = fontNode.render(str(i+1), True, (255, 255, 255))
        degreeText = fontUI.render(str(findDegree(i)), True, (0, 0, 255), (255, 255, 255))
        screen.blit(node,(coordsX[i] - 15, coordsY[i] - 15))
        if showNodeNums:
            screen.blit(nodeText, (coordsX[i] - 7, coordsY[i] - 12))
        if showNodeDegrees:
            screen.blit(degreeText, (coordsX[i] + 5, coordsY[i] + 10))

        

def refreshNodeNum():
    global nodeNumText, presence
    nodeNumText = fontUI.render("number of nodes:    " + str(nodeNum), True, (0, 0, 0))
    getDefaultCoords()
    makeMatrix(presence)
    getDefaultCoords()

def findClickedNode():
    global coordsX, coordsY, nodeRadius, mouseX, mouseY
    for i in range(0, nodeNum):
        if coordsX[i] - nodeRadius < mouseX < coordsX[i] + nodeRadius:
            if coordsY[i] - nodeRadius < mouseY < coordsY[i] + nodeRadius:
                return i
    return -1

def findEdgeNum():
    global edgeMatrix
    #edgeMatrix2 = edgeMatrix.copy()
    edgeNum = 0
    for i in range(0, nodeNum):
        for j in range(i+1, nodeNum):
            if edgeMatrix[i][j] == 1:
                edgeNum += 1
                #edgeMatrix2[i][j] = 2
        #print(edgeMatrix2[i])
    #print()
    return edgeNum

def findDegree(node): #node is indexed at zero
    global edgeMatrix
    degree = -1
    for i in range(0, nodeNum):
        if edgeMatrix[node][i] == 1:
            degree += 1
    return degree

def isEven(num):
    if num % 2 == 1:
        return False
    else:
        return True

def isEulerian():
    evenNodes = 0
    for i in range(0, nodeNum):
        if isEven(findDegree(i)):
            evenNodes += 1
    if evenNodes == nodeNum:
        return "Eulerian"
    elif isEven(nodeNum - evenNodes):
        return "Semi Eulerian"
    else:
        return "Not Eulerian"


def statsWrite():
    global statsText
    v = nodeNum
    e = findEdgeNum()
    f = 2 + e - v
    eulerian = isEulerian()
    statsText = fontUI.render("vertices: " + str(v) + "\nedges: " + str(e) + "\nfaces: " + str(f) + "\neulerian: " + str(eulerian), True, (0, 0, 0))
    
while running:
    #refresh layout
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (200, 200, 200), nodeLand)
    pygame.draw.rect(screen, (200, 200, 200), nodeNumCtrlLand)
    pygame.draw.rect(screen, (200, 200, 200), edgeChangeLand)
    pygame.draw.rect(screen, (200, 200, 200), statsLand)
    screen.blit(nodeNumText, (35, 410))
    screen.blit(arrowL, (175, 410))
    screen.blit(arrowR, (215, 410))
    screen.blit(bgText, (35, 460))
    screen.blit(eflText, (35, 460))
    screen.blit(eblText, (80, 460))
    screen.blit(showNodeNum, (35, 478))
    screen.blit(hideNodeNum, (90, 478))
    screen.blit(showNodeDegree, (35, 496))
    screen.blit(hideNodeDegree, (90, 496))

    statsWrite()
    screen.blit(statsText, (275, 410))
    drawGraph()

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX = pygame.mouse.get_pos()[0]
            mouseY = pygame.mouse.get_pos()[1]
            #print(mouseX, mouseY)

            if (nodeRadius + 25 < mouseX < 615 - nodeRadius) and (nodeRadius + 25 < mouseY < 375 - nodeRadius):
                if selectedNode != -1:
                    if findClickedNode() == -1:
                        coordsX[selectedNode] = mouseX
                        coordsY[selectedNode] = mouseY
                    else:
                        if edgeMatrix[selectedNode][findClickedNode()] == 0:
                            edgeMatrix[selectedNode][findClickedNode()] = 1
                            edgeMatrix[findClickedNode()][selectedNode] = 1
                        else:
                            edgeMatrix[selectedNode][findClickedNode()] = 0
                            edgeMatrix[findClickedNode()][selectedNode] = 0
                    selectedNode = -1
                else:
                    selectedNode = findClickedNode()
            else:
                selectedNode = -1
                if 400 <= mouseY <= 420:
                    keys = pygame.key.get_pressed()
                    if 170 <= mouseX <= 195: #arrowL clicked
                        if keys[pygame.K_LCTRL]:
                            nodeNum = 0
                        else:
                            if nodeNum > 0:
                                nodeNum -= 1
                    elif 210 <= mouseX <= 235: #arrowR clicked
                        if keys[pygame.K_LCTRL]:
                            nodeNum = 30
                        else:
                            if nodeNum < 30:
                                nodeNum += 1
                    refreshNodeNum()
                elif 455 <= mouseY <= 470:
                    if 35 <= mouseX <= 70: #fill edges
                        presence = 1
                    elif 80 <= mouseX <= 120: #blank edges
                        presence = 0
                    makeMatrix(presence)
                elif 475 <= mouseY <= 489:
                    if 35 <= mouseX <= 70: #show node nums
                        showNodeNums = True
                    elif 90 <= mouseX <= 125: #hide node nums
                        showNodeNums = False
                elif 490 <= mouseY <= 510:
                    if 35 <= mouseX <= 70: #show node degrees
                        showNodeDegrees = True
                    elif 90 <= mouseX <= 125: #show node degrees
                        showNodeDegrees = False
                    

            
                
    #tick
    pygame.display.flip()
    delta_time = clock.tick(60) / 1000
    delta_time = max(0.001, min(0.1, delta_time))

pygame.quit()