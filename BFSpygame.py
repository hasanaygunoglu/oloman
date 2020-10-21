import pygame
import sys
from collections import deque
from tkinter import messagebox, Tk

size = (width, height) = (800,600)

rows = 30
cols = 40

rectHeight = width//cols
rectWidth = height//rows

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
PURPLE = (102, 0, 102)
YELLOW = (255,255,0)

pygame.init()

wn = pygame.display.set_mode(size)
pygame.display.set_caption("Shortest Path w/ BFS")

class Node:
    
    def __init__(self, row, col, rectHeight, rectWidth):
        self.row = row
        self.col = col
        self.rectHeight = rectHeight
        self.rectWidth = rectWidth
        self.color = WHITE
        self.neighbors = []
        self.prev = []

    def get_pos(self):
        return self.row, self.col


    def is_visited(self):
        return self.color == GREEN

    def is_obstacle(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == YELLOW

    def is_end(self):
        return self.color == PURPLE

    def make_visited(self):
        self.color = GREEN

    def make_obstacle(self):
        self.color = BLACK

    def make_start(self):
        self.color = RED

    def make_end(self):
        self.color = PURPLE                
    
    def make_queue(self):
        self.color = YELLOW

    def make_path(self):
        self.color = BLUE    

    def draw(self):
        pygame.draw.rect(wn, self.color, (self.row*rectHeight,self.col*rectWidth,self.rectHeight-1,self.rectWidth-1))    


def make_grid(rows):
    for i in range(cols):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, 20, 20)
            grid[i].append(node)
    return grid        

def draw(startNode, endNode, grid, rows):
    for row in grid:
        for node in row:
            if node is not startNode and node != endNode and node.color != BLUE and node.color != BLACK and node in queue:
                node.make_queue()
                node.draw()
            elif node is not startNode and node != endNode and node.color != BLUE and node.color != BLACK and node in visited:
                node.make_visited()
                node.draw()
            else:
                node.draw()        
    
    pygame.display.update()

def BFS(startNode, endNode):
    
    queue.append(startNode)
    visited.add(startNode)

    searchFlag = True
    startFlag = True
    while startFlag and queue:
        current = queue.popleft()
        x,y = current.get_pos()

        if current == endNode:
            back_tracking(current, startNode, endNode)
            Tk().wm_withdraw()
            messagebox.showinfo("Found it","Found it!")
            searchFlag = False 
        if searchFlag:
            if grid[x][y-1].col > 0 and grid[x][y-1] not in visited and not grid[x][y-1].is_obstacle(): # UP
                visited.add(grid[x][y-1])
                queue.append(grid[x][y-1])
                grid[x][y-1].prev.append(grid[x][y])

            if grid[x][y+1].col < 29 and grid[x][y+1] not in visited and not grid[x][y+1].is_obstacle(): # DOWN            
                visited.add(grid[x][y+1])
                queue.append(grid[x][y+1])
                grid[x][y+1].prev.append(grid[x][y])

            if grid[x+1][y].row < 39 and grid[x+1][y] not in visited and not grid[x+1][y].is_obstacle(): # RIGHT            
                visited.add(grid[x+1][y])
                queue.append(grid[x+1][y])            
                grid[x+1][y].prev.append(grid[x][y])

            if grid[x-1][y].row > 0 and grid[x-1][y] not in visited and not grid[x-1][y].is_obstacle(): # LEFT
                visited.add(grid[x-1][y])
                queue.append(grid[x-1][y])
                grid[x-1][y].prev.append(grid[x][y]) 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        draw(startNode, endNode, grid, rows)

def back_tracking(current, startNode, endNode):
    while current != startNode:       
        current = current.prev[0]
        if current != startNode:
            current.make_path()
        draw(startNode, endNode, grid, rows)
        pygame.time.delay(40)    
       
def click_pos(pos):
    a,b = pos
    a = a//rectHeight
    b = b//rectWidth
    return a,b        
    
grid = []
queue = deque()
visited = set()

make_grid(rows)

startNode = None
endNode = None

def main(startNode, endNode):

    still_going = True
    
    while still_going:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                still_going = False
            
            if pygame.mouse.get_pressed()[0]: 
                pos = pygame.mouse.get_pos()
                a,b = click_pos(pos)
                startNode = grid[a][b]
                startNode.make_start()
            elif pygame.mouse.get_pressed()[2]: 
                pos = pygame.mouse.get_pos()
                a,b = click_pos(pos)
                endNode = grid[a][b]
                endNode.make_end()
            elif pygame.mouse.get_pressed()[1]: 
                pos = pygame.mouse.get_pos()
                a,b = click_pos(pos)
                obstacle = grid[a][b]
                obstacle.make_obstacle()               


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and startNode and endNode:
                    BFS(startNode, endNode)    
        draw(startNode, endNode, grid, rows)    

main(startNode, endNode)    