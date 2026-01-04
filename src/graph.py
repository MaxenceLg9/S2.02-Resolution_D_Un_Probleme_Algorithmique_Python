import math
import random
import timeit

import numpy.random as rand


def matriceNumpy(n, a, b):
    M = rand.randint(0, 2, size=(n, n))
    M = M.astype(float)
    for i in range(n):
        for j in range(n):
            if M[i][j] == 0:
                M[i][j] = float('inf')
            else:
                M[i][j] = rand.randint(a, b)
    return M


def matricePNumpy(n, p, a, b):
    M = rand.binomial(1, p, (n, n))
    M = M.astype(float)
    for i in range(n):
        for j in range(n):
            if M[i][j] == 0:
                M[i][j] = float('inf')
            else:
                M[i][j] = rand.randint(a, b)
    return M


def matrice(n, a, b):
    return matricePRandom(n, 0.5, a, b)


def matricePRandom(n, p, a, b):
    G = [[0 for i in range(n)] for i in range(n)]
    # programmation d'un graphe aléatoire pondéré où p des arêtes sont des arêtes de poids 0 et 1 - p des arêtes de
    # poids dans l'intervalle [a,b[
    for i in range(n):
        for j in range(n):
            if random.random() < 1 - p:
                G[i][j] = float('inf')
            else:
                G[i][j] = random.randint(a, b)
    return G


def countPoids0(G):
    n = len(G)
    count = 0
    for i in range(n):
        for j in range(n):
            if G[i][j] != float('inf'):
                count += 1
    return count / n ** 2


def moyennePoidsGraphesNumpy(taille, p):
    a = 2
    b = 10
    moyenne = 0
    for i in range(100):
        G = matriceNumpy(taille, a, b)
        moyenne += countPoids0(G)
    return moyenne / 100


def moyennePoidsGraphesRandom(taille, p):
    a = 2
    b = 10
    moyenne = 0
    for i in range(100):
        G = matrice(taille, a, b)
        moyenne += countPoids0(G)
    return moyenne / 100


def moyennePoidsGraphesProportion(taille, p):
    a = 2
    b = 10
    moyenne = 0
    for i in range(100):
        G = matricePNumpy(taille, p, a, b)
        moyenne += countPoids0(G)
    return moyenne / 100


def affichageMatrice(mat):
    for i in range(len(mat)):
        print(mat[i])


# parcours d'un graphe selon dijkstra
def Dijkstra(M, d):
    # Initialisation des dictionnaires dist, pred et distR
    dist = {i: float('inf') for i in range(len(M))}  # Dictionnaire pour stocker les distances les plus courtes
    pred = {}  # Dictionnaire pour stocker les prédécesseurs
    distR = {i: float('inf') for i in range(len(M))}  # Version restreinte des sommets restant à traiter
    distR[d] = 0  # Distance de d à lui-même

    # Tant qu'il reste des sommets à traiter dans distR
    while distR:
        # Trouver le sommet non encore traité avec la plus petite distance dans distR
        u = min(distR, key=distR.get)
        dist[u] = distR.pop(u)  # Mettre à jour la distance minimale pour ce sommet

        # Parcourir les sommets voisins de u et mettre à jour les distances si nécessaire
        for v in range(len(M)):
            if M[u][v] != float('inf') and v in distR:  # Si v est un voisin de u et n'est pas encore traité
                alt = dist[u] + M[u][v]  # Calculer la distance alternative jusqu'à v
                if alt < distR[v]:  # Si l'alternative est plus courte
                    distR[v] = alt  # Mettre à jour la distance de v
                    pred[v] = u  # Mettre à jour le prédécesseur de v

    # Initialisation du dictionnaire de résultats
    result = {}

    # Calculer les itinéraires à partir des prédécesseurs
    for s in range(len(M)):
        if s != d:
            chemin = [s]
            while chemin[-1] != d:
                if pred.get(chemin[-1]) is None:
                    # Le sommet n'est pas joignable à d par un chemin dans le graphe
                    result[s] = "sommet non joignable à {} par un chemin dans le graphe G".format(d)
                    break
                chemin.append(pred[chemin[-1]])
            if chemin[-1] == d:
                result[s] = (dist[s], chemin[::-1])
            elif s not in result:
                # Le sommet n'est pas joignable à d par un chemin dans le graphe
                result[s] = "sommet non joignable à {} par un chemin dans le graphe G".format(d)
        elif s == d:
            result[s] = 0

    return result


"""
Creer une fonction Python Bellman-Ford(M,d) qui prend en entree la matrice d’un
graphe ponderé a poids de signe quelconque, un sommet d de ce graphe donné par son indice
dans la liste des sommets, et qui, en executant l’algorithme de Bellman-Ford, retourne pour
chacun des autres sommets s :
- soit la longueur et l’itineraire du plus court chemin de d à s ;
- soit la mention ”sommet non joignable depuis d par un chemin dans le graphe G”.
- soit la mention ”sommet joignable depuis d par un chemin dans le graphe G, mais pas
de plus court chemin (presence d’un cycle negatif)”.
On codera à partir du pseudocode presenté dans le cours.
On pourra retourner le resultat sous forme de la liste des sommets du chemin obtenu, mais
aussi en l’affichant graphiquement à l’aide de l’outil d'affichage.
"""


def BellmanFord(M, s):
    n = len(M)
    d = {i: [float('inf'), []] for i in range(n)}
    d[s][0] = 0
    mat = graphPEnNonP(M)
    fleches = parcoursAleatoire(mat)
    modif = True
    taille = 0
    while taille < len(M) - 1 and modif:
        modif = False
        for i, j in fleches:
            if M[i][j] != float('inf') and d[j][0] > d[i][0] + M[i][j]:
                modif = True
                d[j][0] = d[i][0] + M[i][j]
                d[j][1] = d[i][1] + [i]
        taille += 1
    # detection de cycle negatif
    for i in range(n):
        for j in range(n):
            if (M[i][j] != float('inf') and d[i][0] != float('inf') and d[j][0] > d[i][0] + M[i][j]):
                return "sommet joignable depuis d par un chemin dans le graphe G, mais pas de plus court chemin (presence d’un cycle negatif)"
        # renvoie les chemins
    return d


def pp(mat, s):
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


def BellmanFordParcoursLargeur(M, s):
    # intialisation du tableau d
    d = {i: [float('inf'), []] for i in range(len(M))}
    # initialisation de la matrice d'adjacence du graphe non pondéré
    mat = graphPEnNonP(M)
    # parcours en largeur de M depuis s
    parcours = parcoursLargeur(mat, s)
    # liste des fleches du parcours en largeur
    fleches = listeFlechesParcours(mat, parcours)
    # initialisation de d
    d[s][0] = 0
    modif = True
    # boucle principale
    taille = 0
    while modif and taille < len(M) - 1:
        modif = False
        # on parcourt chaque flèche dans le parcours en largeur
        for i, j in fleches:
            if d[i][0] != float('inf') and d[j][0] > d[i][0] + M[i][j]:
                modif = True
                d[j][0] = d[i][0] + M[i][j]
                d[j][1] = d[i][1] + [i]
        taille += 1
    # detection de cycle negatif
    for i, j in fleches:
        if M[i][j] != float('inf') and d[i][0] != float('inf') and d[j][0] > d[i][0] + M[i][j]:
            return "sommet joignable depuis d par un chemin dans le graphe G, mais pas de plus court chemin (presence d’un cycle negatif)"
    return d

def BellmanFordParcoursProfondeur(M, s):
    # intialisation du tableau d
    d = {i: [float('inf'), []] for i in range(len(M))}
    # initialisation de la matrice d'adjacence du graphe non pondéré
    mat = graphPEnNonP(M)
    # parcours en largeur de M depuis s
    parcours = pp(mat, s)
    # liste des fleches du parcours en largeur
    fleches = listeFlechesParcours(mat, parcours)
    # initialisation de d
    d[s][0] = 0
    modif = True
    # boucle principale
    taille = 0
    while modif and taille < len(M):
        modif = False
        # on parcourt chaque flèche dans le parcours en largeur
        for i, j in fleches:
            if d[i][0] != float('inf') and d[j][0] > d[i][0] + M[i][j]:
                modif = True
                d[j][0] = d[i][0] + M[i][j]
                d[j][1] = d[i][1] + [i]
        taille += 1
    # detection de cycle negatif
    for i, j in fleches:
        if M[i][j] != float('inf') and d[i][0] != float('inf') and d[j][0] > d[i][0] + M[i][j]:
            return "sommet joignable depuis d par un chemin dans le graphe G, mais pas de plus court chemin (presence d’un cycle negatif)"
    return d

def TempsBF(n, M):
    start = timeit.default_timer()
    BellmanFordParcoursLargeur(M, 1)
    stop = timeit.default_timer()
    return (stop - start) * 1000


def TempsDij(n, M):
    start = timeit.default_timer()
    Dijkstra(M, 1)
    stop = timeit.default_timer()
    return (stop - start) * 1000


def Temps(tab):
    temps = [[], [], [], [], [], []]
    for n in tab:
        M = matricePNumpy(n, 1 / n, 1, 2 ** 31)
        start = timeit.default_timer()
        BellmanFordParcoursLargeur(M, 0)
        stop = timeit.default_timer()
        temps[0].append((stop - start) * 1000)
        start = timeit.default_timer()
        #Dijkstra(M, 0)
        stop = timeit.default_timer()
        temps[1].append((stop - start) * 1000)
        matnonp = graphPEnNonP(M)
        start = timeit.default_timer()
        #parcoursLargeur(matnonp, 0)
        stop = timeit.default_timer()
        temps[2].append((stop - start) * 1000)
        start = timeit.default_timer()
        #pp(matnonp, 0)
        stop = timeit.default_timer()
        temps[3].append((stop - start) * 1000)
        start = timeit.default_timer()
        BellmanFordParcoursProfondeur(M, 0)
        stop = timeit.default_timer()
        temps[4].append((stop - start) * 1000)
        start = timeit.default_timer()
        BellmanFord(M, 0)
        stop = timeit.default_timer()
        temps[5].append((stop - start) * 1000)

    return temps


def listeFlechesParcours(mat, parcours):
    fleches = []
    for s in parcours:
        for i in range(len(mat)):
            if mat[s][i] == 1:
                fleches.append((s, i))
    return fleches


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

def Tours(tab):
    tours = [[], [], [], [], [], []]
    for n in tab:
        M = matricePNumpy(n, 1 / n, 1, 2 ** 31)
        tours[0].append(BellmanFordParcoursLargeur(M, 0))
        tours[1].append(BellmanFord(M, 0))
        tours[2].append(BellmanFordParcoursProfondeur(M, 0))
    return tours

def parcoursAleatoire(mat):
    n = len(mat)
    fleches = []
    for i in range(n):
        for j in range(n):
            if mat[i][j] == 1:
                fleches.append((i, j))
    return fleches