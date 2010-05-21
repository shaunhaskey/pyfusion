"""Basic device class"""

from pyfusion.conf.utils import kwarg_config_handler, import_from_str, get_config_as_dict
import pyfusion

class Device(object):
    """Represent a laboratory device.  

    In general, a customised subclass of Device will be used.
    
    Usage: Device(device_name, **kwargs)

    Arguments:
    device_name -- name of device as listed in configuration file, 
       i.e.: [Device:device_name]
    
    Keyword arguments:
    Any setting in the [Device:device_name] section of the
    configuration file can be overridden by supplying a keyword
    argument to here, e.g.: Device(device_name)

    """
    
    #__tablename__ = 'devices'
    #id = Column(Integer, primary_key=True)
    #name = Column(String(50), unique=True)


    def __init__(self, config_name, **kwargs):
        if pyfusion.config.pf_has_section('Device', config_name):
            self.__dict__.update(get_config_as_dict('Device', config_name))
        self.__dict__.update(kwargs)
        self.name = config_name

        #### attach acquisition
        if hasattr(self, 'acq_name'):
            acq_class_str = pyfusion.config.pf_get('Acquisition',
                                          self.acq_name, 'acq_class')
            self.acquisition = import_from_str(acq_class_str)(self.acq_name)
            # shortcut
            self.acq = self.acquisition
        else:
            pyfusion.logging.warning(
                "No acquisition class specified for device")


if pyfusion.USE_ORM:
    from sqlalchemy import Table, Column, Integer, String
    from sqlalchemy.orm import mapper
    device_table = Table('devices', pyfusion.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('name', String, unique=True))

    pyfusion.metadata.create_all()
    mapper(Device, device_table)

def getDevice(device_name):
    """Find and instantiate Device (sub)class from config."""
    dev_class_str = pyfusion.config.pf_get('Device', device_name, 'dev_class')
    return import_from_str(dev_class_str)(device_name)
