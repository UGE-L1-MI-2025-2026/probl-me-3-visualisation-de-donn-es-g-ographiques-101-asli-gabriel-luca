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
SCALE = 2300
y_max = SCALE * math.log(math.tan(math.pi / 4 + 44))
temp_dep = {}


def creation_depart(shape):
    pts = shape.points
    out = []
    for i in range(len(pts)):
        phi = math.radians(pts[i][1])
        x = SCALE * math.radians(pts[i][0])
        y = y_max - SCALE * math.log(math.tan(math.pi / 4 + phi / 2))
        out.append((x, y))
    return out

def calcule_parametres(x_min, y_min, x_max, y_max, X_orig, Y_orig, W, H):
    a = min(W / (x_max - x_min), H / (y_max - y_min))
    B = X_orig - a * x_min  # centre : + W/2
    C = Y_orig - a * y_min  # centre : + H/2
    return a, B, C

def place_points(x, y, a, B, C):
    X = a * x + B
    Y = a * -y + C
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

LAR_FENETRE = 600
LONG_FENETRE = 800
sf = shapefile.Reader(path.join(MAP_DATA_DIR, "departements-20180101"))
sf.records()  # visualisation de toutes les entrées du fichier



# tests
fltk.cree_fenetre(LONG_FENETRE, LAR_FENETRE)
seine_et_marne = sf.shape(47)
long_min, lat_min, long_max, lat_max = seine_et_marne.bbox
pts = seine_et_marne.points
a, B, C = calcule_parametres(long_min, lat_min, long_max, lat_max, 0, 0, LAR_FENETRE, LONG_FENETRE)
for x, y in zip(pts[::2], pts[1::2]):
    print(place_points(x, y, a, B, C))
    
breakpoint()

#####
for i in range(102):
    depart = sf.shape(i)
    pts = creation_depart(sf.shape(i))
    fltk.polygone(pts, tag=str(i))
    fltk.deplace(str(i), 300, 2325)
# coords = fltk.coordonnees_objet("seine")
# print(coords)
# offset_x = -1 * min(x[0] for x in coords)
# offset_y = -1 * min(y[1] for y in coords)
# fltk.deplace("seine", offset_x, offset_y)
fltk.attend_ev()
fltk.ferme_fenetre()
