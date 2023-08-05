# -*- coding: utf-8 -*-
""" This is the CLPU module for image manipulation.

Please do only add or modify but not delete content.

requires explicitely {
 - os
 - sys
 - numpy
 - cv2
 - PIL
}

import after installation of pyclpu via {
  from pyclpu import image
}

import without installation via {
  root = os.path.dirname(os.path.abspath(/path/to/pyclpu/image.py))
  sys.path.append(os.path.abspath(root))
  import image
  from importlib import reload 
  reload(image)
}

"""

# =============================================================================
# PYTHON HEADER
# =============================================================================
# EXTERNAL
import os
import sys
from inspect import getsourcefile
from importlib import reload

import math
import numpy as np

import cv2
import PIL

# INTERNAL
root = os.path.dirname(os.path.abspath(getsourcefile(lambda:0))) # get environment
sys.path.append(os.path.abspath(root))                           # add environment
sys.path.append(os.path.abspath(root)+os.path.sep+"LIB")         # add library

if "constants" not in globals() or globals()['constants'] == False:
    import constants                        # import all global constants from                   constants.py
    import formats                          # import all global formats from                     formats.py
    from manager import error               # import error() from management                     manager.py
    from manager import message             # import message() from management                   manager.py
    from manager import warning             # import warning() from management                   manager.py
    from manager import give_extension      # import give_extension() from management            manager.py
    from s33293804 import *                 # import zoom PanZoomWindow for display images from  s33293804.py
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
global_avoid_underflow = False
global_fill_screen_percent = 0.9


# =============================================================================
# METHODS
# =============================================================================
# INTEGRATION AND TESTING
def test_pingpong(*args, **kwargs):
    """ Tests functionality of functions. 
 
    Function prints any input.
 
    Args:
        `*args`   : Any number of positional arguments.
        `**kwargs`: Any number of named keyval arguments.
    
    Returns:
        exit_stat (bool) : True in case of success and False else.
    
    Examples:
        ```python
        test_pingpong(True,kwa=True)
        ```
        returns
        ```
        True
        kwa : True
        ```
    """
    try:
        for arg in args:
            print(arg)
        for key, value in kwargs.items():
            print(str(key) + " : "+ str(value))
    except:
        return False
    return True

# IMAGE T/I/O
def isimg(path: str) -> bool:
    """ Checks for image file. 
 
    The function looks up if the argument of type string describes the path to an image file.
 
    Args:
        path (str) : The path which is to be checked.
    
    Returns:
        exit_stat (bool) : True in case there is an image file and False else.
    
    Examples:
        ```python
        isimg("")
        ```
        returns
        ```
        False
        ```
        
    Todo:
        * accept image object as input as well
    """
    global global_load_method
    try:
        extension = give_extension(path)
        if extension in formats.acceptedinput[global_load_method]:
            return True
        else:
            return False
    except:
        error(isimg.__name__,"",code=1287)

def imread(path):
    """ Reads image file. 
 
    The function tries to read an image file to a numpy array as `[channel,y,x]`.
 
    Args:
        path (str) : The path to an image file.
    
    Returns:
        img (:obj: `numpy.array`) : Matrix of color values as ``[channel,y,x]``
    """
    global global_load_method
    if global_load_method == 'opencv':
        img = cv2.imread(path,cv2.IMREAD_UNCHANGED)
        if img is None: # happens if there is trouble with the path -> 8bit PIL
            try:
                img = PIL.Image.open(path)
                img = img.convert("RGB")
                img = np.array(img.getdata(),dtype = np.float32).reshape(img.size[1], img.size[0], 3)
                img = img.astype(np.uint8)
                img = img[:,:,:3]
            except:
                error(imread.__name__,"",code=667)
        return img
    #elif global_load_method == 'tifffile': # !!! tifffile not part of the project !!!
    #    return tiff.imread(os.path.abspath(path))
    else:
        error(imread.__name__,"",code=1169)
        
def imshow(img, *args, **kwargs):
    name = kwargs.get('name', "ANONYMOUS")
    # Routine
    message(imshow.__name__,"ZOOM IN  BY HOLDING RIGHT MOUSE KEY AND MOVE UP\nZOOM OUT BY HOLDING RIGHT MOUSE KEY AND MOVE DOWN\nEXIT BY WINDOW-X, q or esc",headline="ENABLE ZOOM")
    window = PanZoomWindow(img, name)
    key = -1
    while key != ord('q') and key != 27 and cv2.getWindowProperty(window.WINDOW_NAME, 0) >= 0:
        key = cv2.waitKey(5) #User can press 'q' or 'ESC' to exit
    cv2.destroyAllWindows()
    return True
 
def imwrite(full_name, img):
    try:
        if not cv2.imwrite(full_name, img):
            message(imwrite.__name__,'Issue with "'+full_name.replace(os.path.sep,'/')+'\nWrite out to shell directory instead.')
            if not cv2.imwrite(os.path.split(full_name)[1], img):
                message(imwrite.__name__,'Shell directory protected!')
                error(imwrite.__name__,"",code=161)
        return True
    except:
        error(imwrite.__name__,"",13)
        
# IMAGE MANIPULATION
def to_RGB(img):
    # get color
    try:
        img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
    except:
        message(to_RGB.__name__,"Image can not be transformed via GRAY2RGB.")
    return img
    
def to_8bit(img):
    return ((img-np.nanmin(img))/(np.nanmax(img)-np.nanmin(img))*(2**8-1)).astype("uint8")

def enhanced_visibility(img):
    # get color
    img = to_RGB(img)
    # adjust dynamic range
    img = to_8bit(img)
    # return in color scale
    return cv2.applyColorMap(img, cv2.COLORMAP_JET)
    
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

# INTERACTIVE IMAGE
class Interactive:
    def __new__(cls, *args, **kwargs):
        #1) Create from this class as cls a new instance of an object Main
        return Main(*args, **kwargs)
        
class PointPicker():
    """ Interactive point picker.
    The class allows interactive picking of a veriable number of points in a picture.
    
    Args:
        image  (:obj: ``numpy.array``,optional) : Source image.
        n      (int,optional) : Number of points that should be picked.
    
    Attributes:
        status (bool) : True if processing was successfull, else False.
            Initializes to False.
    
    Returns:
        point_list (:obj: ``numpy.array``) : List of picked or parsed points of shape `(n,2)`.
        
    Note:
        The source image is not part of the object after processing.
        
    Examples:
        The class can be used in a functional way

        ```python 
        from pyclpu import image
        pick = image.PointPicker(image = image.imread("path/to/test.jpg"))
        ```

        A more object oriented use case demonstrates how a run can be started after initialization

        ```python 
        from pyclpu import image
        pick = image.PointPicker()
        image = image.imread("path/to/test.jpg")
        pick.image = image
        pick.n = 3
        pick.run()
        pick.status
        ```
        returns
        ```
        True
        ```
    """
    # INI
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)
    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)
        self.status = False
        # INTEGRITY
        if not hasattr(self, 'image'):
            warning(self.__class__.__name__,"No source image `IMG` defined, expect key `image` as `image=IMG`.")
        if not hasattr(self, 'n'):
            warning(self.__class__.__name__,"No number of points defined, expect key `n` as `n=INT`.")
        # IN PLACE
        if hasattr(self, 'image') and hasattr(self, 'n'):
            self.__run__()
        return None
    def __run__(self):
        # INTEGRITY
        if not hasattr(self, 'image'):
            error(self.__class__.__name__,"No source image `IMG` defined, expect key `image` as `image=IMG`. DO NOTHING.",1169)
            return None
        if not hasattr(self, 'n'):
            error(self.__class__.__name__,"No number of points defined, expect key `n` as `n=INT`. DO NOTHING.",1169)
            return None
        # VARIABLES
        self.point_list = np.zeros((self.n, 2), dtype = "int")
        self.point_list_pointer = 0
        # METHODS
        def click_and_get(event, x, y, flags, param):
            '''
            HELPER FUNCTION: CLICK EVENT FUNCTION
            https://www.pyimagesearch.com/2015/03/09/capturing-mouse-click-events-with-python-and-opencv/
            '''
            # grab references to the nonlocal variables
            #nonlocal self.point_list
            #nonlocal self.point_list_pointer
            # if the left mouse button was clicked, record (x, y) coordinates, if the right mouse button was clicked, remove last entry
            if event == cv2.EVENT_LBUTTONDOWN:
                self.point_list[self.point_list_pointer,0] = x
                self.point_list[self.point_list_pointer,1] = y
                self.point_list_pointer = (self.point_list_pointer + 1) % self.n
            elif event == cv2.EVENT_RBUTTONDOWN:
                self.point_list_pointer = self.point_list_pointer - 1
                if self.point_list_pointer == -1:
                    self.point_list_pointer  = self.n - 1
                self.point_list[self.point_list_pointer,0] = 0
                self.point_list[self.point_list_pointer,1] = 0
            # draw points in the open named canvas outside the function
            self.drawing = self.enhanced.copy()
            for point in self.point_list:
                if point[0] != 0 and point[1] != 0:
                    cv2.circle(self.drawing, (point[0],point[1]), 10, (255, 10, 10), -1)
            cv2.imshow(self.__class__.__name__, self.drawing)
        # MAIN
        # prepare display
        self.enhanced = enhanced_visibility(self.image)
        self.drawing = self.enhanced.copy()
        # print instructions
        message(self.__class__.__name__,"PRESS LEFT MOUSE BUTTON TO ADD NEW POINT\nPRESS RIGHT MOUSE BUTTON TO REMOVE LAST POINT\nPRESS C TO CONFIRM SELECTION\nPRESS R KEY TO RESET\nPRESS Q KEY TO QUIT",headline="SELECT POINT")
        # create canvas and start dialogue
        cv2.namedWindow(self.__class__.__name__)
        cv2.setMouseCallback(self.__class__.__name__, click_and_get)
        # keep looping until the 'q' key is pressed
        while True:
            # display the image and wait for a keypress
            cv2.imshow(self.__class__.__name__, self.drawing)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("r"):
                # if the 'r' key is pressed, reset
                self.point_list = np.zeros((self.n, 2), dtype = "int")
                self.point_list_pointer = 0
            elif key == ord("c") or key == ord("q"):
                # if the 'c' key is pressed, break from the loop
                break
        # integrity of results
        if np.shape(np.unique(self.point_list, axis=0))[0] < self.n:
            message(self.__class__.__name__,"Detected two or more equal points.")
            self.status = False
        else:
            self.status = True
        # housekeeping
        cv2.destroyAllWindows()
        del self.image
        del self.enhanced
        del self.drawing
        return None
    def start(self):
        # START
        self.__run__()

# IMAGE MANIPULATION
class Manipulate:
    def __new__(cls, *args, **kwargs):
        #1) Create from this class as cls a new instance of an object Main
        return Main(*args, **kwargs)
        
class PerspectiveTransform():
    """
    The class allows to transform a linearly distorted input image into a trapez-corrected view on it. Coordinates are interpreted as (x,y).
    
    Args:
        source  (:obj: ``numpy.array``,optional) : Source image.
        sourcecorners (:obj: ``PointPicker``,optional) : Object of type `PointPicker`, i.e. `sourcecorners.point_list` is a list of shape `(4,2)` which describe the source's corner coordinates in the original image matrix;`sourcecorners.n` equals 4; and `sourcecorners.status` should return True.
    
    Attributes:
        status (bool) : True if processing was successfull, else False.
            Initializes to False.
        flag_new (bool) : True if processing was successfull, else False.
            Initializes to False.
            Intended to be modified from outside in use cases where this routine delivers output for another process.
    
    Returns:
        warped  (:obj: ``numpy.array``) : Warped image.
        
    Note:
        The source image is not part of the object in its final form.
    
    Examples:
        The class can be used in a functional way

        ```python 
        from pyclpu import image
        warp = image.PerspectiveTransform(source = image.imread("path/to/test.jpg"))
        ```

        A more object oriented use case can deal with loops where all warps have the same source corner coordinates

        ```python 
        from pyclpu import image
        warp_it = image.PerspectiveTransform()
        image_stack = image.imread("path/to/directory/with/many/images/")
        warp = []
        for image in image_stack:
            warp_it.source = image
            warp.append[{"warped" : warp.warped, "sourcecorners" : warp.sourcecorners}]
        ```
        with results beeing stored in a list `warp`. The dynamic modification of `warp.sourcecorners` is possible.
    """
    # INI
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)
    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)
        self.status = False
        self.flag_new = False
        # INTEGRITY
        if not hasattr(self, 'source'):
            warning(self.__class__.__name__,"No source image `IMG` defined, expect key `source` as `source=IMG`.")
        if not hasattr(self, 'sourcecorners'):
            warning(self.__class__.__name__,"Found no corners (x,y) of target rectangle, optional key `sourcecorners` as `sourcecorners=np.array((4,2),dtype='int')`.")
        # IN PLACE
        if hasattr(self, 'source'):
            self.__run__()
        return None
    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name == "source":
            self.__run__()
        return None
    def __run__(self):
        self.status = False
        # METHODS
        def order_points(pts):
            """
            Orders automatically a list of coordinates of (rectangular) image corners as follows: top-left, top-right, bottom-right, bottom-left.
            """
            rect = np.zeros((4, 2), dtype = "float32")
            s = pts.sum(axis = 1)
            rect[0] = pts[np.argmin(s)]
            rect[2] = pts[np.argmax(s)]
            diff = np.diff(pts, axis = 1)
            rect[1] = pts[np.argmin(diff)]
            rect[3] = pts[np.argmax(diff)]
            return rect   
        def four_point_transform(image, pts):
            """
            Transforms the input image with the OPENCV (CV2) four point transform algorithm.
            """
            # define order of corner points
            rect = order_points(pts)
            (tl, tr, br, bl) = rect
            # caculate image properties
            widthB = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
            widthT = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
            maxWidth = max(int(widthB), int(widthT))
            heightR = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
            heightL = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
            maxHeight = max(int(heightR), int(heightL))
            # construct set of destination points to obtain a top-dpown view
            dst = np.array([
                [0, 0],
                [maxWidth - 1, 0],
                [maxWidth - 1, maxHeight - 1],
                [0, maxHeight - 1]], dtype = "float32")
            # compute perspective transform matrix and apply it
            M = cv2.getPerspectiveTransform(rect, dst)
            warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
            # return the warped image
            return warped    
        # MAIN
        first_warp = False
        if not hasattr(self,'sourcecorners'):
            first_warp = True
            warning(self.__class__.__name__,"Found no corners of target rectangle, open interactive dialogue to pick them.")
            self.sourcecorners = PointPicker(image=self.source,n=4)
        self.warped = four_point_transform(self.source, self.sourcecorners.point_list)
        if first_warp == True:
            first_warp = False
            message(self.__class__.__name__,"PRESS ANY KEY TO CLOSE IMAGE AND PROCEED",headline="DISPLAY WARP")
            cv2.namedWindow(self.__class__.__name__)
            cv2.imshow(self.__class__.__name__, self.warped)
            cv2.waitKey(0)
        # housekeeping
        cv2.destroyAllWindows()
        del self.source
        self.status = True
        self.flag_new = True
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
    