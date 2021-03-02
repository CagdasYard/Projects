import pyglet
import random
from time import process_time
class cellgame:
       def __init__(self,_WINDOW_WIDTH_,_WINDOW_HEIGHT_,_CELL_SIZE_,_PERCENT_FILL_):
              self.GRID_WIDTH  = _WINDOW_WIDTH_  // _CELL_SIZE_
              self.GRID_HEIGHT = _WINDOW_HEIGHT_ // _CELL_SIZE_
              self.PERCENT_FILL= _PERCENT_FILL_
              self.CELL_SIZE   = _CELL_SIZE_
              self.CELLS       = []
              self.generate_cells()
       def generate_cells(self):
              for ROW in range(self.GRID_HEIGHT):
                     self.CELLS.append([])
                     for COLUMN in range(self.GRID_WIDTH):
                            if random.random() > self.PERCENT_FILL:
                                   self.CELLS[ROW].append(1)
                            else:
                                   self.CELLS[ROW].append(0)

       def rules(self):
              TEMP=[]
              for ROW in range(self.GRID_HEIGHT):
                     TEMP.append([])
                     for COLUMN in range(self.GRID_WIDTH):
                            CELL_SUM= sum([self.get_cell_value(ROW-1,COLUMN  ),
                                           self.get_cell_value(ROW-1,COLUMN-1),
                                           self.get_cell_value(ROW  ,COLUMN-1),
                                           self.get_cell_value(ROW+1,COLUMN-1),
                                           self.get_cell_value(ROW+1,COLUMN  ),
                                           self.get_cell_value(ROW+1,COLUMN+1),
                                           self.get_cell_value(ROW  ,COLUMN+1),
                                           self.get_cell_value(ROW-1,COLUMN+1)])

                            if self.CELLS[ROW][COLUMN] == 0 and CELL_SUM == 3:
                                   TEMP[ROW].append(1)
                            elif self.CELLS[ROW][COLUMN] == 1 and (CELL_SUM==3 or CELL_SUM==2):
                                   TEMP[ROW].append(1)
                            else:
                                   TEMP[ROW].append(0)

              self.CELLS= TEMP                            
       def get_cell_value(self,ROW,COLUMN):
              if ROW >= 0 and ROW < self.GRID_HEIGHT and COLUMN >= 0 and COLUMN < self.GRID_WIDTH:
                        return self.CELLS[ROW][COLUMN]
              return 0
       def draw(self):
              for ROW in range(self.GRID_HEIGHT):
                     for COLUMN in range(self.GRID_WIDTH):
                            if self.CELLS[ROW][COLUMN] == 1:
                                   SQUARE_COORDINATES=(ROW*self.CELL_SIZE   , COLUMN   *self.CELL_SIZE,
                                                       ROW*self.CELL_SIZE   ,(COLUMN+1)*self.CELL_SIZE,
                                                      (ROW+1)*self.CELL_SIZE, COLUMN   *self.CELL_SIZE,
                                                      (ROW+1)*self.CELL_SIZE,(COLUMN+1)*self.CELL_SIZE)
                                   pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,[0,1,2,1,2,3],
                                                                ('v2i',SQUARE_COORDINATES))

              
class appwindow(pyglet.window.Window):

       def __init__(self):
              super().__init__(600,600)
              self.CELLGAME = cellgame(self.get_size()[0],self.get_size()[1],10,0.6)
              pyglet.clock.schedule_interval(self.update, 1.0/30.0)
       def on_draw(self):
              self.clear()
              self.CELLGAME.draw()
       def update(self,dt):
              self.CELLGAME.rules()


if __name__ == '__main__':
       
       WINDOW = appwindow()

       WINDOW.set_exclusive_mouse(False)
## Gives complete control of the mouse to our application if true
       pyglet.app.run()
