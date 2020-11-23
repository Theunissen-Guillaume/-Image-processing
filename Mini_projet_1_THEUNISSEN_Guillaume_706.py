#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from PIL import Image, ImageTk


def negatif():
    """
    Fonction negatif : Elle recupere la photo, la parcours, et récupere les valeurs rgb de chaqsue pixel. Ces valeurs
    sont ensuite remplacé par leurs inverses.
    """
    photo = photo_trans
    taille = photo.size
    for i in range(taille[0]):
        for j in range(taille[1]):
            pixel = photo.getpixel((i, j))
            photo.putpixel((i, j), (255 - pixel[0], 255 - pixel[1], 255 - pixel[2]))
    affiche_photo2(photo)
    return


def NetB():
    """
    Fonction NetB, qui parcours les pixel de l'image, determijne le niveau de gris à l'aide d'une formule, et suivant
    un seuil, donne la couleur noir ou blanc au pixel.
    """
    photo = photo_trans
    seuil = scale_seuil.get()  # Récuperation du seuil du scale
    taille = photo.size
    for i in range(taille[0]):
        for j in range(taille[1]):
            pixel = photo.getpixel((i, j))
            gray = int(round(0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2]))  # Formule d'internet
            if gray <= seuil:
                photo.putpixel((i, j), (255, 255, 255))
            elif gray > seuil:
                photo.putpixel((i, j), (0, 0, 0))
    affiche_photo2(photo)
    return


def contour_image():
    """
    Fonction coutour_image : Elle parcours chaque pixel. Garde en memoire les pixels adjacents. Grace à la fonction
    moyenne, elle determine la moyenne des 3 couleurs RGB. On compare ainsi les pixels, et suivant un seuil réglable,
    ils deviennent soit noir ou blanc.
    """
    photo = photo_trans
    seuil = scale_seuil.get()  # Récuperation du seuil du scale
    taille = photo.size
    for i in range(0, taille[0] - 1):
        for j in range(0, taille[1] - 1):
            a = photo.getpixel((i, j))
            b = photo.getpixel((i + 1, j))
            c = photo.getpixel((i, j + 1))
            if abs(moyenne_pixel(a) - moyenne_pixel(b)) > seuil or abs(moyenne_pixel(a) - moyenne_pixel(c)) > seuil:
                photo.putpixel((i, j), (0, 0, 0))
            else:
                photo.putpixel((i, j), (255, 255, 255))
    affiche_photo2(photo)
    return


def moyenne_pixel(x):
    """
    Fonction qui fait la moyenne des valeurs RGB d'un pixels.
    :param x: x etant le pixel envoyer par la fonctioncoutour_image
    :return:  returne la moyenne
    """
    moy = int((x[0] + x[1] + x[2]) / 3)
    return moy


def mirroir():
    """
    Fonction mirroir: Elle parcours seulement la partie gauche de l'image. Chaques pixels est prit un par un dans une
    variable 'b', et son symetrique dans 's'. Elle donne donc ensuite, la valeur de 's' à 'b', puis 'b' à 's'.
    """
    photo = photo_trans
    taille = photo.size

    for i in range(int(taille[0] / 2)):
        for j in range(taille[1]):
            b = photo.getpixel((i, j))  # Pixel gauche
            s = photo.getpixel((taille[0] - i - 1, j))  # Symétrique à droite
            photo.putpixel((i, j), s)
            photo.putpixel((taille[0] - i - 1, j), b)
    affiche_photo2(photo)
    return


def Redim():
    """
    Fonction Redim : Marche avec la fonction resize. On utilise pas de facteur, mais l'utilisateur choisie la longueur
    de l'image, et la hauteur est calculé en gardant le bon rapport.
    """
    photo = photo_trans
    facteur = scale_facteur.get()   # Récuperation du facteur du scale

    wpercent = (facteur / float(photo.size[0]))
    hsize = int((float(photo.size[1]) * float(wpercent)))
    photo = photo.resize((facteur, hsize), Image.ANTIALIAS)
    affiche_photo2(photo)

    """
    --------------------------------------------------
    Trace de recherche sans fonction resize :
    --------------------------------------------------
    
    taille = photo.size
    image_fini = Image.new('RGB', (taille[0] * facteur + 1000, taille[1] * facteur + 1000), "white")

    for i in range(taille[0] - 1):
        for j in range(taille[1]):
            p_gauche = photo.getpixel((i, j))
            p_droite = photo.getpixel((i + 1, j))

            diff_rouge = p_gauche[0] - p_droite[0]
            diff_vert = p_gauche[1] - p_droite[1]
            diff_bleu = p_gauche[2] - p_droite[2]

            nb_p = facteur - 2
            if nb_p == 0:
                nb_p = 1

            rouge = int(diff_rouge / nb_p)
            vert = int(diff_vert / nb_p)
            bleu = int(diff_bleu / nb_p)

            image_fini.putpixel((i, j), (p_gauche[0], p_gauche[1], p_gauche[2]))

            for k in range(1, nb_p + 1):
                image_fini.putpixel((i + k, j), (p_gauche[0] - rouge, p_gauche[1] - vert, p_gauche[2] - bleu))
            image_fini.putpixel((i * facteur, j * facteur), (p_droite[0], p_droite[1], p_droite[2]))
    """
    return


def recup_txt():
    """
    Fonction recup_txt : Elle permet de récuperer le nom de l'image du entry.
    :return: 'txt' , le nom de l'image
    """
    txt = entry.get()
    return (txt)


def affiche_photo():
    """
    Fonction affiche_photo : Elle affiche le photo de base à l'ouverture.
    """
    global main
    txt = recup_txt()   # Récuperation nom de l'image
    global photo_depart
    global photo_trans
    photo_depart = Image.open(txt)
    photo_trans = photo_depart  # on sauvegarde l'exemplaire original

    im1 = ImageTk.PhotoImage(file=txt)  # On affiche le photo avec tkinter
    cadrePhoto = Label(zoneImage, image=im1)
    cadrePhoto.image = im1
    cadrePhoto.grid(column=0, columnspan=3, row=1, rowspan=400)
    main.destroy()  # On ferme le fenetre main, celle qui demande le nom du fichier


def affiche_photo2(txt):
    """
    Fonction affiche_photo2 : Elle affiche tout les autres photos modifiée0.
    """
    im1 = ImageTk.PhotoImage(txt)
    cadrePhoto = Label(zoneImage, image=im1)
    cadrePhoto.image = im1
    cadrePhoto.grid(column=0, columnspan=3, row=1, rowspan=400)


def open_picture():
    """
    Fonction open_picture : Elle gere la fenetre main, d'ouverture de la photo, du nom avec entry...
    """
    global entry
    global main
    main = Tk()

    # widget pour choisir son image
    texte = Label(main, text="nom de votre image")
    texte.grid(column=0, row=0)

    entry = Entry(main)  # Entry pour le chemin de la photo
    entry.grid(column=1, row=0)

    bouton = Button(main, text="valider", activebackground="gray", command=affiche_photo)
    bouton.grid(column=2, row=0)


def save():
    """
    Fonction qui sauvegarde sous le nom "b.jpg" les modifications apporté à la photo.
    """
    sauvegarde = Tk()
    photo_trans.show()
    # widget pour choisir son image
    texte = Label(sauvegarde, text="nom de votre image")
    texte.grid(column=0, row=0)

    entry_save = Entry(sauvegarde) # Entry pour le chemin de la photo
    entry_save.grid(column=1, row=0)

    bouton = Button(sauvegarde, text="valider", activebackground="gray")
    bouton.grid(column=2, row=0)
    txt = str(input("nom du ficher à sauvegarder"))
    photo_trans.save(txt)



global photo_depart
global photo_trans
global entry
global main

# Création de la fenêtre
fen_princ = Tk()
fen_princ.title("Phototon")

# Création du cadre-conteneur pour les menus
zoneMenu = Frame(fen_princ, borderwidth=3, bg='#557788')
zoneMenu.pack(fill=X)

# Création du cadre-conteneur pour les scales
zoneReglage = Frame(fen_princ, bg='#557788',)
zoneReglage.pack(side=RIGHT, fill=Y)

# Création du cadre-conteneur pour l'image
zoneImage = Frame(fen_princ)
zoneImage.pack()



# Création de l'onglet Fichier
menuFichier = Menubutton(zoneMenu, text='Fichier', width='20', borderwidth=2, bg='gray', activebackground='darkorange', relief=RAISED)
menuFichier.grid(row=0, column=0)

# Création de l'onglet Edition
menuEdit = Menubutton(zoneMenu, text='Editer', width='20', borderwidth=2, bg='gray', activebackground='darkorange', relief=RAISED)
menuEdit.grid(row=0, column=1)

# Création de l'onglet Format
menuImage = Menubutton(zoneMenu, text='Image', width='20', borderwidth=2, bg='gray', activebackground='darkorange', relief=RAISED)
menuImage.grid(row=0, column=2)

# Création de l'onglet Affichage
menuAffichage = Menubutton(zoneMenu, text='Affichage', width='20', borderwidth=2, bg='gray', activebackground='darkorange', relief=RAISED)
menuAffichage.grid(row=0, column=3)

# Création d'un menu défilant
menuDeroulant1 = Menu(menuFichier, tearoff=0)
menuDeroulant1.add_command(label="Open", command=open_picture)
menuDeroulant1.add_command(label="Save", command=save)

menuDeroulant2 = Menu(menuEdit, tearoff=0)
menuDeroulant2.add_command(label="Mirroir", command=mirroir)
menuDeroulant2.add_command(label="Négatif", command=negatif)
menuDeroulant2.add_command(label="Contour", command=contour_image)

menuDeroulant3 = Menu(menuImage, tearoff=0)
menuDeroulant3.add_command(label="Redimensionner", command=Redim)

# Attribution du menu déroulant au menu Fichier
menuFichier.configure(menu=menuDeroulant1)
menuEdit.configure(menu=menuDeroulant2)
menuImage.configure(menu=menuDeroulant3)

# Création des scale
scale_seuil = Scale(zoneReglage, orient='horizontal', bg="#557788", highlightthickness=0, from_=0, to=255, resolution=10, tickinterval=50, length=200, label='Seuil (N&blanc / Contour image)')
scale_seuil.grid(column=2, row=4)

scale_facteur = Scale(zoneReglage, orient='horizontal', bg="#557788", highlightthickness=0, from_=0, to=4000, resolution=50, tickinterval=1000, length=200, label='Facteur (Redimensionner)')
scale_facteur.grid(column=2, row=2)

fen_princ.mainloop()

