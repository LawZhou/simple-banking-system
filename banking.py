"""Simple in‑memory banking system with CSV persistence.

Designed for an assignment that values readability, testability, and a lean
feature set.  One module, no external dependencies except Python standard
library.
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

    def withdrawl(self, amount: Decimal) -> None:
        """Remove *amount* from this account.

        Prevents overdrafts by raising ValueError if insufficient funds.
        """
        if amount <= 0:
            raise ValueError("amount must be positive")
        if amount > self.balance:
            raise ValueError("insufficient funds")
        self.balance -= amount
