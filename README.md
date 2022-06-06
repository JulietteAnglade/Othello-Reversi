# Othello-Reversi
Le super projet d'info

from tkinter import *

#Fonctions de creations de pion

def creer_pion(event):
    
    # position du pointeur de la souris
    X = event.x
    Y = event.y
    # position de la souris dans la grille
    x0 = X - X%60 + 5
    y0 = Y - Y%60 + 5
    
    # test si la souris est "dans la grille"*
    if 59 < x0 < 500 and 59 < y0 < 500:
        #creation du pion
        pion = canvas.create_oval(x0,y0,x0 + 50,y0 + 50, fill = 'yellow')



#Interface graphique

fenetre = Tk() #Creation de 'la base' de l'interface
canvas = Canvas(fenetre, width=600, height=600, background='#090909') #creation du canvas (le support visuel)

#creation de la grille
    #grille 8x8, taille d'une case : 60x60

for ligne in range(10):
    canvas.create_line(60, ligne * 60, 540, ligne * 60, fill = '#DDDDDD')
for colonne in range(10):
    canvas.create_line(colonne * 60, 60, colonne * 60, 540, fill = '#DDDDDD')


canvas.pack() #permet de faire apparaître le canvas

#test de 'souris'

fenetre.bind("<Button-1>", creer_pion)

fenetre.mainloop() #fait apparaître le résultat


