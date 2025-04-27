"""
Unit tests dedicated to the `BankAccount` dataclass.
"""

from decimal import Decimal

import pytest

from banking import BankAccount


@pytest.fixture
def fresh_account():
    """Create an empty account for each test."""
    return BankAccount(id="acc-1", name="Alice")


def test_initial_balance_zero(fresh_account):
    assert fresh_account.balance == Decimal("0.00")


def test_deposit_increases_balance(fresh_account):
    fresh_account.deposit(Decimal("50.00"))
    assert fresh_account.balance == Decimal("50.00")


def test_withdraw_reduces_balance(fresh_account):
    fresh_account.deposit(Decimal("30.00"))
    fresh_account.withdraw(Decimal("10.00"))
    assert fresh_account.balance == Decimal("20.00")


def test_overdraft_disallowed(fresh_account):
    with pytest.raises(ValueError):
        fresh_account.withdraw(Decimal("100.00"))


def test_non_positive_amounts_rejected(fresh_account):
    with pytest.raises(ValueError):
        fresh_account.deposit(Decimal("0.00"))
    with pytest.raises(ValueError):
        fresh_account.withdraw(Decimal("-1.00"))
