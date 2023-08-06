from datetime import datetime
from ...method.checkpath import *
from os import listdir
import shutil
class dofile():
    def __init__(self,local,destination,dateNow,timeNow):
        self.dateNow = dateNow
        self.timeNow = timeNow
        self.local = local
        self.destination = destination
        self.allFileCSV = []
        self.allFilePDF = []

    def getListFile(self,path):
        try:
            for file in listdir(path):
                try:
                    if file[-4:] == ".csv" or file[-4:] == ".txt" or file[-4:] == ".CSV" or file[-4:] == ".TXT":
                        self.allFileCSV.append(file)
                    elif file[-4:] == ".pdf" or file[-4:] == ".PDF":
                        self.allFilePDF.append(file)
                except Exception as e:
                    print(str(self.dateNow + self.timeNow) + ">> List file failed. : " + str(e))
        except Exception as e:
            pass
            print(str(self.dateNow + self.timeNow) + ">> Error Exception  : " + str(e))

    def getFile(self):
        self.getListFile(self.destination.getDestinationPathCSV())
        self.getListFile(self.destination.getDestinationPathPDF())
        try:
            if len(self.allFileCSV) < 1 :
                self.status = "ER"
                self.errorMessage = "No file in folder."
                print(str(self.dateNow + self.timeNow) + self.errorMessage)
            else:
                matching = False
                check_path(self.local.getLocalPathNow())
                for input in self.all_file_csv:
                    if input[:-4]+'.pdf' in self.all_file_pdf:
                        round = 1
                        while round <= 3:
                            try:
                                shutil.move(self.destination.getDestinationPathCSV() + input , self.local.getLocalPathNow() + input)
                                self.status = "OK"
                                self.message = "Get sftp file success."
                                matching = True
                                print(str(self.dateNow + self.timeNow) + ">> Get sftp file " + str(input)+" success.({0})".format(round))
                                round = 4 ### สิ้นสุด
                            except Exception as e:
                                print(str(self.dateNow + self.timeNow) + ">> Get sftp file " + str(input)  + " failed ({0}) : ".format(round) + str(e))
                                round += 1 ### ทำ 3 รอบ
                if matching == False:
                    shutil.rmtree(self.local.getLocalPathNow())
        except Exception as e:
            self.status = "ER"
            self.errorMessage = "Get sftp file error. : "+ str(e)
            print(str(self.dateNow + self.timeNow) + ">> Get sftp file error. : "+ str(e))