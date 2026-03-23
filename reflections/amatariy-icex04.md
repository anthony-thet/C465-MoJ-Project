# Testing Reflection — ICEX_MJ04-EXT
**Route / Function:** /jokes  
**Author:** @amatariy  
**Date:** 2026-03-23  

## Tests Written
| Test Name | Level | What It Covers |
|-----------|-------|----------------|
| test_submit_joke_valid | HAPPY PATH | Submitting a normal non-empty joke succeeds with 201 and returns the submitted text. |
| test_submit_joke_max_length | EDGE CASE | Submitting text exactly 500 characters succeeds and ensures text is not truncated. |
| test_submit_joke_empty_text | ERROR CASE | Submitting empty text fails with 400 Bad Request |
## Coverage Output
============================= test session starts ==============================
platform darwin -- Python 3.11.7, pytest-9.0.2, pluggy-1.6.0 -- /Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11
cachedir: .pytest_cache
rootdir: /Users/aminmatariyeh/sp26-team-05-moj
plugins: anyio-4.9.0
collected 3 items

tests/test_jokes_amatariy.py::test_submit_joke_valid PASSED [ 33%]
tests/test_jokes_amatariy.py::test_submit_joke_max_length PASSED [ 66%]
tests/test_jokes_amatariy.py::test_submit_joke_empty_text PASSED [100%]

============================== 3 passed in 0.04s ==============================


## What Is Not Covered — and Why
This file does not test whitespace only jokes or text over 500 characters. Those cases are handled elsewhere or need extra setup we didn’t include.  

## What I Learned
Even simple tests can reveal edge cases I didn’t expect, like empty submissions or max length limits.
