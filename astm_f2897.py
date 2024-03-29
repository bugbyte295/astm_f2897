#@bugbyte295
#made for decoding astm f2897 codes
#base 62 0=0, a=10, A=36, Z=61
#json imports data from ASTM 
# dimension holds dicts containing cid, size, units, and description. 
#material contains a dict with codes = material
#componentType holds dict of dicts of component data
#list of dicts in componentType
#pipe, coupling, adapterCoupling, endCap, elbow, 3-wayTee, reducer, tappingTee, highVolumeTappingTee
#cont.. branchSaddle, mechanicalSaddle,serviceTee, serviceSaddle, flange, transitionFitting, riser
#cont... valve, excessFlowValve, meterSetAssembly, regulator, filter, anode, pressureControlFitting
#cont... union, repairClamp
#manufacturer holds information about them
import base62
import datetime
import json

class BC:
    def __init__(self):
        self.manufacturer = 'null'
        self.lotCode = None
        self.productionDate = None
        self.material = None
        self.componentType = None
        self.componentSize = None
        self.checkDigit = None
        self.barcode = None

    def parseBarcode(self):
        self.setManufacturer(self.barcode[:2])
        self.lotCode = self.barcode[2:6] #7 digit base 10, 4 digit base 62
        self.productionDate = self.barcode[6:9] #5 digit base 10, 3 digit base 62. ex 12312 = 123rd day of 2012
        self.material = self.barcode[9]
        self.componentType = self.barcode [10:12]
        self.componentSize = self.barcode[12:15] #5 digit base 10, 3 digit base 62
        self.checkDigit = self.barcode[15] 
    
    def getManufacturer(self):
        return self.manufacturer

    def setManufacturer(self, value):
        self.manufacturer = value

    def getLotCode(self):
        return self.lotCode

    def setLotCode(self, value):
        self.lotCode = value

    def getProductionDate(self):
        return self.productionDate

    def setProductionDate(self, value):
        self.productionDate = value

    def getMaterial(self):
        return self.material

    def setMaterial(self, value):
        self.material = value

    def getComponentType(self):
        return self.componentType

    def setComponentType(self, value):
        self.componentType = value

    def getComponentSize(self):
        return self.componentSize

    def setComponentSize(self, value):
        self.componentSize = value

    def getCheckDigit(self):
        return self.checkDigit

    def setCheckDigit(self, value):
        self.checkDigit = value

    def getBarcode(self):
        return self.barcode

    def setBarcode(self, value):
        self.barcode = value
    
    def convertSize(self, value): # value is base 10
        for x in range(360):
            for y in range(360):
                num = (y*378) + x + 1
                if num == int(value):
                    return (x,y)
    def convertDate(self):
        dayOfYear = int(self.productionDate[0:3])
        year = 2000 + int(self.productionDate[3:])
        iso_date = datetime.datetime(year, 1, 1) + datetime.timedelta(days=dayOfYear - 1)
        return(iso_date.isoformat()[0:10])



def setBC(string):
    tempBc = BC()
    tempBc.setBarcode(string)
    tempBc.parseBarcode()
    tempBc.setLotCode(base62.decode(str(tempBc.lotCode)))
    tempBc.setProductionDate(str(base62.decode(str(tempBc.productionDate))))
    tempBc.setComponentSize(tempBc.convertSize(base62.decode(str(tempBc.componentSize))))
    tempBc.setProductionDate(tempBc.convertDate())
    return tempBc

def retrieve_nested_value(mapping, key_of_interest):
    hold = mapping
    mappings = [mapping]
    while mappings:
        mapping = mappings.pop()
        try:
            items = mapping.items()
        except AttributeError:
            # we didn't store a mapping earlier on so just skip that value
            continue

        for key, value in items:
            if key == key_of_interest:
                return (list(hold.keys())[list(hold.values()).index(mapping)], value)
            else:
                # type of the value will be checked in the next loop
                mappings.append(value)
    
def getData(obj):
    f = open('data.json','r')
    data = json.load(f)
    dim = data['dimension']
    mat = data['material']
    comp = data['componentType']
    man = data['manufacturers']
    sizes = obj.componentSize
    c1 = str(sizes[0])
    c2 = str(sizes[1])
    obj.setManufacturer(man[obj.manufacturer])
    obj.setMaterial(mat[obj.material])
    obj.setComponentSize((dim[c1],dim[c2]))
    k = obj.componentType
    obj.setComponentType(retrieve_nested_value(comp,k))
    dict = {
    "manufacturer": obj.manufacturer,
    "lotCode": obj.lotCode,
    "productionDate": obj.productionDate,
    "material": obj.material,
    "componentType": obj.componentType,
    "componentSize": obj.componentSize,
    "barcode": obj.barcode
}
    return dict
    
def main(string):
    return getData(setBC(string))

print(main('PE4q8W8DRB121Yh0'))
