import pygame as pg,sys,math,random,os
from pygame.locals import *


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

colorSUBTITLES = (255, 255, 255)
#Background pygame color
background_color = (0,0,0)

font = pg.font.SysFont("cambria",30)


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

    screen.fill(background_color)
    
    screen.blit(font.render(f"", True, (255,255,255)), (40,40))
    print()
    pg.display.update()
    clock.tick(120)