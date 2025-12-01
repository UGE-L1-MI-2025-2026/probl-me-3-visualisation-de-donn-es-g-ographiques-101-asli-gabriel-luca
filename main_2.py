import shapefile
#import fltk_modifie as fltk

SCALE = 100
LAR_FENETRE = 600
LONG_FENETRE = 800
import fltk
import math

fltk.cree_fenetre(LONG_FENETRE, LAR_FENETRE)

sf = shapefile.Reader("departements-20180101") #ouverture du fichier shapefile
sf.records() # visualisation de toutes les entrées du fichier

seine_et_marne = sf.shape(47) # Récupération de l'entrée correspondant à la Seine-et-Marne
seine_et_marne.bbox # Les points extrémaux de la seine-et-marne

#print(seine_et_marne.points) # La liste des points du contour de la Seine-et-Marne
var = seine_et_marne.points

rayon = 2300

def creation_depart(var):
    for i in range(len(var)):
        X = var[i][0]*(math.pi/180)
        Y = var[i][1]*(math.pi/180)
        
        x = rayon * X
        y = rayon * ( math.log( math.tan( ( math.pi/4)+( Y/2) ) ) )
        y_max = rayon * ( math.log( math.tan( ( math.pi/4)+(44) ) ) )
        
        x = x-seine_et_marne.bbox[0]
        y = y_max - y
        
        
        var[i] = (x, y)
        


for i in range(102):
    depart = sf.shape(i)
    var = depart.points
    creation_depart(var)
    fltk.polygone(var,tag="departement"+str(i))
    fltk.deplace("departement"+str(i),300, 2325)

    
print(var)

fltk.attend_ev()
fltk.ferme_fenetre()
