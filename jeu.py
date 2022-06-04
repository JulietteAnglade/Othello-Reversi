plateau = [[-1 for _ in range(8)] for _ in range(8)]

pion = {0 : "blancs", 1 : "noirs"}
def initialisation():
    plateau = [[-1 for _ in range(8)] for _ in range(8)]
    plateau[3][3], plateau[4][4]= 1, 1
    plateau[4][3], plateau[3][4] = 0, 0
    return plateau 


def mettre_pion (x, y, couleur):
    plateau[x][y]= couleur

def changer_de_couleur(x, y):
    plateau[x][y] = (plateau[x][y]+1)%2

def Nord(x, y, couleur):
    return 42
    # pour un pion placé, cherche s'il y a une case de l'autre couleur au nord
    # si c'est le cas, regarde la case au dessus : 
        # si elle est de l'autre couleur : recommence
        # si elle est vide : renvoie le couple (-1, -1) (ou autre chose qui indique que ça marche pas)
        # si elle est de la couleur : renvoie le couple de coordonnées de la case

def Sud(x, y, couleur):
    return 42
    #même principe que sandwich nord

def Est(x, y, couleur): 
    return 42 

def Ouest(x, y, couleur): 
    return 42

def NO(x, y, couleur): 
    return 42
def NE(x, y, couleur): 
    return 42

def SE(x, y, couleur): 
    return 42

def SO(x, y, couleur): 
    return 42

def est_disponible(x, y, couleur):
    a=Sud(x, y, couleur) + Nord(x, y, couleur)+ Est(x, y, couleur) + Ouest(x, y, couleur)
    + NE(x, y, couleur)+NO(x, y, couleur)+SE(x, y, couleur)+SO(x, y, couleur) 
    if a==(-8, -8):
        return False
    else: 
        return True

def partie(): 
    plateau = initialisation()
    for i in range(60):
        couleur = i%2 
        print("C'est aux {} de jouer". format(pion[couleur]))
        x, y = input("Où voulez-vous placer votre pion ? (donner les coordonnées (x, y)")
        if not est_disponible(x, y, couleur):
            print("Vous ne pouvez pas jouer ici")
        else: 



# comment joue l'ordinateur : parcourir toutes les cases disponibles et jouer celle qui retourne le plus de pions 

