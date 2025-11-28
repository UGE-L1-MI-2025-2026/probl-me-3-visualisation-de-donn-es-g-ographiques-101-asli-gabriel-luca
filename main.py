import shapefile
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
    X = var[i][0]*(math.pi/180)
    Y = var[i][1]*(math.pi/180)
    
    x = rayon * X
    y = rayon * ( math.log( math.tan( ( math.pi/4)+( Y/2) ) ) )
    y_max = rayon * ( math.log( math.tan( ( math.pi/4)+(44) ) ) )
    
    x = x-seine_et_marne.bbox[0]
    y = y_max - y
    
    var[i] = (x, y)
print(var)


fltk.cree_fenetre(800, 600)
fltk.polygone(var,tag="seine")
fltk.deplace('seine', 0, 4800)
fltk.attend_ev()
fltk.ferme_fenetre()
