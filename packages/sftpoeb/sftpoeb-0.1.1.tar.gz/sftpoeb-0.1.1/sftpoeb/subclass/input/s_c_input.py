from os.path import isfile, join
from os import listdir
from ..file.s_c_file import *
from ..file.s_c_file_transfer import *
import paramiko
import json,shutil

class inputFile():
    def __init__(self,local,destination,dateNow,timeNow):
        self.local = local
        self.destination = destination
        self.dateNow = dateNow
        self.timeNow = timeNow
    
    def formation_1(self): ### ทำภายใน local ตัวเองอย่างเดียว ไม่มีการส่งข้าม server ไปหาปลายทาง
        c_input = dofile(self.local,self.destination,self.dateNow,self.timeNow)
        c_input.getFile()
        return c_input

    def formation_2(self,hostNameServer,hostUserName,hostPassword,hostPort): ### มีการส่งข้อมูลข้ามไปหา server ปลายทาง
        c_input = fileTransfer(self.local,self.destination,self.dateNow,self.timeNow,hostNameServer,hostUserName,hostPassword,hostPort)
        c_input.connectServer()
        if c_input.status != "ER":
            c_input.getFile()
        
        return c_input