import shapefile
import fltk_modifie as fltk

SCALE = 100
LAR_FENETRE = 600
LONG_FENETRE = 800
import fltk
import math
sf = shapefile.Reader("departements-20180101") #ouverture du fichier shapefile
sf.records() # visualisation de toutes les entrées du fichier

seine_et_marne = sf.shape(47) # Récupération de l'entrée correspondant à la Seine-et-Marne
seine_et_marne.bbox # Les points extrémaux de la seine-et-marne

#print(seine_et_marne.points) # La liste des points du contour de la Seine-et-Marne
var = seine_et_marne.points

rayon = 5000

for i in range(len(var)):
    var[i] = (SCALE * var[i][0],
              SCALE * (90 - var[i][1]))
               # Les ordonnées vont du haut au bas de l'écran sur python
               # donc on fait une soustraction. La longitude max est de 90 donc
               # on soustrait la longitude à 90 pour "retourner" l'image"
    X = var[i][0]*(math.pi/180)
    Y = var[i][1]*(math.pi/180)
    
    x = rayon * X
    y = rayon * ( math.log( math.tan( ( math.pi/4)+( Y/2) ) ) )
    y_max = rayon * ( math.log( math.tan( ( math.pi/4)+(44) ) ) )
    
    x = x-seine_et_marne.bbox[0]
    y = y_max - y
    
    var[i] = (x, y)
print(var)


fltk.cree_fenetre(LONG_FENETRE, LAR_FENETRE)
fltk.polygone(var,tag="seine")
coords = fltk.coordonnees_objet("seine")
offset_x = -1 * min(x[0] for x in coords)
offset_y = -1 * min(y[1] for y in coords)
fltk.deplace("seine", offset_x, offset_y)
fltk.deplace('seine', 0, 4800)
fltk.attend_ev()
fltk.ferme_fenetre()
