import requests
import json
def sendit(data):
    url = "https://hooks.airtable.com/workflows/v1/genericWebhook/appyXNoDQSrFR8sIS/wfl8yyvj4U7k9RlME/wtrSYdGh47sPP8Fnu"
    jsonPayload = json.dumps(data)
    x = requests.post(url,dict)
    print(x)
    
dict = {"manufacturer": "Kameron", 
        "lotCode": "1021000", 
        "productionDate": "2023-04-24", 
        "material": "Polyamide 11 - PA11", 
        "componentType": ["coupling", "Mechanical interference fit"], 
        "componentSize": ["3/4 IPS  DR 11 0.095 (2.41)", "3/4 IPS  DR 11 0.095 (2.41)"], 
        "barcode": "RW4hkameron"}    
sendit(dict)
