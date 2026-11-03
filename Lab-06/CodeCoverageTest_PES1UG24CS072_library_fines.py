import pytest
from library_fines import late_fine, can_borrow, renewal_status


def test_invalid_inputs():
    with pytest.raises(ValueError, match="unknown member"):
        late_fine("unknown", 10, False)

    with pytest.raises(ValueError, match="invalid days"):
        late_fine("student", -1, False)


def test_fine_paths():
    assert late_fine("student", 14, False) == 0
    assert late_fine("faculty", 231, True) == 350


def test_borrow_paths():
    assert can_borrow(0, 101, "student") is False
    assert can_borrow(9, 0, "faculty") is True
    assert can_borrow(2, 0, "student") is True


def test_renewal_paths():
    assert renewal_status(0, True, 1) == "denied"
    assert renewal_status(2, False, 1) == "limit reached"
    assert renewal_status(0, False, -1) == "overdue"
    assert renewal_status(0, False, 0) == "renewed"
