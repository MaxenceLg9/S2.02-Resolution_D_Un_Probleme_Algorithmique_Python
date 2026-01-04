# -*- coding: utf-8 -*-
"""
Created on Mon May 13 08:15:55 2024

@author: senne
"""

import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import math
import timeit


def creer_matrice(s, p):
    M = []
    for i in range(s):
        M.append([])
        for j in range(s):
            M[i].append(0)

    prop = 0
    while prop / (s ** 2) <= p:
        index = random.randint(0, s - 1)
        indice = random.randint(0, s - 1)
        if M[index][indice] != 1:
            M[index][indice] = random.randint(0, 99999)
            prop += 1

    return np.array(M)


def creer_graphe(M):
    G = nx.from_numpy_array(M, create_using=nx.DiGraph)

    # Ajouter les attributs 'poids' aux arêtes
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i][j] != 0:
                G.add_edge(i, j, poids=M[i][j])

    return G


def dessiner_chemin_avec_poids(G, pos, chemin):
    if chemin is not None:
        for i in range(len(chemin) - 1):
            nx.draw_networkx_edges(G, pos=pos, edgelist=[(chemin[i], chemin[i + 1])], edge_color='r', width=2,arrows=True)

        edge_labels = {(i, j): d['poids'] for i, j, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    else:
        print("Chemin impossible")


def Dijkstra(M, d):
    # Liste des sommets
    listeSommet = []
    for s in range(len(M)):
        listeSommet.append(s)

    # Dictionnaire distance, prédécésseur de chaque sommet
    dico_dijkstra = {}
    # Liste de sommets
    A = [d]
    # Création de la liste des sommets hors de A
    sommetHorsDeA = listeSommet.copy()
    # Suppresion du premier element de A
    sommetHorsDeA.remove(d)

    # Remplissage du dictionnaire
    for s in listeSommet:
        if s == d:
            dico_dijkstra[s] = (0, None)
        elif s in successeur(M, d):
            dico_dijkstra[s] = (M[d][s], d)
        else:
            dico_dijkstra[s] = (math.inf, None)

    # Effectuer le code pour tous les sommets
    while len(sommetHorsDeA) != 0:

        # Obtention du sommet ayant la distance minimale
        dist_mini = math.inf
        for elt in sommetHorsDeA:
            if dist_mini >= dico_dijkstra[elt][0]:
                dist_mini = dico_dijkstra[elt][0]
                sommet_dist_mini = elt

        # Ajout du sommet ayant la plus distance dans A
        A.append(sommet_dist_mini)
        sommetHorsDeA.remove(sommet_dist_mini)

        for t in successeur(M, sommet_dist_mini):
            if t not in A:
                if dico_dijkstra[sommet_dist_mini][0] + M[sommet_dist_mini][t] < dico_dijkstra[t][0]:
                    dico_dijkstra[t] = (dico_dijkstra[sommet_dist_mini][0] + M[sommet_dist_mini][t], sommet_dist_mini)

    dico_final = {}
    for s in listeSommet:
        if s == d:
            dico_final[s] = ([dico_dijkstra[s][0]], None)
        else:
            if dico_dijkstra[s][0] == math.inf:
                dico_final[s] = ("Noeud inaccessible", None)
            else:
                chemin = [s]
                prede = dico_dijkstra[s][1]
                while prede != d:
                    chemin.append(prede)
                    prede = dico_dijkstra[prede][1]
                chemin.append(d)
                chemin.reverse()
                dico_final[s] = (dico_dijkstra[s][0], chemin)
    return dico_final


def successeur(M, s):
    successeurs = []
    for i in range(len(M[s])):
        if M[s][i] != 0:
            successeurs.append(i)
    return successeurs


def TempsDij(n):
    p = 1 / n
    M = np.random.binomial(n * 50, p, (n, n))

    start = timeit.default_timer()
    chemin = Dijkstra(M, 1)
    stop = timeit.default_timer()

    return (stop - start) * 1000


def parcoursLargeur(mat, s):
    n = len(mat)
    file = [s]
    visites = []
    while file:
        sommet = file.pop(0)
        for i in range(n):
            if mat[sommet][i] != float('inf') and (sommet, i) not in visites:
                visites.append((sommet, i))
                file.append(i)
    return visites


def pp(M, s):
    n = len(M)  # taille du tableau = nombre de sommets
    couleur = {}  # On colorie tous les sommets en blanc et s en vert
    for i in range(n):
        couleur[i] = 'blanc'
    couleur[s] = 'vert'
    pile = [s]  # on initialise la pile à s
    Resultat = [s]  # on initialise la liste des résultats à s

    while pile != []:  # tant que la pile n'est pas vide,
        i = pile[-1]  # on prend le dernier sommet i de la pile
        Succ_blanc = []  # on crée la liste de ses successeurs non déjà visités (blancs)
        for j in range(n):
            if (M[i, j] == 1 and couleur[j] == 'blanc'):
                Succ_blanc.append(j)
        if Succ_blanc != []:  # s'il y en a,
            v = Succ_blanc[0]  # on prend le premier (si on veut l'ordre alphabétique)
            couleur[v] = 'vert'  # on le colorie en vert,
            pile.append(v)  # on l'empile
            Resultat.append(v)  # on le met en liste rsultat
        else:  # sinon:
            pile.pop()  # on sort i de la pile

    return (Resultat)


def BellmanFordParcours(M, s):
    n = len(M)
    d = {i: [float('inf'), []] for i in range(n)}
    parcours = parcoursLargeur(M, s)
    d[s][0] = 0
    for r in range(n - 1):
        for f in parcours:
            i = f[0]
            j = f[1]
            if d[j][0] > d[i][0] + M[i][j]:
                d[j][0] = d[i][0] + M[i][j]
                d[j][1].append(i)
    for i in range(n):
        d[i][1].append(i)
    # detection de cycle negatif
    d = listeSommetEnFlèche(d)
    for r in range(n - 1):
        for f in parcours:
            i = f[0]
            j = f[1]
            if d[j][0] == float('inf'):
                d[j] = "sommet non joignable depuis d par un chemin dans le graphe G"
            elif d[i][0] == float('inf'):
                d[i] = "sommet non joignable depuis d par un chemin dans le graphe G"
            elif M[i][j] != float('inf') and not isinstance(d[i], str) and not isinstance(d[j], str):
                # print(f"{j} : {d[j][0]} / {d[i][0] + M[i][j]}")
                if d[j][0] > d[i][0] + M[i][j] or d[j][0] < 0:
                    d[
                        j] = "sommet joignable depuis d par un chemin dans le graphe G, mais pas de plus court chemin (presence d’un cycle negatif)"
    return d


def listeSommetEnFlèche(M):
    n = len(M)
    for i in range(n):
        line = []
        for x in range(len(M[i][1])):
            line.append((M[i][1][x - 1], M[i][1][x]))
        M[i][1] = line
    return M


def TempsBF(n):
    p = 1 / n
    M = np.random.binomial(n * 50, p, (n, n))

    start = timeit.default_timer()
    chemin = BellmanFordParcours(M, 1)
    stop = timeit.default_timer()
    return (stop - start) * 1000


n_valeurs = range(2, 201)
# temps_dij = [TempsDij(n) for n in n_valeurs]
temps_BF = [TempsBF(n) for n in n_valeurs]
plt.figure(figsize=(10, 5))
# plt.loglog(n_valeurs, temps_dij, label='Dijkstra')
plt.loglog(n_valeurs, temps_BF, label='Bellman Ford')
plt.xlabel('Nombre de sommets n')
plt.ylabel('Temps d\'exécution (ms)')
plt.title('Comparaison du temps d\'exécution des algorithmes de plus courts chemins')
plt.legend()
plt.grid(True)
plt.show()