# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 23:47:40 2019

@author: yqlim
"""
import logging
logger = logging.getLogger(__name__)

import os
import datetime
import struct
import pathlib
import platform
import subprocess
import psutil
import re
from win32api import GetUserName

import pandas as pd

def get_sys_bit():
    """
    Get system bits
    
    Returns
    -------
    integer
        number of bits
    """
    return 8 * struct.calcsize("P")

def is_32_bit():
    """
    Check if operating system is 32-bit
    
    Returns
    -------
    boolean
        True if operating system is 32-bit
    """
    return get_sys_bit() == 32

def is_64_bit():
    """
    Check if operating system is 64-bit
    
    Returns
    -------
    boolean
        True if operating system is 64-bit
    """
    return get_sys_bit() == 64

def get_user_name():
    """
    Get Windows username using win32api.GetUserName().

    Returns
    -------
    GetUserName : str
        Windows username of current login.

    """
    return GetUserName()

def file_exists(str_file_path):
    path = pathlib.Path(str_file_path)
    return path.is_file()

def directory_exists(str_directory_path):
    path = pathlib.Path(str_directory_path)
    return path.is_dir()

def find_file(str_file_name_with_ext,
              str_drive = ''):
    if not str_drive:
        __ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        drives = ['%s:' % d for d in __ if os.path.exists('%s:' % d)]
    else:
        drives = [str_drive]
        
    for drive in drives:
        for p, d, f in os.walk(os.path.join(drive, os.path.sep)):
            if str_file_name_with_ext in f:
                return os.path.normpath(os.path.join(p, str_file_name_with_ext))
    return None

def get_operating_system():
    return platform.system()

def get_modified_date(str_file_path, str_time_format=None):
    if str_time_format:
        return datetime.datetime.fromtimestamp(os.path.getmtime(str_file_path)).strftime(str_time_format)
    else:
        return datetime.datetime.fromtimestamp(os.path.getmtime(str_file_path))

def get_creation_date(str_file_path, str_time_format=None):
    '''
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    '''
    if get_operating_system() == 'Windows':
        __ = os.path.getctime(str_file_path)
    else:
        stat = os.stat(str_file_path)
        try:
            __ = stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            __ = stat.st_mtime
            
    if str_time_format:
        return datetime.datetime.fromtimestamp(__).strftime(str_time_format)
    else:
        return datetime.datetime.fromtimestamp(__)


class TaskManager(object):
    """
    Represents an instance of Windows Task Manager.    
  
    Methods
    -------
    refresh
    get_tasks
    kill_task_by_pid
    kill_task_by_name
    get_pid_by_name
    run_cmd
    """    
    def __init__(self):
        self.__msg = None
        self.__err = None
        self.tasks = None
        
        self.refresh()
        
    def refresh(self):
        try:
            self.__msg, self.__err = subprocess.Popen('tasklist', stdout=subprocess.PIPE).communicate()
            lst_output = []
            for line in self.__msg.split(b'\n'):
                lst_row = []
                for col in re.sub('\s\s+', ' ', line.decode('utf-8')).split():
                    str_col = col.strip()
                    lst_row.append(str_col)
                lst_output.append(lst_row)
                
            lst_output[1] = [str(lst_output[1][0]) + ' ' + str(lst_output[1][1]),
                              str(lst_output[1][2]),
                              str(lst_output[1][3]) + str(lst_output[1][4]),
                              str(lst_output[1][5]),
                              str(lst_output[1][6]) + str(lst_output[1][7])]
            
            i = 3
            for line in lst_output[3:-1]:
                lst_output[i] = lst_output[i][:-2] + [str(lst_output[i][-2]) + ' ' + str(lst_output[i][-1])]
                if len(lst_output[i])>5:
                    lst_output[i] =  [' '.join(lst_output[i][:-4])] + lst_output[i][-4:]
                i+=1
         
            df_output = pd.DataFrame(lst_output[3:-1], columns=lst_output[1])
            df_output.dropna(how='all', inplace=True)
            self.tasks = df_output            
            return True
        except:
            return False

    def get_tasks(self, bln_refresh = True):
        if bln_refresh:
            self.refresh()
        
        return self.tasks
    
    def kill_task_by_pid(self, pid, bln_forcefully=False):
        p = psutil.Process(pid)
        try:
            if bln_forcefully:
                p.kill()
#                os.kill(pid, signal.SIGKILL)
            else:
                p.terminate()
#                os.kill(pid, signal.SIGTERM)
            logger.info('Process {pid} successfully killed.'.format(pid=pid))
            return True
        except Exception as e:
            logger.error('Error occurred while killing process {pid} - {err_msg}'.format(pid=pid, err_msg=str(e)))
            return False
        
    def kill_task_by_name(self, name, bln_forcefully=False):
        
        if bln_forcefully:
            os.system('taskkill /F /IM {process_name}'.format(process_name=name))
        else:
            os.system('taskkill /IM {process_name}'.format(process_name=name))
        return True
    
    def get_pid_by_name(self, name, bln_refresh = True):
        if bln_refresh:
            self.refresh()
        return self.tasks[self.tasks['Image Name']==name]['PID'].tolist()
    
    def run_cmd(self, lst_cmd, bln_shell=False):
        proc = subprocess.Popen(lst_cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, shell=bln_shell)
        output, error = proc.communicate()
        return output.decode('ascii'), error.decode('ascii')
        
    
class Folder(object):
    """
    Represents a folder.
    
    Attributes
    ----------
    folder_path
    folder_exists
    
    Methods
    -------
    get_files
    get_sub_directories    
    """
    def __init__(self, str_full_folder_path):
        self.folder_path = str_full_folder_path        
        if not self.folder_exists:
            logger.info(self.folder_path + ' does not exist.')     
    
    def __repr__(self):
        pass
    
    def __len__(self):
        pass
    
    @property
    def folder_path(self):
        return self.__str_folder_path
    
    @folder_path.setter
    def folder_path(self, str_folder_path):
        self.__str_folder_path = os.path.normpath(str_folder_path)
        
    @property
    def folder_exists(self):
        return directory_exists(self.folder_path)
    
    def get_files(self, lst_file_extensions = None):
        __ = []
        # r=root, d=directories, f = files
        for r, d, f in os.walk(self.folder_path):
            for file in f:
                if lst_file_extensions:
                    if File(os.path.join(r, file)).get_file_extension() in lst_file_extensions:
                        __.append(os.path.join(r, file))
                else:
                    __.append(os.path.join(r, file))
        return __
    
    def get_sub_directories(self):
        __ = []

        # r=root, d=directories, f = files
        for r, d, f in os.walk(self.folder_path):
            for folder in d:
                __.append(os.path.join(r, folder))
        
        return __

class File(object):
    """
    Represents a file.
    
    Attributes
    ----------
    file_path
    file_name
    file_exists
    file_extension
    file_directory
    
    Methods
    -------
    delete_file
    directory_exists
    get_file_extension
    get_file_directory
    get_file_name
    get_file_size
    get_creation_date
    get_modified_date
    rename    
    """
    def __init__(self, str_file_path):
        self.file_path = str_file_path        
        self.__file_name_idx = self.file_path.rfind('/')
        self.__file_ext_idx = self.file_path.rfind('.')
        if not self.file_exists:
            logger.info(self.file_path + ' does not exist.')
            
    def __repr__(self):
        pass
    
    def __len__(self):
        pass
    
    @property
    def file_path(self):
        return self.__str_file_path
    
    @file_path.setter
    def file_path(self, str_file_path):
        self.__str_file_path = os.path.normpath(str_file_path)
    
    @property
    def file_name(self):
        return os.path.split(self.file_path)[1]
    
    @property
    def file_exists(self):
        return file_exists(self.file_path)
    
    @property
    def file_extension(self):
        return os.path.splitext(self.file_path)[1]
    
    @property
    def file_directory(self):
        return os.path.split(self.file_path)
    
    def delete_file(self):
        try:
            if self.file_exists:
                os.remove(self.file_path)
                logger.debug(self.file_path + ' deleted.')
            else:                
                logger.debug(self.file_path + ' does not exist.')    
            
            return True
        except:
            logger.debug('Failed to delete ' + self.file_path)
            return False
    
        
    def directory_exists(self):
        return directory_exists(self.get_file_directory())
    
    def get_file_extension(self):
        return self.file_extension
    
    def get_file_directory(self):
        return self.file_directory
    
    def get_file_name(self):
        return self.file_name
    
    def get_file_size(self):
        return os.stat(self.file_path).st_size
    
    def get_creation_date(self, str_time_format='%Y-%m-%d %H:%M:%S'):
        return get_creation_date(self.file_path, str_time_format)
    
    def get_modified_date(self, str_time_format='%Y-%m-%d %H:%M:%S'):
        return get_modified_date(self.file_path, str_time_format)
    
    def rename(self, str_new_full_path):
        try:
            os.rename(self.file_path, str_new_full_path)
            return True
        except:
            return False

