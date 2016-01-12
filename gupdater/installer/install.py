

from gupdater.common import util
from gupdater.common import package
from gupdater.common.log import Logger
from gupdater.common.exception import InstallPackageFailed
from gupdater.common.conf import CONF

import os

LOG = Logger(__name__).getLogger()


class Installer(object):

    def __init__(self, package_path="/opt/gupdater", tmp_path="/tmp/", package_=""):

        self.ppath = package_path
        self.tmp_path = tmp_path
        self.package = package_

        self.unpack_dir = ""

    def _work_thread(self):
        pass

    def _unpack(self):
        unpack_dir = os.path.join(self.tmp_path, self.package.replace(".zip", ""))
        if package.unpackage(os.path.join(self.ppath, self.package), unpack_dir):
            return unpack_dir
        else:
            LOG.error("unpackage [%s] failed." % self.package)
            return None

    def install(self):
        self.unpack_dir = self._unpack()
        if self.unpack_dir is None:
            raise InstallPackageFailed(msg="unpack package [%s] failed." % self.package)
        install_script = os.path.join(self.unpack_dir, package.INSTALL_SCRIPT)
        if os.path.isfile(install_script):
            LOG.info("find install script [%s], now install." % install_script)
        else:
            LOG.error("install script does not exist. [%s]" % install_script)
            return False

        # call script to install package
        # install script accepts two args, first is dir where script placed,
        # second is log file position, thus install script can make records
        log_path = os.path.join(CONF.GENERAL.get("log", ""), "install.log")
        cmd = "/bin/bash \"" + install_script + "\" " \
                    + self.unpack_dir + " " + log_path
        ret = os.system(cmd)
        LOG.debug("cmd [%s] exit code [%d]" % (cmd, ret))
        return ret == 0

    def restart(self):
        # restart service, if necessary.
        reb_script = os.path.join(self.unpack_dir, package.RESTART_SCRIPT)
        ret = 0
        if os.path.isfile(reb_script):
            cmd = "/bin/bash \"" + reb_script + "\" "
            ret = os.system(cmd)
        else:
            LOG.debug("not found restart script, seems not necessary.")
        self._clean_tmp_file()

        return ret == 0

    def _clean_tmp_file(self):
        unpack_dir = os.path.join(self.tmp_path, self.package.replace(".zip", ""))
        LOG.debug("clean tmp dir [%s]" % unpack_dir)
        os.system("rm -rf " + unpack_dir)
