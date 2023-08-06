from subclass.path.s_c_setgetlocal import *
from subclass.path.s_c_setgetdestination import *
from subclass.path.s_c_setgetrecovery import *
from subclass.file.s_c_file import *
from subclass.process.s_c_process_package_1 import *
from datetime import date, datetime
from subclass.input.s_c_input import *
class SFTP():
    def __init__(self,myPath="None",sftpPath="None",custPath="None",payloadData="None"):
        self.myPath = myPath
        self.sftpPath = sftpPath
        self.custPath = custPath
        self.dateNow = datetime.now().strftime("%Y%m%d")
        self.timeNow = datetime.now().strftime("%H%M%S")
        self.payloadData = payloadData
        ### Local
        self.local = setgetlocal(self.myPath,self.sftpPath,self.dateNow,self.timeNow)
        ### Destination
        self.destination = setgetdestination(self.custPath,self.sftpPath,self.dateNow,self.timeNow)
        ### Recovery
        self.recovery = setgetrecovery(self.myPath,self.sftpPath)
        ### inputFile
        self.input = inputFile(self.local,self.destination,self.dateNow,self.timeNow)

    def package1(self,quantityThread):

        ### เปิดคลาสกระบวนการดำเนินการไฟล์
        c_process = packageprocess(self.local,self.destination,self.recovery,self.payloadData,self.dateNow,self.timeNow)
        c_process.runThreadProcess(quantityThread)
        c_process.writelog()
        c_process.finalProcess()
