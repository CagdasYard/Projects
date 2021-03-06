import pyglet
import random
def out_of_bounds(WIDTH,HEIGHT,POS,DIRECTION):
       return POS[1]+DIRECTION[1] < 0 or POS[1]+DIRECTION[1] >= HEIGHT or POS[0]+DIRECTION[0]< 0 or POS[0]+DIRECTION[0] >= WIDTH


class Labyrinth(pyglet.window.Window):
       def __init__(self,_COLUMN_,_ROW_,_GRID_SIZE_,_LINE_WIDTH_):
              self.GRID_SIZE   = int(_GRID_SIZE_)
              self.ROW_SIZE    = int(_ROW_)
              self.COLUMN_SIZE = int(_COLUMN_)
              self.LINE_WIDTH  = _LINE_WIDTH_
              self.HEIGHT      = self.ROW_SIZE    * self.GRID_SIZE +self.LINE_WIDTH
              self.WIDTH       = self.COLUMN_SIZE * self.GRID_SIZE +self.LINE_WIDTH
              self.POS         = [0,0]
              self.LINES       = []
              self.BLOCKS      = []
              self.STACK       = []
              self.RESTART     = False
              self.DIRECTION   = []
              self.DIRECTIONS  = [[1,0],[0,1],[-1,0],[0,-1]]
              self.ALTERNATIVE_ROUTE=True
              self.STOP        = False
              super().__init__(self.WIDTH,self.HEIGHT)
              self.initialize()
              pyglet.clock.schedule_interval(self.update, 1.0/60.0)
       def on_draw(self):
              self.clear()
              pyglet.gl.glLineWidth(self.LINE_WIDTH)
              for LINE in self.LINES:
                     ## HORIZONTAL LINES
                     if LINE[1]== LINE[3]:
                            COORDINATES= (LINE[0]*self.GRID_SIZE,
                                          LINE[1]*self.GRID_SIZE+self.LINE_WIDTH/2,
                                          LINE[2]*self.GRID_SIZE+self.LINE_WIDTH,
                                          LINE[3]*self.GRID_SIZE+self.LINE_WIDTH/2)
                            pyglet.graphics.draw(2, pyglet.gl.GL_LINES,('v2f', COORDINATES))
       
                     # VERTICAL LINES
                     if LINE[0]== LINE[2]:
                            COORDINATES= (LINE[0]*self.GRID_SIZE+self.LINE_WIDTH/2,
                                          LINE[1]*self.GRID_SIZE,
                                          LINE[2]*self.GRID_SIZE+self.LINE_WIDTH/2,
                                          LINE[3]*self.GRID_SIZE+self.LINE_WIDTH)
                            pyglet.graphics.draw(2, pyglet.gl.GL_LINES,('v2f', COORDINATES))
                            
              RECTANGLE= (self.POS[0]*self.GRID_SIZE    + 2*self.LINE_WIDTH, self.POS[1]   *self.GRID_SIZE + 2*self.LINE_WIDTH,
                          self.POS[0]*self.GRID_SIZE    + 2*self.LINE_WIDTH,(self.POS[1]+1)*self.GRID_SIZE - 1*self.LINE_WIDTH,
                         (self.POS[0]+1)*self.GRID_SIZE - 1*self.LINE_WIDTH,(self.POS[1]+1)*self.GRID_SIZE - 1*self.LINE_WIDTH,
                         (self.POS[0]+1)*self.GRID_SIZE - 1*self.LINE_WIDTH, self.POS[1]   *self.GRID_SIZE + 2*self.LINE_WIDTH)

              pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
                                                         [0,1,2,2,3,0],('v2f',RECTANGLE))
       def initialize(self):
              ## HORIZONTAL LINES
              for ITER1 in range(self.ROW_SIZE+1):                   
                     for ITER2 in range(self.COLUMN_SIZE):
                            self.LINES.append((ITER2,ITER1,ITER2+1,ITER1))
                            
              ## VERTICAL LINES
              for ITER1 in range(self.COLUMN_SIZE+1):
                     for ITER2 in range(self.ROW_SIZE):             
                            self.LINES.append((ITER1,ITER2,ITER1,ITER2+1))
                            
              for ITER1 in range(self.COLUMN_SIZE):
                     for ITER2 in range(self.ROW_SIZE):
                            self.BLOCKS.append([ITER1,ITER2])
              self.BLOCKS.remove(self.POS)

       def on_key_press(self,symbol,modifiers):
              if symbol == pyglet.window.key.SPACE:
                     self.RESTART=not self.RESTART
       def restart(self):
              if self.RESTART:
                     self.LINES.clear()
                     ## HORIZONTAL LINES
                     for ITER1 in range(self.ROW_SIZE+1):                   
                            for ITER2 in range(self.COLUMN_SIZE):
                                   self.LINES.append((ITER2,ITER1,ITER2+1,ITER1))
                                   
                     ## VERTICAL LINES
                     for ITER1 in range(self.COLUMN_SIZE+1):
                            for ITER2 in range(self.ROW_SIZE):             
                                   self.LINES.append((ITER1,ITER2,ITER1,ITER2+1))
                                   
                     for ITER1 in range(self.COLUMN_SIZE):
                            for ITER2 in range(self.ROW_SIZE):
                                   self.BLOCKS.append([ITER1,ITER2])
                     self.BLOCKS.remove(self.POS)
              else:
                     pass
              
       def update(self,dt):
              if not self.STOP:
                     if len(self.BLOCKS) != 0:
                            self.DIRECTION=random.choice(self.DIRECTIONS)
                            if out_of_bounds(self.COLUMN_SIZE,self.ROW_SIZE,self.POS,self.DIRECTION):
                                   self.ALTERNATIVE_ROUTE=False
                                   for DIRECTION in self.DIRECTIONS:
                                          if not out_of_bounds(self.COLUMN_SIZE,self.ROW_SIZE,self.POS,DIRECTION):
                                                 self.ALTERNATIVE_ROUTE=True    
                                                 self.DIRECTION=DIRECTION
                                                 break
                            if [self.DIRECTION[0]+self.POS[0],self.DIRECTION[1]+self.POS[1]] not in self.BLOCKS:
                                   self.ALTERNATIVE_ROUTE=False              
                                   for DIRECTION in self.DIRECTIONS:
                                          if [DIRECTION[0]+self.POS[0],DIRECTION[1]+self.POS[1]] in self.BLOCKS:
                                                 self.ALTERNATIVE_ROUTE=True    
                                                 self.DIRECTION=DIRECTION
                                                 break
                            if not self.ALTERNATIVE_ROUTE:
                                   self.POS=self.STACK[-1] 
                                   self.STACK.pop()

                            if self.ALTERNATIVE_ROUTE:
                                   POS=self.POS.copy()
                                   self.STACK.append(POS)
                                   if self.DIRECTION == [1,0]:
                                          LINE=(self.POS[0]+self.DIRECTION[0],self.POS[1]+self.DIRECTION[1],
                                                self.POS[0]+self.DIRECTION[0],self.POS[1]+self.DIRECTION[1]+1)
                                   elif self.DIRECTION == [0,1]:
                                          LINE=(self.POS[0]+self.DIRECTION[0],self.POS[1]+self.DIRECTION[1],
                                                self.POS[0]+self.DIRECTION[0]+1,self.POS[1]+self.DIRECTION[1])
                                   elif self.DIRECTION == [-1,0]:
                                          LINE=(self.POS[0],self.POS[1],self.POS[0],self.POS[1]+1)
                                   else:
                                          LINE=(self.POS[0],self.POS[1],self.POS[0]+1,self.POS[1])
                                          
                                   self.POS[0]+=self.DIRECTION[0]
                                   self.POS[1]+=self.DIRECTION[1]
                                   
                                   if LINE in self.LINES:
                                          self.LINES.remove(LINE)
                                   self.BLOCKS.remove(self.POS)
                     else:
                            self.restart()
       
if __name__ == '__main__' :
       WINDOW = Labyrinth(35,20,30,1)
       WINDOW.push_handlers(pyglet.window.event.WindowEventLogger())
       WINDOW.set_exclusive_mouse(False)
#### Gives complete control of the mouse to our application if true
       pyglet.app.run()
