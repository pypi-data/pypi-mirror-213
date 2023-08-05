"""
This module implements basic calculator functionality.
"""

class Calculator:
    INITIAL_VALUE: int = 0
    value: int = INITIAL_VALUE

    def memory(self) -> float:
        """
        Return the current value stored in the calculator's memory

        Args:
            Takes in no arguments

        Returns:
            float: The current value stored in the calulator
        """
        return self.value

    def add(self, num: float = 0) -> float:
        """
        Add value to the calculator's current value.

        Args:
            num (float): The number to add to the calculator's current value.

        Returns:
            float: The value of num added to the calculator's current value
        """        
        self.value += num
        return self.value

    def subtract(self, num:float = 0) -> float:
        """
        Subtract value from the calculator's current value.

        Args:
            num (float): The number to subtract from the calculator's current value.

        Returns:
            float: The value of num subtracted from the calculator's current value
        """
        self.value -= num
        return self.value

    def multiply(self, num:float = 1) -> float:
        """
        Multiply value of the calculator's current value.

        Args:
            num (float): The number to multiply the calculator's current value by.

        Returns:
            float: The value of num multiplied to the calculator's current value
        """
        self.value *= num
        return self.value

    def divide(self, num:float = 1) -> float:
        """
        Divide value of the calculator's current value.

        Args:
            num (float): The number to divide the calculator's current value by.

        Returns:
            float: The value of num divided by the calculator's current value
        """
        self.value /= num
        return self.value

    def nroot(self, num:float, n:int) -> float:
        """
        Calculate the nth root of a number

        Args:
            num (float): The number to calculate the root of.
            n (int): The degree of the root.

        Returns:
            float: The nth root of the number.
        """
        if num < 0 and n % 2 == 0:
            raise ValueError("Cannot calculate even root of a negative number")
        
        if type(n) == float:
            raise ValueError("The degree of the root must an integer")
        
        return num ** (1/n)
    
    def reset(self) -> int:
        """
        Reset the calculators value in memory back to zero.
        
        Args:
            Takes in no arguments

        Returns:
            int: The default value of the calulator
        """
        self.value = self.INITIAL_VALUE
        return self.value
    