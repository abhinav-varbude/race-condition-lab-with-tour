"""
Simulated Payment Service — Account Balance Module
----------------------------------------------------
This is a tiny in-memory "account" service used by the API layer.
It exposes a single operation: withdraw(amount).

INCIDENT REPORT (read this first):
  Users are reporting that concurrent withdrawals from the same account
  sometimes result in an incorrect final balance — as if one of the
  withdrawals never happened, even though both requests returned
  "success" to the client.

  Single-user / sequential testing works perfectly. It only shows up
  under concurrent load.

Your task: find the bug and fix it. Do not rewrite the whole class —
the fix should be small.
"""

import time
import threading


class Account:
    def __init__(self, starting_balance: float):
        self.balance = starting_balance
        # NOTE: a lock already exists on the class, but look carefully
        # at whether it's actually being used where it needs to be.
        self._lock = threading.Lock()

    def withdraw(self, amount: float) -> bool:
        """
        Withdraw `amount` from the account if sufficient funds exist.
        Returns True if the withdrawal succeeded, False if declined
        (insufficient funds).
        """
        # --- BUG LIVES IN THIS METHOD ---
        # Step 1: check if there's enough balance
        if self.balance < amount:
            return False

        # Simulate some processing time (e.g. fraud check, ledger write)
        # This makes the race condition much easier to trigger reliably.
        time.sleep(0.01)

        # Step 2: deduct the amount
        self.balance -= amount
        return True

    def get_balance(self) -> float:
        return self.balance
