import processing
#import variables
filepath = "D:\\Uni\\2021Semester2\\Geospatial_Programming\\s3542758_SourceData\\"
firehistory = "FIRE_HISTORY.shp"
heathlands = "Heathlands.shp"
siteborder = "siteborder.shp"

#import fire history, site border, and heathlands
fhistoryLayer = iface.addVectorLayer(filepath + firehistory, firehistory[:-4], "ogr")
heathLayer = iface.addVectorLayer(filepath + heathlands, heathlands[:-4], "ogr")
siteborder = iface.addVectorLayer(filepath + siteborder, siteborder[:-4], "ogr")
#define fireborder clip dictionary
fireborderDict = {'INPUT':fhistoryLayer, 'OVERLAY':siteborder, 'OUTPUT':filepath + 'fireborder.shp'}
#clip firehistory layer to site border
fireborderClip = processing.run("native:clip", fireborderDict)
fireborderLayer = iface.addVectorLayer(filepath + 'fireborder.shp', "", "ogr")
#define heathland clip
heathlandDict = {'INPUT':heathLayer, 'OVERLAY':siteborder, 'OUTPUT':filepath + 'heathborder.shp'}
#clip heathland clip dictionary
heathClip = processing.run("native:clip", heathlandDict)
heathLayer = iface.addVectorLayer(filepath + 'heathborder.shp', "", "ogr")

#initiate editing for clipped fire history layer
fireborderLayer.startEditing()
fireborderLayer.addAttribute(QgsField('GPSUIT', QVariant.String))
#assign 'GPSUIT' (ground parrot suitability) attribute with string as data type
fireborderLayer.updateFields()
fireborderLayer.commitChanges()
#solidify edits

#define year list, latest date and earliest date variables for use in loop
yearList = [2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005, 2004, 2003, 2002, 2001, 2000, 1999, 1998, 1997, 1996, 1995, 1994, 1993, 1992, 1991]
latestDate = yearList[0]
earliestDate = yearList[-1]

#create loop to perform tasks related to creation of latest fire layers
#the loop functions as follows:
# (i) represents a year from yearList[], from 2021-1991.
# the loop starts by extracting a layer using the most recent date if (i) == 'latestDate' or 2021.
# this layer is called total(i).shp or total2021.shp.
# then after the latest date has passed: if (i) < 'latestDate' (or (i) < 2021), the loop creates a new extract using the next (i) in the list: 2020.
# This file is called (i).shp or 2020.shp
# The loop then performs the difference between total(i+1).shp and (i).shp, which would be the difference between 2021 and 2020 - giving a cropped 2020 which doesnt overlap with 2021 fires.
# The output of this cropped 2021 is then named (i)new.shp or 2020new.shp.
# Then a merge is performed on (i)new.shp and total(i+1).shp - making a merge of 2021 and cropped 2020 - which represents the latest fire layer as of 2021 with dates ranging back to 2020 or (i).
# This is named total(i).shp or total2020.
# Now (i) is 2019, so the loop first extracts 2019.shp, the loop then differences 2019.shp and total(i+1).shp. As (i) is 2019, the new total(i+1).shp is total2020.shp.
# total2020.shp is the output of the previously merged 2020 and 2021 latest fire layer - so 2019 is now being differenced with the latest fire layer of 2021+2020.
# This means with each iteration of (i) the shapefile of that year (i) is differenced with the latest fire layer of all the previous years and merged in with it to create the new output.
# When the loop reaches 1991, the last output is created, known as total1991.shp - this is the latest fire layer with years 2021-1991.
for i in yearList:
    if i == latestDate:
        TotalDict = {'INPUT':fireborderLayer, 'FIELD':'SEASON', 'OPERATOR':0, 'VALUE':i, 'OUTPUT':filepath + "total" + str(i) + ".shp"}
        TotalProcess = processing.run("native:extractbyattribute", TotalDict)
    elif i < latestDate:
        NewDict = {'INPUT':fireborderLayer, 'FIELD':'SEASON', 'OPERATOR':0, 'VALUE':str(i), 'OUTPUT':filepath + str(i) + ".shp"}
        NewProcess = processing.run("native:extractbyattribute", NewDict)
        diffDict = {'INPUT':filepath + str(i) + ".shp", 'OVERLAY':filepath + "total" + str(i+1) + ".shp", 'OUTPUT':filepath + str(i) + "new.shp"}
        processing.run("native:difference", diffDict)
        mergeDict = {'LAYERS':[filepath + str(i) + "new.shp", filepath + "total" + str(i+1) + ".shp"], 'CRS':fireborderLayer, 'OUTPUT':filepath + "total" + str(i) + ".shp"}
        processing.run("native:mergevectorlayers", mergeDict)
latestfireLayer = iface.addVectorLayer(filepath + "total" + str(earliestDate) + ".shp","LatestFire", "ogr")
#The total1991.shp latest fire layer is then extracted and renamed LatestFire
#As 1991 is equivalent to the earliestDate variable created before the loop, the output can be extracted using filepath + str(earliestDate) + ".shp" - no need to know 1991 is the last date.

#create loop to iterate through new LatestFire layer and assign suitability values based on fire age
zones = latestfireLayer.getFeatures()
for zone in zones:
    fireage = latestDate - zone['SEASON']
    if fireage <6:
        suitClass = 'Unsuitable'
        #as optimal fire age is between 5 and 15
    elif fireage <16:
        suitClass = 'Suitable'
    else:
        suitClass = 'Unsuitable'
    latestfireLayer.startEditing()
    #initiade editing inside the loop
    zone['GPSUIT'] = suitClass
    latestfireLayer.updateFeature(zone)
    #solidify edits
    latestfireLayer.commitChanges()

#union the cropped heathland layer with the new suitability enabled LatestFire layer to combine attributes
unionDict = {'INPUT':latestfireLayer, 'OVERLAY':heathLayer,'OVERLAY_FIELDS_PREFIX':"1",'OUTPUT':filepath + "fireAgeHeath.shp"}
processing.run("native:union", unionDict)

#clip the new layer to remove the polygons of bushfire which do not overlap with heathland
clipmaskDict = {'INPUT':filepath + "fireAgeHeath.shp", 'MASK':heathLayer, 'OPTIONS':'', 'OUTPUT':filepath + "FAclipped.shp"}
processing.run("gdal:clipvectorbypolygon", clipmaskDict)

#remerge heathland layer as those without fire in the last 30 years but still are within heathland would be removed from eariler processes.
hfmergeDict = {'LAYERS':[filepath + "FAclipped.shp", filepath + "heathborder.shp"], 'CRS':fireborderLayer, 'OUTPUT':filepath + "heathfirecomplete.shp"}
processing.run("native:mergevectorlayers", hfmergeDict)
hfc = iface.addVectorLayer(filepath + "heathfirecomplete.shp","","ogr")
#this heathfirecomplete layer represents the final output of the suitability analysis 

#define layer list to be used in loop
layerList = ['heathborder', 'LatestFire total1991', 'fireborder', 'siteborder', 'Heathlands', 'FIRE_HISTORY', 'heathfirecomplete']
prj = QgsProject.instance()
#create loop to iterate through layer list and turn off visibility if not the desired heathfirecomplete layer
#does not provide and analytical function - purely for user convenience
for name in layerList:
    layer = prj.mapLayersByName(name)[0]
    if name != 'heathfirecomplete':
        prj.layerTreeRoot().findLayer(layer.id()).setItemVisibilityCheckedParentRecursive(False)
    else:
        prj.layerTreeRoot().findLayer(layer.id()).setItemVisibilityCheckedParentRecursive(True)
