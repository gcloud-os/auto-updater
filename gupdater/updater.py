# encoding: utf-8

from gupdater.common.log import Logger
from gupdater.common import util
from gupdater.common import package
# from gupdater.common import exception
from gupdater.common.conf import CONF
from gupdater.installer import install
from gupdater.downloader.drivers import ftp
from gupdater.common import util

import os
import time
import threading
import traceback

LOG = Logger().getLogger()

_PACKAGE_PATH = CONF.GENERAL.get("store_path", "/opt/gupdater")
_UNPACK_PATH = CONF.GENERAL.get("unpack_path", "/tmp/")
_INTERVAL_TIME = CONF.GENERAL.get("interval", "36000")


def _get_downloader(type_=None):

    if type_ == "FTP":
        return ftp.FtpDriver(CONF.FTP)
    else:
        return None


class Updater(object):

    running = False

    def __init__(self, downloader_type=CONF.GENERAL.get('downloader', 'FTP')):

        self.downloader = _get_downloader(type_=downloader_type)

        if not os.path.isdir(_PACKAGE_PATH):
            LOG.warn('[%s] not exist, make one.' % _PACKAGE_PATH)
            os.mkdir(_PACKAGE_PATH)

    def launch_loop(self):
        self.running = True
        LOG.info("start working loop ...")
        # waiting for network service...
        time.sleep(10)
        th = threading.Thread(target=self._work_loop)
        th.start()
        th.join()
        LOG.info("working loop finished.")

    def stop_loop(self):
        self.running = False

    def _need_download(self, local_packs, remote_package):
        """
        check customer and version info.
        :param local_packs:
        :param remote_package: package to check
        :return: boolean
        """
        cust_id = CONF.GENERAL.get("customer_id", None)
        pinfo = package.PackageInfo(remote_package)
        if cust_id is not None:
            # not specific customer id in remote packages
            # means no limitations.
            if pinfo.CUSTOMER is not None and pinfo.CUSTOMER != "common":
                if pinfo.CUSTOMER != cust_id:
                    LOG.debug("remote package cust id is [%s] not match [%s]."
                              % (pinfo.CUSTOMER, cust_id))
                    return False
        else:
            # no matter what
            pass

        # then check version.
        if local_packs:
            not_found_type = True
            for l in local_packs:
                linfo = package.PackageInfo(l)
                # 类型一样，本地的版本低，或者只是download没有install的，都
                # 重新下载安装，这样就可以重走一遍安装流程，以防上次的安装流程
                # 被中断了
                if linfo.TYPE == pinfo.TYPE:
                    not_found_type = False
                    if int(linfo.VERSION) < int(pinfo.VERSION):
                        LOG.debug("remote package version[%s] is newer[%s], "
                                  "need download." % (pinfo.VERSION, linfo.VERSION))
                        return True

                    s = util.package_get_status(l)
                    if s is None or s is util.PackageStatus.DOWNLOADED:
                        return True

            # if False, which means find same type but local version is old.
            return not_found_type
        else:
            # not found in local paths, of course we need a download.
            return True

    def _work_loop(self):
        # if self.cnt_long_enough():
        while self.running:
            try:
                local_packs = util.get_all_packages()
                remote_packs = []
                with ConnecterMaintainer(self):
                    rlist = self.downloader.get_list()
                    LOG.debug("get remote package list is [%s]" % rlist)
                    for f in rlist:
                        if self._remote_package_check(f):
                            remote_packs.append(f)
                        else:
                            LOG.warn("package [%s] not legal, ignore" % f)

                    if not remote_packs:
                        LOG.info("remote packages list is empty.")

                    # if packages not exist in remote, we do not
                    # need to handle related update packages.
                    for rp in remote_packs:
                        LOG.debug("check remote package [%s]." % rp)
                        if self._need_download(local_packs, rp):
                            if self.download(rp):
                                if not self._after_download(rp):
                                    LOG.error("after-download processing failed, abort install.")
                                else:
                                    self._install(rp)
                            else:
                                LOG.info("can not make a correct download for [%s],"
                                         " wait for next around." % remote_packs)
                        else:
                            LOG.debug("remote package [%s] not need to download." % rp)

            except Exception as e:
                LOG.error("caught exception in main loop [%s]." % e.message)
                LOG.debug(traceback.format_exc())

            self._wait_for_next()

        return rlist

    def _install(self, package_):
        inst = install.Installer(_PACKAGE_PATH, _UNPACK_PATH, package_)
        if inst.install():
            # set install marker
            LOG.info("intall package [%s] done." % package_)
            util.package_set_status(package_, util.PackageStatus.INSTALLED)
            LOG.debug("restart service.")
            inst.restart()
        else:
            LOG.error("install package [%s] failed." % package_)

    def _remote_package_check(self, package_name):
        # check package name format mainly.
        return package.legal_package(package_name)

    def _after_download(self, package_):
        # delete old version, set done file
        local_packs = util.get_all_packages()
        if not local_packs:
            LOG.warn("find nothing in local paths after download.")
            return False

        if package_ not in local_packs:
            LOG.warn("not found new download package [%s] in local "
                     "store path, do nothing." % package_)
            return False

        pinfo = package.PackageInfo(package_)
        for l in local_packs:
            linfo = package.PackageInfo(l)
            if linfo.TYPE == pinfo.TYPE and package_ != l:
                # delete same type old package.
                util.delete_package(l)

        # set status to downloaded.
        return util.package_set_status(package_, util.PackageStatus.DOWNLOADED)

    def download(self, package_, try_times=3):
        while try_times > 0:
            try_times -= 1
            if not self._download(package_):
                LOG.warn("download package [%s] last time [%d] failed."
                         % (package_, try_times + 1))
                time.sleep(3)
            else:
                LOG.info("[%s] download done. check md5." % package_)
                # md5 check and so on...
                if not package.check(package_):
                    LOG.error("package [%s] md5 check failed, redownload." % package_)
                    util.delete_package(package_)
                else:
                    return True

        return False

    def _download(self, package):
        LOG.debug("going to download [%s]..." % package)
        try:
            local_path = os.path.join(_PACKAGE_PATH, package)
            self.downloader.download(local_path=local_path,
                                     breakpoint=False,
                                     remote_path=package)
        except Exception as e:
            LOG.error("download package [%s] caught exception." % e.message)
            return False
        else:
            LOG.debug('download package done [%s]' % package)
            return True

    def _wait_for_next(self):
        LOG.debug("wait for next round ...")
        time.sleep(float(_INTERVAL_TIME))


class ConnecterMaintainer(object):

    def __init__(self, _updater):
        self.up = _updater
        self.down = _updater.downloader

    def __enter__(self):
        LOG.info("make new connection...")
        self.down.connect()
        self.up.cnt_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            LOG.info("close connection...")
            self.down.disconnect()
        except Exception as e:
            pass

'''
testconf = {
    'host': "20.251.32.20",
    'port': "21",
    'username': "test",
    'password': "test"
}
'''

