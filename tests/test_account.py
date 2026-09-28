"""
Test suite for the Account withdraw() race condition lab.

Run with:  pytest tests/ -v

test_sequential_withdrawals_work  -> sanity check, should ALWAYS pass,
    even with the bug present. If this fails, something else is broken.

test_concurrent_withdrawals_are_safe -> the real test. This will FAIL
    while the race condition bug is present, and PASS once it's fixed.
    It works by firing many concurrent withdrawals at an account that
    only has enough balance for exactly half of them to succeed, then
    checking that the final balance is exactly correct and that the
    account was never overdrawn.
"""

import threading
from app.account import Account


def test_sequential_withdrawals_work():
    acc = Account(starting_balance=100.0)
    assert acc.withdraw(30) is True
    assert acc.withdraw(30) is True
    assert acc.withdraw(30) is True
    assert acc.withdraw(30) is False  # only 10 left, should decline
    assert acc.get_balance() == 10.0


def test_concurrent_withdrawals_are_safe():
    # Starting balance allows exactly 50 successful withdrawals of $1.
    # We fire 100 concurrent withdrawal attempts of $1 each.
    # Correct behavior: exactly 50 succeed, exactly 50 are declined,
    # and the final balance is exactly 0 — never negative, never
    # left over from a "lost" deduction.
    acc = Account(starting_balance=50.0)
    results = []
    results_lock = threading.Lock()

    def attempt_withdraw():
        success = acc.withdraw(1)
        with results_lock:
            results.append(success)

    threads = [threading.Thread(target=attempt_withdraw) for _ in range(100)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    successful = sum(1 for r in results if r)
    final_balance = acc.get_balance()

    # The core correctness properties a fixed implementation must satisfy:
    assert final_balance >= 0, (
        f"Account went negative! Final balance: {final_balance}. "
        f"This means two threads both read a balance that allowed the "
        f"withdrawal before either had deducted it."
    )
    assert successful == 50, (
        f"Expected exactly 50 successful withdrawals, got {successful}. "
        f"final_balance={final_balance}. If this number is off, some "
        f"withdrawals were incorrectly approved or declined due to a "
        f"race between the balance check and the deduction."
    )
    assert final_balance == 0, (
        f"Expected final balance of exactly 0, got {final_balance}. "
        f"A non-zero result here is the classic symptom of a lost "
        f"update: two threads both read the same balance, both passed "
        f"the check, and one thread's deduction overwrote the other's."
    )
