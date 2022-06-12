from bases_du_jeu import *
from cgi import test
from mimetypes import init
from tkinter import *
from tkinter import messagebox
import tkinter.font
from IA import ordi_joue_tout_seul


couleurs_interface={0: "#AAAAAA", 1:"#090909"}
plateau = initialisation()
scores=[2,2]

def coord_jeu_vers_interface(xj, yj):
    return ((xj+1)*60, (8-yj)*60)

def coord_interface_vers_jeu(xi, yi):
    return (xi//60 -1), (-yi//60+8)

def creer_pion(xj, yj, couleur):
    #prend en argument les coordonnées du jeu et une couleur (0 ou 1) et met un pion sur
    # la case en question
    xi, yi = coord_jeu_vers_interface(xj, yj)
    x0, y0 = xi + 5, yi +5
    # test si la souris est "dans la grille"*
    if 59 < x0 < 500 and 59 < y0 < 500:
        #creation du pion
       pion = canvas.create_oval(x0,y0,x0 + 50,y0 + 50, fill = couleurs_interface[couleur])

def retourner_pion(xj, yj, couleur):
    creer_pion(xj, yj, couleur)


def waithere():
    var = IntVar()
    fenetre.after(500, var.set, 1)
    fenetre.wait_variable(var)

def un_joueur_joue(plateau, couleur, x0, y0):
#   Pour un clic du joueur sur une case, renvoie les coordonnées de la case si le joueur peut jouer sur cette 
#   case et renvoie le couple -1, -1 si ce n'est pas le cas
    x, y = coord_interface_vers_jeu(x0, y0)
    cases_gagnees=est_disponible(x, y, couleur, plateau)
    if len(cases_gagnees)==0:
        return -1, -1
    return x,y

def tour_avec_interface(x, y, couleur, plateau, scores):
    scores[couleur]+=1
    cases_gagnees=est_disponible(x, y, couleur, plateau)
    mettre_pion(x, y, couleur, plateau)
    creer_pion(x,y,couleur)
    for direction in cases_gagnees:
        (a,b)=cases_gagnees[direction]
        if direction==2 or direction==6:
            n=abs(x-a)
        else:
            n=abs(y-b)
        x1, y1 = x, y
        for _ in range(n-1):
            xwin, ywin = go_to(x1, y1, direction)
            changer_de_couleur(xwin, ywin, plateau)
            retourner_pion(xwin,ywin,couleur)
            scores[couleur]+=1
            scores[(couleur+1)%2]-=1
            x1, y1 = xwin, ywin


def tourglobal(event):
    X = event.x
    Y = event.y
    x0 = X - X%60
    y0 = Y - Y%60
    couleurjoueur=1
    couleurordi=0
    tour_daffiler_jeu=0
    x,y=un_joueur_joue(plateau, couleurjoueur, x0, y0)
    if scores[0]+scores[1]== taille*taille:
        messagebox.showerror("Fin", "Victoire des {}".format(couleurs[gagnant(scores)]))
    if not test_si_jeu_possible(plateau, couleurjoueur):
        messagebox.showerror("Info", "Vous ne pouvez pas jouer, au tours des {}".format(couleurs[couleurordi]))
        if test_si_jeu_possible(plateau,couleurordi):
            x,y = ordi_joue_tout_seul(plateau, couleurordi)
            tour_avec_interface(x, y, couleurordi, plateau, scores)
    if (x,y)==(-1,-1):
        messagebox.showerror("Erreur", "Vous ne pouvez pas jouer ici")
    elif test_si_jeu_possible(plateau, couleurjoueur):
        tour_avec_interface(x, y, couleurjoueur, plateau, scores)
        waithere()
        if test_si_jeu_possible(plateau, couleurordi):
            x,y = ordi_joue_tout_seul(plateau, couleurordi)
            tour_avec_interface(x, y, couleurordi, plateau, scores)
        else: 
            messagebox.showerror("Info", "L'ordinateur ne peut pas jouer, à vous de jouer")
    if tour_daffiler_jeu ==2:
        messagebox.showerror("Fin", "Plus personne ne peut jouer. \n La partie est terminée \n Victoire des {}".format(couleurs[gagnant(scores)]))
    canvas.itemconfig(score, text="Score - Noirs : {} / Blancs : {}".format(scores[1], scores[0]))


fenetre = Tk() #Creation de 'la base' de l'interface
canvas = Canvas(fenetre, width=600, height=650, background='#0092F8') #creation du canvas (le support visuel)
fenetre.title("Othello - Prêts à rivaliser avec notre IA imbattable ?")
#creation de la grille
    #grille 8x8, taille d'une case : 60x60

for ligne in range(10):
    canvas.create_line(60, ligne * 60, 540, ligne * 60, fill = '#090909')
for colonne in range(10):
    canvas.create_line(colonne * 60, 60, colonne * 60, 540, fill = '#090909')

creer_pion(3,3,1)
creer_pion(4,4,1)
creer_pion(3,4,0)
creer_pion(4,3,0)



police = tkinter.font.Font(size = 20)


canvas.pack() #permet de faire apparaître le canvas

messagebox.askyesno("Démarrer une partie", "Prêts à rivaliser avec une IA quasi-imbattable ?")


score = canvas.create_text ( 300 , 600 , text = "Score - Noirs : {} / Blancs: {} ".format(scores[1], scores[0]), fill = couleurs_interface[1], font = police)

fenetre.bind("<Button-1>", tourglobal)

fenetre.mainloop() #fait apparaître le résultat



