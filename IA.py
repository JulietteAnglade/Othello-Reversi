from bases_du_jeu import *
from random import randint

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
#       celle où le nombre de pions gagnés est maximal, et joue dans un coin du plateau lorsque c'est possible
    xopti, yopti = -1, -1
    pions_gagnes_max=0
    for x in range(taille):
        for y in range(taille):
            cases_gagnees = est_disponible(x, y, couleur, plateau)
            pions_gagnes = compte_pions_gagnes(x, y, cases_gagnees)
            if pions_gagnes > pions_gagnes_max:
                pions_gagnes_max=pions_gagnes
                xopti, yopti = x, y
            if pions_gagnes !=0 and ((x, y) == (0,0) or (x, y) == (7,0) or (x, y) == (0,7) or (x, y) == (7,7)):
                return x, y
    return xopti, yopti


def IA_random(plateau, couleur):
    coups_possibles=[]
    for x in range(taille):
        for y in range(taille):
            cases_gagnees=est_disponible(x,y,couleur,plateau)
            if len(cases_gagnees)>0:
                coups_possibles.append((x,y))
    i=randint(1, (len(coups_possibles)))
    return coups_possibles[i-1]

def IA_coup_max(plateau, couleur):
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

def IA_coupmax_random(plateau, couleur):
    coups_opti_possibles=[]
    pions_gagnes_max=0
    for x in range(taille):
        for y in range(taille):
            cases_gagnees = est_disponible(x, y, couleur, plateau)
            pions_gagnes = compte_pions_gagnes(x, y, cases_gagnees)
            if pions_gagnes > pions_gagnes_max:
                pions_gagnes_max=pions_gagnes
    for x in range(taille):
        for y in range(taille):
            cases_gagnees = est_disponible(x, y, couleur, plateau)
            pions_gagnes = compte_pions_gagnes(x, y, cases_gagnees)
            if pions_gagnes == pions_gagnes_max:
                coups_opti_possibles.append((x,y))
    i = randint(1, len(coups_opti_possibles))
    return coups_opti_possibles[i-1]

def IA_coupmax_coins_random(plateau, couleur): 
    coups_opti_possibles=[]
    pions_gagnes_max=0
    for x in range(taille):
        for y in range(taille):
            cases_gagnees = est_disponible(x, y, couleur, plateau)
            pions_gagnes = compte_pions_gagnes(x, y, cases_gagnees)
            if pions_gagnes >pions_gagnes_max:
                pions_gagnes_max=pions_gagnes
            if pions_gagnes !=0 and ((x, y) == (0,0) or (x, y) == (7,0) or (x, y) == (0,7) or (x, y) == (7,7)):
                return x, y
    for x in range(taille):
        for y in range(taille):
            cases_gagnees = est_disponible(x, y, couleur, plateau)
            pions_gagnes = compte_pions_gagnes(x, y, cases_gagnees)
            if pions_gagnes == pions_gagnes_max:
                coups_opti_possibles.append((x,y))       
    i=randint(1, len(coups_opti_possibles))
    return coups_opti_possibles[i-1]

def ordi_joue_tout_seul(plateau, couleur):
    return coup_pseudo_optimal(plateau, couleur)

def ordiVSordi(IA1, IA2):
    plateau=initialisation()
    scores=[2,2]
    couleurIA1=1
    couleurIA2=0
    tour_daffiler_jeu=0
    while tour_daffiler_jeu !=2 and (scores[0]+scores[1]!=taille*taille):
        tour_daffiler_jeu=0
        if not test_si_jeu_possible(plateau, couleurIA1):
            tour_daffiler_jeu+=1
            if test_si_jeu_possible(plateau,couleurIA2):
                x,y = IA2(plateau, couleurIA2)
                tour(x, y, couleurIA2, plateau, scores)
            else:
                tour_daffiler_jeu+=1
        else:
            x,y=IA1(plateau, couleurIA1)
            tour(x, y, couleurIA1, plateau, scores)
            if test_si_jeu_possible(plateau, couleurIA2):
                x,y = IA2(plateau, couleurIA2)
                tour(x, y, couleurIA2, plateau, scores)
    return gagnant(scores)




random_gagne=100
for i in range(100):
    random_gagne-=ordiVSordi(IA_coupmax_coins_random, IA_coupmax_coins_random)
print(random_gagne)