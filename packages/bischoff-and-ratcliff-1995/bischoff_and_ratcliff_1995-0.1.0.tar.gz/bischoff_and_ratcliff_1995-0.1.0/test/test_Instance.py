import json
import pytest

import bischoff_and_ratcliff_1995 as br95


def expected(case_name):
    with open(f"test/data/{case_name}.json", "r") as file:
        expected = json.load(file)
    return expected


@pytest.mark.parametrize(
    "number_of_box_types, seed, case_name",
    [
        (8, 2507305, "case_1"),
        (10, 2508405, "case_2"),
        (12, 2506505, "case_3"),
        (8, 2506105, "case_4"),
        (10, 2504605, "case_5"),
        (12, 2502605, "case_6"),
        (3, 2502505, "case_7"),
    ],
)
def test_case(number_of_box_types, seed, case_name):
    actual = br95.Instance(
        C={"length": 587, "width": 233, "height": 220},
        n=number_of_box_types,
        a=[30, 25, 20],
        b=[120, 100, 80],
        L=2,
        s=seed,
    )
    assert actual.to_dict() == expected(case_name)
    return
