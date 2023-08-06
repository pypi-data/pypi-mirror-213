import numpy as np
import warnings  # warning handling
warnings.filterwarnings("error")  # enable it to be caught in try except block


class Calculator:
    """
    - A calculator class with the add/ substract/ multipliy/ divide/ root/ and reset methods.

    - numpy.float32: single-precision float is used during calculation phase to ignore small discrepancy in resulted from the python default 64 bit double precision float 
    eg) 0.1 * 3 = 0.30000000000000004 
    eg) np.float32(0.1 * 3) ==  0.3 #True

    - Calculation range:
    max: 3.4028235e+38 (np.finfo(np.float32).max)
    min -3.4028235e+38 (np.finfo(np.float32).min)


    Attributes
    ----------
    initial_value: float/string (optional)

    Methods
    -------
    """

    def __init__(self, initial_value=0) -> None:
        """
        Construct the calculator instance with the initial_value if provided

        Args:
            initial_value (float, optional): Starting value of the calculator. Defaults to 0.
        """

        # ensure initial_value type to be float or int to proceed
        type_guard(initial_value)
        self.current_value = initial_value

    def __repr__(self) -> str:
        """
        Show the current_value of the calculator instance when calculator instance is printed

        Returns:
            str: current value of the calculator
        """
        return f"🧮 current value: {self.current_value}"

    def add(self, input: float) -> float:
        """
        Add input value to the current_value 

        Args:
            input (float, integer)

        Returns:
            float, integer
        """
        type_guard(input)

        try:
            self.current_value = float(np.float32(self.current_value + input))
        except RuntimeWarning as err:
            print("🤖: 🚫", err)
            raise
        else:
            self.current_value = remove_integer_decimal(self.current_value)
            s_print(self.current_value)
            return self.current_value

    def substract(self, input: float) -> float:
        """
        Substract input value from the current_value

        Args:
            input (float, integer)

        Returns:
            float, integer
        """
        type_guard(input)

        try:
            self.current_value = float(np.float32(self.current_value - input))
        except RuntimeWarning as err:
            print("🤖: 🚫", err)
            raise
        else:
            self.current_value = remove_integer_decimal(self.current_value)
            s_print(self.current_value)
            return self.current_value

    def multiply(self, input: float) -> float:
        """
        Multiply current_value with the input value

        Args:
            input (float,integer)

        Returns:
            float, integer
        """
        type_guard(input)

        try:
            self.current_value = float(np.float32(self.current_value * input))
        except RuntimeWarning as err:
            print("🤖: 🚫", err)
            raise
        else:
            self.current_value = remove_integer_decimal(self.current_value)
            s_print(self.current_value)
            return self.current_value

    def divide(self, input: float) -> float:
        """
        Divide current_value by the input value

        Args:
            input (float,integer): input cannot be 0

        Returns:
            float, integer
        """

        type_guard(input)

        try:
            self.current_value = float(np.float32(self.current_value / input))
        except ZeroDivisionError as err:
            print("🤖: 🚫", err)
            raise

        except RuntimeWarning as err:
            print("🤖: 🚫", err)
            raise

        else:
            self.current_value = remove_integer_decimal(self.current_value)
            s_print(self.current_value)
            return self.current_value

    def root(self, input: float) -> float:
        """
        Take the nth(input) root of the current_value.
        If the operation results in a complex number, raise ValueError

        Args:
            input (float, integer): input cannot be 0

        Returns:
            float, integer
        """

        type_guard(input)

        try:
            self.current_value = float(np.float32(
                (self.current_value) ** (1/input)))

        except ZeroDivisionError:
            print("🤖: 🚫", "cannot take the 0th root of a number")
            raise

        except TypeError as er:
            print("🤖: 🚫", er)
            raise

        else:
            self.current_value = remove_integer_decimal(self.current_value)
            s_print(self.current_value)
            return self.current_value

    def reset(self) -> float:
        """
        Reset current_value to 0

        Returns:
            0
        """
        self.current_value = 0
        s_print(self.current_value)
        return self.current_value


# helper functions

def type_guard(input) -> None:
    """
    If the input type is not float or int, raise TypeError 

    Args:
        input (float, int): input for checking
    """
    if not isinstance(input, (int, float)):
        print(
            f"🤖 🚫ERR: Input type {type(input)} is not allowed, only accepts operation of type int or float")
        raise (TypeError)


def remove_integer_decimal(input: float) -> float:
    """
    If the input value is a float and its fractional part is 0, remove the 
    .0 by converting it into integer (eg: 10.0)  for better readibility.
    Returns:
         float, integer
     """
    should_remove_fractional_part = input.is_integer()
    result = int(input) if should_remove_fractional_part else input
    return result


def s_print(input):
    """
    Only print out input when the file is executed as a script,
    used for development and debugging

    Args:
        input (float): result of the calculation
    """
    if __name__ == '__main__':
        print("🤖 ", input)
