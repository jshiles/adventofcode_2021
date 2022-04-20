"""
day 18 tests.
"""

import pytest
from functools import reduce
from advent_of_code.day_18 import str2sailfishnumber


def test_add():
    """Test basic addition without reduction req'd"""
    add_1_sfn1 = str2sailfishnumber("[1,2]")
    add_1_sfn2 = str2sailfishnumber("[[3,4],5]")
    add_1_result = str2sailfishnumber("[[1,2],[[3,4],5]]")
    assert add_1_sfn1.add(add_1_sfn2) == add_1_result


def test_split():
    """Test basic splitting without explosion"""

    split_1_sfn = str2sailfishnumber("[1,10]")
    split_1_result = str2sailfishnumber("[1,[5,5]]")
    assert split_1_sfn.split() == split_1_result

    split_2_sfn = str2sailfishnumber("[11, 14]")
    split_2_result = str2sailfishnumber("[[5,6],[7,7]]")
    assert split_2_sfn.split().split() == split_2_result


def test_explode():
    """Test explode function"""

    expl_1_sfn = str2sailfishnumber("[[[[[9,8],1],2],3],4]")
    expl_1_result = str2sailfishnumber("[[[[0,9],2],3],4]")
    assert expl_1_sfn.explode() == expl_1_result

    expl_2_sfn = str2sailfishnumber("[7,[6,[5,[4,[3,2]]]]]")
    expl_2_result = str2sailfishnumber("[7,[6,[5,[7,0]]]]")
    assert expl_2_sfn.explode() == expl_2_result

    expl_3_sfn = str2sailfishnumber("[[6,[5,[4,[3,2]]]],1]")
    expl_3_result = str2sailfishnumber("[[6,[5,[7,0]]],3]")
    assert expl_3_sfn.explode() == expl_3_result

    expl_4_sfn = str2sailfishnumber("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]")
    expl_4_result = str2sailfishnumber("[[3,[2,[8,0]]],[9,[5,[7,0]]]]")
    assert expl_4_sfn.explode().explode() == expl_4_result


def test_magnitude():
    """unit test magnitude computation given their examples."""
    assert str2sailfishnumber("[9,1]").magnitude() == 29
    assert str2sailfishnumber("[1,9]").magnitude() == 21
    assert str2sailfishnumber("[[9,1],[1,9]]").magnitude() == 129
    assert (
        str2sailfishnumber("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]").magnitude()
        == 1384
    )
    assert (
        str2sailfishnumber("[[[[1,1],[2,2]],[3,3]],[4,4]]").magnitude() == 445
    )
    assert (
        str2sailfishnumber("[[[[3,0],[5,3]],[4,4]],[5,5]]").magnitude() == 791
    )
    assert (
        str2sailfishnumber("[[[[5,0],[7,4]],[5,5]],[6,6]]").magnitude() == 1137
    )
    assert (
        str2sailfishnumber(
            "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"
        ).magnitude()
        == 3488
    )


def test_example1():
    """
    Run the first full test example.
    Test end result against desired end result.
    """
    p1_test = str2sailfishnumber("[[[[4,3],4],4],[7,[[8,4],9]]]")
    p2_test = str2sailfishnumber("[1,1]")
    assert p1_test.add(p2_test) == str2sailfishnumber(
        "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
    )

    # same but test "+" operator
    p1_test = str2sailfishnumber("[[[[4,3],4],4],[7,[[8,4],9]]]")
    p2_test = str2sailfishnumber("[1,1]")
    assert p1_test + p2_test == str2sailfishnumber(
        "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
    )


def test_example2():
    """
    Run the second full test example.
    Test end result against desired end result.
    """

    test_input_raw = [
        "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]",
        "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]",
        "[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]",
        "[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]",
        "[7,[5,[[3,8],[1,4]]]]",
        "[[2,[2,2]],[8,[8,1]]]",
        "[2,9]",
        "[1,[[[9,3],9],[[9,0],[0,7]]]]",
        "[[[5,[7,4]],7],1]",
        "[[[[4,2],2],6],[8,7]]",
    ]
    sailfish_nums = [str2sailfishnumber(s) for s in test_input_raw]

    snailfish_num = reduce(lambda a, b: a + b, sailfish_nums)
    assert (snailfish_num) == str2sailfishnumber(
        "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"
    )

    assert snailfish_num.magnitude() == 3488  # the answer.
