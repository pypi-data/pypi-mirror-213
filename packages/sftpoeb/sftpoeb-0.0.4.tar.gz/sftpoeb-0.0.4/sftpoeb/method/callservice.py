from requests_toolbelt.multipart.encoder import MultipartEncoder
from config.variable import *
import os,requests,time,urllib3
urllib3.disable_warnings()

def serviceSigning(data, fileNameText, fileNamePDF, pathFile,round,serviceCode):
    multipart_data = MultipartEncoder(
        fields={
            "SellerTaxId": data['SellerTaxid'],
            "SellerBranchId": data['SellerBranchId'],
            "APIKey": data['APIKey'],
            "UserCode": data['UserCode'],
            "AccessKey": data['AccessKey'],
            "ServiceCode": serviceCode,
            "TextContent": (fileNameText, open(os.path.abspath(os.path.join(pathFile + '/' + fileNameText)), 'rb'), "multipart/form-data"),
            "PDFContent": (fileNamePDF, open(os.path.abspath(os.path.join(pathFile + '/' + fileNamePDF)), 'rb'), "multipart/form-data"),
            "SendMail": "YES"
            # "PdfTemplateId":PdfTemplateId
        }
    )
    headers = {
        'Content-Type': multipart_data.content_type,
        'Authorization': data['Authorization']
    }
    try:
        response = requests.post(SERVICE_SIGNING_URL, data=multipart_data, headers=headers, verify=False)
        if response.status_code == 200:
            result = response.json()
        else:
            if round < 3:
                time.sleep(0.5)
                result = serviceSigning(data, fileNameText, fileNamePDF, pathFile,round+1,serviceCode)
            else:
                result = {
                    "status": "ER",
                    "errorMessage": "Service Stamp was problem.",
                    "errorCode": response.status_code
                }
    except Exception as e:
        if round < 3:
            time.sleep(0.5)
            result = serviceSigning(data, fileNameText, fileNamePDF, pathFile,round+1,serviceCode)
        else:
            result = {
                "status": "ER",
                "errorCode": "EXC001",
                "errorMessage": "send_for_getfile : " + str(e)
            }
    return result
    
def checkStatus(data,TransactionCode,round):
    multipart_data = MultipartEncoder(
        fields={
            "SellerTaxId":data['SellerTaxid'],
            "SellerBranchId": data['SellerBranchId'],
            "APIKey": data['APIKey'],
            "UserCode": data['UserCode'],
            "AccessKey": data['AccessKey'],
            "TransactionCode": TransactionCode,
            "ServiceCode": "S06"
        }
    )
    headers = {
        'Content-Type': multipart_data.content_type,
        'Authorization': data['Authorization']
    }
    try:
        response = requests.post(SERVICE_CHECKSTATUS_URL, data=multipart_data, headers=headers, verify=True)
        if response.status_code == 200:
            result = response.json()
            print(result)
            if result['status'] == "OK":
                return result
            elif round == 20:
                result = {
                    "status": "PR",
                    "errorMessage": "Service Check transaction 20 rounds",
                    "errorCode": "ERPC002"
                }
                return result
            elif result['status'] == "PC":
                time.sleep(0.5 + (round / 2))
                result = checkStatus(data,TransactionCode,round+1)
            else:
                print("Service Stamp [PC] failed.")
                return result
        else:
            res = response.json()
            print(res)
            result = {
                "status": "PR",
                "errorMessage": "Service Check transaction was Problem",
                "errorCode": "ERPC001"
            }
    except Exception as e:
        result = {
            "status": "PR",
            "errorMessage": "Service Check transaction error.  : " + str(e),
            "errorCode": "EXPC001"
        }
    return result
    
def saveFile(file,path,nameSave,rounds):
    try:
        headers = {
            'Content-Type': "text/xml; charset=utf-8",
            'Cache-Control': "no-cache",
        }
        response = requests.get(url=file, headers=headers, verify=True,allow_redirects=True)
        # current_app.logger.info(response.content)
        # print(eval(response.headers['Content-Disposition'].split("=")[1]))
        file = open(path + nameSave, "wb")
        file.write(response.content)
        file.close()
        r = {
            "status":"OK",
            "message":"Save file success."
        }
    except Exception as e:
        if rounds <= 5 :
            time.sleep(0.5)
            r = saveFile(file,path,nameSave,(rounds+1))
        else:
            r = {
                "status":"ER",
                "errorMessage": str(e),
                "errorCode":"ER999"
            }
    return r