class Calculator:
    """ 
    A calculator class with the add/ substract/ multipliy/ divide/ and root methods 

    Attributes
    ----------
    initial_value: float/string (optional)

    Methods
    -------
    """

    def __init__(self, initial_value: float = 0) -> None:
        """
        Construct the calculator instance with the initial_value if provided

        Args:
            initial_value (float, optional): Starting value of the calculator. Defaults to 0.
        """
        self.current_value = initial_value

    def __repr__(self) -> str:
        """
        Show the current_value of the calculator instance when printed

        Returns:
            str: _description_
        """
        return f"🧮 current value: {self.current_value}"

    def remove_integer_decimal(self) -> float:
        """
        Remove the .0 by converting it into integer if the current_value is a float and its fractional part is 0 
        (eg: 10.0)  for better readibility.

        Returns:
            float, integer
        """
        if isinstance(self.current_value, float):
            should_remove_fraction = self.current_value.is_integer()
            transformed_float = (
                int(self.current_value) if should_remove_fraction
                else self.current_value
            )
            self.current_value = transformed_float
            return self.current_value

    def add(self, input: float) -> float:
        """
        Add input value to the current_value

        Args:
            input (float, integer)

        Returns:
            float, integer
        """
        self.current_value += input
        self.remove_integer_decimal()
        print(f"🤖 {self.current_value}")
        return self.current_value

    def substract(self, input: float) -> float:
        """
        Substract input value from the current_value

        Args:
            input (float, integer)

        Returns:
            float, integer
        """
        self.current_value -= input
        self.remove_integer_decimal()
        print(f"🤖 {self.current_value}")
        return self.current_value

    def multiply(self, input: float) -> float:
        """
        Multiply current_value with the input value

        Args:
            input (float,integer)

        Returns:
            float, integer
        """
        self.current_value *= input
        self.remove_integer_decimal()
        print(f"🤖 {self.current_value}")
        return self.current_value

    def divide(self, input: float) -> float:
        """
        Divide current_value by the input value

        Args:
            input (float,integer): input cannot be 0

        Returns:
            float, integer
        """
        try:
            self.current_value /= input
            self.remove_integer_decimal()
            print(f"🤖 {self.current_value} ")

        except (ZeroDivisionError):
            print("🤖 🚫ERR: The divisor cannot be 0 !")
            raise (ZeroDivisionError) from None
            # avoid handling error twice

        return self.current_value

    def root(self, input: float) -> float:
        """
        Take the nth(input) root of current_value

        Args:
            input (float, integer): input cannot be 0

        Returns:
            float, integer
        """
        try:
            self.current_value **= 1/input
            self.remove_integer_decimal()
            print(f"🤖 {self.current_value}")

        except (ZeroDivisionError):
            print("🤖 🚫ERR: Cannot take the 0th root of a number !")
            raise (ZeroDivisionError) from None
            # avoid handling error twice

        return self.current_value

    def reset(self) -> float:
        """
        Reset current_value to 0

        Returns:
            0
        """
        self.current_value = 0
        print(f"🤖 {self.current_value}")

        return self.current_value
