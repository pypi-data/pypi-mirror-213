from datetime import datetime
from method.checkpath import *
class setgetdestination():
    def __init__(self,custPath,sftpPath,dateNow,timeNow):
        self.destinationPath = custPath + "/" + sftpPath + "/"
        self.destinationPathCSV = custPath + "/" + sftpPath + "/Inbound/CSV/"
        self.destinationPathPDF = custPath + "/" + sftpPath + "/Inbound/PDF/"
        self.destinationCsvArchivePath = custPath + "/" + sftpPath + '/History/' + self.transformDate(dateNow) + '/CSV/Archived_File/'
        self.destinationCsvErrorPath = custPath + "/" + sftpPath + '/History/' + self.transformDate(dateNow) + '/CSV/Error_File/'
        self.destinationPdfArchivePath = custPath + "/" + sftpPath + '/History/' + self.transformDate(dateNow) + '/PDF/Archived_File/'
        self.destinationPdfErrorPath = custPath + "/" + sftpPath + '/History/' + self.transformDate(dateNow) + '/PDF/Error_File/'
        self.destinationOutputPdfPath = custPath + "/" + sftpPath + '/Outbound/' + self.transformDate(dateNow) + '/PDF/'
        self.destinationOutputXmlPath = custPath + "/" + sftpPath + '/Outbound/' + self.transformDate(dateNow) + '/XML/'
        self.destinationLogPath = custPath + "/" + sftpPath + '/Outbound/' + self.transformDate(dateNow) + '/Logfile/'

########## SET ############
    def setDestinationPath(self,path):
        self.destinationPath = path
        return self.destinationPath

    def setDestinationPathCSV(self,path):
        self.destinationPathCSV = path
        return self.destinationPathCSV

    def setDestinationPathPDF(self,path):
        self.destinationPathPDF = path
        return self.destinationPathPDF

    def setDestinationCsvArchivePath(self,path):
        self.destinationCsvArchivePath = path
        return self.destinationCsvArchivePath

    def setDestinationCsvErrorPath(self,path):
        self.destinationCsvErrorPath = path
        return self.destinationCsvErrorPath

    def setDestinationPdfArchivePath(self,path):
        self.destinationPdfArchivePath = path
        return self.destinationPdfArchivePath

    def setDestinationPdfErrorPath(self,path):
        self.destinationPdfErrorPath = path
        return self.destinationPdfErrorPath

    def setDestinationOutputPdfPath(self,path):
        self.destinationOutputPdfPath = path
        return self.destinationOutputPdfPath

    def setDestinationOutputXmlPath(self,path):
        self.destinationOutputXmlPath = path
        return self.destinationOutputXmlPath

    def setDestinationLogPath(self,path):
        self.destinationLogPath = path
        return self.destinationLogPath
########## END SET ############

########## GET ############
    def getDestinationPath(self):
        check_path(self.destinationPath)
        return self.destinationPath

    def getDestinationPathCSV(self):
        check_path(self.destinationPathCSV)
        return self.destinationPathCSV

    def getDestinationPathPDF(self):
        check_path(self.destinationPathPDF)
        return self.destinationPathPDF

    def getDestinationCsvArchivePath(self):
        check_path(self.destinationCsvArchivePath)
        return self.destinationCsvArchivePath

    def getDestinationCsvErrorPath(self):
        check_path(self.destinationCsvErrorPath)
        return self.destinationCsvErrorPath
    
    def getDestinationPdfArchivePath(self):
        check_path(self.destinationPdfArchivePath)
        return self.destinationPdfArchivePath

    def getDestinationPdfErrorPath(self):
        check_path(self.destinationPdfErrorPath)
        return self.destinationPdfErrorPath

    def getDestinationOutputPdfPath(self):
        check_path(self.destinationOutputPdfPath)
        return self.destinationOutputPdfPath

    def getDestinationOutputXmlPath(self):
        check_path(self.destinationOutputXmlPath)
        return self.destinationOutputXmlPath

    def getDestinationLogPath(self):
        check_path(self.destinationLogPath)
        return self.destinationLogPath

########## END GET ############

########## transformDate ############
    def configTransformDate(self,formatOld,formatNew):
        self.formatOld = formatOld
        self.formatNew = formatNew

    def transformDate(self,date):
        return str(datetime.strptime(date, self.formatOld).strftime(self.formatNew))

########## END transformDate ############