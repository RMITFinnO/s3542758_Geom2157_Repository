import processing
#import variables
filepath = "D:\\Uni\\2021Semester2\\Geospatial_Programming\\Final_Project_Dataset\\Order_CJPSZB\\mga2020_55\\esrishape\\vicgov_region\\GIPPSLAND-0\\FIRE\\"
firehistory = "FIRE_HISTORY.shp"
siteborder = "siteborder.shp"

#import fire history and site border
fhistoryLayer = iface.addVectorLayer(filepath + firehistory, firehistory[:-4], "ogr")
siteborder = iface.addVectorLayer(filepath + siteborder, siteborder[:-4], "ogr")
#define fireborder clip dictionary
fireborderDict = {'INPUT':fhistoryLayer, 'OVERLAY':siteborder, 'OUTPUT':filepath + 'fireborder.shp'}
#clip firehistory layer to site border
fireborderClip = processing.run("native:clip", fireborderDict)
fireborderLayer = iface.addVectorLayer(filepath + 'fireborder.shp', "", "ogr")

fireborderLayer.startEditing()
fireborderLayer.addAttribute(QgsField('SUITABILITY', QVariant.String))
fireborderLayer.updateFields()
fireborderLayer.commitChanges()

currentYear = 2021
extractDict = {'INPUT':fireborderLayer, 'FIELD':'SEASON', 'OPERATOR':0, 'VALUE':str(currentYear), 'OUTPUT':filepath + str(currentYear) + ".shp"}
Testprocess = processing.run("native:extractbyattribute", extractDict)
CurrentYearLayer = iface.addVectorLayer(filepath + str(currentYear) + ".shp", str(currentYear), "ogr")