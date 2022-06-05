taille=8
 ################################# Bases du jeu ###################################################
couleurs = {0 : "blancs", 1 : "noirs"} #on note les couleurs avec des muméros

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

########################### Ordinateur qui joue ##############################################

def compte_pions_gagnes(x,y, cases_gagnees):
    #Pour un pion joué sur la case de coordonnées (x,y) renvoie le nombre de pions gagnés
    pions_gagnes=0 
    for direction in cases_gagnees: 
        a,b=cases_gagnees[direction]
        if direction==2 or direction==6: 
            pions_gagnes+=abs(x-a)-1
        else:
            pions_gagnes+=abs(y-b)-1
    return pions_gagnes

def coup_pseudo_optimal(plateau, couleur):
#    Parcours les cases disponibles du plateau et renvoie les coordonnées de
#       celle où le nombre de pions gagnés est maximal
    xopti, yopti = -1, -1
    pions_gagnes_max=0
    for x in range(taille):
        for y in range(taille):
            cases_gagnees = est_disponible(x, y, couleur, plateau)
            pions_gagnes = compte_pions_gagnes(x, y, cases_gagnees)
            if pions_gagnes > pions_gagnes_max:
                pions_gagnes_max=pions_gagnes
                xopti, yopti = x, y
    return xopti, yopti

def ordi_joue_tout_seul(plateau, couleur):
    return coup_pseudo_optimal(plateau, couleur)


######################## Relations avec l'utilisateur #################################

def choix_couleur():
    coul=input("Voulez-vous jouer avec les pions noirs ou les pions blancs ? (noir/blanc)")
    if coul=="blanc":
        coul=0
    elif coul=="noir":
        coul=1
    else:
        print("la couleur renseignée n'est pas correcte")
        choix_couleur()
    return coul

def un_joueur_joue(plateau, couleur):
#   demande au joueur les coordonnées de la case sur laquelle il veut jouer, vérfie qu'il peut jouer sur cette case 
#   et si c'est le cas, revoie les coordonnées de la case. 
    x, y = int(input("Où voulez-vous placer votre pion ? (donner la coordonnée x) ")), int(input("donner la coordonée y"))
    cases_gagnees=est_disponible(x, y, couleur, plateau)
    while len(cases_gagnees)==0:
        print("Vous ne pouvez pas jouer ici")
        x, y = int(input("Où voulez-vous placer votre pion ? (donner la coordonnée x) ")), int(input("donner la coordonée y "))
        cases_gagnees=est_disponible(x, y, couleur, plateau)
    return x,y     


########################### Le coeur du jeu ################################### 


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
    print(plateau)
    print(scores)



def partie(): 
    plateau = initialisation()
    scores=[2,2]
    print(plateau)
    print(scores)
    couleurjoueur=choix_couleur()
    for i in range(taille*taille - 4):
        couleur = i%2
        if couleur==couleurjoueur:
            print("A vous de jouer")
            x,y=un_joueur_joue(plateau, couleur)
        else:
            print("l'ordinateur joue...")
            x,y = ordi_joue_tout_seul(plateau, couleur)
            print("l'ordinateur a joué ", x, y) 
        tour(x, y, couleur, plateau, scores)
    print("Fin de la partie")
    if scores[0] > scores[1]:
        print("Les blancs gagnent")
    else: 
        print("Les noirs gagnent") 
    print("noirs : {} pions \n blancs : {} pions".format(scores[1], scores[0]))


def partie_ordiVSordi():
    plateau = initialisation()
    scores=[2,2]
    print(plateau)
    print(scores)
    for i in range(taille*taille - 4):
        couleur = i%2
        x,y = ordi_joue_tout_seul(plateau, couleur)
        print("Aux {} de jouer".format(couleurs[couleur]))
        print("Les {} ont joué ".format(couleurs[couleur]), (x, y)) 
        tour(x, y, couleur, plateau, scores)
    print("Fin de la partie")
    if scores[0] > scores[1]:
        print("Les blancs gagnent")
    else: 
        print("Les noirs gagnent") 
    print("noirs : {} pions \n blancs : {} pions".format(scores[1], scores[0]))


partie()



