import matplotlib.pyplot as plt
import networkx as nx
import graph as g


def toDiGraph(mat):
    G = nx.DiGraph()
    n = len(mat)
    for i in range(n):
        for j in range(n):
            if mat[i][j] != float('inf') and i != j:
                G.add_edge(i + 1, j + 1, weight=mat[i][j])
    return G

nx.bfs_edges
def affichage(mat):
    G = toDiGraph(mat)
    pos = nx.spring_layout(G)  # Positions des nœuds pour le dessin du graphe
    # Dessiner les nœuds
    nx.draw_networkx_nodes(G, pos, node_size=700)
    # Dessiner les arêtes avec leurs poids
    edge_labels = {(i, j): str(weight) for i, j, weight in G.edges(data='weight')}
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), arrowstyle='-|>', arrowsize=20)
    # Ajouter les étiquettes des arêtes (poids)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12)
    # Dessiner les étiquettes des nœuds
    nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')
    plt.title("Graphe dirigé à partir d'une matrice d'adjacence avec pondération")
    plt.show()


def afficheCourbeTemps(a, b):
    n_valeurs = range(a, b)
    temps = g.Temps(n_valeurs)
    temps_BFPL = temps[0]
    temps_dij = temps[1]
    temps_parcoursL = temps[2]
    temps_pp = temps[3]
    temps_BFPP = temps[4]
    temps_BF = temps[5]
    plt.figure(figsize=(10, 5))
    #plt.loglog(n_valeurs, temps_dij, label='Dijkstra')
    plt.loglog(n_valeurs, temps_BFPL, label='Bellman Ford Parcours Largeur')
    plt.loglog(n_valeurs, temps_BFPP, label='Bellman Ford Parcours Profondeur')
    #plt.loglog(n_valeurs, temps_parcoursL, label='Parcours en largeur')
    #plt.loglog(n_valeurs, temps_pp, label='PP')
    plt.loglog(n_valeurs, temps_BF, label='Bellman Ford')
    plt.xlabel('Nombre de sommets n')
    plt.ylabel('Temps d\'exécution (ms)')
    plt.title('Comparaison du temps d\'exécution des algorithmes de plus courts chemins')
    plt.legend()
    plt.grid(True)
    plt.show()
    # Calculez les sommes des temps pour chaque algorithme
    print(f"Somme des temps pour Dijkstra : {sum(temps_dij)}")
    print(f"Somme des temps pour Bellman Ford Parcours Largeur : {sum(temps_BFPL)}")
    print(f"Somme des temps pour Bellman Ford Parcours Profondeur : {sum(temps_BFPP)}")
    print(f"Somme des temps pour Bellman Ford : {sum(temps_BF)}")


def printParcours(parcours):
    if isinstance(parcours,str):
        print(parcours)
    else:
        for i in range(len(parcours)):
            print(f"Sommet : {i}")
            print(f"Distance : {parcours[i][0]} , Prédecesseur : {parcours[i][1]}")

def afficheCourbeTours(a,b):
    n_valeurs = range(a, b)
    tours = g.Tours(n_valeurs)
    tours_BFPL = tours[0]
    tours_BF = tours[1]
    tours_BFPP = tours[2]
    plt.figure(figsize=(10, 5))
    plt.loglog(n_valeurs, tours_BFPL, label='Bellman Ford Parcours Largeur')
    plt.loglog(n_valeurs, tours_BFPP, label='Bellman Ford Parcours Profondeur')
    plt.loglog(n_valeurs, tours_BF, label='Bellman Ford')
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