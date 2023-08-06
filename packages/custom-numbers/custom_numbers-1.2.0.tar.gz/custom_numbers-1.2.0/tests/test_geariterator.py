import pytest
import pickle
import sys
from custom_numbers import custom_numbers as cn


# Common parameter
sys3 = cn.CustomNumeralSystem("pba")

# Scenario 0) Invalid parameters exception test
# params0_1 = [cn.CustomNumeralSystem(""), 0, 2]              # Empty set
params0_2 = [sys3, 3, 2]  # min_length > max_length
params0_3 = [sys3, 5, 10, "ppp"]  # len(init_value) < min_length
params0_4 = [sys3, 5, 10, "ppppppppppppppp"]  # len(init_value) > max_length
params0_5 = [sys3, 3, 10, "pbz"]  # Invalid symbol in init_value

# Scenario 1) no init_value, max_length=2, full test
params1 = [sys3, 0, 2, ""]
expected1 = [
    ("p"),
    ("b"),
    ("a"),
    ("bp"),
    ("bb"),
    ("ba"),
    ("ap"),
    ("ab"),
    ("aa"),
]

# Scenario 2) init_value="pa", min_value=2, max_length=3, partial test
params2 = [sys3, 2, 3, "ap"]
expected2 = [
    ("ap"),
    ("ab"),
    ("aa"),
    ("bpp"),
    ("bpb"),
]



class TestGearIterator:
    r"""GearIterator test class."""

    
    @classmethod
    def setup_class(cls):
        cls.scenario1 = cn.GearIterator(*params1)
        cls.scenario2 = cn.GearIterator(*params2)

    
    def test_scenario0_2(self):
        with pytest.raises(Exception):
            i = cn.GearIterator(*params0_2)

    
    def test_scenario0_3(self):
        with pytest.raises(Exception):
            i = cn.GearIterator(*params0_3)

    
    def test_scenario0_4(self):
        with pytest.raises(Exception):
            i = cn.GearIterator(*params0_4)

    
    def test_scenario0_5(self):
        with pytest.raises(Exception):
            i = cn.GearIterator(*params0_5)

    
    @pytest.mark.parametrize("expected", expected1)
    def test_scenario1(self, expected):
        result = self.scenario1
        assert next(result) == expected

    
    def test_scenario1_expected_exception(self):
        result = self.scenario1
        with pytest.raises(StopIteration):
            assert next(result)

    
    @pytest.mark.parametrize("expected", expected2)
    def test_scenario2(self, expected):
        result = self.scenario2
        assert next(result) == expected

    
    def test_scenario3(self):
        """Testing serialization"""

        our_iterator = self.scenario2
        assert next(our_iterator) == "bpa"
        serialized = pickle.dumps(our_iterator)
        print("\n-----")
        print("Serialized length: {0}".format(len(serialized)))  # 302
        print("Serialized size: {0}".format(sys.getsizeof(serialized)))  # 335

        assert next(our_iterator) == "bbp"
        assert next(our_iterator) == "bbb"

        our_iterator = pickle.loads(serialized)
        assert next(our_iterator) == "bbp"

    
    def test_combinations_calculation(self):
        expected = 4
        sysN = cn.CustomNumeralSystem("01")
        it = cn.GearIterator(sysN, 0, 2)
        result = it.combinations
        assert result == expected

    
    @classmethod
    def teardown_class(cls):
        del cls.scenario1
        del cls.scenario2

