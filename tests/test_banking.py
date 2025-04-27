from decimal import Decimal
from pathlib import Path

import pytest

from banking import BankingSystem


def test_create_and_get_balance():
    bank = BankingSystem()
    acc = bank.create_account("Alice", 100)
    assert bank.get_balance(acc) == Decimal("100.00")


def test_create_account_with_negative_balance():
    bank = BankingSystem()
    with pytest.raises(ValueError):
        acc = bank.create_account("Alice", -100)


def test_deposit_and_withdraw():
    bank = BankingSystem()
    acc = bank.create_account("Bob")
    bank.deposit(acc, 50)
    bank.withdraw(acc, 20)
    assert bank.get_balance(acc) == Decimal("30.00")


def test_overdraft_blocked():
    bank = BankingSystem()
    acc = bank.create_account("Charlie", 5)
    with pytest.raises(ValueError):
        bank.withdraw(acc, 10)


def test_transfer():
    bank = BankingSystem()
    a = bank.create_account("Dave", 80)
    b = bank.create_account("Eve", 0)
    bank.transfer(a, b, 30)
    assert bank.get_balance(a) == Decimal("50.00")
    assert bank.get_balance(b) == Decimal("30.00")


def test_save_and_load(tmp_path: Path):
    csv_path = tmp_path / "accounts.csv"

    bank = BankingSystem()
    alice = bank.create_account("Alice", 200)
    bob = bank.create_account("Bob")
    bank.transfer(alice, bob, 75)

    # Save and reload through CSV
    bank.save_csv(csv_path)
    reloaded = BankingSystem.load_csv(csv_path)

    assert reloaded.get_balance(alice) == Decimal("125.00")
    assert reloaded.get_balance(bob) == Decimal("75.00")


def test_save_creates_file(tmp_path: Path):
    """
    file should exist after save_csv.
    """

    path = tmp_path / "acc.csv"
    bank = BankingSystem()
    bank.create_account("Solo", 10)
    bank.save_csv(path)

    assert path.exists()
    assert path.stat().st_size > 0


def test_empty_system(tmp_path: Path):
    """
    file should exist after save_csv.
    """

    path = tmp_path / "acc_not_exist.csv"
    bank = BankingSystem.load_csv(path)

    # system should have zero accounts
    assert len(bank._accounts) == 0

    # and still be fully usable
    acc = bank.create_account("Solo", 10)
    assert bank.get_balance(acc) == Decimal("10.00")
