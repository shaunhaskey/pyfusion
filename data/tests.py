"""Tests for data code."""

from pyfusion.test.tests import BasePyfusionTestCase
from pyfusion.data.base import BaseData
from pyfusion.data.timeseries import SCTData, MCTData

class TestSCTData(BasePyfusionTestCase):
    """Tests for single channel timeseries (SCT) data."""
    def testBaseClasses(self):
        self.assertTrue(BaseData in SCTData.__bases__)

class TestMCTData(BasePyfusionTestCase):
    """Tests for multiple-channel timeseries (MCT) data."""
    def testBaseClasses(self):
        self.assertTrue(BaseData in MCTData.__bases__)

class TestTimebase(BasePyfusionTestCase):
    """Test Timebase class."""

    def test_timebase(self):
        from pyfusion.data.timeseries import Timebase
        from numpy import arange
        t0=0.3
        n_samples=500
        sample_freq=1.e6
        test_tb = Timebase(t0=t0,n_samples=n_samples, sample_freq=sample_freq)
        local_tb = arange(t0, t0+n_samples/sample_freq, 1./sample_freq)
        self.assertTrue((test_tb.timebase == local_tb).all())

class TestSignal(BasePyfusionTestCase):
    """Test Signal class."""

    def test_signal(self):
        from pyfusion.data.timeseries import Signal
        from numpy.random import random
        test_input = random(size=100)
        test_signal = Signal(test_input)
        self.assertTrue((test_input == test_signal.signal).all())