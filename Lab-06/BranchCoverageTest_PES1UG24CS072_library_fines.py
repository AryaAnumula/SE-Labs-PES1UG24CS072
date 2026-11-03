import pytest
from library_fines import late_fine, can_borrow, renewal_status


def test_unknown_member():
    with pytest.raises(ValueError, match="unknown member"):
        late_fine("unknown", 10, False)


def test_negative_days():
    with pytest.raises(ValueError, match="invalid days"):
        late_fine("student", -1, False)


def test_on_time():
    assert late_fine("student", 14, False) == 0


def test_overdue_below_cap():
    assert late_fine("student", 15, False) == 2


def test_capped_and_damaged():
    assert late_fine("faculty", 231, True) == 350


def test_borrow_high_fine():
    assert can_borrow(0, 101, "student") is False


def test_borrow_faculty():
    assert can_borrow(9, 100, "faculty") is True


def test_borrow_student():
    assert can_borrow(3, 100, "student") is False


def test_renewal_reserved():
    assert renewal_status(0, True, 1) == "denied"


def test_renewal_limit():
    assert renewal_status(2, False, 1) == "limit reached"


def test_renewal_overdue():
    assert renewal_status(1, False, -1) == "overdue"


def test_renewal_success():
    assert renewal_status(1, False, 0) == "renewed"
