"""
helper functions for pyfusion
"""
from numpy import fft, conjugate, array
import settings
from datetime import datetime

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
    return max(abs(a.timebase - b.timebase)) < settings.TIMEBASE_DIFFERENCE_TOLERANCE
