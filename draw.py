import numpy as np
import pygame as p
import itertools
from time import sleep

PSIZE = 0.6
LINEWIDTH = 2
MUL = 0.11
SPACING = 7
TOPMARGIN = 20
white = (255,255,255)
black = (0,0,0)

with open("pol_msk_alt.asc") as f:
    data =f.readlines()[6:]

data = [row[:-2].split() for row in data]
data = [ [int(el) for el in row] for row in data]
data = np.array(data)

p.init()
s = p.display.set_mode((int(1224*PSIZE),700),p.DOUBLEBUF,32)
s.fill(white)
p.display.flip()


def drawsingle(base,x,h1,h2):
    if not (h1 and h2):
        return
    p1 = (x,base-h1)
    p2 = (x+PSIZE,base-h2)
    p3 = (x+PSIZE,base)
    p4 = (x,base)
    p.draw.polygon(s,white,(p1,p2,p3,p4))
    p.draw.line(s,black,p1,p2,LINEWIDTH)

def drawrow(row,base,x=0):
    counter = 0
    for i in range(len(row)):
        h1 = row[i]
        h2 = row[i+1] if i+1<len(row) else 0
        counter +=1
        drawsingle(base,x+i*PSIZE,h1*MUL if h1!=-9999 else False,h2*MUL if h2!=-9999 else False)
        if counter == 100:
            counter = 0
            sleep(0.0001)
            p.display.flip()
    p.display.flip()


done = False
drawn = False
start_drawing = False
while not done:
    for event in p.event.get():
        if event.type == p.QUIT:
            done = True
    if p.mouse.get_pressed()[0]:
        start_drawing = True
    if drawn or not start_drawing: continue
    for y,row in enumerate(data[::SPACING]):
        drawrow(row,(y*SPACING)+TOPMARGIN)
        sleep(0.03)
    drawn = True

    # p.display.flip