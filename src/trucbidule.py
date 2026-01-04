import numpy as np
import numpy.random as rand
import networkx as nx
import matplotlib.pyplot as plt
import timeit

from numpy import array


############ GENERATION D'UNE MATRICE AVEC UNE PROPORTION P DE FLECHES ##############

def matricePNumpy(n, p, a, b):
    return rand.binomial(1, p, (n, n))


############ GENERATION D'UNE MATRICE AVEC UNE PROPORTION 1/2 DE FLECHES ##############

def matriceNumpy(n, a, b):
    return rand.randint(0, 2, size=(n, n))


############ CREER UN GRAPHE A PARTIR D'UNE MATRICE M ##############

def creer_graphe(M):
    G = nx.from_numpy_array(M, create_using=nx.DiGraph)

    for i in range(len(M)):
        for j in range(len(M)):
            if M[i][j] != 0:
                G.add_edge(i, j, poids=M[i][j])

    return G


############ DESSINE LES POIDS SUR LE GRAPHE G ##############

def dessiner_poids(G, pos, M):
    edge_labels = {}
    for i, j, d in G.edges(data=True):
        if d['poids'] != float('inf'):
            edge_labels[(i, j)] = M[i][j]

    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)


############ TRACE LE CHEMIN SUR LE GRAPHE G ##############

def tracer_chemin(G, pos, chemin):
    if chemin is not None:
        for i in range(len(chemin) - 1):
            nx.draw_networkx_edges(G, pos=pos, edgelist=[(chemin[i], chemin[i + 1])], edge_color='r', width=2,arrows=True)
    else:
        print("Chemin impossible")


############ PONDERE UNE MATRICE M ALLANT DE a A b ##############

def ponderer(M, a, b):
    M_ponderer = np.copy(M)
    M_ponderer = M_ponderer.astype('float64')
    taille = np.shape(M)[0]
    for ligne in range(taille):
        for elt in range(taille):
            if M_ponderer[ligne][elt] == 1:
                M_ponderer[ligne][elt] = rand.randint(a, b)
            else:
                M_ponderer[ligne][elt] = float('inf')
    return M_ponderer


############ TRANSFORMATION GRAPHE PONDERE EN NON PONDERE ##############

def graphPEnNonP(mat):
    n = len(mat)
    M = []
    for i in range(n):
        ligne = []
        for j in range(n):
            if mat[i][j] != float('inf'):
                ligne.append(1)
            else:
                ligne.append(0)
        M.append(ligne)
    return M


############ PARCOURS LARGEUR ET PROFONDEUR ##############

def parcoursLargeur(M, s):
    n = len(M)
    file = [s]
    couleur = [0] * n
    sommets = []
    couleur[s] = 1
    while file != []:
        i = file.pop(0)  # on prend le premier terme de la file
        for j in range(n):
            if M[i][j] == 1 and couleur[j] == 0:
                couleur[j] = 1
                sommets.append(i)
                file.append(j)
    return sommets


def parcoursProfondeur(mat, s):
    n = len(mat)  # taille du tableau = nombre de sommets
    couleur = {}  # On colorie tous les sommets en blanc et s en vert
    for i in range(n):
        couleur[i] = 0
    couleur[s] = 1
    pile = [s]  # on initialise la pile à s
    Resultat = [s]  # on initialise la liste des résultats à s
    while pile != []:  # tant que la pile n'est pas vide,
        i = pile[-1]  # on prend le dernier sommet i de la pile
        Succ_blanc = []  # on crée la liste de ses successeurs non déjà visités (blancs)
        for j in range(n):
            if (mat[i][j] == 1 and couleur[j] == 0):
                Succ_blanc.append(j)
        if Succ_blanc != []:  # s'il y en a,
            v = Succ_blanc[0]  # on prend le premier (si on veut l'ordre alphabétique)
            couleur[v] = 1  # on le colorie en vert,
            pile.append(v)  # on l'empile
            Resultat.append(v)  # on le met en liste rsultat
        else:  # sinon:
            pile.pop()  # on sort i de la pile

    return (Resultat)


############ GENERATION DES FLECHES ##############

def listeFlechesAleatoires(mat):
    n = len(mat)
    fleches = []
    for i in range(n):
        for j in range(n):
            if mat[i][j] == 1:
                fleches.append((i, j))
    return fleches


############ ALGORITHME BELMAN FORD ##############

def BellmanFord(M, s):
    # Initialisation
    n = len(M)
    d = {i: [float('inf'), []] for i in range(n)}
    d[s][0] = 0
    mat = graphPEnNonP(M)
    fleches = listeFlechesAleatoires(mat)
    modif = True
    taille = 0
    while taille < len(M) - 1 and modif:
        modif = False
        for i, j in fleches:
            if M[i][j] != float('inf') and d[j][0] > d[i][0] + M[i][j]:
                modif = True
                print(f"Dist(j) : {d[j][0]} : Dist(i) + M(i,j): {d[i][0] + M[i][j]}")
                d[j][0] = d[i][0] + M[i][j]
                d[j][1] = d[i][1] + [i]
        taille += 1

    for i, j in fleches:
        if d[i][0] == float('inf'):
            d[i] = ("Noeud inaccessible", None)
    d[s] = [0, [None]]
    print(d)
    return d


############ ALGORITHME DIJKSTRA ##############

def Dijkstra(M, d):
    # Liste des sommets
    listeSommet = []
    for s in range(len(M)):
        listeSommet.append(s)

    # Distance de s0 vers s0
    dist = 0
    # prédécésseur de s0
    pred = 0
    # Dictionnaire distance, prédécésseur de chaque sommet
    dico_dijkstra = {0: (dist, pred)}
    # Liste de sommets
    A = [0]
    # Création de la liste des sommets hors de A
    sommetHorsDeA = listeSommet.copy()
    # Suppresion du premier element de A
    sommetHorsDeA.remove(d)

    # Remplissage du dictionnaire
    for s in listeSommet:
        if s in successeur(M, d):
            dico_dijkstra[s] = (M[d][s], d)
        else:
            dico_dijkstra[s] = (float('inf'), None)
            # Effectuer le code pour tous les sommets
    while sommetHorsDeA:
        # Sélectionner le sommet avec la distance minimale
        dist_mini = float('inf')
        sommet_dist_mini = None
        for elt in sommetHorsDeA:
            if dico_dijkstra[elt][0] < dist_mini:
                dist_mini = dico_dijkstra[elt][0]
                sommet_dist_mini = elt

        if sommet_dist_mini is None:
            break

        # Ajouter le sommet avec la distance minimale à A
        A.append(sommet_dist_mini)
        sommetHorsDeA.remove(sommet_dist_mini)

        for t in successeur(M, sommet_dist_mini):
            if t not in A:
                if dico_dijkstra[sommet_dist_mini][0] + M[sommet_dist_mini][t] < dico_dijkstra[t][0]:
                    dico_dijkstra[t] = (dico_dijkstra[sommet_dist_mini][0] + M[sommet_dist_mini][t], sommet_dist_mini)

    dico_final = {}
    for s in listeSommet:
        if s == 0:
            dico_final[s] = ([dico_dijkstra[s][0]], [])
        else:
            chemin = [s]
            prede = dico_dijkstra[s][1]
            while prede != 0:
                chemin.append(prede)
                prede = dico_dijkstra[prede][1]
            chemin.append(0)

            chemin.reverse()
            dico_final[s] = (dico_dijkstra[s][0], chemin)

    return dico_final


def successeur(M, s):
    successeurs = []
    for i in range(len(M[s])):
        if M[s][i] != 0:
            successeurs.append(i)
    return successeurs


############ EXECUTION DU CODE ##############

Taille_mat = 5
Borne_inf = -1  # Exclu
Borne_supp = 10  # Exclu
Sommet_depart = 0  # doit etre compris entre 0 et Taille_mat - 1
Sommet_fin = 4  # doit etre compris entre Sommet_depart + 1 et Taille_mat - 1

Matrice_demi = matriceNumpy(Taille_mat, 0, 2)  # Génération d'une matrice avec une proportion de 1/2 de flèches
# print(Matrice_demi) # Afficher dans la console la matrice binaire

M_ponderer = ponderer(Matrice_demi, Borne_inf, Borne_supp)
# print(M_ponderer) # Afficher dans la console la matrice pondérée

# Création du graphe à partir de la matrice binaire
G = creer_graphe(Matrice_demi)

# Positionnement des nœuds
pos = nx.spring_layout(G)

# Dessin du graphe
nx.draw(G, pos, with_labels=True)

############ TRACAGE DU CHEMIN AVEC DJIKSTRA ##############

# Calcul du plus court chemin avec l'algorithm  e de Dijkstra et Bellman Ford
#chemin = Dijkstra(M_ponderer, Sommet_depart)



print(BellmanFord())