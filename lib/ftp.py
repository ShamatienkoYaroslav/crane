import io
from ftplib import FTP

class BinaryFTP(FTP):
    def __init__(self, host, user, passwd, cwd, filename):
        self.output = io.BytesIO()
        self.wrapper = io.TextIOWrapper(self.output, encoding='latin-1', write_through=True)

        if host is not None and user is not None and passwd is not None and cwd is not None and filename is not None:
            super().__init__(host)
            self.login(user=user, passwd=passwd)
            self.cwd(cwd)
            self.retrbinary('RETR ' + self.filename, self.wrapper.write, 1024)
        else:
            raise BinaryFTP.FTPError('incorect init params')

    def getBuffer(self):
        return self.output.getvalue()

    def close():
        self.output.close()
        self.quit()


    ### ERRORS

    class FTPError(BaseException):
        def __init__(self, arg):
            self.message = 'Some FTP error occurred: %s' %(arg)
        def __str__(self):
            return self.message
