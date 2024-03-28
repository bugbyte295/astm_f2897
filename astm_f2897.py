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
        
    # print(tempBc.manufacturer)
    # print(tempBc.lotCode)
    # print(tempBc.productionDate)
    # print(tempBc.material)
    # print(tempBc.componentType)
    # print(tempBc.componentSize)
    # print(tempBc.checkDigit)
    # print(tempBc.barcode)
    
    
bark = 'RW6FDa7d8K8S1Yz0'
setBC(bark)

