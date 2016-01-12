# encoding: utf-8

import zipfile
import hashlib
import os

from gupdater.common.conf import CONF

_PACKAGE_PATH = CONF.GENERAL.get("store_path", "/opt/gcloud/gupdater")

INSTALL_SCRIPT = "install.sh"
RESTART_SCRIPT = "restart.sh"

class PackageInfo(object):

    prefix = ('typ', 'cst', 'ver', 'md5')
    TYPE = None
    CUSTOMER = None
    VERSION = None
    MD5 = None

    def __init__(self, package_name):
        info = package_name.split('.')[0].split('_')
        for i in info:
            if i[:3] == 'typ':
                self.TYPE = i[3:]
            elif i[:3] == 'cut':
                self.CUSTOMER = i[3:]
            elif i[:3] == 'ver':
                self.VERSION = i[3:]
            elif i[:3] == 'md5':
                self.MD5 = i[3:]
            else:
                pass


def unpackage(package_path, dest):
    # dest = os.path.join(dest, os.path.basename(package_path).split('.')[0])
    if not os.path.isdir(dest):
        os.mkdir(dest)

    f = zipfile.ZipFile(package_path, 'r')
    for file_ in f.namelist():
        f.extract(file_, dest)
    f.close()
    return True


def check_md5(pinfo, package_path):
    md5 = hashlib.md5()
    f = file(package_path, "r")
    while True:
        data = f.read(4096*10)
        if data:
            md5.update(data)
        else:
            break
    f.close()
    return md5.hexdigest() == pinfo.MD5


def check(package):
    # check md5
    pinfo = PackageInfo(package)
    return check_md5(pinfo, os.path.join(_PACKAGE_PATH, package))


def legal_package(package_name):
    if not package_name.endswith(".zip"):
        return False

    pinfo = PackageInfo(package_name)
    return (pinfo.MD5 and pinfo.VERSION and pinfo.CUSTOMER and pinfo.TYPE)
