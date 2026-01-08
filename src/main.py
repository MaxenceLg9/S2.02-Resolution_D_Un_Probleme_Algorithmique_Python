import numpy as np

import graph as g
import affichageG as ag
import timeit
import mainSeuil as ms

M1=[[float('inf'), float('inf'),  8., 11., float('inf'),  6., float('inf'),  7., 14.,  7.],
    [ 1., float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 14., float('inf'), float('inf')],
    [float('inf'),  8., float('inf'), 14., float('inf'), float('inf'), float('inf'), float('inf'), 14.,  5.],
    [float('inf'), float('inf'), float('inf'), float('inf'), float('inf'),  9., float('inf'), 12., float('inf'),  6.],
    [ 9., float('inf'), float('inf'), float('inf'),  8., float('inf'), 14.,  9., float('inf'), float('inf')],
    [float('inf'), float('inf'), float('inf'), 12., float('inf'), 12.,  4., float('inf'), float('inf'),  6.],
    [float('inf'), 10., float('inf'), 13., float('inf'), float('inf'), 11., float('inf'), float('inf'),  7.],
    [float('inf'), 12., 14., float('inf'), float('inf'), float('inf'), float('inf'),  9., float('inf'), float('inf')],
    [11.,  7., float('inf'),  6., float('inf'),  6., 11.,  6.,  6., float('inf')],
    [12., float('inf'), float('inf'), float('inf'), float('inf'), 11.,  1.,  2., float('inf'), float('inf')]]


N1=[[-3., float('inf'), float('inf'),  4., float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), -1.],
    [ 3., float('inf'),  0., float('inf'), float('inf'), float('inf'), float('inf'), float('inf'),  3., float('inf')],
    [float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), -4.],
    [ 3., float('inf'), float('inf'), float('inf'),  3., float('inf'), float('inf'), float('inf'), -5., float('inf')],
    [-4., float('inf'), float('inf'), float('inf'),  5.,  3., float('inf'),  5., -6., float('inf')],
    [float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), -7., -3.],
    [ 5., float('inf'), -1., float('inf'), float('inf'), -7., float('inf'), float('inf'), -4., -7.],
    [float('inf'), float('inf'), float('inf'), float('inf'),  4.,  5., -3., float('inf'),  3., float('inf')],
    [ 2., float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf')],
    [-7., float('inf'), float('inf'), -5., float('inf'),  0.,  4., float('inf'), float('inf'), float('inf')]]


P1=np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
       [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
       [0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
       [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

def main():
    # print(g.BellmanFordParcoursLargeur(N1, 3))
    # print(g.BellmanFordParcoursProfondeur(N1, 3))
    # print(g.BellmanFord(N1, 3))
    # print(g.Dijkstra(N1, 3))
    print(ms.fc(P1))
    #ag.afficheCourbeTours(2, 200)


if __name__ == '__main__':
    main()
