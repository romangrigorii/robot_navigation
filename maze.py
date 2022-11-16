##############################
# Python maze generator code #
##############################

import pygame, sys, time ,random, numpy as np, pickle

class Environment:

    WHITE = (255,255,255)
    GREEN = (0,255,0)
    BLUE = (0,0,255)
    YELLOW = (255,255,0)
    RED = (255,0,0)
    BLACK = (0,0,0)

    def __init__(self,width = 500, height = 500, ncellsx = 20, ncellsy = 20, visualize = 0):

        self.visualize = visualize

        self.width = width
        self.height = height
        self.size = (self.width,self.height)
        self.screen = None
        self.clock = None

        self.ncellsx = ncellsx
        self.ncellsy = ncellsy
        self.pos = (int(self.ncellsx/2),int(self.ncellsy/2))
        self.pos = (0,0)
        self.oldpos = self.pos
        self.wx = self.width/self.ncellsx
        self.wy = self.height/self.ncellsy

        self.grid = []
        self.visited = []
        self.stack = []
        self.solution = {}
        self.graph = {}
        self.paths = []

        self.FPS = 10


    def init_maze_environment(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('a maze')
        self.clock = pygame.time.Clock()
    
    def build_grid(self):
        self.screen.fill(self.BLACK)
        for x in range(self.ncellsx+1):
            pygame.draw.line(self.screen,self.WHITE, [x*self.wx,0],[x*self.wx,self.height])
        for y in range(self.ncellsy+1):
            pygame.draw.line(self.screen,self.WHITE, [0,y*self.wy],[self.width,y*self.wy])

    def build_maze(self):
        self.visited.append(self.pos);
        self.stack.append(self.pos)
        while self.stack:
        #for i in range(10):
            if self.visualize:
                time.sleep(.00)
            locs = np.random.permutation([(1,0),(-1,0),(0,1),(0,-1)])
            flag = 1
            for loc in [tuple(a) for a in locs]:
                newpos = (loc[0]+self.pos[0],loc[1]+self.pos[1])
                if newpos[0]>=0 and newpos[0]<self.ncellsx and newpos[1]>=0 and newpos[1]<self.ncellsy and newpos not in self.visited:
                    if self.pos not in self.graph:
                        self.graph[self.pos] = []
                    self.graph[self.pos].append(newpos)
                    flag = 0
                    self.visited.append(newpos)
                    self.stack.append(self.pos)
                    direction = int(loc==(1,0)) + 2*int(loc==(0,1)) + 3*int(loc == (-1,0))
                    if self.visualize:
                        self.draw_rect(self.BLUE,4,self.oldpos,self.wx,self.wy)
                        self.draw_rect(self.BLUE,direction,self.pos,self.wx,self.wy)
                        self.draw_pos(self.pos)
                    self.oldpos = self.pos
                    self.pos = newpos
                    break
            if flag and self.stack:
                self.pos = self.stack.pop()

    def build_corner():
        pass

    def populate_maze(self):
        for x in range(self.ncellsx):
            for y in range(self.ncellsy):
                if self.graph.get((x,y)):
                    for h in self.graph.get((x,y)):
                        self.draw_rect_2(self.BLUE,(x,y),h)


    def run(self):
        flag = 1
        pygame.display.flip() 
        while flag:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                flag = event.type != pygame.QUIT

    def draw_pos(self, pos):
        pygame.draw.circle(self.screen,self.WHITE,((pos[0]+.5)*self.wx, (pos[1]+.5)*self.wy),self.wx/3)
        pygame.display.update()

    def draw_rect(self,color,direction,pos,dx,dy):
        if direction == 'left' or direction == 3 :
            pygame.draw.rect(self.screen,color, (pos[0]*self.wx-self.wx/2-dx/2+1,pos[1]*self.wy+1,dx + self.wx - 1, self.wy-1))
        if direction == 'right' or direction == 1 :
            pygame.draw.rect(self.screen,color, (pos[0]*dx+(self.wx-dx)/2+1,pos[1]*dy+1,dx + self.wx-1, self.wy-1))
        if direction == 'up' or direction == 0:
            pygame.draw.rect(self.screen,color, (pos[0]*dx+1,pos[1]*dy-self.wx/2-dy/2+1,self.wx-1, dx + self.wy-1))
        if direction == 'down' or direction == 2:
            pygame.draw.rect(self.screen,color, (pos[0]*dx+1,pos[1]*dy+1+(self.wy-dy)/2,self.wx - 1, dx + self.wy-1))
        else:
            pygame.draw.rect(self.screen,color, (pos[0]*self.wx+1+(self.wx-dx)/2,pos[1]*self.wy+(self.wy-dy)/2+1,dx-1, dy-1))
        pygame.display.update()

    def draw_rect_2(self,color,pos1,pos2):
        loc = (pos2[0]-pos1[0], pos2[1]-pos1[1])
        direction = int(loc==(1,0)) + 2*int(loc==(0,1)) + 3*int(loc == (-1,0))
        self.draw_rect(color,direction,pos1,self.wx,self.wy)

    def state_machine(self, type = "maze", build = 1):
        if self.visualize:
            self.init_maze_envronment()
            self.build_grid()
        if type == "maze":
            if build:
                self.build_maze()
            else:
                self.populate_maze()
        if type == "corner":
            if build:
                self.build_corner((7,13),(7,7),(13,7),(13,13))
            else:
                self.populate_corner()
        
        if self.visualize:
            self.run()

    def retgraph(self):
        return self.graph
    
    def save_graph(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.graph, file, protocol=pickle.HIGHEST_PROTOCOL)
        
    def load_graph(self,filename):
        with open(filename,'rb') as file:
            self.graph = pickle.load(file)

if __name__ == "__main__":
    m = MAZE(ncellsx = 12, ncellsy = 9, visualize = True)
    m.state_machine()
    print(m.retgraph())    
    m.save_graph("amaze.pickle")
    m.build_grid()
    m.state_machine(build = 0)