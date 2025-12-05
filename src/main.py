import shapefile
import csv
# import fltk_modifie as fltk
import fltk
import math
from os import path

ROOT_DIR = path.dirname(path.dirname(__file__))
ASSETS_DIR = path.join(ROOT_DIR, 'assets')
MAP_DATA_DIR = path.join(ASSETS_DIR, 'map_data')
IMG_DIR = path.join(ASSETS_DIR, 'images')
LONG_FENETRE = 600
LARG_FENETRE = 800
temp_dep = {}


def mercator_pts(shape):
    pts = shape.points
    parts = list(shape.parts) + [len(pts)]
    out = []
    for idx0, idx1 in zip(parts[:-1], parts[1:]):
        poly = []
        for i in range(idx0, idx1):
            phi = math.radians(pts[i][1])
            x = math.radians(pts[i][0])
            y = math.log(math.tan(math.pi / 4 + phi / 2))
            poly.append((x, y))
        out.append(poly)
    return out

def calcule_parametres(x_min, y_min, x_max, y_max, X_orig, Y_orig, W, H):
    a = min(W / (x_max - x_min), H / (y_max - y_min))
    B = X_orig - a * x_min  # centre : + W/2
    C = Y_orig + a * y_min  # centre : + H/2
    return a, B, C

def place_points(x, y, a, B, C, LONG_FENETRE):
    X = a * x + B
    Y = LONG_FENETRE - a * y + C
    return X, Y

with open(
          path.join(MAP_DATA_DIR,
                    'temperature-quotidienne-departementale.csv'),
          encoding='UTF-8-sig',
          newline=''
          ) as csv_file:
    reader = csv.reader(csv_file, delimiter=';')
    next(reader)
    for row in reader:
        # temp_dep[code insee departement] =
        # {TMin: temp, TMax: temp, TMoy: temp}
        # code insee departement : str car 2B est un département
        temp_dep[str(row[1])] = {'TMin': row[3],
                                 'TMax': row[4],
                                 'TMoy': row[5]
                                 }

sf = shapefile.Reader(path.join(MAP_DATA_DIR, "departements-20180101"))
sf.records()  # visualisation de toutes les entrées du fichier



fltk.cree_fenetre(LARG_FENETRE, LONG_FENETRE)
liste_poly = []
y_min, x_min, y_max, x_max = float("inf"), float("inf"), float("-inf"), float("-inf")
for i in range(102):
    depart = sf.shape(i)
    poly_depart = mercator_pts(sf.shape(i))
    ordonnees = [x for pts in poly_depart for x, y in pts]
    abcisses = [y for pts in poly_depart for x, y in pts]
    y_min = min(ordonnees + [y_min])
    x_min = min(abcisses + [x_min])
    y_max = max(ordonnees + [y_max])
    x_max = max(abcisses + [x_max])
    liste_poly += poly_depart

a, B, C = calcule_parametres(y_min, x_min, y_max, x_max, 0, 0, LARG_FENETRE, LONG_FENETRE)
for pts in liste_poly:
    new_pts = []
    for x, y in pts:
        new_pts.append(place_points(x, y, a, B, C, LONG_FENETRE))
    fltk.polygone(new_pts)
# coords = fltk.coordonnees_objet("seine")
# print(coords)
# offset_x = -1 * min(x[0] for x in coords)
# offset_y = -1 * min(y[1] for y in coords)
# fltk.deplace("seine", offset_x, offset_y)
fltk.attend_ev()
fltk.ferme_fenetre()
