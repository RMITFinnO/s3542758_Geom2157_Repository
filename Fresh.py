filepath = "D:\\Uni\\2021Semester2\\Geospatial_Programming\\Final_Project_Dataset\\Order_CJPSZB\\mga2020_55\\esrishape\\vicgov_region\\GIPPSLAND-0\\FIRE\\"
firehistory = "FIRE_HISTORY.shp"
siteborder = "siteborder.shp"

fhistoryLayer = iface.addVectorLayer(filepath + firehistory, firehistory[:-4], "ogr")
siteborder = iface.addVectorLayer(filepath + siteborder, siteborder[:-4], "ogr")
fireborderDict = {'INPUT':fhistoryLayer, 'OVERLAY':siteborder, 'OUTPUT':filepath + 'fireborder.shp'}

fireborderClip = processing.run("native:clip", fireborderDict)
fireborderLayer = iface.addVectorLayer(filepath + 'fireborder.shp', "fireborderLayer", "ogr")