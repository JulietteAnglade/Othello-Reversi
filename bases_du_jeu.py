
couleurs = {0 : "blancs", 1 : "noirs"} #on note les couleurs avec des muméros
taille=8
tour_daffiler_jeu=0 

def initialisation():
    #Au début, le plateau est vide sauf les 4 cases du milieu 
    plateau = [[-1 for _ in range(taille)] for _ in range(taille)]
    plateau[3][3], plateau[4][4]= 1, 1
    plateau[4][3], plateau[3][4] = 0, 0
    return plateau



def mettre_pion (x, y, couleur, plateau):
    #On repère les cases avec des coordonnées cartésiennes (origine en bas à gauche)
    #Cette fonction met un pion de la couleur demandée sur le plateau
    plateau[x][y]= couleur

def changer_de_couleur(x, y, plateau):
    #Cette fonction retourne un pion, i.e en change la couleur
    plateau[x][y] = (plateau[x][y]+1)%2

def go_to(x,y, direction):
    """ Pour une case donnée, de coordonnées (x,y), cette fonction renvoie les coordonnées d'une case contiguë
    en fonction d'une direction donnée (Nord, Sud, Est, Ouest, Nord-Est, etc...). """
    if direction==0: # direction Nord
        if y >=taille -1 : 
            return (-1, -1)
        else:
            return (x, y+1)
    if direction==1: #direction Nord Ouest
        if y>=taille-1 or x <=0:
            return (-1, -1)
        else:
            return (x-1, y+1)
    if direction==2: #direction Ouest
        if x<=0:
            return (-1, -1)
        else:
            return (x-1, y)
    if direction==3: #direction Sud Ouest
        if x<=0 or y<=0:
            return (-1, -1)
        else:
            return (x-1,y-1)
    if direction==4: #direction Sud 
        if y<=0:
            return (-1, -1)
        else:
            return (x,y-1)
    if direction==5: #direction Sud Est 
        if x>=taille-1 or y<=0:
            return (-1, -1)
        else:
            return (x+1,y-1)
    if direction==6: #direction Est 
        if x>=taille-1:
            return (-1, -1)
        else:
            return (x+1,y)
    if direction==7: #direction Nord Est 
        if x>=taille-1 or y>=taille-1:
            return (-1, -1)
        else:
            return (x+1,y+1)


def recherche(x, y, couleur, direction, plateau):
    """ Pour une case donnée, on regarde dans une direction donnée si placer un pion sur cette case permet d'encadrer des
    pions de l'autre couleur. Si c'est le cas la fonction renvoie les coordonnee de l'autre pion de la même couleur 
    qui permet d'encadrer le(s) pion(s). Sinon la fonction renvoie le couple (-1,-1) """
    xprim, yprim = go_to(x,y, direction)
    if plateau[xprim][yprim]==couleur:
        return (-1,-1)
    xencadre, yencadre = -1, -1
    while (xprim, yprim) != (-1, -1) and plateau[xprim][yprim]!=-1 and (xencadre,yencadre) ==(-1, -1): 
        x, y = xprim, yprim
        if plateau[xprim][yprim]==couleur:
            xencadre, yencadre= xprim, yprim
        xprim, yprim = go_to(x, y, direction)
    return xencadre, yencadre


def est_disponible(x, y, couleur, plateau):
    """ On regarde si placer un pion de la couleur "couleur" permet d'encadrer des pions de l'autre couleur (pour ça, 
    on fait appelle à la question recheche). On stocke dans un dictionnaire (cases_gagnees) les coordonnees des cases 
    des pions encadres (i.e ce que renvoie la fonction recherche) avec la direction comme clé.  """
    cases_gagnees={}
    if plateau[x][y] !=-1:
        return cases_gagnees
    for i in range(8):
        (a,b)=recherche(x,y, couleur, i, plateau)
        if (a,b) != (-1, -1):
            cases_gagnees[i]=(a,b)
    return cases_gagnees

def test_si_jeu_possible(plateau, couleur):
    global tour_daffiler_jeu
    cases_dispo=0
    for i in range(taille):
        for j in range(taille):
            cases_gagnees=est_disponible(i, j, couleur, plateau)
            if len(cases_gagnees) != 0:
                cases_dispo+=1
    if cases_dispo==0:
        tour_daffiler_jeu +=1
    return cases_dispo != 0

def tour(x, y, couleur, plateau, scores):
    scores[couleur]+=1
    cases_gagnees=est_disponible(x, y, couleur, plateau)
    mettre_pion(x, y, couleur, plateau)
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
            scores[couleur]+=1
            scores[(couleur+1)%2]-=1
            x1, y1 = xwin, ywin


def gagnant(scores):
    if scores[0]>scores[1]:
        return 0
    else:
        return 1




