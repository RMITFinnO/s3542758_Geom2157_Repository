import processing
#import variables
filepath = "D://Uni//2021Semester2//Geospatial_Programming//Final_Project_Dataset//Order_CJPSZB//mga2020_55//esrishape//vicgov_region//GIPPSLAND-0//FIRE//"
firehistory = "FIRE_HISTORY.shp"
heathlands = "Heathlands.shp"
siteborder = "siteborder.shp"

#import fire history and site border and heathlands
fhistoryLayer = iface.addVectorLayer(filepath + firehistory, firehistory[:-4], "ogr")
heathLayer = iface.addVectorLayer(filepath + heathlands, heathlands[:-4], "ogr")
siteborder = iface.addVectorLayer(filepath + siteborder, siteborder[:-4], "ogr")
#define fireborder clip dictionary
fireborderDict = {'INPUT':fhistoryLayer, 'OVERLAY':siteborder, 'OUTPUT':filepath + 'fireborder.shp'}
#clip firehistory layer to site border
fireborderClip = processing.run("native:clip", fireborderDict)
fireborderLayer = iface.addVectorLayer(filepath + 'fireborder.shp', "", "ogr")
#heathland clip
heathlandDict = {'INPUT':heathLayer, 'OVERLAY':siteborder, 'OUTPUT':filepath + 'heathborder.shp'}
#clip heathland clip dictionary
heathClip = processing.run("native:clip", heathlandDict)
heathLayer = iface.addVectorLayer(filepath + 'heathborder.shp', "", "ogr")

fireborderLayer.startEditing()
fireborderLayer.addAttribute(QgsField('GPSUIT', QVariant.String))
fireborderLayer.updateFields()
fireborderLayer.commitChanges()

yearList = [2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005, 2004, 2003, 2002, 2001, 2000, 1999, 1998, 1997, 1996, 1995, 1994, 1993, 1992, 1991]
latestDate = yearList[0]
earliestDate = yearList[-1]

for i in yearList:
    if i == latestDate:
        TotalDict = {'INPUT':fireborderLayer, 'FIELD':'SEASON', 'OPERATOR':0, 'VALUE':i, 'OUTPUT':filepath + "total" + str(i) + ".shp"}
        TotalProcess = processing.run("native:extractbyattribute", TotalDict)
        #TotalLayer = iface.addVectorLayer(filepath + "total" + str(i) + ".shp","", "ogr")
    elif i < latestDate:
        NewDict = {'INPUT':fireborderLayer, 'FIELD':'SEASON', 'OPERATOR':0, 'VALUE':str(i), 'OUTPUT':filepath + str(i) + ".shp"}
        NewProcess = processing.run("native:extractbyattribute", NewDict)
        diffDict = {'INPUT':filepath + str(i) + ".shp", 'OVERLAY':filepath + "total" + str(i+1) + ".shp", 'OUTPUT':filepath + str(i) + "new.shp"}
        processing.run("native:difference", diffDict)
        #unionDict = {'INPUT':filepath + str(i) + "new.shp" , 'OVERLAY':filepath + "total" + str(i+1) + ".shp" ,'OVERLAY_FIELDS_PREFIX':"1",'OUTPUT':filepath + "total" + str(i) + ".shp"}
        #processing.run("native:union", unionDict)
        mergeDict = {'LAYERS':[filepath + str(i) + "new.shp", filepath + "total" + str(i+1) + ".shp"], 'CRS':fireborderLayer, 'OUTPUT':filepath + "total" + str(i) + ".shp"}
        processing.run("native:mergevectorlayers", mergeDict)
latestfireLayer = iface.addVectorLayer(filepath + "total" + str(earliestDate) + ".shp","LatestFire", "ogr")
    
zones = latestfireLayer.getFeatures()
for zone in zones:
    fireage = latestDate - zone['SEASON']
    if fireage <6:
        suitClass = 'Unsuitable'
    elif fireage <19:
        suitClass = 'Suitable'
    else:
        suitClass = 'Unsuitable'
    latestfireLayer.startEditing()
    zone['GPSUIT'] = suitClass
    latestfireLayer.updateFeature(zone)
    #print(zone['SEASON'], zone['SUITABILITY'])
    latestfireLayer.commitChanges()

unionDict = {'INPUT':latestfireLayer, 'OVERLAY':heathLayer,'OVERLAY_FIELDS_PREFIX':"1",'OUTPUT':filepath + "fireAgeHeath.shp"}
processing.run("native:union", unionDict)

clipmaskDict = {'INPUT':filepath + "fireAgeHeath.shp", 'MASK':heathLayer, 'OPTIONS':'', 'OUTPUT':filepath + "FAclipped.shp"}
processing.run("gdal:clipvectorbypolygon", clipmaskDict)

hfmergeDict = {'LAYERS':[filepath + "FAclipped.shp", filepath + "heathborder.shp"], 'CRS':fireborderLayer, 'OUTPUT':filepath + "heathfirecomplete.shp"}
processing.run("native:mergevectorlayers", hfmergeDict)
hfc = iface.addVectorLayer(filepath + "heathfirecomplete.shp","","ogr")

layerList = [layer.name() for layer in QgsMapLayerRegistry.instance().mapLayers().values()]
prj = QgsProject.instance()
for name in layerList:
    layer = prj.mapLayersByName(name)[0]
    if name != 'heathfirecomplete':
        prj.layerTreeRoot().findLayer(layer.id()).setItemVisibilityCheckedParentRecursive(False)
    else:
        prj.layerTreeRoot().findLayer(layer.id()).setItemVisibilityCheckedParentRecursive(True)
