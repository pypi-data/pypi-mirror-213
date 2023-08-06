# Simple Calculator

This is a simple calculator that can add, subtract, multiply, divide and take the nth root of a number.
It's a part of a school project at https://turingcollege.com.

In the notebook run the first code cell
Then in the second code cell you can use:
- calc.add()
- calc.sub()
- calc.multi()
- calc.div()
- calc.root()
- calc.reset()

They all take 1 argument except for calc.reset() which takes 0 arguments and calc.root which takes 2.
The first argument in calc.root is the root and the second argument is the value. calc.root will not be saved in the memory.

The Calculator also has it's own memory, so it will start from 0 and will do the calculations from it's memory as you go until you use calc.reset()

Examples:
-- calc.add(5)
5

-- calc.sub(2)
3

-- calc.multi(2)
6

-- calc.div(2)
3

-- calc.reset()
0

-- calc.root(2, 25)
5