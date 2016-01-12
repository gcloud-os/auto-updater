from gupdater.common.exception import IncorrectDriver
from gupdater.common.log import Logger
from gupdater.common.conf import CONF

LOG = Logger().getLogger()


def get_downloader():
    driver = CONF.general.get('drivers')
    if driver.upper() == "FTP":
        from gupdater.downloader.drivers.ftp import FtpDriver
        return FtpDriver()

    else:
        LOG.error("not specific ftp drivers.")
        raise IncorrectDriver()