import shapefile
# import fltk_modifie as fltk
import fltk
import math
from os import path

ROOT_DIR = path.dirname(path.dirname(__file__))
ASSETS_DIR = path.join(ROOT_DIR, 'assets')
MAP_DATA_DIR = path.join(ASSETS_DIR, 'map_data')
IMG_DIR = path.join(ASSETS_DIR, 'images')
RAYON = 5000
y_max = RAYON * math.log(math.tan(math.pi / 4 + 44))

SCALE = 100
LAR_FENETRE = 600
LONG_FENETRE = 800
sf = shapefile.Reader(path.join(MAP_DATA_DIR, "departements-20180101"))
sf.records()  # visualisation de toutes les entrées du fichier


# Récupération de l'entrée correspondant à la Seine-et-Marne
seine_et_marne = sf.shape(47)
pts_seine_et_marne = seine_et_marne.points

for i in range(len(pts_seine_et_marne)):
    lmbd = pts_seine_et_marne[i][0] * (math.pi / 180)  # lambda
    phi = pts_seine_et_marne[i][1] * (math.pi / 180)  # phi
    x = RAYON * lmbd - seine_et_marne.bbox[0]
    y = y_max - RAYON * math.log(math.tan(math.pi / 4 + phi / 2))
    pts_seine_et_marne[i] = (x, y)

fltk.cree_fenetre(LONG_FENETRE, LAR_FENETRE)
fltk.polygone(pts_seine_et_marne, tag="seine")
# coords = fltk.coordonnees_objet("seine")
# print(coords)
# offset_x = -1 * min(x[0] for x in coords)
# offset_y = -1 * min(y[1] for y in coords)
# fltk.deplace("seine", offset_x, offset_y)
fltk.deplace('seine', 0, 4800)
fltk.attend_ev()
fltk.ferme_fenetre()
