import bischoff_and_ratcliff_1995 as br95


def test_case_1():
    SEED = 7
    NUMBER_OF_RANDOM_NUMBERS = 13
    random = br95.Random(SEED)
    actual = [random.integer() for i in range(NUMBER_OF_RANDOM_NUMBERS)]
    expected = [
        117649,
        1977326743,
        621132276,
        452154665,
        1566311569,
        1143995257,
        707192808,
        1615021558,
        1621510873,
        1165762081,
        1469983786,
        1365616214,
        1753973209,
    ]
    print(actual)
    print(expected)
    assert actual == expected
    return
