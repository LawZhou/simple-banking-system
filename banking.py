"""
Simple in‑memory banking system with CSV persistence.
"""

from __future__ import annotations

import csv
import uuid
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path
from typing import Dict


@dataclass
class BankAccount:
    """Represents a single customer account.

    Attributes
    ----------
    id:
        Unique identifier for the account.
    name:
        Account holder name.
    balance:
        Current balance.
    """

    id: str
    name: str
    # use decimal instead float for perfect precision
    balance: Decimal = field(default=Decimal("0.00"))

    # ── public API ──────────────────────────────────────────────────────────
    def deposit(self, amount: Decimal) -> None:
        """Add *amount* to this account.

        Parameters
        ----------
        amount:
            Positive value to credit.

        Raises
        ------
        ValueError
            If *amount* is not strictly positive.
        """
        if amount <= 0:
            raise ValueError("amount must be positive")
        self.balance += amount

    def withdraw(self, amount: Decimal) -> None:
        """Remove *amount* from this account.

        Prevents overdrafts by raising ValueError if insufficient funds.
        """
        if amount <= 0:
            raise ValueError("amount must be positive")
        if amount > self.balance:
            raise ValueError("insufficient funds")
        self.balance -= amount


class BankingSystem:
    """A banking system managing many `BankAccount`s"""

    def __init__(self) -> None:
        # internal store keyed by account id
        self._accounts: Dict[str, BankAccount] = {}

    # ── account creation ────────────────────────────────────────────────────
    def create_account(self, name: str, opening_balance: float = 0.0) -> str:
        """
        Create a new account and return its id.
        """
        if opening_balance < 0:
            raise ValueError("amount must be positive")
        acc_id = str(uuid.uuid4())
        self._accounts[acc_id] = BankAccount(
            id=acc_id, name=name, balance=to_decimal(opening_balance)
        )
        return acc_id

    # ── money deposit/withdraw/transfer ──────────────────────────────────────────────────────
    def deposit(self, acc_id: str, amount: float) -> None:
        """
        Deposit *amount* into *acc_id*.
        """
        self._accounts[acc_id].deposit(to_decimal(amount))

    def withdraw(self, acc_id: str, amount: float) -> None:
        """
        Withdraw *amount* from *acc_id*.
        """
        self._accounts[acc_id].withdraw(to_decimal(amount))

    def transfer(self, src_id: str, dst_id: str, amount: float) -> None:
        """Move funds from *src_id* to *dst_id*.

        Uses *withdraw* / *deposit* to ensure the usual validations apply.
        """
        amt = to_decimal(amount)
        self._accounts[src_id].withdraw(amt)
        self._accounts[dst_id].deposit(amt)

    # ── balance queries ─────────────────────────────────────────────────────────────
    def get_balance(self, acc_id: str) -> Decimal:
        """
        Return current balance for *acc_id*.
        """
        return self._accounts[acc_id].balance

    # ── persistence ─────────────────────────────────────────────────────────
    def save_csv(self, path: str | Path = "accounts.csv") -> None:
        """
        Serialize all accounts to *path* in CSV format.
        """
        with Path(path).open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(("id", "name", "balance"))
            for acc in self._accounts.values():
                w.writerow((acc.id, acc.name, str(acc.balance)))

    @classmethod
    def load_csv(cls, path: str | Path = "accounts.csv") -> "BankingSystem":
        """
        Recreate a `BankingSystem` from *path*.

        Returns a new instance. If the file does not exist an empty system is
        returned.
        """
        sys = cls()
        p = Path(path)
        if not p.exists():
            return sys
        with p.open() as f:
            for row in csv.DictReader(f):
                sys._accounts[row["id"]] = BankAccount(
                    id=row["id"],
                    name=row["name"],
                    balance=Decimal(row["balance"]),
                )
        return sys


def to_decimal(amount: float) -> Decimal:
    """
    Helper function to convert amount to Decimal with 2 digits rounding
    """
    return Decimal(f"{amount:.2f}")
