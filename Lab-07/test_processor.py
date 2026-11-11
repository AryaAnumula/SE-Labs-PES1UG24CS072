"""Hypothesis fuzz tests for the Lab 7 library-fines application.

Malformed member IDs and day lists should return None. Missing/blank titles
should return an empty code; a one-word title should use its first initial.
The original application intentionally fails these robustness properties.
"""

import string

import pytest
from hypothesis import example, given, strategies as st

from processor import parse_member_id, shelf_code, total_fine


WORDS = st.text(alphabet=string.ascii_letters, min_size=1, max_size=30)
NON_TEXT = st.one_of(
    st.integers(),
    st.floats(),
    st.booleans(),
    st.binary(),
    st.lists(st.integers(), max_size=10),
    st.dictionaries(st.text(max_size=10), st.integers(), max_size=5),
)


@given(st.text() | st.none())
def test_parse_member_id_no_crash(value):
    """Arbitrary Unicode or None must not cause an unhandled exception."""
    result = parse_member_id(value)
    if result is not None:
        assert isinstance(result, tuple) and len(result) == 2
        member_type, number = result
        assert isinstance(member_type, str) and member_type
        assert member_type == member_type.upper()
        assert type(number) is int and number >= 0


@given(st.text() | st.none())
def test_total_fine_no_crash(value):
    """Reject malformed input safely or return a nonnegative integer fine."""
    result = total_fine(value)
    assert result is None or (type(result) is int and result >= 0)


@given(st.text() | st.none())
def test_shelf_code_no_crash(value):
    """Even missing titles must have a safe string result."""
    assert isinstance(shelf_code(value), str)


@given(member_type=WORDS, number=st.integers(min_value=0, max_value=10**30))
@example(member_type="stu", number=1023)
def test_parse_member_id_valid(member_type, number):
    assert parse_member_id(f"{member_type}-{number}") == (
        member_type.upper(), number
    )


@given(days=st.lists(st.integers(min_value=0, max_value=10**12), min_size=1))
@example(days=[10, 20, 30])
@example(days=[0, 14, 15])
def test_total_fine_valid(days):
    """Each book has 14 free days and costs 2 per overdue day."""
    days_csv = ",".join(str(day) for day in days)
    expected = 2 * sum(max(day - 14, 0) for day in days)
    assert total_fine(days_csv) == expected


@given(words=st.lists(WORDS, min_size=2, max_size=10))
def test_shelf_code_valid(words):
    expected = (words[0][0] + words[1][0]).upper()
    assert shelf_code(" \t".join(words)) == expected


@given(st.text().filter(lambda value: "-" not in value))
def test_parse_member_id_missing_separator(value):
    assert parse_member_id(value) is None


@given(st.integers(min_value=0, max_value=10**12))
def test_total_fine_malformed_field(days):
    """Do not silently ignore an invalid field or return a partial fine."""
    assert total_fine(f"{days},invalid") is None


@given(st.text(alphabet=" \t\n\r\v\f"))
def test_shelf_code_blank(value):
    assert shelf_code(value) == ""


@given(WORDS)
def test_shelf_code_one_word(word):
    assert shelf_code(word) == word[0].upper()


@pytest.mark.parametrize(
    "function, expected",
    [(parse_member_id, None), (total_fine, None), (shelf_code, "")],
    ids=["parse_member_id", "total_fine", "shelf_code"],
)
@given(value=NON_TEXT)
def test_non_text_inputs(function, expected, value):
    assert function(value) == expected
