from tkinter import *

canvas_width = 500
canvas_height = 150
arq = open("arq.txt", "w")
l = []
primeiro = 0

def paint( event ):
   python_green = "#476042"
   x1, y1 = ( event.x - 10 ), ( event.y - 10 )
   x2, y2 = ( event.x + 10 ), ( event.y + 10 )
   # print(x1,x2,y1,y2)
   # if primeiro == 0:
   #    l.append(x1)
   #    l.append(y1)
   #    primeiro = 1
   # else:
   #    if x1 != l[-2] and y1 != l[-1]:
   #       l.append(x1)
   #       l.append(y1)
          
   # w.create_line( x1, y1, x2, y2, fill = python_green, width=5 )
   w.create_oval( x1, y1, x2, y2, fill = "black", width=5 )

def save(event):
   string = ""
   for i in l:
      string += str(i) + ","
   arq.write(string)
   arq.close()

master = Tk()
master.title( "Painting using Ovals" )
w = Canvas(master, 
           width=canvas_width, 
           height=canvas_height)
w.pack(expand = YES, fill = BOTH)
w.bind( "<B1-Motion>", paint )
w.bind( "<ButtonPress-3>", save)

message = Label( master, text = "Press and Drag the mouse to draw" )
message.pack( side = BOTTOM )
    
mainloop()