from src.calculator import Calculator


def test_calculator():

    calc = Calculator()

    assert calc.add(2) == 2.0
    assert calc.add(5) == 7.0
    assert calc.add(100) == 107.0

    assert calc.sub(2) == 105.0
    assert calc.sub(10) == 95.0
    assert calc.sub(15) == 80.0

    assert calc.multi(1) == 80.0
    assert calc.multi(5) == 400.0
    assert calc.multi(2) == 800.0

    assert calc.div(2) == 400.0
    assert calc.div(5) == 80.0
    assert calc.div(10) == 8.0

    assert calc.root(2, 25) == 5.0
    assert calc.root(5, 75) == 2.3714406097793117
    assert calc.root(7, 25) == 1.583819608766579

    assert calc.reset() == 0
