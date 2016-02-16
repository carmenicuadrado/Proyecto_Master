#-------------------------------------------------------------------------------
# Name:        Impacto Ambiental
# Purpose:     Esta herramienta selecciona el poligono cuyo impacto ambiental
#              es menor y lo copia en una nueva clase de entidad. Para ello bebe
#              de un raster que almacena el valor del impacto ambiental
#              (Raster_ImpactoAbietal) de cada pixel.
#              El geoprocesamiento sigue el siguiente proceso:
#
#                   1. Se emplea la herramienta Extract by Mask para obtener un
#                      raster de cada uno de los poligonos introducidos por el
#                      usuario.
#
#                   2. Se realiza la media del valor del pixel de cada uno de
#                      los r?ster creados para cada poligono de cada alternativa.
#
#                   3. Se selecciona el poligono cuya media de los valores de
#                      los pixeles es menor, ya que se corresponde con la
#                      alternativa que produce menor impacto.
#
#                   4. Esta alternativa seleccionada se copia en una feature class
#                      existente (Proyectos).
#
# Author:      Carmen Izquierdo Cuadrado
#
# Created:     07/02/2016
# Copyright:   (c) Carmen 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# Se importa el modulo Arcpy:
import arcpy
from arcpy.sa import *

# Se establecela geodatabase
wksp = "C:\Student\PROYECTO\Datos\Scratch.gdb"                                 ## PARAMETRO: Geodatabase donde se encuentran los datos de entrada y donde se almacenar?n los aoutputs
arcpy.env.workspace = wksp
arcpy.env.overwriteOutput = True


# Se crea una variable con el raster de impactos. *Esta variable, cuando se suba
# como geoprocesamiento, entiendo que llama al servicio de imagen que almacena
# el raster. Esta variable luego se pasa con la herramienta "arcpy.GetParameter".
Raster_ImpactoAmbiental = arcpy.GetParameterAsText(0)                                 ## PARAMETRO: raster que indica el impacto ambiental

# Se crean tres variables, cada una de las cuales con la clase de entidad que
# simula cada una de las alternativas del proyecto. *Estas variables, cuando se
# suban como geoprocesamiento, entiendo que llaman a los poligonos dibujados por
# el usuario (esto se implementa con javascript?).
# Esta variable luego se pasa con la herramienta "arcpy.GetParameter".

Alternativa_1 = arcpy.GetParameterAsText(1)                                                   ## PARAMETRO: feature class que recoge el pol?gono de la alternativa 1
Alternativa_2 = arcpy.GetParameterAsText(2)                                                   ## PARAMETRO: feature class que recoge el pol?gono de la alternativa 2
Alternativa_3 = arcpy.GetParameterAsText(3)                                                  ## PARAMETRO: feature class que recoge el pol?gono de la alternativa 3

# Se crea una funcion que obtenga el valor medio del impacto ambiental de una
# alternativa. Para ello se sigue el siguiente proceso:
#   1. Saber que tipo de proyecto es.
#   2. En funcion del tipo de proyecto se define un valor para el area de
#      influencia de ese proyecto.
#   3. Se pasa la herramienta buffer con el valor anterior para obtener el area
#      de influencia.
#   4. Se emplea la herramienta "Zonal Statistics as Table" con el poligono
#      creado con el buffer como"Input Raster or feature zone data", y el raster
#      de Impacto Ambiental como "Input Value Raster"

# *Modificar luego en JavaScript. En funcion de si el proyecto es de un tipo u
# otro, el valor del buffer es distinto. En el siguiente paso se simula esta
# situaci?n, sin embargo, esto se realizar? posteriormente como un desplegable
# mediante JavaScript.

# 1. Se le pide al usuario que diga que tipo de proyecto desea realizar.
#    Esta accion es auxiliar ya que en futuro se pedir? con un desplegable:
Tipo_Proyecto = arcpy.GetParameterAsText(4)
                                                                                 ## PARAMETRO: tipolog?a del proyecto
# 2. En funcion de la tipologia introducida se le asigna un valor a la variable
#    que almacena la distancia del buffer.
if Tipo_Proyecto == "0":
    Dist_buffer = 50

elif Tipo_Proyecto == "1":
    Dist_buffer = 20

elif Tipo_Proyecto == "2":
    Dist_buffer = 20

elif Tipo_Proyecto == "3":
    Dist_buffer = 30

elif Tipo_Proyecto == "4":
    Dist_buffer = 10

elif Tipo_Proyecto == "5":
    Dist_buffer = 20

elif Tipo_Proyecto == "6":
    Dist_buffer = 30
elif Tipo_Proyecto == "7":
    Dist_buffer = 50

elif Tipo_Proyecto == "8":
    Dist_buffer = 10

elif Tipo_Proyecto == "9":
    Dist_buffer = 20

elif Tipo_Proyecto == "10":
    Dist_buffer = 10

elif Tipo_Proyecto == "11":
    Dist_buffer = 100

elif Tipo_Proyecto == "12":
    Dist_buffer = 500

elif Tipo_Proyecto == "13":
    Dist_buffer = 50


print "El area de influencia tiene una distancia de {} m.".format(Dist_buffer)



# 3. Se ejecuta la herramienta buffer con el valor de distancia obtenido arriba:
#    Primero se crea una Feature layer con el poligono que representa cada
#    alternativa del proyecto.

FL_Alternativa1 = arcpy.MakeFeatureLayer_management(Alternativa_1, "FL_Alternativa1")
FL_Alternativa2 = arcpy.MakeFeatureLayer_management(Alternativa_2, "FL_Alternativa2")
FL_Alternativa3 = arcpy.MakeFeatureLayer_management(Alternativa_3, "FL_Alternativa3")

#    Una vez se dispone de las Feature layers se procede a ejecutar un buffer
#    para cada alternativa, que se almacenan en tres feature classes diferentes:

Dist_buffer_m = str(Dist_buffer) + " meters"
AI_Aternativa1 = arcpy.Buffer_analysis(FL_Alternativa1,"AI_Alternativa1", Dist_buffer_m)
AI_Aternativa2 = arcpy.Buffer_analysis(FL_Alternativa2,"AI_Alternativa2", Dist_buffer_m)
AI_Aternativa3 = arcpy.Buffer_analysis(FL_Alternativa3,"AI_Alternativa3", Dist_buffer_m)


# 4. Se calcula el impacto ambiental medio del rater extraido arriba, mediante
#    el calculo del valor medio de todas las celdas con herramienta Zonal
#    Statistics as Table.

AI_AternativaDesc1 = arcpy.Describe(AI_Aternativa1)
zone_field1 = AI_AternativaDesc1.OIDFieldName


AI_AternativaDesc2 = arcpy.Describe(AI_Aternativa2)
zone_field2 = AI_AternativaDesc2.OIDFieldName


AI_AternativaDesc3 = arcpy.Describe(AI_Aternativa3)
zone_field3 = AI_AternativaDesc3.OIDFieldName


arcpy.CheckOutExtension("Spatial")

Table_MediaImpacto1 =ZonalStatisticsAsTable(AI_Aternativa1,zone_field1,Raster_ImpactoAmbiental, "Media_Impacto1","NODATA", "MEAN")
Table_MediaImpacto2 = ZonalStatisticsAsTable(AI_Aternativa2,zone_field2,Raster_ImpactoAmbiental, "Media_Impacto2","NODATA", "MEAN")
Table_MediaImpacto3 = ZonalStatisticsAsTable(AI_Aternativa3,zone_field3,Raster_ImpactoAmbiental, "Media_Impacto3","NODATA", "MEAN")


#   Se introduce un cursor para extraer el valor de la media del impacto de la
#   tabla que se acaba de crear:


with arcpy.da.SearchCursor(Table_MediaImpacto1, "MEAN") as cursor:
    for row in cursor:
        valor_impacto1 = row[0]
        print "La media del impacto 1 es: " + str(valor_impacto1)


with arcpy.da.SearchCursor(Table_MediaImpacto2, "MEAN") as cursor:
    for row in cursor:
        valor_impacto2 = row[0]
        print "La media del impacto 2 es: " + str(valor_impacto2)


with arcpy.da.SearchCursor(Table_MediaImpacto3, "MEAN") as cursor:
    for row in cursor:
        valor_impacto3 = row[0]
        print "La media del impacto 3 es: " + str(valor_impacto1)


# 5. Se comprueba cual de los tres valores de impacto es mayor:

FC_Proyectos = arcpy.GetParameterAsText(5)                                                     ##PARAMETRO: clase de entidad de salida en la que se copia el poligono de la alternativa seleccionada
outRaster_Imapcto = arcpy.GetParameterAsText(6)                        ## PARAMETRO: raster de salida de impacto ambiental en el area de influencia de la alternativa seleccionada
outFC_AInfluencia = arcpy.GetParameterAsText(7)                                            ##PARAMETRO: clase de entidad de salida en la que se copia el poligono del area de influencia de la alternativa seleccionada

if valor_impacto1 < valor_impacto2:
    if valor_impacto1 < valor_impacto3:
        print "La Alternativa 1 causaria un impacto ambiental medio menor que las otras dos alternativas"
        # Se copia el poligono que representa la alternativa 1 en la clase de
        # entidad Proyectos, y se hace los mismo con su area de influencia en la
        # feature class AreasInfluencia
        arcpy.CopyFeatures_management(FL_Alternativa1, FC_Proyectos)
        arcpy.CopyFeatures_management(AI_Aternativa1, outFC_AInfluencia)


        # Se extrae un rater (Extract by mask) que represente el impacto
        # ambiental en la zona comprendida por la alternativa 1 y su area de
        # influencia:
        arcpy.CheckOutExtension("Spatial")
        outExtractByMask = ExtractByMask(Raster_ImpactoAmbiental, AI_Aternativa1)
        arcpy.CheckInExtension ("Spatial")
        outExtractByMask.save(outRaster_Imapcto)



    else:
        print "La Alternativa 3 causaria un impacto ambiental medio menor que las otras dos alternativas"
        # Se copia el poligono que representa la alternativa 3 en la clase de
        # entidad proyectos, y se hace los mismo con su area de influencia en la
        # feature class AreasInfluencia
        arcpy.CopyFeatures_management(FL_Alternativa3, FC_Proyectos)
        arcpy.CopyFeatures_management(AI_Aternativa3, outFC_AInfluencia)

        # Se extrae un rater (Extract by mask) que represente el impacto
        # ambiental en la zona comprendida por la alternativa 3 y su area de
        # influencia:
        arcpy.CheckOutExtension("Spatial")
        outExtractByMask = ExtractByMask(Raster_ImpactoAmbiental, AI_Aternativa3)
        arcpy.CheckInExtension ("Spatial")
        outExtractByMask.save(outRaster_Imapcto)

else:
    if valor_impacto2 < valor_impacto3:
        print "La Alternativa 2 causaria un impacto ambiental medio menor que las otras dos alternativas"
        # Se copia el poligono que representa la alternativa 2 en la clase de
        # entidad proyectos, y se hace los mismo con su area de influencia en la
        # feature class AreasInfluencia:
        arcpy.CopyFeatures_management(FL_Alternativa2, FC_Proyectos)
        arcpy.CopyFeatures_management(AI_Aternativa2, outFC_AInfluencia)

        # Se extrae un rater (Extract by mask) que represente el impacto
        # ambiental en la zona comprendida por la alternativa 1 y su area de
        # influencia:
        arcpy.CheckOutExtension("Spatial")
        outExtractByMask = ExtractByMask(Raster_ImpactoAmbiental, AI_Aternativa2)
        arcpy.CheckInExtension ("Spatial")
        outExtractByMask.save(outRaster_Imapcto)

    else:
        print "La Alternativa 3 causaria un impacto ambiental medio menor que las otras dos alternativas"
        # Se copia el poligono que representa la alternativa 1 en la clase de
        # entidad proyectos, y se hace los mismo con su area de influencia en la
        # feature class AreasInfluencia:
        arcpy.CopyFeatures_management(FL_Alternativa3, FC_Proyectos)
        arcpy.CopyFeatures_management(AI_Aternativa3, outFC_AInfluencia)

        # Se extrae un rater (Extract by mask) que represente el impacto
        # ambiental en la zona comprendida por la alternativa 1 y su area de
        # influencia:
        arcpy.CheckOutExtension("Spatial")
        outExtractByMask = ExtractByMask(Raster_ImpactoAmbiental, AI_Aternativa3)
        arcpy.CheckInExtension ("Spatial")
        outExtractByMask.save(outRaster_Imapcto)

# Se eliminan las tablas, capas y clases de entidad intermedias que se han creado
# durante el geoprocesamiento y que no se van a necesitar, con la intencion
# de no ocupar demasiado espacio en la geodatabase:
arcpy.Delete_management(FL_Alternativa1)
arcpy.Delete_management(FL_Alternativa2)
arcpy.Delete_management(FL_Alternativa3)
arcpy.Delete_management(AI_Aternativa1)
arcpy.Delete_management(AI_Aternativa2)
arcpy.Delete_management(AI_Aternativa3)
arcpy.Delete_management(Table_MediaImpacto1)
arcpy.Delete_management(Table_MediaImpacto2)
arcpy.Delete_management(Table_MediaImpacto3)