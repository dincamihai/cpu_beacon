# coding: utf-8
from salttesting import skipIf, TestCase
from salttesting.helpers import destructiveTest, ensure_in_syspath
import os
from .. import cpu
import flexmock


ensure_in_syspath('../../')


@skipIf(not cpu.HAS_PSUTIL, 'psutil is not available')
class CPUBeaconTestCase(TestCase):
    '''
    Test case for salt.beacons.cpu
    '''
    def setUp(self):
        flexmock(cpu.psutil).should_receive('cpu_percent').and_return(10.2)

    def test_validate_empty_config(self):
        config = {}
        self.assertTrue(cpu.validate(config))

    def test_validate_config_with_threshold(self):
        config = {"threshold": 10}
        self.assertTrue(cpu.validate(config))

    def test_validate_config_with_non_numeric_threshold(self):
        config = {"threshold": "a"}
        self.assertFalse(cpu.validate(config))

    def test_validate_non_dict_config(self):
        config = list()
        self.assertFalse(cpu.validate(config))

    def test__virtual__returns_false_when_no_psutil(self):
        mock_cpu = flexmock(cpu, HAS_PSUTIL=False)
        self.assertFalse(cpu.__virtual__())

    def test__virtual__returns__virtualname__(self):
        mock_cpu = flexmock(cpu, HAS_PSUTIL=True, __virtualname__="abc")
        self.assertEqual(cpu.__virtual__(), "abc")

    def test_beacon_no_threshold(self, *args, **kwargs):
        config = {}
        ret = cpu.beacon(config)
        self.assertEqual(ret, [{"cpu%": 10.2}])

    def test_beacon_threshold_higher(self, *args, **kwargs):
        config = {"threshold": 11}
        ret = cpu.beacon(config)
        self.assertEqual(ret, [])

    def test_beacon_threshold_lower(self, *args, **kwargs):
        config = {"threshold": 10.1}
        ret = cpu.beacon(config)
        self.assertEqual(ret, [{"cpu%": 10.2}])
