import numpy.random as rand
from matplotlib import pyplot as plt


############################################################################################################
########################################### MATRICES GEN ###################################################


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

# Bellman Ford : différentes implémentations
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
                d[j][1] = i
        taille += 1
    # detection de cycle negatif
    for i, j in fleches:
        if M[i][j] != float('inf') and d[i][0] != float('inf') and d[j][0] > d[i][0] + M[i][j]:
            return "sommet joignable depuis d par un chemin dans le graphe G, mais pas de plus court chemin (presence d’un cycle negatif)"
    return taille


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
                d[j][1].append(i)
        taille += 1
    # detection de cycle negatif
    for i, j in fleches:
        if M[i][j] != float('inf') and d[i][0] != float('inf') and d[j][0] > d[i][0] + M[i][j]:
            return "sommet joignable depuis d par un chemin dans le graphe G, mais pas de plus court chemin (presence d’un cycle negatif)"
    return taille


def BellmanFord(M, s):
    n = len(M)
    d = {i: [float('inf'), []] for i in range(n)}
    d[s][0] = 0
    mat = graphPEnNonP(M)
    fleches = parcoursAleatoireEnFleches(mat)
    modif = True
    taille = 0
    while taille < len(M) - 1 and modif:
        modif = False
        for i, j in fleches:
            if M[i][j] != float('inf') and d[j][0] > d[i][0] + M[i][j]:
                modif = True
                d[j][0] = d[i][0] + M[i][j]
                d[j][1] = i
        taille += 1
    # detection de cycle negatif
    for i in range(n):
        for j in range(n):
            if (M[i][j] != float('inf') and d[i][0] != float('inf') and d[j][0] > d[i][0] + M[i][j]):
                return "sommet joignable depuis d par un chemin dans le graphe G, mais pas de plus court chemin (presence d’un cycle negatif)"
        # renvoie les chemins
    return taille


############################################################################################################
############################################## PARCOURS ####################################################

# Parcours en Profondeur
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

    return Resultat


# Parcours en Largeur
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


def parcoursAleatoireEnFleches(mat):
    n = len(mat)
    fleches = []
    for i in range(n):
        for j in range(n):
            if mat[i][j] == 1:
                fleches.append((i, j))
    return fleches


# Transformation du Graphe Pondéré en Non Pondéré

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

# Liste des fleches du parcours

def listeFlechesParcours(mat, parcours):
    fleches = []
    for s in parcours:
        for i in range(len(mat)):
            if mat[s][i] == 1:
                fleches.append((s, i))
    return fleches

def Tours(tab):
    tours = [[], [], [], [], [], []]
    for n in tab:
        M = matricePNumpy(n, 1 / n, 1, 2 ** 31)
        tours[0].append(BellmanFordParcoursLargeur(M, 0))
        tours[1].append(BellmanFord(M, 0))
        tours[2].append(BellmanFordParcoursProfondeur(M, 0))
    return tours

def afficheGraphTours(a,b):
    n_valeurs = range(a, b)
    tours = Tours(n_valeurs)
    tours_BFPL = tours[0]
    tours_BF = tours[1]
    tours_BFPP = tours[2]
    plt.figure(figsize=(10, 5))
    plt.plot(n_valeurs, tours_BFPL, label='Bellman Ford Parcours Largeur')
    plt.plot(n_valeurs, tours_BFPP, label='Bellman Ford Parcours Profondeur')
    plt.plot(n_valeurs, tours_BF, label='Bellman Ford')
    plt.xlabel('Nombre de sommets n')
    plt.ylabel('Temps d\'exécution (ms)')
    plt.title('Comparaison du nombre de tours d\'exécution des algorithmes de plus courts chemins')
    plt.legend()
    plt.grid(True)
    plt.show()
    # Calculez les sommes des temps pour chaque algorithme
    print(f"Somme des tours pour Bellman Ford Parcours Largeur : {sum(tours_BFPL)}")
    print(f"Somme des tours pour Bellman Ford Parcours Profondeur : {sum(tours_BFPP)}")
    print(f"Somme des tours pour Bellman Ford : {sum(tours_BF)}")


afficheGraphTours(2, 200)