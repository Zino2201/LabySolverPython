from io import *
import os.path

# Labyrinthe
blocs = []
matrice = []
blocs_chemins = []

# Constantes

# Taille labyrinthe
LARGEUR_LABY = 32
HAUTEUR_LABY = 32

# Type de blocs
BLOC_MUR = 0
BLOC_ENTREE = 1
BLOC_VIDE = 2
BLOC_SORTIE = 3

# Variables
x_joueur = 0
y_joueur = 0
x_sortie = 0
y_sortie = 0
chemin = []

# Initialise le labyrinthe
for x in range(0, LARGEUR_LABY):
    blocs.append([])
    blocs_chemins.append([])
    for y in range(0, HAUTEUR_LABY):
        blocs[x].append(BLOC_MUR)
        blocs_chemins[x].append(False)

# Initialise la matrice
for x in range(0, LARGEUR_LABY):
    matrice.append([])
    for y in range(0, HAUTEUR_LABY):
        matrice[x].append(0)

def lire_labyrinthe(chemin):
    """
    Lis le fichier donné pour générer un labyrinthe
    """
    fichier = open(chemin, 'r')

    # Lis chaque caractère pour le transformer en un bloc
    # '#' = du vide
    # '_' = un mur
    # 'E' = l'entrée
    # 'S' = la sortie

    x = 0
    y = 0
    while True:
        c = fichier.read(1)

        if c == '\n':
            continue

        # Quitte la boucle quand on a fini de lire le fichier
        if not c:
            break

        global x_joueur
        global y_joueur
        global x_sortie
        global y_sortie

        # Teste si c'est du vide
        if c == '_':
            blocs[x][y] = BLOC_VIDE
        elif c == 'E':
            blocs[x][y] = BLOC_ENTREE
            x_joueur = x
            y_joueur = y
        elif c == 'S':
            blocs[x][y] = BLOC_SORTIE
            x_sortie = x
            y_sortie = y

        x = x + 1

        # Si on arrive au bout de la ligne, on change de colonne
        if x >= LARGEUR_LABY:
            x = 0
            y = y + 1

            # On sort de la boucle si on est arrivé à la fin de la liste
            if y >= HAUTEUR_LABY:
                break

    fichier.close()

def generer_points(k):
    """
    Génére autour du point k des points valant k+1
    """
    for x in range(len(matrice)):
        for y in range(len(matrice[x])):
            if matrice[x][y] == k:
                if x > 0 and matrice[x - 1][y] == 0 and blocs[x - 1][y] >= BLOC_VIDE:
                    matrice[x - 1][y] = k + 1
                if y > 0 and matrice[x][y - 1] == 0 and blocs[x][y - 1] >= BLOC_VIDE:
                    matrice[x][y - 1] = k + 1
                if x < len(matrice) - 1 and matrice[x + 1][y] == 0 and blocs[x + 1][y] >= BLOC_VIDE:
                    matrice[x + 1][y] = k + 1
                if y < len(matrice[x]) - 1 and matrice[x][y + 1] == 0 and blocs[x][y + 1] >= BLOC_VIDE:
                    matrice[x][y + 1] = k + 1

def resoudre_labyrinthe():
    """
    Résouds le labyrinthe
    :return:
    """

    global x_joueur
    global y_joueur
    global x_sortie
    global y_sortie
    global chemin

    # Génére une matrice de points jusqu'à qu'on trouve la sortie
    matrice[x_joueur][y_joueur] = 1;
    k = 0
    while matrice[x_sortie][y_sortie] == 0:
        k = k + 1
        generer_points(k)

    # Maintenant, on génére un chemin depuis la sortie vers l'entrée
    # en cherchant autour de k un point k - 1 jusqu'a remonté vers l'entrée
    x = x_sortie
    y = y_sortie
    k = matrice[x][y]
    chemin = [(x, y)]
    while k > 1:
        if x > 0 and matrice[x - 1][y] == k - 1:
            x = x - 1
            blocs_chemins[x][y] = True
            chemin.append((x, y))
            k -= 1
        elif y > 0 and matrice[x][y - 1] == k - 1:
            y = y - 1
            blocs_chemins[x][y] = True
            chemin.append((x, y))
            k -= 1
        elif x < len(matrice) - 1 and matrice[x + 1][y] == k - 1:
            x = x + 1
            blocs_chemins[x][y] = True
            chemin.append((x, y))
            k -= 1
        elif y < len(matrice[x]) - 1 and matrice[x][y + 1] == k - 1:
            y = y + 1
            blocs_chemins[x][y] = True
            chemin.append((x, y))
            k -= 1

def afficher_labyrinthe():
    """
    Affiche le labyrinthe
    """

    for y in range(0, HAUTEUR_LABY):
        for x in range(0, LARGEUR_LABY):
            bloc = blocs[x][y]
            if bloc == BLOC_VIDE:
                if blocs_chemins[x][y]:
                    print('.', end='')
                else:
                    print(' ', end='')
            elif bloc == BLOC_MUR:
                print('#', end='')
            elif bloc == BLOC_ENTREE:
                print('E', end='')
            elif bloc == BLOC_SORTIE:
                print('S', end='')
            else:
                print('A', end='')
        print("")

    print("Légende:")
    print("- # : Mur")
    print("- . : Chemin")
    print("- E : Entrée")
    print("- S : Sortie")

def afficher_matrice():
    for y in range(0, HAUTEUR_LABY):
        for x in range(0, LARGEUR_LABY):
            print(matrice[x][y], end='\t')
        print("")

print("SUPER LABYRINTHE DE OUF !!!!!")
while True:
    print("Fichier à ouvrir: ")
    fichier = input()
    if os.path.exists(fichier):
        lire_labyrinthe(fichier)
        resoudre_labyrinthe()
        afficher_labyrinthe()
        #print(chemin)
        #afficher_matrice()
        break
    else:
        print("Fichier introuvable! Réessayez")