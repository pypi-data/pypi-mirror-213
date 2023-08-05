r"""Swiss-army knife for custom numeral systems.

Copyright (c) 2023 Evgueni Antonov. All rights reserved.
This work is licensed under the terms of the MIT license.
See LICENSE file.

Project homepage and documentation:
https://github.com/StrayFeral/custom_numbers
"""

import re
import math
from typing import List

__version__: str = "1.1.3"
__author__: str = r"Evgueni Antonov (Evgueni.Antonov@gmail.com)"



class CustomNumeralSystem:
    r"""Definition of custom numeral systems with basic consistency validation.

    Args:
        digits: String of characters to be perceived as digits.
                The character order is important: 'smallest' is the first on the left!
                This string length would be the numeral system base.
                Obviously each "digit" would consist of a single-
                character.

                Forbidden characters: -, +, *, /, % and space

    For the needs of basic validation, the equality and iequality Python
    operators were implemented, so you could compare two objects.

    However the comparisson would be by the list (basically the string)
    of the characters representing the digits, rather than standard
    Python object (reference) comparisson.

    Example:
        sys1 = CustomNumeralSystem("012ab") # Custom Base5 numeral system
        sys2 = CustomNumeralSystem("mab87")

        # Details
        sys3 = CustomNumeralSystem("paf") # Custom Base3 numeral system
        # Example counting from the smallest possible value:
        # "p" # "p" assumes to be the analog of the zero
        # "a"
        # "f"
        # "ap"
        # "aa"
        # and so on. You get the idea.

        # COMPARISSON
        sys1 = cn.CustomNumeralSystem("paf")
        sys2 = cn.CustomNumeralSystem("paf")

        # The two objects are different, despite being initialized with
        # the same value
        id(sys1) == id(sys2) # False

        # However the set of characters (the digits) is the same, the
        # base is the same, so I accept they are the same numeral systems
        sys1 == sys2 # True

        # And you could also test for inequality
        sys1 = cn.CustomNumeralSystem("paf")
        sys2 = cn.CustomNumeralSystem("paz")
        sys1 != sys2 # True
    """

    _FORBIDDENCHARACTERS: str = r"+-*/%\s"

    
    def __init__(self, digits: str) -> None:
        self._digits: str = digits
        self._base: int = len(digits)

        if len(digits) == 0:
            raise ValueError("Empty 'digits' argument given.")

        digit_set = set([x for x in digits])
        if len(digits) != len(digit_set):
            raise ValueError("Duplicate characters in the 'digits' argument.")

        # I don't think we need to put a limit here. Let the user decide.
        # if self._base > self._MAXBASE:
        #    raise ValueError(f"Unsupported numeral base given {self._base}. Maximum base supported is {self._MAXBASE}.")

    
    def __repr__(self) -> str:
        return self._digits

    
    def __eq__(self, other) -> bool:
        """This compare both the digits and the Base."""
        return self._digits == str(other)

    
    def __ne__(self, other) -> bool:
        """This compare both the digits and the Base."""
        return self._digits != str(other)

    
    @property
    def forbidden_characters(self) -> str:
        return self._FORBIDDENCHARACTERS

    
    @property
    def base(self) -> int:
        return self._base

    
    def valid_number(self, number: str) -> bool:
        r"""Validation: Is this digit belonging to this numeral system?"""

        if len(number) == 0:
            raise ValueError("Passed an empty string as a 'number' argument.")

        # Test if string contains forbidden characters.
        # Generally I dislike the + string concatenation, but as an
        # f-string the regexes triggered some warnings, despite I
        # escaped them.
        regex_str = r"[" + re.escape(self._FORBIDDENCHARACTERS) + r"]"
        regex = re.compile(regex_str)
        if regex.search(number):
            return False

        # Test if string contains any characters outside the defined set
        regex_str = r"[^" + re.escape(self._digits) + r"]"
        regex = re.compile(regex_str)
        if regex.search(number):
            return False

        return True



class CustomNumber:
    r"""Definition of a number from the CustomNumericalSystem.

    Args:
        numeral_system: The custom numeral system the number is going to be from.
        number: The number as a string. Signed numbers are supported.

    Basic math operations are supported trough standard Python operators.

    Comparisson operators are supported as well.

    Example:
        sysN = cn.CustomNumeralSystem("paf")
        numN1 = cn.CustomNumber(sysN, "-a") # A negative number
        numN2 = cn.CustomNumber(sysN, "a")  # A positive number
        numN3 = cn.CustomNumber(sysN, "+a") # A positive number
    """

    _POSITIVE: str = r"+"
    _NEGATIVE: str = r"-"

    
    def __init__(self, numeral_system: CustomNumeralSystem, number: str) -> None:
        self._numeral_system: CustomNumeralSystem = numeral_system
        self._init_value: str = number  # Just in case we will keep the original value
        self._value: str = number

        self.absolute()  # This will set the sign as well

        if not numeral_system.valid_number(self._value):
            raise ValueError("Invalid characters in number, which are not in the chosen numeral system.")

    
    def __repr__(self) -> str:
        if self._sign == self._NEGATIVE:
            return f"-{self._value}"
        return self._value

    
    @property
    def numeral_system(self) -> CustomNumeralSystem:
        return self._numeral_system

    
    @property
    def init_value(self) -> str:
        r"""Return the value the class was initialized with, as it was originally passed to the class."""
        return self._init_value

    
    def __eq__(self, other) -> bool:
        if self.numeral_system != other.numeral_system:
            raise ValueError("Numbers must be from the same numeral system.")
        return self.to_decimal() == other.to_decimal()

    
    def __ne__(self, other) -> bool:
        if self.numeral_system != other.numeral_system:
            raise ValueError("Numbers must be from the same numeral system.")
        return self.to_decimal() != other.to_decimal()

    
    def __ge__(self, other) -> bool:
        if self.numeral_system != other.numeral_system:
            raise ValueError("Numbers must be from the same numeral system.")
        return self.to_decimal() >= other.to_decimal()

    
    def __gt__(self, other) -> bool:
        if self.numeral_system != other.numeral_system:
            raise ValueError("Numbers must be from the same numeral system.")
        return self.to_decimal() > other.to_decimal()

    
    def __lt__(self, other) -> bool:
        if self.numeral_system != other.numeral_system:
            raise ValueError("Numbers must be from the same numeral system.")
        return self.to_decimal() < other.to_decimal()

    
    def __le__(self, other) -> bool:
        if self.numeral_system != other.numeral_system:
            raise ValueError("Numbers must be from the same numeral system.")
        return self.to_decimal() <= other.to_decimal()

    
    def __add__(self, other) -> object:
        if self.numeral_system != other.numeral_system:
            raise ValueError("Numbers must be from the same numeral system.")
        result: int = self.to_decimal() + other.to_decimal()
        num: CustomNumber = CustomNumber(self.numeral_system, str(self.numeral_system)[0])  # Dummy init_value
        num.from_decimal(result)
        return num

    
    def __sub__(self, other) -> object:
        if self.numeral_system != other.numeral_system:
            raise ValueError("Numbers must be from the same numeral system.")
        result: int = self.to_decimal() - other.to_decimal()
        num: CustomNumber = CustomNumber(self.numeral_system, str(self.numeral_system)[0])  # Dummy init_value
        num.from_decimal(result)
        return num

    
    def __mul__(self, other) -> object:
        if self.numeral_system != other.numeral_system:
            raise ValueError("Numbers must be from the same numeral system.")
        result: int = self.to_decimal() * other.to_decimal()
        num: CustomNumber = CustomNumber(self.numeral_system, str(self.numeral_system)[0])  # Dummy init_value
        num.from_decimal(result)
        return num

    
    def __floordiv__(self, other) -> object:
        if self.numeral_system != other.numeral_system:
            raise ValueError("Numbers must be from the same numeral system.")
        result: int = self.to_decimal() // other.to_decimal()
        num: CustomNumber = CustomNumber(self.numeral_system, str(self.numeral_system)[0])  # Dummy init_value
        num.from_decimal(result)
        return num

    
    def __truediv__(self, other) -> object:
        return self.__floordiv__(other)

    
    def __div__(self, other) -> object:
        return self.__floordiv__(other)

    
    def __pow__(self, other) -> object:
        if self.numeral_system != other.numeral_system:
            raise ValueError("Numbers must be from the same numeral system.")
        result: int = self.to_decimal() ** other.to_decimal()
        num: CustomNumber = CustomNumber(self.numeral_system, str(self.numeral_system)[0])  # Dummy init_value
        num.from_decimal(result)
        return num

    
    def __mod__(self, other) -> object:
        if self.numeral_system != other.numeral_system:
            raise ValueError("Numbers must be from the same numeral system.")
        result: int = self.to_decimal() % other.to_decimal()
        num: CustomNumber = CustomNumber(self.numeral_system, str(self.numeral_system)[0])  # Dummy init_value
        num.from_decimal(result)
        return num

    
    def absolute(self, number: str = "") -> str:
        """Returns the absolute value."""

        num: str = number
        if len(number) == 0:
            num = self._value

        sign: str = self._POSITIVE
        if num[0] == self._NEGATIVE:
            sign = self._NEGATIVE

        if num[0] == self._POSITIVE or num[0] == self._NEGATIVE:
            num = num[1:]  # Strip sign

        if len(number) == 0:
            self._value = num
            self._sign = sign

        return num

    
    def digit_to_int(self, digit: str) -> int:
        r"""Fastest and simplest possible conversion. Left-most one is the zero."""

        if len(digit) != 1:
            raise ValueError("Invalid digit. Must be one character.")
        return str(self._numeral_system).index(digit)

    
    def int_to_digit(self, i: int) -> str:
        return str(self.numeral_system)[i]

    
    def to_decimal(self) -> int:
        r"""Converts a number of a custom numeral system to a decimal integer."""

        power = 0
        int_value = 0

        for digit in self._value[::-1]:
            int_value += self.digit_to_int(digit) * (self._numeral_system.base**power)
            power += 1

        if self._sign == self._NEGATIVE:
            int_value = -abs(int_value)

        return int_value

    
    def from_decimal(self, number: int) -> None:
        r"""Converts the number to the current numeral system and sets the internal value to it."""

        sign: str = self._POSITIVE
        if number < 0:
            sign = self._NEGATIVE
        self._sign = sign

        value: str = ""
        num = float(abs(number))
        while int(num) > 0:
            num = num / self.numeral_system.base
            remainder, integr = math.modf(num)
            remainder *= self.numeral_system.base
            value = f"{self.int_to_digit(int(remainder))}{value}"

        if number == 0:
            value = f"{self.int_to_digit(0)}"

        self._value = value



class GearIterator:
    r"""GearIterator.

    Briefly simulates old gear counters, like the old cars odometer.

    The class is serializable, works with both pickle and dill.
    The class implements the context management protocol.

    Args:
        numeral_system: Custom numeral system. Mind the order of symbols!
        min_length: Minimum length, default is zero
        max_length: Maximum length, default is zero - means no limit
        init_value: Value to initialize with

    Returns:
        str
    """

    
    def __init__(self, numeral_system: CustomNumeralSystem, min_length: int = 0, max_length: int = 0, init_value: str = "") -> None:
        self._numeral_system: CustomNumeralSystem = numeral_system
        self._symbol_list: List[str] = [x for x in str(numeral_system)]
        self._min_length: int = min_length
        self._max_length: int = max_length
        self._init_value: str = init_value
        self._init_value_returned: bool = False
        self._index: int = 0
        self._combinations: int = 0

        # Basic validation ...
        if max_length > 0 and min_length > max_length:
            raise ValueError("min_length is greather than max_length.")

        if len(init_value) > 0:
            if len(init_value) < min_length or (max_length > 0 and len(init_value) > max_length):
                raise ValueError("Incorrect init_value length.")

            if not numeral_system.valid_number(init_value):
                raise ValueError("Invalid characters in init_value, which are not in the chosen numeral system.")

            if init_value == str(numeral_system)[0] * len(init_value):
                raise ValueError("Init_value contains only smallest digits (zero-equivalents).")

            # Strip the leading "zeroes"
            while init_value[0] == str(numeral_system)[0]:
                init_value = init_value[1:]

            self._init_value = init_value[::-1]  # Reverse the string

        min_len: int = min_length
        if min_len == 0:
            min_len = 1

        self._gears: List[list] = []

        # Initialization with init_value
        for symbol in self._init_value:
            seq = self._symbol_list.copy()

            while seq[0] != symbol:
                seq.pop(0)

            self._gears.append(seq)

        # Additional initialization until min_length is reached
        for i in range(len(self._gears), min_len):
            seq = self._symbol_list.copy()

            if len(self._init_value) > 0 and i < len(self._init_value):
                symbol = self._init_value[i]
                while seq[0] != symbol:
                    seq.pop(0)

            self._gears.append(seq)

    
    @property
    def combinations(self) -> int:
        """Combinations calculation.

        People may argue with me here, but in a set of only two values,
        like {0, 1}, if we make two gears out of these and rotate them,
        the values would be:
        # 0
        # 1
        # 10
        # 11
        And while for mathematicians "01" == "10", for me they are not
        the same.
        """

        if self._combinations == 0:
            n: int = len(self._symbol_list)
            r: int = self._max_length
            c: int = n * r

            self._combinations = c

        return self._combinations

    
    def __repr__(self) -> str:
        result: str = ""
        for gear in self._gears:
            result += gear[0]
        return result[::-1]  # Reverse the string

    
    def __iter__(self) -> object:
        return self

    
    # l = list(generator) # internally call next() until exhaustion
    def __next__(self) -> str:
        if not self._init_value_returned:
            self._init_value_returned = True
            return repr(self)

        spin_wheels: bool = True
        i = 0
        while spin_wheels:
            self._gears[i].pop(0)

            # Reset gear
            if len(self._gears[i]) == 0:
                self._gears[i] = self._symbol_list.copy()
                i += 1

                # Add a new gear
                if i == len(self._gears) and i < self._max_length:
                    self._gears.append(self._symbol_list.copy())
                    self._gears[i].pop(0)  # Remove the "zero"
                    spin_wheels = False

                if i == self._max_length:
                    raise StopIteration
            else:  # Wheel not yet reached the final set value
                spin_wheels = False

        return repr(self)

    
    def __enter__(self) -> object:
        r"""Context management protocol.

        Not sure we would need this, but it's there.
        """
        return self

    
    def __exit__(self, exc_type: object, exc_value: object, exc_tb: object) -> bool:
        r"""Context management protocol.

        StopIteration exception will not be propagated.

        Not sure we would need this, but it's there.
        """
        return True  # We won't propagate the StopIteration exception
