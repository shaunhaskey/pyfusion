"""MDSPlus acquisition."""


from pyfusion.acquisition.base import BaseAcquisition

class MDSPlusAcquisition(BaseAcquisition):
    def __init__(self, *args, **kwargs):
        from MDSplus import Data
        self._Data = Data
        super(MDSPlusAcquisition, self).__init__(*args, **kwargs)
        self._Data.execute("mdsconnect('%(server)s')" %{'server':self.server})

    def __del__(self):
        self._Data.execute("mdsdisconnect()")
        
    def getdata(self, shot, *args, **kwargs):
        kwargs.update({'_Data':self._Data})
        return super(MDSPlusAcquisition, self).getdata(shot,*args, **kwargs)
