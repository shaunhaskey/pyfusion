"""
helper functions for pyfusion
"""
from numpy import fft, conjugate, array, choose
#import settings
from datetime import datetime
import pyfusion

def r_lib(r_inst, libname):
    """
    If R fails to import library, give user option to install and try again.
    r_inst is an RPy instance (from rpy import r)
    """
    try:
        r_inst.library(libname)
    except:
        raw_input("\nR library %s not found: press Enter to install...\n" %libname)
        r_inst("install.packages('%s')" %libname)
        r_inst.library(libname)

def local_import(name):
    """
    Taken from http://docs.python.org/lib/built-in-funcs.html
    """
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def get_conditional_select(input_list, key_list, exclude_keys=True):
    """
    returns a list of values, filtered by key_list and an arg determining whether to exlude the list or those not on the list
    """
    if exclude_keys == True:
        use_keys = [i for i in input_list if i not in key_list]
    else:
        use_keys = key_list

    return use_keys


def check_inputtype(calling_object, input_data,requested_datatype):
    # TODO: should learn how to define types, and check object type in less ambiguous way
    if not requested_datatype in str(input_data.__class__):
        raise ValueError, "Class %s requires input to be an instance of %s" %(str(calling_object.__class__),datatype)

def cps(a,b):
    """
    cross power spectrum
    """
    return fft.fft(array(a))*conjugate(fft.fft(array(b)))

def timestamp(fstr = '%y%m%d%H%M'):
    """
    return a string timestamp. 
    """
    return datetime.now().strftime(fstr)
    
def check_same_timebase(a,b):
    if len(a.timebase) != len(b.timebase):
        return False
    return max(abs(array(a.timebase) - array(b.timebase))) < pyfusion.settings.TIMEBASE_DIFFERENCE_TOLERANCE

from time import time
timelast=time()
timestart=time()

def delta_t(categ, total=False):
    """ returns a convenient string delta_t (wall) in ms since last
    Has the potential to accumulate delta_t in different categories
    Can also return the total wall time since initialization
    """
    global timelast, timestart
    timenow=time()
    if total: dt=timenow-timestart
    else: dt=timenow-timelast
    retval=str('%.3g s') % (1*dt)
    if total: retval = retval + ' total'
    timelast=time()
    return retval

def bigger(x,y):
    """
    more like the IDL > - note - different to numpy.greater
    """
    return choose(x < y, (x,y))


def smaller(x,y):
    """
    more like the IDL < - note - different to numpy.lesser
    """
    return choose(x > y, (x,y))
