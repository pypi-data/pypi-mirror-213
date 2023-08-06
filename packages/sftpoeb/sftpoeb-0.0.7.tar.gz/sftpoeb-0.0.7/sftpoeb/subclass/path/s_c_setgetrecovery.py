from method.checkpath import *
from datetime import datetime
class setgetrecovery():
    def __init__(self,myPath,sftpPath,dateNow,timeNow):
        self.dateNow = dateNow
        self.timeNow = timeNow
        self.recoveryPath = myPath + "/" + sftpPath + "/Inbound/Temp_recover/"
        self.peddingPath = myPath + "/" + sftpPath + "/Inbound/Pending/"

########## SET ############
    def setRecoveryPath(self,path):
        self.recoveryPath = path
        return self.recoveryPath

    def setPeddingPath(self,path):
        self.peddingPath = path
        return self.peddingPath

########## END SET ############

########## GET ############
    def getRecoveryPath(self):
        check_path(self.recoveryPath)
        return self.recoveryPath

    def getPeddingPath(self):
        check_path(self.peddingPath)
        return self.peddingPath

    def getRecoverySavePath(self):
        savePath = self.recoveryPath + '/save/' + self.transformDate(self.dateNow) + '/'
        check_path(savePath)
        return savePath

    def getRecoverySignPath(self):
        signPath = self.recoveryPath + '/sign/' + self.transformDate(self.dateNow) + '/'
        check_path(signPath)
        return signPath

    def getRecoveryCheckPath(self):
        checkPath = self.recoveryPath + '/check/' + self.transformDate(self.dateNow) + '/'
        check_path(checkPath)
        return checkPath
########## END GET ############

########## transformDate ############
    def configTransformDate(self,formatOld,formatNew):
        self.formatOld = formatOld
        self.formatNew = formatNew

    def transformDate(self,date):
        return str(datetime.strptime(date, self.formatOld).strftime(self.formatNew))

########## END transformDate ############