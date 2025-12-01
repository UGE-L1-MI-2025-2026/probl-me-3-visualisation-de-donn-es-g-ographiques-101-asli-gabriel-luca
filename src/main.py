import shapefile
# import fltk_modifie as fltk
import fltk
import math
from os import path

ROOT_DIR = path.dirname(path.dirname(__file__))
ASSETS_DIR = path.join(ROOT_DIR, 'assets')
MAP_DATA_DIR = path.join(ASSETS_DIR, 'map_data')
IMG_DIR = path.join(ASSETS_DIR, 'images')
RAYON = 2300
y_max = RAYON * math.log(math.tan(math.pi / 4 + 44))

SCALE = 100
LAR_FENETRE = 600
LONG_FENETRE = 800
sf = shapefile.Reader(path.join(MAP_DATA_DIR, "departements-20180101"))
sf.records()  # visualisation de toutes les entrées du fichier


# Récupération de l'entrée correspondant à la Seine-et-Marne
seine_et_marne = sf.shape(47)
pts_seine_et_marne = seine_et_marne.points


def creation_depart(shape):
    pts = shape.points
    out = []
    for i in range(len(pts)):
        lmbd = pts[i][0] * (math.pi / 180)  # lambda
        phi = pts[i][1] * (math.pi / 180)  # phi
        x = RAYON * lmbd - seine_et_marne.bbox[0]
        y = y_max - RAYON * math.log(math.tan(math.pi / 4 + phi / 2))
        out.append((x, y))
    return out


fltk.cree_fenetre(LONG_FENETRE, LAR_FENETRE)
for i in range(102):
    depart = sf.shape(i)
    pts = creation_depart(sf.shape(i))
    fltk.polygone(pts, tag="departement" + str(i))
    fltk.deplace("departement" + str(i), 300, 2325)
# coords = fltk.coordonnees_objet("seine")
# print(coords)
# offset_x = -1 * min(x[0] for x in coords)
# offset_y = -1 * min(y[1] for y in coords)
# fltk.deplace("seine", offset_x, offset_y)
fltk.attend_ev()
fltk.ferme_fenetre()
