# -*- coding: utf-8 -*-
"""This is the main CLPU module. 

Please do only add or modify but not delete content.

requires explicitely {
  - os
  - sys
  - importlib
  - math
  - numpy
  - scipy
  - matplotlib
}

import after installation of pyclpu via {
  from pyclpu import main
}

import without installation via {
  root = os.path.dirname(os.path.abspath(/path/to/pyclpu/main.py))
  sys.path.append(os.path.abspath(root))
  import main
  from importlib import reload 
  reload(main)
}

"""

# =============================================================================
# PYTHON HEADER
# =============================================================================
# EXTERNAL
import os
import sys

import math

import numpy as np
import scipy

import matplotlib as mpl
mpl.use('TKAgg')
import matplotlib.pyplot as plt

from matplotlib.colors import LogNorm,SymLogNorm

# STYLE
mpl.style.use('classic')
mpl.rcParams['image.cmap'] = 'viridis'

mpl.rcParams['grid.color'] = 'k'
mpl.rcParams['grid.linestyle'] = ':'
mpl.rcParams['grid.linewidth'] = 0.5

mpl.rcParams['axes.linewidth'] = 2

mpl.rcParams['xtick.major.size'] = 10
mpl.rcParams['xtick.major.width'] = 2
mpl.rcParams['xtick.minor.size'] = 5
mpl.rcParams['xtick.minor.width'] = 1

mpl.rcParams['ytick.major.size'] = 10
mpl.rcParams['ytick.major.width'] = 2
mpl.rcParams['ytick.minor.size'] = 5
mpl.rcParams['ytick.minor.width'] = 1

mpl.rcParams['figure.figsize'] = [8.0, 8.0]
mpl.rcParams['figure.dpi'] = 80
mpl.rcParams['savefig.dpi'] = 600

mpl.rcParams['font.size'] = 26
mpl.rcParams['legend.fontsize'] = 'xx-small'
mpl.rcParams['figure.titlesize'] = 'medium'

mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = ['Times New Roman']

# =============================================================================
# CONSTANTS
# =============================================================================
# INTEGRATION AND TESTING
test = True


# =============================================================================
# METHODS
# =============================================================================
# INTEGRATION AND TESTING
test = True

def test_pingpong(*args, **kwargs):
    try:
        for arg in args:
            print(arg)
        for key in kwargs:
            print(key + " : "+ kwargs.get(key))
    except:
        return False
    return True


# VISUALIZATION: PLOTTER
def colormap(twoDmap,save_to,*args, **kwargs):
    # Options
    x_dpi = kwargs.get('x_dpi', None)
    y_dpi = kwargs.get('y_dpi', None)
    x_label = kwargs.get('x_label', "X")
    y_label = kwargs.get('y_label', "Y")
    color_label = kwargs.get('color_label', "Z")
    color_scale = kwargs.get('color_scale', "lin")
    color_range = kwargs.get('color_range', None)
    
    # Plot
    fig, axs = plt.subplots(nrows=1, ncols=1)
    fig.set_tight_layout(True)
    
    if x_dpi == None:
        axs.set_xlabel(x_label)
        x_dpi = 1
    else:
        axs.set_xlabel(x_label+" / [ dot/"+str(x_dpi)+"dpi]")
    if y_dpi == None:
        axs.set_ylabel(y_label)
        y_dpi = 1
    else:
        axs.set_ylabel(y_label+" / [ dot/"+str(y_dpi)+"dpi]")
    
    x_lins = np.arange(0,twoDmap.shape[1],1)/x_dpi
    y_lins = np.arange(0,twoDmap.shape[0],1)/y_dpi
    
    (ax_x,ax_y) = np.meshgrid(x_lins, y_lins)
    
    if isinstance(color_range,list):
        range = color_range
    else:
        range = [np.nanmin(twoDmap),np.nanmax(twoDmap)]
    
    levels = 20
    c_tik = np.linspace(range[0],range[1],levels)
    
    if color_scale == 'symlog':
        #c_tik = np.logspace(np.sign()*np.log2(np.abs(np.nanmin(twoDmap))),np.sign(np.nanmax(twoDmap))*np.log2(np.abs(np.nanmax(twoDmap))), num=levels, base=2.0)
        norm  = SymLogNorm(linthresh=0.00003, linscale=0.01,\
                           vmin=np.nanmin(twoDmap), vmax=np.nanmax(twoDmap), base=10)
        
    tmp = axs.contourf(ax_x, ax_y, twoDmap, vmin=range[0],vmax=range[1], levels=levels)
    
    if color_scale == 'log' or color_scale == 'symlog':
        getty = axs.contour(ax_x, ax_y, twoDmap, vmin=range[0],vmax=range[1], levels = tmp.levels[::2], colors='w', linewidths=2, norm = norm)
        cbar = fig.colorbar(tmp, ax=axs, shrink=0.95, ticks = c_tik)
    else:
        getty = axs.contour(ax_x, ax_y, twoDmap, vmin=range[0],vmax=range[1], levels = tmp.levels[::2], colors='w', linewidths=2)
        cbar = fig.colorbar(tmp, ax=axs, shrink=0.95, ticks = c_tik, format="%.2e")

    cbar.ax.set_ylabel(color_label)
    cbar.add_lines(getty)
    
    if os.path.isfile(save_to):
        os.remove(save_to)
    plt.savefig(save_to)
    #plt.show()
    plt.close()
    
    return True
    
def plot2D(x_array,y_arrays,save_to,*args, **kwargs):

    # Options
    x_label = kwargs.get('x_label', "X")
    y_label = kwargs.get('y_label', "Y")
    
    title = kwargs.get('title', None)
    
    x_scale = kwargs.get('x_scale', "linear")
    y_scale = kwargs.get('y_scale', "linear")
    
    labels = kwargs.get('labels', None)
    
    ptype = kwargs.get('type', 'plot')
    
    # Plot
    fig, axs = plt.subplots(nrows=1, ncols=1)
    fig.set_tight_layout(True)
    
    axs.set_xlabel(x_label)
    axs.set_ylabel(y_label)
    
    if isinstance(title,str):
        axs.set_title(title)
    
    axs.set_xscale(x_scale)
    axs.set_yscale(y_scale)
    
    if isinstance(y_arrays[0],list) or isinstance(y_arrays[0],np.ndarray):
        if not isinstance(labels,list) and not isinstance(labels,np.ndarray):
            lables = []
            for y_array in y_arrays:
                lables.append(None)
        for y_array,label in zip(y_arrays,labels):
            if ptype == 'scatter':
                axs.scatter(x_array,y_array,label=label)
            elif ptype == 'hist2D':
                axs.hist2d(x_array,y_array,label=label)
            else:
                axs.plot(x_array,y_array,label=label)
    else:
        if ptype == 'scatter':
            axs.scatter(x_array,y_arrays,label=labels)
        elif ptype == 'hist2D':
            axs.hist2d(x_array,y_arrays,label=labels)
        else:   
            axs.plot(x_array,y_arrays,label=labels)
    
    axs.legend()
    
    # Save
    if os.path.isfile(save_to):
        os.remove(save_to)
    plt.savefig(save_to)
    plt.show()
    plt.close()

    return True
    
def imshow(img,*args,**kwargs):
    # CHECK OPTIONAL PRIORITARIAN INPUT
    name = kwargs.get('name', "Input Image")
    # PLOT
    plt.imshow(img, cmap = 'gray')
    plt.title(name), plt.xticks([]), plt.yticks([])
    plt.show()
    plt.close()
    
# MATH: FAST FOURIER TRANSFORMS
def rfft(*args,**kwargs):
    """
    OPTION ONE: NAMED VARIABLES (PRIORITIZED)
    numpy.array, dimension(2) :: data[(x,y)] = ordinate (samples) and abscissa (sampling) array
    numpy.array, dimension(1) :: x           = ordinate (samples) array
    numpy.array, dimension(1) :: y           = abscissa (sampling) array
    real       , dimension(0) :: dx          = sampling increment
    bool       , dimension(0) :: prompts     = TRUE for terminal output, FALSE else
    string     , dimension(0) :: descartes   = REAL for real amplitude output, COMPLEX for full output
    string     , dimension(1) :: path        = path to which the results are exported as CSV, default is working directory
    string     , dimension(1) :: filename    = CSV file containing columns time[s],value[V] without header
    
    OPTION TWO: POSITIONAL ARGUMENTS (FALLBACK)
    string, dimension(0) ::               filename of CSV containing columns time[s],value[V] without header
    bool,   dimension(0) ::               TRUE for terminal output, FALSE else
    string, dimension(0) ::               path to which the results are exported as CSV, default is working directory
    real,   dimension(0) ::               sampling increment
    
    OUTPUT
    tupple     , dimension(1) :: (y_RFFT,x_F) = first position RFFT of y, second position frequencies
    """
    # PARSE INPUT
    # prefer named input
    data = kwargs.get("data",None)
    x = kwargs.get("x",None)
    y = kwargs.get("y",None)
    dx = kwargs.get("dx",None)
    prompts = kwargs.get("prompts",False)
    descartes = kwargs.get("descartes","REAL")
    path = kwargs.get("path",None)
    filename = kwargs.get("filename",None)
    # fall back to positional arguments
    if not isinstance(data,np.ndarray) and not isinstance(y,np.ndarray) and not isinstance(filename,str):
        if prompts:
            print("> no named parameter for data detected")
        try:
            filename = args[0]
        except:
            if prompts:
                print("> no positional argument for data detected")
    if kwargs.get("prompts",None) == None:
        if prompts:
            print("> no named parameter for user feedback detected")
        try:
            prompts = args[1]
        except:
            if prompts:
                print("> no positional argument for user feedback detected")
    if path == None:
        if prompts:
            print("> no named parameter for output directory detected")
        try:
            path = args[2]
        except:
            if prompts:
                print("> no positional argument for export path detected")
    if dx == None:
        try:
            dx = float(args[3])
        except:
            if prompts:
                print("> no positional argument for sampling detected")    
    # RAISE ATTENTION
    if prompts:
        print("\nCLPU RFFT MODULE")
    # PREPARE SAMPLING AND DATA
    # emergency break
    if isinstance(data,np.ndarray) and (isinstance(x,np.ndarray) or isinstance(y,np.ndarray) or dx != None or isinstance(filename,str)):
        sys.exit("> data specified but overload detected  >> EXIT")
    elif not isinstance(data,np.ndarray) and not isinstance(y,np.ndarray):
        sys.exit("> no data specified  >> EXIT")
    elif not isinstance(data,np.ndarray) and not isinstance(x,np.ndarray) and dx == None:
        sys.exit("> no sampling specified  >> EXIT")
    elif isinstance(x,np.ndarray) and dx != None:
        sys.exit("> sampling specified but overload detected  >> EXIT")
    # parser to x (sampling) and y (samples) arrays
    try:
        if isinstance(data,np.ndarray):
            x = data[:,0]
            y = data[:,1]
        elif isinstance(y,np.ndarray) and isinstance(x,np.ndarray):
            y = y
            x = x
        elif isinstance(y,np.ndarray) and dx != None:
            y = y
            x = np.arange(0., y.size * dx, dx)
        elif isinstance(filename,str) and dx != None:
            data = np.genfromtxt(filename, delimiter=',')
            if data.ndim == 1:
                y = data
                x = np.arange(0., y.size * dx, dx)
            elif data.ndim == 2:
                x = data[:,0]
                y = data[:,1]
            else:
                sys.exit("> dimensionality of input file troublesome  >> EXIT")
        else:
            sys.exit("> data not clearly specified  >> EXIT")
    except:
        sys.exit("> data specified but wrong format detected  >> EXIT")
    if prompts:
        print("> x:")
        print(x)
        print("> y:")
        print(y)
    # NAN test
    for iy in y:
        if iy != iy:
            sys.exit("> NaN in y  >> EXIT")
    # REAL FOURIER TRANSFORM
    # environmental variables
    N  = y.size
    if prompts:
        print("> number of samples = "+str(N))
    dx = x[1] - x[0]
    if prompts:
        print("> sampling interval = "+str(dx))
    # do transform
    try:
        signal_FFT         = np.fft.rfft(y)             # scipy.fft.rfft(y,workers = os.cpu_count())
        signal_frequencies = np.fft.rfftfreq(N, d = dx) # scipy.fft.rfftfreq(N, d = dx)
        if prompts:
            print('> terminate transform')
    except:
        sys.exit("> transform failed  >> EXIT")
    # PREPARE OUTPUT
    if descartes == "REAL":
        signal_FFT = np.abs(signal_FFT)
    # TMP CSV FILES
    if path != None:
        np.savetxt(path+"signal_FFT.csv", signal_FFT, delimiter=",")
        np.savetxt(path+"signal_frequencies.csv", signal_frequencies, delimiter=",")
    # RETURN RESULTS
    return {'signal_FFT':signal_FFT, 'signal_frequencies':signal_frequencies}
    
# OPTICS: SO CALLED SOLID ANGLE
def give_angularfraction_lens_pointsource(*args,**kwargs):
    """
    Give the angular fraction of emission hitting a lens when sseen from a point-like source,
     e.g. call the function via give_angularfraction_lens_pointsource(0.,1.,1.) to run
     an example with a lens of unit radius one unit avay from the source on its axis.
    
    Mandatory arguments are (in order of occurrance)
    dr   :: radial distance of the pointsource, with respect to the optical axis 
             of the lens
    dz   :: longitidinal distance of pointsource and centre of lens, with respect
             to the optical axis of the lens
    lR   :: radius of the imaging lens
    
    Optional arguments are (positioned after mandatory)
    'h','-h','-help','help' :: print help
    
    Named optional arguments are (positioned after optional/mandatory arguments)
    meth  :: method of calculation, can be   'mcs' for monte carlo, 
                                             'std' for default,
                                             'num' for numerical,
                                             'saa' for small angle approximation
              the default is 'mcs' for large angles and 'saa' for small angles
    mcs_n :: number of monte carlo shots if mcs is chosen as method of calculation,
              the default is 1000000
    """
    # Variables
    silent_run = False
    
    # Parse overload
    for arg in args:
        if not isinstance(arg,str):
            continue
        if arg == 'h' or arg == '-h' or arg == '-help' or arg == 'help':
            func.MESSAGE_PRINT(give_angularfraction_lens_pointsource.__name__, \
                "Mandatory arguments are (in the following order)", \
                " dr   :: radial distance of the pointsource", \
                " dz   :: longitidinal distance of pointsource and centre of lens", \
                " lR   :: radius of the imaging lens", \
                "Named optional argument is meth (method of calculation) with", \
                " possible values 'mcs' for monte carlo, 'std' for default,", \
                "                 'num' for numerical",    \
                "                 'saa' for small angle approximation",    \
                " (defaults to 'mcs')")
            func.ERROR_PRINT(1160)
        elif arg == 'test':
            args = (0.,1.,1.,)
            break
        elif arg == 'silent':
            silent_run = True
        #else:
        #    func.MESSAGE_PRINT(give_angularfraction_lens_pointsource.__name__, \
        #        "Found useless input > "+str(arg))
    
    if len(args) < 3:
        func.MESSAGE_PRINT(give_angularfraction_lens_pointsource.__name__, \
                "Mandatory arguments missing.")
        give_angularfraction_lens_pointsource('h')
        func.ERROR_PRINT(1160)
    
    # Parse mandatory arguments, change type if not ndarray
    if not isinstance(args[0], np.ndarray):
        dr = np.array([args[0]])
    else:
        dr = args[0]
    if not isinstance(args[1], np.ndarray):
        dz = np.array([args[1]])
    else:
        dz = args[1]
    lR = args[2]
    
    # Parse optional arguments
    default_meth = None
    if kwargs.get('meth', None) == None and not silent_run:
        func.MESSAGE_PRINT(give_angularfraction_lens_pointsource.__name__, \
            "Method of calculation meth can be chosen via optional argument meth,",\
            " possible values 'mcs' for monte carlo, 'std' for default,", \
                "                 'num' for numerical",    \
            " defaults to meth = "+str(default_meth))
    meth = kwargs.get('meth', default_meth)

    # Evaluate request
    if meth == 'mcs':
        # Parse auxilliary optional arguments
        default_n = 100000
        if kwargs.get('mcs_n', None) == None and not silent_run:
            func.MESSAGE_PRINT(give_angularfraction_lens_pointsource.__name__, \
                "Method of calculation mcs allows for further specification of", \
                " the number of monte carlo shots via optional argument mcs_n,",\
                " defaults to mcs_n = "+str(default_n))
        mcs_n = kwargs.get('mcs_n', default_n)
        
        # Calculate elliptical radius of lens seen from source, for lens-sided rays
        A = np.sqrt((dr-lR)**2+dz**2) # short side of triangle formed by lens and source in xz-plane
        B = np.sqrt((dr+lR)**2+dz**2) # long side of triangle formed by lens and source in xz-plane
        xz_plane_opening_angle = np.arccos((A**2+B**2-(2.*lR)**2)/(2. * A * B))

        small_half_axis = A/np.sqrt(2) * np.sqrt(1. - np.cos(xz_plane_opening_angle))
        large_half_axis = np.array([lR])
        
        ellidist = small_half_axis/np.tan(xz_plane_opening_angle/2.) # is presumed z direction
        
        # Create random rays within area of interest spanned by large half axis
        # which punch through the positive half-sphere in an equidistributed manner
        # https://mathworld.wolfram.com/SpherePointPicking.html
        
        # random variable u = cos(phi) in [-1,1]
        u = np.random.random_sample(mcs_n) * 2. - 1.
        
        # polar angle in [0,2pi)
        phi  = np.random.random_sample(mcs_n) * 2. * np.pi
        
        # unit vectors
        x = np.sqrt(1. - u**2) * np.cos(phi)
        y = np.sqrt(1. - u**2) * np.sin(phi)
        z = u

        # selection process
        x_non_zero = np.nonzero(x)
        
        phi = np.arctan2(x[x_non_zero],y[x_non_zero])
        theta = np.arccos(z/np.sqrt(x**2+y**2+z**2))
        
        directions_z = z

        # Select strictly lens-sided rays
        lens_sided = np.where(directions_z > 0.)
        
        # Calculate lens ellipse for phis present in beam
        
        lens_ellipse = 1./np.sqrt((np.cos(phi[lens_sided])/small_half_axis[:,None])**2 + (np.sin(phi[lens_sided])/large_half_axis[:,None])**2)
        
        lens_theta = np.arctan(lens_ellipse / ellidist[:,None])
        
        # Select rays per phi with a theta that allows them to pass inside the lens ellipse
        
        passing = np.less_equal(theta[lens_sided],lens_theta)
        
        hits = passing.sum(axis=1)
        hits_per_full_sphere = hits # (*)
        
        
        # renormalize Areal fraction of half sphere
        frac_interest = 1.
        
        # Calculate solid angle
        angular_fraction = frac_interest * hits_per_full_sphere/mcs_n
        
        
    elif meth == 'num':
    
        # Parse auxilliary optional arguments
        default_n = 10
        if kwargs.get('num_n', None) == None and not silent_run:
            func.MESSAGE_PRINT(give_angularfraction_lens_pointsource.__name__, \
                "Method of calculation num_saa allows for further specification of", \
                " the number of bessel terms via optional argument num_n,",\
                " defaults to num_n = "+str(default_n))
        num_n = kwargs.get('num_n', default_n)
        
        # Setup Angle Function
        def inside_integral(x,a,b,alpha):
            return 1.-np.cos(np.arctan(b*np.tan(alpha/2.)/np.sqrt((b*np.cos(x))**2+(a*np.sin(x))**2)))
                
        def integrate(a,b,alpha,n):
            mini = 0.
            maxi = 2.*np.pi
            
            h = (maxi - mini) / float(n)
            
            integral = h * (inside_integral(mini,a,b,alpha) + inside_integral(maxi,a,b,alpha)) / 2.
            
            for i in range(1,n):
                
                integral += h * inside_integral((mini + i * h),a,b,alpha)
            
            return integral
        
        # Calculate elliptical parameters
        A = np.sqrt((dr-lR)**2+dz**2) # short side of triangle formed by lens and source in xz-plane
        B = np.sqrt((dr+lR)**2+dz**2) # long side of triangle formed by lens and source in xz-plane
        xz_plane_opening_angle = np.arccos((A**2+B**2-(2.*lR)**2)/(2. * A * B))
        
        small_half_axis = A/np.sqrt(2) * np.sqrt(1. - np.cos(xz_plane_opening_angle))
        large_half_axis = np.array([lR])
        
        # Calculate solid angle
        angular_fraction = -1 #integrate(small_half_axis,large_half_axis,xz_plane_opening_angle,num_n)/(4.*np.pi)
        
    elif meth == 'saa':
    
        # Calculate elliptical parameters
        A = np.sqrt((dr-lR)**2+dz**2) # short side of triangle formed by lens and source in xz-plane
        B = np.sqrt((dr+lR)**2+dz**2) # long side of triangle formed by lens and source in xz-plane
        xz_plane_opening_angle = np.arccos((A**2+B**2-(2.*lR)**2)/(2. * A * B))
        
        small_half_axis = A/np.sqrt(2) * np.sqrt(1. - np.cos(xz_plane_opening_angle)) # general: np.minimum(A,B) * np.sin(xz_plane_opening_angle/2.)
        large_half_axis = np.array([lR])
        
        ellidist = small_half_axis/np.tan(xz_plane_opening_angle/2.)
        
        # Perform calculation of areal fraction in small angle approximation
        angular_fraction = np.pi * small_half_axis * large_half_axis / (4. * np.pi * ellidist**2)
    
    elif meth == 'spherical_cap':
    
        # Calculate spherical parameters with maximum radius = lens radius
        DIST = np.sqrt(dr**2+dz**2) # point-centre distance of lens and source
        xy_plane_opening_angle = np.arctan(lR/DIST)

        # Perform calculus of spherical cap approximation
        angular_fraction = (1.-np.cos(xy_plane_opening_angle)) / 2.
    
    else:

        # Calculate elliptical radius of lens seen from source, for lens-sided rays
        A = np.sqrt((dr-lR)**2+dz**2) # short side of triangle formed by lens and source in xz-plane
        B = np.sqrt((dr+lR)**2+dz**2) # long side of triangle formed by lens and source in xz-plane
        xz_plane_opening_angle = np.arccos((A**2+B**2-(2.*lR)**2)/(2. * A * B))

        small_half_axis = A/np.sqrt(2) * np.sqrt(1. - np.cos(xz_plane_opening_angle))
        large_half_axis = np.array([lR])
        
        ellidist = small_half_axis/np.tan(xz_plane_opening_angle/2.) # is presumed z direction
        
        # The Largest occuring angle
        large_half_axis = np.array([lR])
        
        large_theta = np.arctan(large_half_axis/ellidist) # is presumed z direction
        
        # Return
        angular_fraction = np.where(large_theta < 0.2, \
                            give_angularfraction_lens_pointsource(dr,dz,lR,'silent',meth='saa'),\
                            give_angularfraction_lens_pointsource(dr,dz,lR,'silent',meth='mcs'))
    
    # Output
    if not silent_run:
        func.MESSAGE_PRINT(give_angularfraction_lens_pointsource.__name__, \
            "Result = "+str(angular_fraction))
                
    return angular_fraction
    
def give_angularfraction_lens_blobsource(*args,**kwargs):
    """
    Give the angular fraction of emission hitting a lens when seen from a blob-like source,
     e.g. call the function via give_solidangle_lens_blobsource(0.,1.,1.) to run
     an example with a lens of unit radius one unit avay from the source on its axis.
    
    Mandatory arguments are (in order of occurrance)
    lP   :: absolute lens position, type np.array(3)
    eP   :: absolute positions of N emitters, type np.array((N,3))
    lR   :: radius of the imaging lens
    ln   :: normal of the imaging lens, type np.array(3)
    
    Optional arguments are (positioned after mandatory)
    'h','-h','-help','help' :: print help
    
    Named optional arguments are (positioned after optional/mandatory arguments)
    meth  :: method of calculation, can be   'mcs' for monte carlo, 
                                             'std' for default,
              the default is 'mcs'
    mcs_n :: number of monte carlo shots if mcs is chosen as method of calculation,
              the default is 1000000
    type  :: type of source, can be     'cloud' for point cloud
                                        'ellip' for ellipse with equidistributed points
    cloud_xyz :: numpy array of 3-vectors representing source points in case of type = 'cloud'
    ellip_sma :: small half axis of ellipse in case of type = 'ellip'
    ellip_lar :: large half axis of ellipse in case of type = 'ellip'
    ellip_til :: zx-plane tilt angle (around y axis) of ellipse in case of type = 'ellip'
    """
    # Parse overload
    for arg in args:
        if not isinstance(arg,str):
            continue
        if arg == 'h' or arg == '-h' or arg == '-help' or arg == 'help':
            func.MESSAGE_PRINT(give_angularfraction_lens_blobsource.__name__, \
                "Mandatory arguments are (in the following order)", \
                " lP   :: absolute lens position, type np.array(3)", \
                " eP   :: absolute positions of N emitters, type np.array((N,3))", \
                " lR   :: radius of the imaging lens", \
                " ln   :: normal of the imaging lens, type np.array(3)")
            func.ERROR_PRINT(1160)
        elif arg == 'test':
            lP = np.array([1.,1.,1])
            eP = np.array([[0.1,0.1,0.1],[0.,0.1,0.1],[0.1,0.,0.1],[0.1,0.1,0.],\
                           [0.,0.,0.1],[0.,0.1,0.],[0.1,0.,0.],[0.,0.,0.]])
            lR = 0.5
            ln = np.array([1.,0.,0.])
            args = (lP,eP,lR,ln,)
            break
        #else:
        #    func.MESSAGE_PRINT(give_angularfraction_lens_pointsource.__name__, \
        #        "Found useless input > "+str(arg))
    
    if len(args) < 4:
        func.MESSAGE_PRINT(give_angularfraction_lens_blobsource.__name__, \
                "Mandatory arguments missing.")
        give_angularfraction_lens_blobsource('h')
        func.ERROR_PRINT(1160)
    
    # Parse mandatory arguments
    lP = args[0]
    eP = args[1]
    lR = args[2]
    ln = args[3]
    
    # Calculate Angular Fraction point by point
    # dr   :: radial distance of the pointsource, with respect to the optical axis 
    #          of the lens
    # dz   :: longitidinal distance of pointsource and centre of lens, with respect
    #          to the optical axis of the lens
    normal = ln/np.linalg.norm(ln)
    e_to_l = (eP - lP)
    dz     = np.dot(e_to_l,normal)
    dr     = np.linalg.norm(e_to_l - dz[:,None] * normal, axis=1)
    
    angular_fraction = give_angularfraction_lens_pointsource(np.abs(dr),np.abs(dz),lR,'silent',meth='mcs')
    
    # Output
    func.MESSAGE_PRINT(give_angularfraction_lens_blobsource.__name__, \
        "Mean               = "+str(np.mean(angular_fraction)),\
        "Standard Deviation = "+str(np.std(angular_fraction)) )
        
    return angular_fraction

# =============================================================================
# PYTHON MAIN
# =============================================================================
# SELF AND TEST
if globals()["__name__"] == '__main__':
    # STARTUP
    print("START TEST OF CLPU MODULE")
    # parse command line
    args = sys.argv
    # TESTS
    """    
    MATH METHODS
    - rfft() :: real fast fourier transform
      1. Kronecker delta test with named variables
      2. Kronecker delta test with positional arguments
    """
    # real fast fourier transform
    try:
        # Kronecker delta test with named variables
        delta = np.zeros(100)
        large_number = 1.e12
        delta[delta.size//2] = large_number
        analyzed = rfft(y=delta,dx=1.,prompts=True)
        delta_FFT, frequencies = analyzed['signal_FFT'], analyzed['signal_frequencies']
        result = math.isclose(np.sum(np.abs(delta_FFT))/delta_FFT.size,large_number)
        if result:
            print("> OK : math method for rfft by Kronecker test by named variables")
        else:
            print("> FAILED : math method for rfft by Kronecker test by named variables")
        del delta, large_number, analyzed, delta_FFT, frequencies, result
        # Kronecker delta test with positional arguments
        dx = 0.1
        delta = np.sin(2.*np.arange(0., 10.*np.pi, dx))
        analyzed = rfft(y=delta,prompts=True,dx=0.001,descartes='COMPLEX')
        print(analyzed)
        
        delta_FFT, frequencies = analyzed['signal_FFT'], analyzed['signal_frequencies']
        #result = math.isclose(np.sum(np.abs(delta_FFT))/delta_FFT.size,large_number)
        result = True
        if result:
            print("> OK : math method for rfft by Kronecker test by positional arguments")
        else:
            print("> FAILED : math method for rfft by Kronecker test by positional arguments")
        del delta, large_number, analyzed, delta_FFT, frequencies, result
        # Kronecker delta test with named variables and saving of data to files
        delta = np.zeros(100)
        large_number = 1.e12
        delta[delta.size//2] = large_number
        analyzed = rfft(y=delta,dx=1.,prompts=True,path='')
        delta_FFT, frequencies = analyzed['signal_FFT'], analyzed['signal_frequencies']
        result = math.isclose(np.sum(np.abs(delta_FFT))/delta_FFT.size,large_number)
        if result:
            print("> OK : math method for rfft by Kronecker test by named variables")
        else:
            print("> FAILED : math method for rfft by Kronecker test by named variables")
        del delta, large_number, analyzed, delta_FFT, frequencies, result
    except Exception as e:
        sys.exit(str(e)+"\n> fail test for RFFT >> EXIT")
    # EXIT
    print("\n> run complete >> EXIT")