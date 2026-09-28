Run the tests again. Both should be green now:

```
pytest tests/ -v
```

If `test_concurrent_withdrawals_are_safe` still fails intermittently,
double-check the lock wraps *both* the read and the write.
