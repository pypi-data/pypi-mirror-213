class Calculator:
    ''' A simple calculator that can do addition, subtraction, 
    multiplication, division and take the nth root of a number. 
    '''

    def __init__(self, memory: float = 0.0):
        self.memory = memory

    # Return the memory when printing Calculator class
    def __str__(self):
        return f"{self.memory}"

    def add(self, value: float):
        '''Add the attribute to the memory'''
        print(f"{self.memory} + {value} =", end=" ")
        self.memory += value
        return self.memory

    def sub(self, value: float):
        '''Subtract the attribute from the memory'''
        print(f"{self.memory} - {value} =", end=" ")
        self.memory -= value
        return self.memory

    def multi(self, value: float):
        '''Multiply the attribute with the memory'''
        print(f"{self.memory} * {value} =", end=" ")
        self.memory *= value
        return self.memory

    def div(self, value: float):
        '''Divide the attribute by the memory'''
        print(f"{self.memory} / {value} =", end=" ")
        self.memory /= value
        return self.memory

    def root(self, root: float, value: float):
        '''Take the nth root of a number
        The first attribute is the nth root
        The second attribute is the value

        Calculator.root(2, 25)
        5.0
        '''
        return value**(1/root)

    def reset(self):
        '''Sets the memory back to 0'''
        self.memory = 0
        return self.memory
