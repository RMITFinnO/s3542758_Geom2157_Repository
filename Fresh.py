import processing
#import variables
filepath = "H:\\s3542758_FinalProject\\FinalProject_SourceData\\"
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

#currentYear = 2021
#extractDict = {'INPUT':fireborderLayer, 'FIELD':'SEASON', 'OPERATOR':0, 'VALUE':str(currentYear), 'OUTPUT':filepath + str(currentYear) + ".shp"}
#Testprocess = processing.run("native:extractbyattribute", extractDict)
#currentYearLayer = iface.addVectorLayer(filepath + str(currentYear) + ".shp", str(currentYear), "ogr")

yearList3 = [2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005, 2004, 2003, 2002, 2001, 2000, 1999, 1998, 1997, 1996, 1995, 1994, 1993, 1992, 1991]
 
#for i in yearList3:
    #if i = 2021:
        #pass
   # elif i <2021:
        #loopDict = {'INPUT':fireborderLayer, 'FIELD':'SEASON', 'OPERATOR':0, 'VALUE':str(i), 'OUTPUT':filepath + str(i) + ".shp"}
        #loopProcess = processing.run("native:extractbyattribute", loopDict)
        #loopAddLayer = iface.addVectorLayer(filepath + str(i) + ".shp", "", "ogr")

#look into splitvectorlayer 
#total = 2021 layer
for i in yearlist3:
    if i = 2021:
        TotalDict = {'INPUT':fireborderLayer, 'FIELD':'SEASON', 'OPERATOR':0, 'VALUE':str(i), 'OUTPUT':filepath + "total.shp"}
        TotalProcess = processing.run("native:extractbyattribute", TotalDict)
    elif i <2021:
        NewDict = {'INPUT':fireborderLayer, 'FIELD':'SEASON', 'OPERATOR':0, 'VALUE':str(i), 'OUTPUT':filepath + str(i) + ".shp"}
        NewProcess = processing.run("native:extractbyattribute", NewDict)
        diffDict = {'INPUT':filepath + str(i) + ".shp", 'OVERLAY':filepath + "total.shp", 'OUTPUT':filepath + "new.shp"}
        processing.run("native:difference", diffDict)
        mergeList = [filepath + "new.shp",filepath + "total.shp"]
        mergeDict = {'INPUT':mergeList, 'CRS':fireborderLayer, 'OUTPUT': filepath + "total.shp"}
LatestFireLayer = iface.addVectorLayer(filepath + "total.shp", "", "ogr")
    
    