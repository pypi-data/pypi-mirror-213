from datetime import datetime
from method.checkpath import *
class setgetlocal():
    def __init__(self,myPath,sftpPath,dateNow,timeNow):
        self.formatOld = '%Y%m%d'
        self.formatNew = '%Y-%m-%d'
        self.localPath = myPath + "/" + sftpPath + "/Inbound/"
        self.localFilerun = self.localPath+ '/Filerun/' + self.transformDate(dateNow) + '/'
        self.localPathNow = self.localPath + "/" + str( dateNow + timeNow ) + "/"
        self.localCsvArchivePath = myPath + "/" + sftpPath + "/History/" + self.transformDate(dateNow) + '/CSV/Archived_File/'
        self.localCsvErrorPath = myPath + "/" + sftpPath + "/History/" + self.transformDate(dateNow) + '/CSV/Error_File/'
        self.localPdfArchivePath = myPath + "/" + sftpPath + "/History/" + self.transformDate(dateNow) + '/PDF/Archived_File/'
        self.localPdfErrorPath = myPath + "/" + sftpPath + "/History/" + self.transformDate(dateNow) + '/PDF/Error_File/'
        self.localOutputPdfPath = myPath + "/" + sftpPath + "/Outbound/" + self.transformDate(dateNow) + '/PDF/'
        self.localOutputXmlPath = myPath + "/" + sftpPath + "/Outbound/" + self.transformDate(dateNow) + '/XML/'
        self.localLogPath = myPath + "/" + sftpPath + "/Outbound/" + self.transformDate(dateNow) + '/Logfile/'

########## SET ############
    def setLocalPath(self,path):
        self.localPath = path
        return self.localPath

    def setLocalFileRun(self,path):
        self.localFilerun = path
        return self.localFilerun

    def setLocalCsvArchivePath(self,path):
        self.localCsvArchivePath = path
        return self.localCsvArchivePath

    def setLocalCsvErrorPath(self,path):
        self.localCsvErrorPath = path
        return self.localCsvErrorPath

    def setLocalPdfArchivePath(self,path):
        self.localPdfArchivePath = path
        return self.localPdfArchivePath

    def setLocalPdfErrorPath(self,path):
        self.localPdfErrorPath = path
        return self.localPdfErrorPath

    def setLocalOutputPdfPath(self,path):
        self.localOutputPdfPath = path
        return self.localOutputPdfPath

    def setLocalOutputXmlPath(self,path):
        self.localOutputXmlPath = path
        return self.localOutputXmlPath

    def setLocalLogPath(self,path):
        self.localLogPath = path
        return self.localLogPath
    
########## END SET ############

########## GET ############
    def getLocalPath(self):
        check_path(self.localPath)
        return self.localPath

    def getLocalFileRun(self):
        check_path(self.localFilerun)
        return self.localFilerun

    def getLocalCsvArchivePath(self):
        check_path(self.localCsvArchivePath)
        return self.localCsvArchivePath

    def getLocalCsvErrorPath(self):
        check_path(self.localCsvErrorPath)
        return self.localCsvErrorPath
    
    def getLocalPdfArchivePath(self):
        check_path(self.localPdfArchivePath)
        return self.localPdfArchivePath

    def getLocalPdfErrorPath(self):
        check_path(self.localPdfErrorPath)
        return self.localPdfErrorPath

    def getLocalOutputPdfPath(self):
        check_path(self.localOutputPdfPath)
        return self.localOutputPdfPath

    def getLocalOutputXmlPath(self):
        check_path(self.localOutputXmlPath)
        return self.localOutputXmlPath

    def getLocalLogPath(self):
        check_path(self.localLogPath)
        return self.localLogPath

    def getLocalPathNow(self):
        check_path(self.localPathNow)
        return self.localPathNow
########## END GET ############

########## transformDate ############
    def configTransformDate(self,formatOld,formatNew):
        self.formatOld = formatOld
        self.formatNew = formatNew

    def transformDate(self,date):
        return str(datetime.strptime(date, self.formatOld).strftime(self.formatNew))

########## END transformDate ############