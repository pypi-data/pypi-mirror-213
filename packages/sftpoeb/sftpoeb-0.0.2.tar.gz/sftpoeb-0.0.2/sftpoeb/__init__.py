import mainclass.c_sftp as c_sftp

myPath = '/home/natthawut.th/kpc.prd/kpc.prd/'
custPath = '/home/sftp/kpc.prd/kpc.prd/'
payloadData = {
    "SellerTaxid":"0105542005283",
    "SellerBranchId":"00000",
    "UserCode":"kpcacc21",
    "AccessKey":"etax@KPC2021"
}
sftpPath = 'abc'


### เรียกคลาส SFTP
sftp = c_sftp.SFTP(myPath,sftpPath,custPath,payloadData)
sftp.package1(quantityThread=4)
### จบ SFTP