from os.path import isfile, join
from os import listdir
from datetime import datetime,timedelta
import paramiko
import json
import os,time

class fileTransfer():
    def __init__(self,local,destination,dateNow,timeNow,hostNameServer,hostUserName,hostPassword,hostPort):
        self.hostNameServer = hostNameServer
        self.hostUserName = hostUserName
        self.hostPassword = hostPassword
        self.hostPort = hostPort
        self.local = local
        self.destination = destination
        self.dateNow = dateNow
        self.timeNow = timeNow
        self.transport = paramiko.SSHClient()
        self.transport.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sftp = None

    def connectServer(self):
        try:
            round = 1
            while round <= 3:
                try:
                    self.transport = paramiko.SSHClient()
                    self.transport.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    self.transport.connect(hostname=self.hostNameServer, username=self.hostUserName, password=self.hostPassword, port=self.hostPort)
                    self.sftp = self.transport.open_sftp()
                    print("Connect success.")
                    self.status = "OK"
                    round = 4
                except paramiko.SSHException:
                    time.sleep(1)
                    round += 1
                    pass
        except Exception as e:
            print("Connect failed : " + str(e))
            self.status = "ER"
            self.errorMessage = "Connect failed : " + str(e)
            
    def closeSftp(self):
        if self.sftp != None:
            self.sftp.close()
            self.transport.close()

    def sftpMoveFile(self, outpath, newpath):
        try:
            self.sftp.rename(outpath, newpath)  # Test if remote_path exists
        except Exception:
            self.sftp.remove(newpath)  # Create remote_path
            self.sftp.rename(outpath, newpath)
    
    def createDir(self, path):
        try:
            self.sftp.chdir(path)  # Test if remote_path exists
            self.sftp.chdir(None)
        except Exception:
            self.sftp.mkdir(path)  # Create remote_path
            self.sftp.chdir(None)

    def getNameFileAll(self,path):
        self.all_file = []
        try:
            for file in self.sftp.listdir(path):
                print(file)
                try:
                    type_file = file.split('.')[1]
                    if type_file == "txt":
                        self.all_file.append(file)
                except Exception as e:
                    print("List file failed. " + str(e))
        except Exception as e:
            print("Not found file. =>" + str(e))
    
    def getFile(self):
        self.getNameFileAll(self.destination.getDestinationPath())
        try:
            if len(self.all_file) < 1:
                self.statusdownload = "ER"
                self.errorMessagedownload = "No file in folder."
                print("No file in folder.")
            else:

                for file in self.all_file:
                    print(file)
                    remotefilepath = self.destination.getDestinationPath() + file  ### ไฟล์ input ฝั่งลูกค้า
                    localfilepath = self.local.getLocalPathNow() + file ### ไฟล์ input ที่จะมาวางฝั่งเรา
                    round = 1
                    while round <= 3:
                        try:
                            self.sftp.get(remotefilepath, localfilepath)
                            self.statusdownload = "OK"
                            self.messagedownload = "Download success."
                            print("Download success.")
                            self.sftp.remove(remotefilepath)  ### เมื่อโหลดแล้วลบไฟล์ฝั่งลูกค้า
                            round = 4
                        except Exception :
                            time.sleep(0.5)
                            round += 1
        except Exception as e:
            self.statusdownload = "ER"
            self.errorMessagedownload = 'Downloadfile error. : ' + str(e)
            print('Downloadfile error. : ' + str(e))

    def putFile(self,file):
        localfilepath = self.local.getLocalPathNow() + file
        remotefilepath = self.destination.getDestinationCsvArchivePath() + file
        try:
            self.sftp.put(localfilepath, remotefilepath)  #### upload file.
            self.statusupload = "OK"
            self.messageupload = "Upload success."
            # print('Upload success .')
        except Exception as e:
            self.statusupload = "ER"
            self.errorMessageupload = "Upload failed : " + str(e)
            # print('Upload failed : ' + str(e))