#encoding: utf-8

from gupdater.common.log import Logger
from gupdater.common.conf import CONF

import os

LOG = Logger().getLogger()

_PACKAGE_PATH = CONF.GENERAL.get("store_path", "/opt/gupdater")
if not os.path.isdir(_PACKAGE_PATH):
    os.mkdir(_PACKAGE_PATH)


class PackageStatus():
    def __init__(self):
        pass

    DOWNLOADED = ".downloaded"
    INSTALLED = ".installed"
    NORMAL = '.zip'


def get_file_list(path):
    if not os.path.isdir(path):
        LOG.error("file path [%s] not exist." % path)
        return None
    else:
        file_list = []
        for f in os.listdir(path):
            if os.path.isfile(os.path.join(path, f)):
                file_list.append(f)

        return file_list


def get_installed_packages():
    return _get_package(PackageStatus.INSTALLED)


def get_downloaded_packages():
    """
    complete package means there is a PACKAGE_NAME.done file which
    is created by downloader after package is downloaded.
    :return: List of downloaded package files.
    """
    return _get_package(PackageStatus.DOWNLOADED)


# TODO: lock this function.
def _get_package(state):

    flist = get_file_list(_PACKAGE_PATH)
    if not flist:
        return None
    else:
        package_list = []
        for f in flist:
            if not f.split('.')[-1] in ('zip', 'downloaded', 'installed'):
                LOG.warn("there is file not legal [%s], ignore." % f)
                continue

            if f.endswith(state):
                cp = f.replace(state, '.zip')
                if cp in flist:
                    LOG.debug("found a complete package [%s]." % cp)
                    package_list.append(cp)

        return package_list


def get_all_packages():
    return _get_package(PackageStatus.NORMAL)


def delete_package(package):
    for f in os.listdir(_PACKAGE_PATH):
        fullp = os.path.join(_PACKAGE_PATH, f)
        if os.path.isfile(fullp) and f.startswith(package.split(".")[0]):
            LOG.debug("delete file [%s]" % fullp)
            os.remove(fullp)


def package_set_status(package, status):
    flist = get_file_list(_PACKAGE_PATH)
    if package in flist:
        down = package.replace(".zip", PackageStatus.DOWNLOADED)
        fulld = os.path.join(_PACKAGE_PATH, down)
        new = os.path.join(_PACKAGE_PATH, package.replace(".zip", status))
        if os.path.isfile(fulld):
            os.rename(fulld, new)
        else:
            if not os.path.isfile(fulld):
                os.system("touch " + fulld)
        return True
    else:
        return False


def package_get_status(package):
    flist = get_file_list(_PACKAGE_PATH)
    if package in flist:
        down = package.replace(".zip", PackageStatus.DOWNLOADED)
        fulld = os.path.join(_PACKAGE_PATH, down)
        if os.path.isfile(fulld):
            return PackageStatus.DOWNLOADED

        install = package.replace(".zip", PackageStatus.INSTALLED)
        fulli = os.path.join(_PACKAGE_PATH, install)
        if os.path.isfile(fulli):
            return PackageStatus.INSTALLED

        return None
    else:
        return None


