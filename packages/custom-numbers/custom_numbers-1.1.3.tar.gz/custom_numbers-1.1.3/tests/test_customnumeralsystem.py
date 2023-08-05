import pytest
from custom_numbers import custom_numbers as cn


class TestCustomNumeralSystem:
    r"""CustomNumeralSystem test class."""

    
    def test_empty_argument(self):
        with pytest.raises(Exception):
            sysN = cn.CustomNumeralSystem("")

    
    def test_duplicates_in_argument(self):
        with pytest.raises(Exception):
            sysN = cn.CustomNumeralSystem("abcc")

    
    def test_repr(self):
        expected = "012"
        sysN = cn.CustomNumeralSystem("012")
        result = str(sysN)
        assert result == expected

    
    def test_base(self):
        expected = 3
        sysN = cn.CustomNumeralSystem("012")  # Base 3
        result = sysN.base
        assert result == expected

    
    def test_number_validation(self):
        expected = True
        sysN = cn.CustomNumeralSystem("paf")
        result = sysN.valid_number("ff")  # Valid
        assert result == expected

    
    def test_number_validation_negative(self):
        expected = False
        sysN = cn.CustomNumeralSystem("paf")
        result = sysN.valid_number("xx")  # Invalid
        assert result == expected

    
    def test_number_validation_negative_empty_string(self):
        sysN = cn.CustomNumeralSystem("paf")
        with pytest.raises(Exception):
            result = sysN.valid_number("")  # Invalid

    
    def test_equality(self):
        expected = True
        sysN1 = cn.CustomNumeralSystem("paf")
        sysN2 = cn.CustomNumeralSystem("paf")
        result = sysN1 == sysN2
        assert result == expected

    
    def test_equality_negative(self):
        expected = False
        sysN1 = cn.CustomNumeralSystem("paf")
        sysN2 = cn.CustomNumeralSystem("pa")
        result = sysN1 == sysN2
        assert result == expected

    
    def test_inequality(self):
        expected = True
        sysN1 = cn.CustomNumeralSystem("paf")
        sysN2 = cn.CustomNumeralSystem("pa")
        result = sysN1 != sysN2
        assert result == expected

