
class UpdaterException(Exception):
    message = "unknow exception occurs."

    def __init__(self, _message=None):
        if _message is not None:
            self.message = _message

        super(UpdaterException, self).__init__(self.message)


class FileNotFound(UpdaterException):
    _message = "File not exist."

    def __init__(self, file_path=None):
        if file_path:
            message = "File not exist [%s]" % str(file_path)
        else:
            message = self._message

        super(FileNotFound, self).__init__(message)


class NotDefinedLock(UpdaterException):
    _message = "Lock [%s] is not defined."

    def __init__(self, lock_name):
        msg = self._message % str(lock_name)

        super(NotDefinedLock, self).__init__(msg)


class UnrecognizedUpdateStatus(UpdaterException):
    _message = "Unrecognized updator status [%s]."

    def __init__(self, status):
        msg = self._message % str(status)
        super(UnrecognizedUpdateStatus, self).__init__(msg)


class SaltStackException(Exception):
    message = "unknow saltstack exception"

    def __init__(self, _message=None):
        if _message:
            self.message = _message

        super(SaltStackException, self).__init__(self.message)


class FtpException(Exception):
    message = "unknow ftp exception"

    def __init__(self, _message=None):
        if _message:
            self.message = _message

        super(FtpException, self).__init__(self.message)


class TargetException(Exception):
    message = "unknow target exception"

    def __init__(self, _message=None):
        if _message:
            self.message = _message

        super(TargetException, self).__init__(self.message)


class DownloadQueueFull(UpdaterException):
    _message = "Donwload queue is full."

    def __init__(self):
        super(DownloadQueueFull, self).__init__(self._message)


class InvalidStageFile(UpdaterException):
    _message = "Invalid stage file."

    def __init__(self, msg=None):
        if msg:
            self._message = msg
        super(InvalidStageFile, self).__init__(self._message)


class DeployError(UpdaterException):
    _messaage = "can not deploy to target [%s]."

    def __init__(self, msg=None):
        if msg:
            self._messaage = self._messaage % msg
        super(DeployError, self).__init__(self._messaage)


class NotFoundUpdator(UpdaterException):
    _message = "updator not in cache [%s], maybe the update not exist."

    def __init__(self, updator_name=""):
        if updator_name:
            self._message = self._message % updator_name
        super(NotFoundUpdator).__init__(self._message)


class IncorrectDriver(UpdaterException):
    _messaage = "can not deploy to target [%s]."

    def __init__(self):
        super(IncorrectDriver, self).__init__(self._messaage)


class InstallPackageFailed(UpdaterException):
    _message = "can not install package."

    def __init__(self, package=None, msg=None):
        message = None
        if msg:
            message = msg
        elif package:
            message = self._message + "[%s]." % str(package)
        else:
            pass

        super(InstallPackageFailed, self).__init__(message)
