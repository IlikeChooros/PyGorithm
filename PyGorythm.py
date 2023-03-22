import pygame as pg,sys,math,random,os
from pygame.locals import *
#from src import Tester

klik = pg.key.get_pressed

pg.init()

OKNO = [750,800]
screen = pg.display.set_mode(OKNO)
pg.display.set_caption("PyGorythm")

#Pygame Clock
clock = pg.time.Clock()
#Mouse
M_LEWY = False
M_PRAWY = False
NP = True #Nacisniecie/Puszczenie-mozna nacisknac
offset = [0,0]#Mouse wheel ratation
#Other Inputs
P_ESCAPE = False
NP_ESCAPE = True#False - music puscic aby jeszcze raz nacisnac

#Color Subtitles
colorSUBTITLES = (255, 255, 255)
#Background pygame color
background_color = (0,0,0)
#Colors
colors_of_points = {0:(255,175,68),1:(0,230,200)}
color_graph = (255, 255, 204)
color_ai = (0,0,0)

#Fonts
font = pg.font.SysFont("cambria",30)

#---------
graph_surface = pg.Rect(0,0,OKNO[0],OKNO[1]/2)
points_radius = 10

points_data = []
points_data = [[200,200,1],[150,250,1],[300,250,1],[400,140,0],[250,300,0]]

ai_surface = pg.Rect(0,OKNO[1]/2,OKNO[0],OKNO[1]/2)
neurons_radius = 30


inputs = [12,12]
neurons = [[12,12,3],[4,1,1.4,3.1]]
outputs = [0,1]


#Defs
def ViewGraph(surface_rect,color_of_surface,list_of_points,radius_of_points,colors_of_points):
    pg.draw.rect(screen,color_of_surface,surface_rect)
    for i in range(len(list_of_points)):
        #Protection against leaving the surface
        if surface_rect.x < list_of_points[i][0] < surface_rect.x + surface_rect.width and surface_rect.y < list_of_points[i][1] < surface_rect.y + surface_rect.height:
            #Bliting the points
            pg.draw.circle(screen,colors_of_points[list_of_points[i][2]],
                (int(list_of_points[i][0]),int(list_of_points[i][1])),points_radius)
def ViewAINeurons(surface_rect,color_of_surface,list_of_inputs,list_of_neurons,lsit_of_outputs,radius_of_neuron):
    pg.draw.rect(screen,color_of_surface,surface_rect)
    for i in range(1+len(list_of_neurons)+1):#inputs line + neurons lines + outputs line
        if i == 0:
            for j in range(len(list_of_inputs)):
                pg.draw.circle(screen,(255,255,255),((surface_rect.width/(1+len(list_of_neurons)+1))*i+surface_rect.width/(1+len(list_of_neurons)+1),(surface_rect.height/len(list_of_inputs))*j+surface_rect.height/len(list_of_inputs)),radius_of_neuron)
        elif i > len(list_of_neurons):
            for j in range(len(lsit_of_outputs)):
                pg.draw.circle(screen,(255,255,255),((surface_rect.width/(1+len(list_of_neurons)+1))*i+surface_rect.width/(1+len(list_of_neurons)+1),(surface_rect.height/len(list_of_inputs))*j+surface_rect.height/len(lsit_of_outputs)),radius_of_neuron)
        else:
            for j in range(len(list_of_neurons)):
                pg.draw.circle(screen,(255,255,255),((surface_rect.width/(1+len(list_of_neurons)+1))*i+surface_rect.width/(1+len(list_of_neurons)+1),(surface_rect.height/len(list_of_inputs))*j+surface_rect.height/len(list_of_neurons[i-1])),radius_of_neuron)


while True:
    Mx, My = pg.mouse.get_pos()
    for event in pg.event.get():
        if event.type == pg.QUIT or klik()[pg.K_F4]:
            pg.quit()
            sys.exit(0)
        if event.type == pg.VIDEORESIZE:
            screen = pg.display.set_mode((event.w, event.h))
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                M_LEWY = True
            if event.button == 3:
                M_PRAWY = True
            if event.button == 4:
                offset[1] += -20#Szbkosc obrotu kolka na myszce 10-standard
            if event.button == 5:
                offset[1] += 20#Szbkosc obrotu kolka na myszce 10-standard
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                M_LEWY = False
            if event.button == 3:
                M_PRAWY = False
        if event.type == pg.KEYDOWN:
            if event.key == K_ESCAPE:
                P_ESCAPE = True
        if event.type == pg.KEYUP:
            if event.key == K_ESCAPE:
                P_ESCAPE = False
    #--------BACKGROUND---------#
    screen.fill(background_color)
    #---------GRAPHICS----------#
    ViewGraph(graph_surface,color_graph,points_data,points_radius,colors_of_points)
    ViewAINeurons(ai_surface,color_ai,inputs,neurons,outputs,neurons_radius)
    #-----------CODE------------#
    #---------------------------#
    screen.blit(font.render(f"{colors_of_points[0]}", True, (0,0,0)), (40,40))
    pg.display.update()
    clock.tick(120)