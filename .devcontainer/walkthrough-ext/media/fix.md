```python
def withdraw(self, amount: float) -> bool:
    with self._lock:
        if self.balance < amount:
            return False
        time.sleep(0.01)
        self.balance -= amount
        return True
```

Wrap the **whole** check-then-act sequence in `self._lock` — not just
the update. Locking only part of it doesn't help.
