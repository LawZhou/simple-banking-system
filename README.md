# Simple Banking System

This project is a basic banking system built in Python for a coding assignment.  
It supports creating accounts, deposits, withdrawals, transfers, and saving/loading from CSV files.

## Features

- Create bank accounts
- Deposit and withdraw money
- Transfer between accounts
- Save and load system state to CSV
- Prevent overdrafts and invalid amounts

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run Tests

```bash
pytest -q
```

## Example Usage

```python
from banking import BankingSystem

bank = BankingSystem()
alice = bank.create_account("Alice", 100)
bob = bank.create_account("Bob")
bank.transfer(alice, bob, 50)
bank.save_csv("accounts.csv")
```
