import shapefile
import os
def shape_publish(file_name):
    output_shapefile = "/home/bisag/Documents/1DEM/polygon1.shp"

    r = shapefile.Reader(file_name)

    outlist = []

    for shaperec in r.iterShapeRecords():
        outlist.append(shaperec)
    shapeType =  r.shapeType
    rFields = list(r.fields)
    r = None
    ##to be sure we delete the existing shapefile
    if os.path.exists(file_name):
        pass
        # os.remove(file_name)
    else:
        print("file does not exist"+ file_name)

    ##to be sure we delete the existing dbf file
    dbf_file = file_name.replace(".shp",".dbf")
    if os.path.exists(dbf_file):
        pass
        # os.remove(dbf_file)
    else:
        print("file does not exist" + dbf_file)
    ##to be sure we delete the existing shx file
    shx_file = file_name.replace(".shp", ".shx")
    if os.path.exists(shx_file):
        pass
        # os.remove(shx_file)
    else:
        print("file does not exist" + shx_file)

    w = shapefile.Writer(output_shapefile,shapeType)

    w.fields = rFields
    #print(outlist)
    for shaperec in outlist:
        record = shaperec.record[0]
        if record == 1:
            print(record)
            w.record(record)
            w.shape(shaperec.shape)
        # print(shaperec)
    w.close()

    from json import dumps

    # read the shapefile
    reader = shapefile.Reader(output_shapefile)
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    buffer = []
    for sr in reader.shapeRecords():
        atr = dict(zip(field_names, sr.record))
        geom = sr.shape.__geo_interface__
        buffer.append(dict(type="Feature", geometry=geom, properties=atr)) 
    

    return dumps({"type": "FeatureCollection", "features": buffer}, indent=2)

if __name__ == '__main__':
    ret_val = shape_publish("/home/bisag/Documents/1DEM/polygon.shp")
    print(ret_val)
