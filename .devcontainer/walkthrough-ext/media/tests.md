```
pytest tests/ -v
```

Expect:
- `test_sequential_withdrawals_work` — **passes**
- `test_concurrent_withdrawals_are_safe` — **fails**

That gap between "works alone" and "fails under load" is the shape
of a race condition.
