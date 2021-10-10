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
currentYearLayer = iface.addVectorLayer(filepath + str(currentYear) + ".shp", str(currentYear), "ogr")

yearList3 = [2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005, 2004, 2003, 2002, 2001, 2000, 1999, 1998, 1997, 1996, 1995, 1994, 1993, 1992, 1991]
#yearList = ['2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', '2009', '2008', '2007', '2006', '2005', '2004', '2003', '2002', '2001', '2000', '1999', '1998', '1997', '1996', '1995', '1994', '1993', '199'2, '1991']
zones = fireborderLayer
for zone in zones:
    
for year1 in yearList3:
loopYear = year1
loopDict = {'INPUT':fireborderLayer, 'FIELD':'SEASON', 'OPERATOR':0, 'VALUE':str(loopYear), 'OUTPUT':filepath + str(loopYear) + ".shp"}
loopProcess = processing.run("native:extractbyattribute", loopDict)
print(loopYear)