Look closely at `withdraw()`:

```python
if self.balance < amount:
    return False

time.sleep(0.01)          # simulated processing

self.balance -= amount
return True
```

The check and the update are two separate steps. Nothing stops a
second thread from running its own check in between.
