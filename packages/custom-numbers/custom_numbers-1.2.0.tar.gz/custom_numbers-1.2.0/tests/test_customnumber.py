import pytest
from custom_numbers import custom_numbers as cn



class TestCustomNumber:
    r"""CustomNumber test class."""

    
    def test_invalid_number(self):
        sysN = cn.CustomNumeralSystem("paf")
        with pytest.raises(Exception):
            num = cn.CustomNumber(sysN, "x")  # Invalid

    
    def test_repr(self):
        expected = "1100101"
        sysN = cn.CustomNumeralSystem("01")
        num = cn.CustomNumber(sysN, "1100101")
        result = str(num)
        assert result == expected

    
    def test_init_value(self):
        expected = "1100101"
        sysN = cn.CustomNumeralSystem("01")
        num = cn.CustomNumber(sysN, "1100101")
        result = str(num.init_value)
        assert result == expected

    
    def test_digit_to_int(self):
        expected = 1
        sysN = cn.CustomNumeralSystem("paf")  # 0 1 2
        num = cn.CustomNumber(sysN, "aaa")
        result = num.digit_to_int("a")
        assert result == expected

    
    def test_digit_to_int_hex(self):
        """Just in case"""

        expected = 15
        sysN = cn.CustomNumeralSystem("0123456789abcdef")  # Common hex system
        num = cn.CustomNumber(sysN, "aaa")
        result = num.digit_to_int("f")
        assert result == expected

    
    def test_digit_to_int_negative_more_characters(self):
        sysN = cn.CustomNumeralSystem("paf")  # 0 1 2
        num = cn.CustomNumber(sysN, "aaa")
        with pytest.raises(Exception):
            result = num.digit_to_int("aa")

    
    def test_digit_to_int_negative_empty(self):
        sysN = cn.CustomNumeralSystem("paf")  # 0 1 2
        num = cn.CustomNumber(sysN, "aaa")
        with pytest.raises(Exception):
            result = num.digit_to_int("")

    
    def test_hex_to_decimal(self):
        expected = 240
        sysN = cn.CustomNumeralSystem("0123456789abcdef")  # Common hex system
        num = cn.CustomNumber(sysN, "f0")
        result = num.to_decimal()
        assert result == expected

    
    def test_bin_to_decimal(self):
        expected = 101
        sysN = cn.CustomNumeralSystem("01")  # Common bin system
        num = cn.CustomNumber(sysN, "1100101")
        result = num.to_decimal()
        assert result == expected

    
    def test_ternary_to_decimal(self):
        expected = 4
        sysN = cn.CustomNumeralSystem("paf")
        num = cn.CustomNumber(sysN, "aa")
        result = num.to_decimal()
        assert result == expected

    
    def test_full_equality(self):
        expected = True
        sysN1 = cn.CustomNumeralSystem("paf")
        numN1 = cn.CustomNumber(sysN1, "aa")
        sysN2 = cn.CustomNumeralSystem("paf")
        numN2 = cn.CustomNumber(sysN2, "aa")
        result = numN1 == numN2
        assert result == expected

    
    def test_equality_different_numbers(self):
        expected = False
        sysN1 = cn.CustomNumeralSystem("paf")
        numN1 = cn.CustomNumber(sysN1, "aa")
        sysN2 = cn.CustomNumeralSystem("paf")
        numN2 = cn.CustomNumber(sysN2, "aaa")
        result = numN1 == numN2
        assert result == expected

    
    def test_equality_different_systems(self):
        sysN1 = cn.CustomNumeralSystem("paf")
        numN1 = cn.CustomNumber(sysN1, "aa")
        sysN2 = cn.CustomNumeralSystem("paft")
        numN2 = cn.CustomNumber(sysN2, "aa")
        with pytest.raises(Exception):
            result = numN1 == numN2

    
    def test_inequality(self):
        expected = True
        sysN1 = cn.CustomNumeralSystem("paf")
        numN1 = cn.CustomNumber(sysN1, "aa")
        sysN2 = cn.CustomNumeralSystem("paf")
        numN2 = cn.CustomNumber(sysN2, "a")
        result = numN1 != numN2
        assert result == expected

    
    def test_gt(self):
        expected = True
        sysN1 = cn.CustomNumeralSystem("paf")
        numN1 = cn.CustomNumber(sysN1, "f")
        sysN2 = cn.CustomNumeralSystem("paf")
        numN2 = cn.CustomNumber(sysN2, "a")
        result = numN1 > numN2
        assert result == expected

    
    def test_ge(self):
        expected = True
        sysN1 = cn.CustomNumeralSystem("paf")
        numN1 = cn.CustomNumber(sysN1, "f")
        sysN2 = cn.CustomNumeralSystem("paf")
        numN2 = cn.CustomNumber(sysN2, "p")
        result = numN1 >= numN2
        assert result == expected

    
    def test_lt(self):
        expected = True
        sysN1 = cn.CustomNumeralSystem("paf")
        numN1 = cn.CustomNumber(sysN1, "p")
        sysN2 = cn.CustomNumeralSystem("paf")
        numN2 = cn.CustomNumber(sysN2, "a")
        result = numN1 < numN2
        assert result == expected

    
    def test_le(self):
        expected = True
        sysN1 = cn.CustomNumeralSystem("paf")
        numN1 = cn.CustomNumber(sysN1, "p")
        sysN2 = cn.CustomNumeralSystem("paf")
        numN2 = cn.CustomNumber(sysN2, "a")
        result = numN1 <= numN2
        assert result == expected

    
    def test_addition(self):
        expected = "a"
        sysN1 = cn.CustomNumeralSystem("paf")  # 0 1 2
        numN1 = cn.CustomNumber(sysN1, "p")
        sysN2 = cn.CustomNumeralSystem("paf")
        numN2 = cn.CustomNumber(sysN2, "a")
        result = numN1 + numN2
        assert str(result) == expected

    
    def test_subtraction(self):
        expected = "a"
        sysN1 = cn.CustomNumeralSystem("paf")  # 0 1 2
        numN1 = cn.CustomNumber(sysN1, "f")
        sysN2 = cn.CustomNumeralSystem("paf")
        numN2 = cn.CustomNumber(sysN2, "a")
        result = numN1 - numN2
        assert str(result) == expected

    
    def test_augmented_addition(self):
        expected1 = "f"
        expected2 = "a"
        sysN1 = cn.CustomNumeralSystem("paf")  # 0 1 2
        numN1 = cn.CustomNumber(sysN1, "a")
        sysN2 = cn.CustomNumeralSystem("paf")
        numN2 = cn.CustomNumber(sysN2, "a")
        numN1 += numN2
        assert str(numN1) == expected1
        assert str(numN2) == expected2

    
    def test_augmented_subtraction(self):
        expected1 = "p"
        expected2 = "a"
        sysN1 = cn.CustomNumeralSystem("paf")  # 0 1 2
        numN1 = cn.CustomNumber(sysN1, "a")
        sysN2 = cn.CustomNumeralSystem("paf")
        numN2 = cn.CustomNumber(sysN2, "a")
        numN1 -= numN2
        assert str(numN1) == expected1
        assert str(numN2) == expected2

    
    def test_int_to_digit(self):
        expected = "a"
        sysN = cn.CustomNumeralSystem("paf")  # 0 1 2
        num = cn.CustomNumber(sysN, "aaa")
        result = num.int_to_digit(1)
        assert result == expected

    
    def test_decimal_to_hex(self):
        expected = "1df"
        sysN = cn.CustomNumeralSystem("0123456789abcdef")  # Common hex system
        num = cn.CustomNumber(sysN, "f0")  # The value is irrelevant here, we just want to instantiate
        num.from_decimal(479)
        result = str(num)
        assert result == expected

    
    def test_subtraction_negative_number_result(self):
        expected = "-a"  # -1
        sysN1 = cn.CustomNumeralSystem("paf")  # 0 1 2
        numN1 = cn.CustomNumber(sysN1, "a")
        numN2 = cn.CustomNumber(sysN1, "f")
        result = numN1 - numN2
        assert str(result) == expected

    
    def test_absolute_value_positive_signed(self):
        expected = "a"
        original = "a"
        sysN = cn.CustomNumeralSystem("paf")  # 0 1 2
        num = cn.CustomNumber(sysN, "+a")
        result = abs(num)
        assert str(num) == original
        assert str(result) == expected

    
    def test_absolute_value_negative_number(self):
        expected = "a"
        original = "-a"
        sysN = cn.CustomNumeralSystem("paf")  # 0 1 2
        num = cn.CustomNumber(sysN, original)
        result = abs(num)
        assert str(num) == original
        assert str(result) == expected

    
    def test_negative_number_subtraction1(self):
        expected = "p"  # 0
        sysN1 = cn.CustomNumeralSystem("paf")  # 0 1 2
        numN1 = cn.CustomNumber(sysN1, "-a")
        numN2 = cn.CustomNumber(sysN1, "-a")
        result = numN1 - numN2
        assert str(result) == expected

    
    def test_negative_number_subtraction2(self):
        expected = "-f"  # -2
        sysN1 = cn.CustomNumeralSystem("paf")  # 0 1 2
        numN1 = cn.CustomNumber(sysN1, "-a")
        numN2 = cn.CustomNumber(sysN1, "a")
        result = numN1 - numN2
        assert str(result) == expected

    
    def test_negative_number_addition1(self):
        expected = "-f"  # -2
        sysN1 = cn.CustomNumeralSystem("paf")  # 0 1 2
        numN1 = cn.CustomNumber(sysN1, "-a")
        numN2 = cn.CustomNumber(sysN1, "-a")
        result = numN1 + numN2
        assert str(result) == expected

    
    def test_negative_number_addition2(self):
        expected = "-a"  # -1
        sysN1 = cn.CustomNumeralSystem("paf")  # 0 1 2
        numN1 = cn.CustomNumber(sysN1, "-f")
        numN2 = cn.CustomNumber(sysN1, "a")
        result = numN1 + numN2
        assert str(result) == expected

    
    def test_multiplication(self):
        expected = "25"
        sysN1 = cn.CustomNumeralSystem("0123456789")  # Common decimal system
        numN1 = cn.CustomNumber(sysN1, "5")
        numN2 = cn.CustomNumber(sysN1, "5")
        result = numN1 * numN2
        assert str(result) == expected

    
    def test_division(self):
        expected = "1"
        sysN1 = cn.CustomNumeralSystem("0123456789")  # Common decimal system
        numN1 = cn.CustomNumber(sysN1, "5")
        numN2 = cn.CustomNumber(sysN1, "5")
        result = numN1 / numN2
        assert str(result) == expected

    
    def test_power(self):
        expected = "25"
        sysN1 = cn.CustomNumeralSystem("0123456789")  # Common decimal system
        numN1 = cn.CustomNumber(sysN1, "5")
        numN2 = cn.CustomNumber(sysN1, "2")
        result = numN1**numN2
        assert str(result) == expected

    
    def test_modulo1(self):
        expected = "1"
        sysN1 = cn.CustomNumeralSystem("0123456789")  # Common decimal system
        numN1 = cn.CustomNumber(sysN1, "5")
        numN2 = cn.CustomNumber(sysN1, "2")
        result = numN1 % numN2
        assert str(result) == expected

    
    def test_modulo2(self):
        expected = "0"
        sysN1 = cn.CustomNumeralSystem("0123456789")  # Common decimal system
        numN1 = cn.CustomNumber(sysN1, "5")
        numN2 = cn.CustomNumber(sysN1, "5")
        result = numN1 % numN2
        assert str(result) == expected
    
    
    def test_issue2(self):
        expected = "bc"
        original = "-bc"
        sysN = cn.CustomNumeralSystem("abc")  # 0 1 2
        num = cn.CustomNumber(sysN, original)
        result = abs(num)
        assert str(num) == original
        assert str(result) == expected

