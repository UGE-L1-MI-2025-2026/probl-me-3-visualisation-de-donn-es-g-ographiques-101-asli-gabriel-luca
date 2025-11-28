import shapefile
import fltk

sf = shapefile.Reader("departements-20180101") #ouverture du fichier shapefile
sf.records() # visualisation de toutes les entrées du fichier

seine_et_marne = sf.shape(47) # Récupération de l'entrée correspondant à la Seine-et-Marne
seine_et_marne.bbox # Les points extrémaux de la seine-et-marne

#print(seine_et_marne.points) # La liste des points du contour de la Seine-et-Marne
var = seine_et_marne.points

for i in range(len(var)):
    var[i] = (var[i][0]*100, 600 - var[i][1]*100 + 4500)

fltk.cree_fenetre(800, 600)
fltk.polygone(var,tag="seine")
fltk.attend_ev()
fltk.ferme_fenetre()
