# -*- coding: utf-8 -*-
""" This is the CLPU module for management tasks.

Please do only add or modify but not delete content.

requires explicitely {
 - os
 - sys
 - numpy
}

import after installation of pyclpu via {
  from pyclpu import manager
}

import without installation via {
  root = os.path.dirname(os.path.abspath(/path/to/pyclpu/manager.py))
  sys.path.append(os.path.abspath(root))
  import manager
  from importlib import reload 
  reload(manager)
}

"""

# =============================================================================
# PYTHON HEADER
# =============================================================================
# EXTERNAL
import os
import sys
import threading
import time

from inspect import getsourcefile
from importlib import reload

import math
import numpy as np

# INTERNAL
root = os.path.dirname(os.path.abspath(getsourcefile(lambda:0))) # get environment
sys.path.append(os.path.abspath(root))                           # add environment
sys.path.append(os.path.abspath(root)+os.path.sep+"LIB")         # add library

if "constants" not in globals() or globals()['constants'] == False:
    import constants            # import all global constants from                   constants.py
    import formats              # import all global formats from                     formats.py
    from s33293804 import *     # import zoom PanZoomWindow for display images from  s33293804.py
    reload(constants)
    reload(formats)

# STYLE

# =============================================================================
# CONSTANTS
# =============================================================================
# INTEGRATION AND TESTING
test = True

# PARAMETERS

# METHODOLOGY SELECTORS
# define method used to load images, 
# possible values are
# opencv   :: use the module opencv
# tifffile :: use the module tifffile # !!! tifffile not part of the project !!!
global_load_method = 'opencv'

# CONSTANTS

# =============================================================================
# METHODS
# =============================================================================
# INTEGRATION AND TESTING
def test_pingpong(*args, **kwargs):
    try:
        for arg in args:
            print(arg)
        for key, value in kwargs.items():
            print(str(key) + " : "+ str(value))
    except:
        return False
    return True
    
# MANAGEMENT
def error(source,string,code = None):
    print("\nError ............. "+source+" : "+string)
    lead_string = "                    "
    intend_string = "      "
    if code != None:
        if code == 0:
            print(lead_string+'ERROR_DIVISION_BY_ZERO\n'+intend_string+'The system cannot divide by zero.')
        elif code == 2:
            print(lead_string+'ERROR_FILE_NOT_FOUND\n'+intend_string+'The system cannot find the file specified.')
        elif code == 5:
            print(lead_string+'ERROR_ACCESS_DENIED\n'+intend_string+'Access is denied.')
        elif code == 13:
            print(lead_string+'ERROR_INVALID_DATA\n'+intend_string+'The data is invalid.')
        elif code == 161:    
            print(lead_string+'ERROR_BAD_PATHNAME\n'+intend_string+'The specified path is invalid.')
        elif code == 232:
            print(lead_string+'ERROR_NO_DATA\n'+intend_string+'The pipe is being closed.')
        elif code == 677:
            print(lead_string+'ERROR_EXTRANEOUS_INFORMATION\n'+intend_string+'Too Much Information.')
        elif code == 1160:
            print(lead_string+'ERROR_SOURCE_ELEMENT_EMPTY\n'+intend_string+'The indicated source element has no media.')
        elif code == 1169:
            print(lead_string+'ERROR_NO_MATCH\n'+intend_string+'There was no match for the specified key in the index.')
        elif code == 1287:
            print(lead_string+'ERROR_UNIDENTIFIED_ERROR\n'+intend_string+'Insufficient information exists to identify the cause of failure.')
        elif code == 8322:
            print(lead_string+'ERROR_DS_RANGE_CONSTRAINT\n'+intend_string+'A value for the attribute was not in the acceptable range of values.')
        else:
            print('ERROR\nNo idea what happened.\n')
    print("\n")
    return None
    
def message(source,string,headline = ""):
    print("\nMessage ........... "+source+" :")
    lead_string = "                    "
    if headline != "": print(lead_string+headline)
    intend_string = "      "
    string_list = string.split("\n")
    for s in string_list:
        print(intend_string + s)
    return None

def warning(source,string):
    try:
        print("\nWarning ........... "+source+" : "+string+"\n")
    except:
        error(warning.__name__,"Fail to print.")
    return None
    
def give_extension(filename):
    """
    Function returns extension of a filename as string or `None`.
    """
    try:
        extension = filename.rsplit(".",1)[1]
    except:
        extension = None
    return extension
    
def strip_extension(filename):
    """
    Function returns a filename without extension as string or `None`.
    """
    try:
        noextension = filename[0:-(len(give_extension(filename))+1)]
    except:
        noextension = None
    return noextension

    
# =============================================================================
# CLASSES
# =============================================================================
# INTEGRATION AND TESTING
class Main:
    # https://realpython.com/python-class-constructor/
    def __new__(cls, *args, **kwargs):
        #1) Create from this class as cls a new instance of an object Main
        return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        #2) Initialize from the instance of an object Main as self the initial state of the object Main
        for arg in args:
            warning(self.__class__.__name__,"Object does not accept unnamed arguments! Ignore: "+str(arg))
        for key, value in kwargs.items():
            self.key = value
        return None
            
    def __setattr__(self, name, value):
        #3) Set attributes of the instance during runtime, e.g. to change the initial state
        #if name in self.__dict__:
        #    print("!!! Warning...........Call to __setattr__ overwrites value of "+str(name)+ " with "+str(value))
        super().__setattr__(name, value)
        return None

    def __repr__(self) -> str:
        #anytime) representation as string, e.g. for print()
        string = "(\n"
        for att in self.__dict__:
            string = string + str(att) + " -> " + str( getattr(self,att) ) + "\n"
        return str(type(self).__name__) + string + ")"

# INTERACTIVE
class CatchAndRename():
    """ Responsive file catcher
    This class waits for new files in a directory and renames them upon arrival.
    
    Args:
        directory (str) : Path to directory where new files are expected.
        prefix (str, optional) : Prefix of renamed filename. Defaults to `""`.
        number (int, optional) : Suffix of renamed filename. Defaults to `0`.
        extension (str, optional) : Extension of renamed files. Defaults to the old extension.
        loop (bool, optional) : Activity status of the catcher. Inactive if `False`, active if `True`.
        leap (bool) : Leaps over existing files if set True. Defaults to False. 
            With leap = False, routine will not overwrite exisiting files and exists if an attempt is made.
            With leap = True, routine will not overwrite exisiting files but use the next possible number, counting up.
        
    Attributes:
        filename (str) : Name of last file which was written. Initializes as empty string.
        flag_new (bool) : True if processing was successfull, else False.
            Initializes to False.
            Intended to be modified from outside in use cases where this routine delivers output for another process.
        status (bool) : True if processing was successfull, else False.
            Initializes to False.
        
    Returns:
        ident (int) : Identity of thread. If more than one thread is started, a list is created that contains the identities in chronologic order, with the newest one last.
        ignored (list) : List of files which is ignored.
    
    Notes:
        Rename freshly arriving files to `str(prefix+number+"."+extension)` when loop is activated by setting the input parameter `loop = True`. If elements from the list `inored` are purged during `loop = True`, then corresponding files will be renamed as they are recognized as new.
        
    Examples:
        The class can be used in a functional way
        ```
        from pyclpu import manager
        chase = manager.CatchAndRename(directory = "path/to/directory/", prefix = "any_string", number = 42, loop=True)
        ```
        A more object oriented use case is described below. The chase for new files is activated by setting the input parameter `loop = True` and paused by setting `loop = False`.
        ```
        from pyclpu import manager
        import time

        chase = manager.CatchAndRename()

        chase.directory = "path/to/test"
        chase.prefix = "any_string"
        chase.number = 42

        chase.loop = True
        time.sleep(100)
        chase.loop = False`
        ```
        Files that arrive in the directory during a pause will be ignored when switching on the loop again with `loop = True`.
    """
    # INI
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)
    def __init__(self, *args, **kwargs):
        # INPUT
        self.__dict__.update(kwargs)
        # VARIABLES
        #self.cwd = os.getcwd()
        self.timeout = 2
        self.filename = ""
        self.flag_new = False
        self.status = False
        self.leap = False
        self.ident = None
        # INTEGRITY
        if not hasattr(self, 'loop'):
            warning(self.__class__.__name__,"Find no loop request status, expect key `loop` as boolean and start if `loop = True`.")
        # IN PLACE
        if hasattr(self, 'loop') and self.loop == True:
            self.__run__()
        return None
    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name == "loop" and value == True:
            self.__run__()
        if name == "loop" and value == False:
            #os.chdir(self.cwd)
            self.stop()
        return None
    def __run__(self):
        # INTEGRITY
        if not hasattr(self, 'directory'):
            warning(self.__class__.__name__,"No source directory defined, expect key `directory` as `directory=path/to/directorty`.")
            return None
        if not hasattr(self, 'number'):
            warning(self.__class__.__name__,"No starting integer defined, expect key `number` as `number=integer`. Set `number = 0`.")
            self.number = 0
        if not hasattr(self, 'extension'):
            warning(self.__class__.__name__,"No extension defined, expect key `extension`. Remain with original extension.")
            self.extension = ""
        if not hasattr(self, 'prefix'):
            warning(self.__class__.__name__,"No prefix defined, expect key `prefix` as `prefix=any_string`. Set `prefix = ''`.")
            self.prefix = ""
        # METHODS
        #@classmethod
        def _worker(event):
            self.ident = threading.get_ident()
            self.ignored = os.listdir(self.directory)
            while not self._event.is_set():
                time.sleep(self.timeout)
                file_list = os.listdir(self.directory)
                for file in file_list:
                    if file in self.ignored:
                        continue
                    else:
                        message(self.__class__.__name__,"WORK ON  "+file)
                        try:
                            filename_and_extension = file.rsplit( ".", 1 )
                            old_extension = filename_and_extension[1]
                            old_basename  = filename_and_extension[0]
                        except:
                            old_extension = ""
                            old_basename  = file
                        if self.extension == "":
                            new_extension = old_extension
                        else:
                            new_extension = self.extension
                        if math.isnan(self.number):
                            new_file = self.prefix+old_basename+'.'+new_extension
                        else:
                            new_file = self.prefix+str(self.number).zfill(3)+'.'+new_extension
                            self.number = self.number + 1
                        self.ignored.append(new_file)
                        old_name = os.path.join(self.directory,file)
                        new_name = os.path.join(self.directory,new_file)
                        if os.path.isfile(new_name):
                            message(self.__class__.__name__,"FILE ALREADY EXISTS: "+new_name)
                            find_next_free_number_for_pattern = self.number
                            while True:
                                find_next_free_number_for_pattern = find_next_free_number_for_pattern + 1
                                test_file = self.prefix+str(find_next_free_number_for_pattern).zfill(3)+'.'+new_extension
                                if os.path.isfile(os.path.join(self.directory,test_file)):
                                    continue
                                else:
                                    break
                            new_file = test_file
                            new_name = os.path.join(self.directory,new_file)
                            message(self.__class__.__name__,"FIND NEXT POSSIBLE: "+new_name)
                            if self.leap == True:
                                pass
                            else:
                                warning(self.__class__.__name__,"FILE ALREADY EXISTS: DO NOTHING FOR "+old_name)
                                message(self.__class__.__name__,"EXIT LOOP: loop = False")
                                self.status = False
                                self.loop = False
                                #break
                        message(self.__class__.__name__,"CREATE  "+new_name)
                        os.rename(old_name, new_name)
                        self.filename = new_file
                        self.flag_new = True
                        self.status = True
        # MAIN
        if not hasattr(self,"_event"):
            self._event = threading.Event()
            self._process = threading.Thread(target=_worker, args=(self._event,))
        self.start()
    
    def start(self):
        # START
        if hasattr(self,"_process"):
            self._process.start()
        else:
            warning(self.__class__.__name__,"THREAD ALREADY STARTED: DO NOTHING")
    
    def stop(self):
        self._event.set()
        self._process.join()
        # integrity of results
        # ..
        # housekeeping
        try:
            del self.ident
            del self._event
            del self._process
        except:
            pass
        return None
    
# =============================================================================
# PYTHON MAIN
# =============================================================================
# SELF AND TEST
if globals()["__name__"] == '__main__':
    # STARTUP
    print("START TEST OF CLPU IMAGE MODULE")
    print("!!! -> expect True ")
    # parse command line
    args = sys.argv
    # TESTS
    # (001) CONSTANTS
    print("\n(001) CONSTANTS")
    print(test)
    # (002) FUNCTION CALL
    print("\n(002) FUNCTION CALL")
    print(test_pingpong(True,kwa=True))
    # (003) CLASS INIT
    print("\n(003) CLASS INIT")
    test_class = Main(kwa=True)
    test_class.add = True
    print(test_class)
    del test_class
    