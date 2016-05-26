
def GetEmptyObject(name):
    return type(str(name), (object,), {}) 


def Item_to_dict(row):
    d = dict()
    d['Name'] = row[0]
    d['id'] = row[1]
    d['lat'] = row[2]
    d['lng'] = row[3]
    d['distance'] = row[4]
    return d
