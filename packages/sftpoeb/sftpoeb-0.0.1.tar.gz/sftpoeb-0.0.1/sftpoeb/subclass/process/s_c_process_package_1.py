from method.callservice import *
from method.debug import *
from os import listdir
from os.path import isfile, join, isdir
import threading
import shutil,json
class packageprocess():
    def __init__(self,local,destination,recovery,payloadData,dateNow,timeNow):
        self.local = local
        self.destination = destination
        self.payloadData = payloadData
        self.recovery = recovery
        self.dateNow = dateNow
        self.timeNow = timeNow

        self.countInvoice = 0
        self.success = 0  ####จำนวนที่สำเร็จใน
        self.fail = 0  ####จำนวนที่ไม่สำเร็จใน
        self.losemessage = []  ####ข้อความทีไม่่สำเร็จใน
        self.recover_count = 0
        self.recover = []

        ### เก็บข้อมูลการทำงานรอบ recover
        self.success_recovery_message = []
        self.success_recovery = 0
        self.fail_recovery_message = []
        self.fail_recovery = 0

    def process(self,dataProcess):
        for filename in dataProcess:
            name = str(filename).split('.')[0]
            try:
                serviceCode = 'S06'
                shutil.move(self.destination.getDestinationPathPDF() + name + '.pdf', self.local.getLocalPathNow() + name + '.pdf')  #### วนหยิบ PDF ตามชื่อ text ที่แตกดป็น 1:1 แล้ว
                service = serviceSigning(self.payloadData, filename, name + '.pdf', self.local.getLocalPathNow() , 0, serviceCode)
                if service['status'] == 'OK':
                    self.success = self.success + 1
                    print(str(self.dateNow + self.timeNow) + '>> ' + str(name) + ' Service signing success.')
                    save_pdf = saveFile(service['pdfURL'], self.local.getLocalOutputPdfPath(), name + '.pdf', 0)
                    if save_pdf['status'] == 'OK':
                        print(str(self.dateNow + self.timeNow) + '>> ' + str(name) + ' Save file.pdf success.')
                        shutil.copy(self.local.getLocalOutputPdfPath() + name + '.pdf', self.destination.getDestinationOutputPdfPath() + name + '.pdf')
                        print(str(self.dateNow + self.timeNow) + '>> ' + str(name) + ' Put file.pdf success.')
                        pdf_result = 'OK'  ### เก็บ สถานะการทำงานในส่วน PDF
                    else:
                        print(str(self.dateNow + self.timeNow) + '>> ' + str(name) + ' Save file.pdf failed. : ' + str(save_pdf['errorMessage']))
                        pdf_result = 'ER'  ### เก็บ สถานะการทำงานในส่วน PDF
                    save_xml = saveFile(service['xmlURL'],self.local.getLocalOutputXmlPath(), name + '.xml', 0)
                    if save_xml['status'] == 'OK':
                        print(str(self.dateNow + self.timeNow) + '>> ' + str(name) + ' Save file.xml success.')
                        shutil.copy(self.local.getLocalOutputXmlPath() + name + '.xml',self.destination.getDestinationOutputXmlPath() + name + '.xml')
                        print(str(self.dateNow + self.timeNow) + '>> ' + str(name) + ' Put file.xml success.')
                        xml_result = 'OK'  ### เก็บ สถานะการทำงานในส่วน XML
                    else:
                        print(str(self.dateNow + self.timeNow) + '>> ' + str(name) + ' Save file.xml failed. : ' + str(save_xml['errorMessage']))
                        xml_result = 'ER'  ### เก็บ สถานะการทำงานในส่วน XML
                    ##########นับว่า สำเร็จ หรือ ไม่สำเร็จ #######
                    if pdf_result != 'OK' and xml_result != 'OK':  ### ถ้าสถานะของทั้ง xml และ pdf สำเร็จทั้งคู่จึงจะนับว่า invoice นั้นสำเร็จ
                        with open(self.recovery.getRecoverySavePath() + filename, 'w',encoding='UTF-8') as recover_file: ### สร้างไฟล์เพื่อ recover save
                            recover_file.write(json.dumps({"transactionCode": service['transactionCode']}, indent=4, sort_keys=False,ensure_ascii=False))
                    
                    
                    try:  ##### ขั้นตอนไป filerun
                        shutil.move(self.local.getLocalPathNow() + filename, self.local.getLocalCsvArchivePath() + filename)
                    except Exception as e:
                        print(str(self.dateNow + self.timeNow) + '>> ' + str(name) + ' Move CSV input to Archived_File failed : ' + str(e))
                    
                    ### เก็บไว้ส่งในส่วนของการส่งคืนลูกค้า
                    # try:  ##### ขั้นตอนไป filerun
                    #     shutil.copy(self.destination.getDestinationCsvArchivePath() + filename, self.local.getLocalCsvArchivePath() + filename)
                    # except Exception as e:
                    #     print(str(self.dateNow + self.timeNow) + '>> ' + str(name) + ' Copy CSV input to Archived_File failed : ' + str(e))
                    
                    
                    try:  ##### ขั้นตอนไป filerun
                        shutil.move(self.local.getLocalPathNow() + name + '.pdf', self.local.getLocalPdfArchivePath() + name + '.pdf')  #### วาง PDF ที่ error ที่ path filerun error ฝั่งลูกค้า
                    except Exception as e:
                        print(str(self.dateNow + self.timeNow) + '>> ' + str(name) + ' Move PDF input to Archived_File failed : ' + str(e))
                    
                    ### เก็บไว้ส่งในส่วนของการส่งคืนลูกค้า
                    # try:  ##### ขั้นตอนไป filerun
                    #     shutil.copy(self.destination.getDestinationPdfArchivePath() + name + '.pdf', self.local.getLocalPdfArchivePath() + name + '.pdf')  #### วาง PDF ที่ error ที่ path filerun error ฝั่งลูกค้า
                    # except Exception as e:
                    #     print(str(self.dateNow + self.timeNow) + '>> ' + str(name) + ' Copy PDF input to Archived_File failed : ' + str(e))
                
                elif service['status'] == 'PC':
                    print(str(service['transactionCode']))
                    pc_result = checkStatus(self.payloadData, service['transactionCode'], 0)
                    print(pc_result)
                    if pc_result['status'] == 'OK':
                        self.success = self.success + 1
                        print(str(self.dateNow + self.timeNow) + '>> ' + str(name) + ' Service signing success.')
                        save_pdf_pc = saveFile(pc_result['pdfURL'], self.local.getLocalOutputPdfPath(), name + '.pdf', 0)
                        if save_pdf_pc['status'] == 'OK':
                            print(str(self.dateNow + self.timeNow) + '>> ' + str(name) + ' Save file.pdf success.')
                            shutil.copy(self.local.getLocalOutputPdfPath() + name + '.pdf',self.destination.getDestinationOutputPdfPath() + name + '.pdf')
                            print(str(self.dateNow + self.timeNow) + '>> ' + str(name) + ' Put file.pdf success.')
                            pc_pdf_result = 'OK'  ### เก็บสถานะการทำงานในส่วน PDF
                        else:
                            print(str(self.dateNow + self.timeNow) + '>> ' + str(name) + ' Save file.pdf failed. : ' + str(save_pdf_pc['errorMessage']))
                            pc_pdf_result = 'ER'  ### เก็บสถานะการทำงานในส่วน PDF
                        save_xml_pc = saveFile(pc_result['xmlURL'], self.local.getLocalOutputXmlPath(), name + '.xml', 0)
                        if save_xml_pc['status'] == 'OK':
                            print(str(self.dateNow + self.timeNow) + '>> ' + str(name) + ' Save file.xml success.')
                            shutil.copy(self.local.getLocalOutputXmlPath() + name + '.xml',self.destination.getDestinationOutputXmlPath() + name + '.xml')
                            print(str(self.dateNow + self.timeNow) + '>> ' + str(name) + ' Put file.xml success.')
                            pc_xml_result = 'OK'  ### เก็บสถานะการทำงานในส่วน XML
                        else:
                            print(str(self.dateNow + self.timeNow) + '>> ' + str(name) + ' Save file.xml failed. : ' + str(save_pdf_pc['errorMessage']))
                            pc_xml_result = 'ER'  ### เก็บสถานะการทำงานในส่วน XML


                        ##########นับว่า สำเร็จ หรือ ไม่สำเร็จ #######
                        if pc_pdf_result != 'OK' and pc_xml_result != 'OK':  ### ถ้าสถานะของทั้ง xml และ pdf สำเร็จทั้งคู่จึงจะนับว่า invoice นั้นสำเร็จ
                            with open(self.recovery.getRecoverySavePath() + filename, 'w',encoding='UTF-8') as recover_file: ### สร้างไฟล์เพื่อ recover save
                                recover_file.write(json.dumps({"transactionCode": service['transactionCode']}, indent=4, sort_keys=False,ensure_ascii=False))
                        try:  ##### ขั้นตอนไป filerun
                            shutil.move(self.local.getLocalPathNow() + filename, self.local.getLocalCsvArchivePath() + filename)
                        except Exception as e:
                            print(str(self.dateNow + self.timeNow) + '>> ' + str(name) + ' Move CSV input to Archived_File failed : ' + str(e))
                        
                        ### เก็บไว้ส่งในส่วนของการส่งคืนลูกค้า
                        # try:  ##### ขั้นตอนไป filerun
                        #     shutil.copy(self.destination.getDestinationCsvArchivePath() + filename, self.local.getLocalCsvArchivePath() + filename)
                        # except Exception as e:
                        #     print(str(self.dateNow + self.timeNow) + '>> ' + str(name) + ' Copy CSV input to Archived_File failed : ' + str(e))
                        try:  ##### ขั้นตอนไป filerun
                            shutil.move(self.local.getLocalPathNow() + name + '.pdf', self.local.getLocalCsvArchivePath() + name + '.pdf')  #### วาง PDF ที่ error ที่ path filerun error ฝั่งลูกค้า
                        except Exception as e:
                            print(str(self.dateNow + self.timeNow) + '>> ' + str(name) + ' Move PDF input to Archived_File failed : ' + str(e))
                        
                        ### เก็บไว้ส่งในส่วนของการส่งคืนลูกค้า
                        # try:  ##### ขั้นตอนไป filerun
                        #     shutil.copy(self.destination.getDestinationPdfArchivePath() + name + '.pdf', self.local.getLocalPdfArchivePath() + name + '.pdf')  #### วาง PDF ที่ error ที่ path filerun error ฝั่งลูกค้า
                        # except Exception as e:
                        #     print(str(self.dateNow + self.timeNow) + '>> ' + str(name) + ' Copy PDF input to Archived_File failed : ' + str(e))
                    else:
                        if pc_result['errorCode'] == "ER999" or pc_result['errorCode'] == "ER001" or pc_result['errorCode'] == "ER019" or pc_result['errorCode'] == "AU045":
                            self.recover_count += 1
                            self.recover.append({
                                "invoiceNo": name,
                                "errorCode": str(pc_result["errorCode"]),
                                "errorMessage": str(pc_result["errorMessage"])
                            })
                            shutil.move(self.local.getLocalPathNow() + filename, self.recovery.getRecoverySignPath()+ filename)
                            shutil.move(self.local.getLocalPathNow() + name + '.pdf', self.recovery.getRecoverySignPath()+ name + '.pdf')
                        elif pc_result['errorCode'] == "ER021" or pc_result['errorCode'] == "EX01" or pc_result['errorCode'] == "PC010" or pc_result['errorCode'] == "ERC001" or pc_result['errorCode'] == "ER004" or (pc_result['errorCode'] == "ER400" and pc_result['errorMessage'] == "Not found this transactionCode") or pc_result['errorCode'] == "PC001" or pc_result['errorCode'] == "ERPC002":
                            print('TEST PC')
                            self.recover_count += 1
                            self.recover.append({
                                "invoiceNo": name,
                                "errorCode": str(pc_result["errorCode"]),
                                "errorMessage": str(pc_result["errorMessage"])
                            })
                            with open(self.recovery.getRecoveryCheckPath()+ name +'.txt','w',encoding='UTF-8') as recover_file:### สร้างไฟล์เพื่อ recover check
                                recover_file.write(json.dumps({"transactionCode":service['transactionCode']}, indent=4, sort_keys=False, ensure_ascii=False))
                            shutil.move(self.local.getLocalPathNow() + filename, self.recovery.getPeddingPath()+ filename)
                            shutil.move(self.local.getLocalPathNow() + name + '.pdf', self.recovery.getPeddingPath()+ name + '.pdf')
                        else:
                            self.fail = self.fail + 1
                            print(str(self.dateNow + self.timeNow) + '>> ' + str(name) + ' Service singning failed. : ' + str(pc_result['errorMessage']))
                            self.losemessage.append({
                                'InvoiceName': str(name),
                                'Process DTM': str(self.dateNow + self.timeNow),
                                'errorCode': pc_result['errorCode'],
                                'errorMessage': pc_result['errorMessage']
                            })
                            self.fail_recovery += 1
                            self.fail_recovery_message.append({
                                "inputDate": self.dateNow,
                                "batchName": name,
                                "invoiceNo": name,
                                "errorCode": str(pc_result['errorCode']),
                                "errorMessage": str(pc_result['errorMessage'])
                            })
                            
                            
                            try:  ##### ขั้นตอนไป filerun
                                shutil.move(self.local.getLocalPathNow() + filename, self.local.getLocalCsvErrorPath() + filename)
                            except Exception as e:
                                print(str(self.dateNow + self.timeNow) + '>> ' + str(name) + ' Move CSV input to Error_File failed : ' + str(e))
                            # try:  ##### ขั้นตอนไป filerun
                            #     shutil.copy(self.destination.getDestinationCsvErrorPath() + filename, self.local.getLocalCsvErrorPath() + filename)
                            # except Exception as e:
                            #     print(str(self.dateNow + self.timeNow) + '>> ' + str(name) + ' Copy CSV input to Error_File failed : ' + str(e))
                            
                            
                            try:  ##### ขั้นตอนไป filerun
                                shutil.move(self.local.getLocalPathNow() + name + '.pdf', self.local.getLocalPdfErrorPath() + name + '.pdf')  #### วาง PDF ที่ error ที่ path filerun error ฝั่งลูกค้า
                            except Exception as e:
                                print(str(self.dateNow + self.timeNow) + '>> ' + str(name) + ' Move PDF input to Error_File failed : ' + str(e))
                            # try:  ##### ขั้นตอนไป filerun
                            #     shutil.copy(self.destination.getDestinationPdfErrorPath() + name + '.pdf', self.local.getLocalPdfErrorPath() + name + '.pdf')  #### วาง PDF ที่ error ที่ path filerun error ฝั่งลูกค้า
                            # except Exception as e:
                            #     print(str(self.dateNow + self.timeNow) + '>> ' + str(name) + ' Copy PDF input to Error_File failed : ' + str(e))
                
                else:
                    if service['errorCode'] == "ER999" or service['errorCode'] == "ER001" or service['errorCode'] == "ERC001":
                        self.recover_count += 1
                        self.recover.append({
                            "invoiceNo": name,
                            "errorCode": str(service["errorCode"]),
                            "errorMessage": str(service["errorMessage"])
                        })
                        shutil.move(self.local.getLocalPathNow() + filename, self.recovery.getRecoverySignPath()+ filename)
                        shutil.move(self.local.getLocalPathNow() + name + '.pdf', self.recovery.getRecoverySignPath()+ name + '.pdf')
                    elif service['errorCode'] == "ER021" or service['errorCode'] == "EX01" or service['errorCode'] == "ER004" or service['errorCode'] == "PC001" or service['errorCode'] == "ERPC002":
                        self.recover_count += 1
                        self.recover.append({
                            "invoiceNo": name,
                            "errorCode": str(service["errorCode"]),
                            "errorMessage": str(service["errorMessage"])
                        })
                        with open(self.recovery.getRecoveryCheckPath() + name + '.txt', 'w',encoding='UTF-8') as recover_file: ### สร้างไฟล์เพื่อ recover check
                            recover_file.write(json.dumps({"transactionCode": service['transactionCode']}, indent=4, sort_keys=False,ensure_ascii=False))
                        shutil.move(self.local.getLocalPathNow() + filename, self.recovery.getPeddingPath()+ filename)
                        shutil.move(self.local.getLocalPathNow() + name + '.pdf', self.recovery.getPeddingPath()+ name + '.pdf')
                    else:
                        self.fail = self.fail + 1
                        print(str(self.dateNow + self.timeNow) + '>> ' + str(name) + ' Service singning failed. : ' + str(service['errorMessage']))
                        self.losemessage.append({
                            'InvoiceName': str(name),
                            'Process DTM': str(self.dateNow + self.timeNow),
                            'errorCode': service['errorCode'],
                            'errorMessage': service['errorMessage']
                        })
                        self.fail_recovery += 1
                        self.fail_recovery_message.append({
                            "inputDate": self.dateNow,
                            "batchName": name,
                            "invoiceNo": name,
                            "errorCode": str(service['errorCode']),
                            "errorMessage": str(service['errorMessage'])
                        })


                        try:  ##### ขั้นตอนไป filerun
                            shutil.move(self.local.getLocalPathNow() + filename, self.local.getLocalCsvErrorPath() + filename)
                        except Exception as e:
                            print(str(self.dateNow + self.timeNow) + '>> ' + str(name) + ' Move CSV input to Error_File failed : ' + str(e))
                        # try:  ##### ขั้นตอนไป filerun
                        #     shutil.copy(self.destination.getDestinationCsvErrorPath() + filename, self.local.getLocalCsvErrorPath() + filename)
                        # except Exception as e:
                        #     print(str(self.dateNow + self.timeNow) + '>> ' + str(name) + ' Copy CSV input to Error_File failed : ' + str(e))
                        
                        
                        try:  ##### ขั้นตอนไป filerun
                            shutil.move(self.local.getLocalPathNow() + name + '.pdf', self.local.getLocalPdfErrorPath()  + name + '.pdf')  #### วาง PDF ที่ error ที่ path filerun error ฝั่งลูกค้า
                        except Exception as e:
                            print(str(self.dateNow + self.timeNow) + '>> ' + str(name) + ' Move PDF input to Error_File failed : ' + str(e))
                        # try:  ##### ขั้นตอนไป filerun
                        #     shutil.copy(self.destination.getDestinationPdfErrorPath() + name + '.pdf', self.local.getLocalPdfErrorPath() + name + '.pdf')  #### วาง PDF ที่ error ที่ path filerun error ฝั่งลูกค้า
                        # except Exception as e:
                        #     print(str(self.dateNow + self.timeNow) + '>> ' + str(name) + ' Copy PDF input to Error_File failed : ' + str(e))
            except KeyError as ke:
                self.recover_count += 1
                self.recover.append({
                    "invoiceNo": name,
                    "errorCode": "PS901",
                    "errorMessage": str(ke)
                })
                shutil.move(self.local.getLocalPathNow() + filename, self.recovery.getRecoverySignPath()+ filename) ### ย้ายไป input รอ recover
                shutil.move(self.local.getLocalPathNow() + name + '.pdf', self.recovery.getRecoverySignPath()+ name + '.pdf')
            except Exception as e:
                self.fail = self.fail + 1
                print(str(self.dateNow + self.timeNow) + ">> Failed to Generate Invoice " + str(name) + " : " + str(e))
                self.losemessage.append({
                    'InvoiceName': str(name),
                    'Process DTM': str(self.dateNow + self.timeNow),
                    'errorCode': 'ER888',
                    'errorMessage': 'Failed to Generate Invoice. : ' + str(e)
                })

                try:  ##### ขั้นตอนไป filerun
                    shutil.move(self.local.getLocalPathNow() + filename, self.local.getLocalCsvErrorPath() + filename)
                except Exception as e:
                    print(str(self.dateNow + self.timeNow) + '>> ' + str(name) + ' Move CSV input to Error_File failed : ' + str(e))
                # try:  ##### ขั้นตอนไป filerun
                #     shutil.copy(self.destination.getDestinationCsvErrorPath() + filename, self.local.getLocalCsvErrorPath() + filename)
                # except Exception as e:
                #     print(str(self.dateNow + self.timeNow) + '>> ' + str(name) + ' Copy CSV input to Error_File failed : ' + str(e))
                
                try:  ##### ขั้นตอนไป filerun
                    shutil.move(self.local.getLocalPathNow() + name + '.pdf', self.local.getLocalPdfErrorPath() + name + '.pdf')  #### วาง PDF ที่ error ที่ path filerun error ฝั่งลูกค้า
                except:
                    print('not found pdf.')
                # try:  ##### ขั้นตอนไป filerun
                #     shutil.copy(self.destination.getDestinationPdfErrorPath() + name + '.pdf', self.local.getLocalPdfErrorPath() + name + '.pdf')  #### วาง PDF ที่ error ที่ path filerun error ฝั่งลูกค้า
                # except Exception as e:
                #     print(str(self.dateNow + self.timeNow) + '>> ' + str(name) + ' Copy PDF input to Error_File failed : ' + str(e))

    def testprocess(self,var):
        print("var == " + str(var))

    def runThreadProcess(self,quantityThread=1):
        try:
            allCSV = [f for f in listdir(self.local.getLocalPathNow()) if isfile(join(self.local.getLocalPathNow(), f))]
            # allCSV = ["1","2","3","4"]
            self.countInvoice = len(allCSV)
            divInvoice = (self.countInvoice // quantityThread)
            arrVariable = []
            for i in range(quantityThread):
                arrVariable.append("ThreadProcess" + str(i))
            
            try:
                if self.countInvoice >= quantityThread:
                    
                    for i in range(quantityThread):
                        if i == (quantityThread-1):
                            exec(f"{arrVariable[i]} = threading.Thread(target=self.process, args=(allCSV[divInvoice*i:len(allCSV)],))")
                        else:
                            exec(f"{arrVariable[i]} = threading.Thread(target=self.process, args=(allCSV[divInvoice*i:divInvoice*(i+1)],))")
                        exec(f"{arrVariable[i]}.start()")
                        exec(f"{arrVariable[i]}.join()")
                else:
                    singleProcess = threading.Thread(target=self.process, args=(allCSV,))
                    singleProcess.start()
                    singleProcess.join()
            except Exception as e:
                print(str(self.dateNow + self.timeNow) + ">> Multiprocess prepare error. : " + str(e))
                self.losemessage.append({
                    'InvoiceName': '-',
                    'Process DTM': str(self.dateNow + self.timeNow),
                    'errorCode': 'ER889',
                    'errorMessage': "Multiprocess prepare error. : " + str(e)
                })
        except Exception as e:
            print(str(self.dateNow + self.timeNow) + ">> Failed to Generate batch : " + str(e))
            self.losemessage.append({
                'InvoiceName': '-',
                'Process DTM': str(self.dateNow + self.timeNow),
                'errorCode': 'ER801',
                'errorMessage': "Failed to Generate batch. : " + str(e)
            })

    def writelog(self):
        ################### เขียน log ###############################
        if self.countInvoice == 0:
            totalinvoice = '-'
        else:
            totalinvoice = self.countInvoice
        if self.success + self.fail == 0:
            successinvoice = '-'
            failedinvoice = '-'
        else:
            successinvoice = str(self.success)
            failedinvoice = str(self.fail)
        logfile = {
                'TotalInvoice': str(totalinvoice),
                'SuccessInvoice': str(successinvoice),
                'FailedInvoice': str(failedinvoice),
                "recoverInvoice": str(self.recover_count),
                "RecoverResponseInvoices": self.recover,
                'responseInvoices': self.losemessage
            }
        try:
            with open(self.local.getLocalLogPath()+str(self.dateNow + self.timeNow)+'_log.txt', 'a+', encoding='UTF-8') as log:  ##### write log
                log.write(json.dumps(logfile, indent=4, sort_keys=False, ensure_ascii=False))
                log.close()
            try:
                shutil.copy(self.local.getLocalLogPath()+str(self.dateNow + self.timeNow)+ '_log.txt',self.destination.getDestinationLogPath()+str(self.dateNow + self.timeNow) + '_log.txt')
            except Exception as e:
                print(str(self.dateNow + self.timeNow) + '>>  Put log path error : ' + str(e))
        except Exception as e:
            print(str(self.dateNow + self.timeNow) + '>>  Write log path error : ' + str(e))

    def finalProcess(self):
        try:
            shutil.rmtree(self.local.getLocalPathNow())  ### เมื่อทำงานครบรอบแล้วจะลบ folder input ของรอบนั้นทิ้ง
            os.system("sudo chown -R kpc.prd:sftpuser " + str(self.local.myPath))
        except Exception as e:
            print(str(self.dateNow + self.timeNow) + '>>  Remove Processed Round Folder failed. : ' + str(e))
            result = {"status": "OK", "message": "End of process."}