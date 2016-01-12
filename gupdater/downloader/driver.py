#coding=utf-8

'''
Created on Jul 21, 2015

@author: kongmq
'''


class FileDriver(object):
    """Base class for file manipulation."""

    def __init__(self, *args, **kwargs):
        """Constructor."""
        pass

    def connect(self):
        """connect to file server."""
        raise NotImplementedError('The connect method is not implemented')

    def disconnect(self):
        """disconnect from file server."""
        raise NotImplementedError('The disconnect method is not implemented')

    def upload(self, breakpoint=False, **kwargs):
        """upload file to file server."""
        raise NotImplementedError('The upload method is not implemented')

    def download(self, breakpoint=False, **kwargs):
        """download file from file server."""
        raise NotImplementedError('The download method is not implemented')

    def get_list(self):
        """get list file from file server."""
        raise NotImplementedError('The get list method is not implemented')

    def get_list_detail(self):
        """get list file detail from file server."""
        raise NotImplementedError('The get list detail method is not implemented')

    def file_exists(self, file_name):
        """whether a file exists in the file server."""
        raise NotImplementedError('The file exists method is not implemented')

    def get_file_size(self, file_name):
        """get the file size from the file server."""
        raise NotImplementedError('The get file size method is not implemented')

#file_driver = FileDriver()
#file_driver.connect()