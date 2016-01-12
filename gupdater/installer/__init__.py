

import install

class __Installer():

    """
    super class of installer.
    """

    def __init__(self, package):
        pass

    def handle_package(self):
        pass

    def check(self):
        pass

    def install(self):
        '''call instruction script in package if exist.
            bacause some times the installation is too complicated.
        '''
        pass

    def clean(self):
        '''
        clean temp file
        '''
        pass

    def restart(self):
        '''
        some times does not need to restart anything.
        or restart self...
        :return:
        '''
        pass
