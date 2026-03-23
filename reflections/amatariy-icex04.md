# Testing Reflection — ICEX_MJ04-EXT
**Route / Function:** /jokes
**Author:** @amatariy
**Date:** 2026-03-23

## Tests Written
| Test Name | Level | What It Covers |
|-----------|-------|----------------|
| test_submit_joke_valid | HAPPY PATH | Submitting a normal non-empty joke succeeds with 201 and returns the submitted text. |

## Coverage Output
============================= test session starts ==============================
platform darwin -- Python 3.11.7, pytest-9.0.2, pluggy-1.6.0
cachedir: .pytest_cache
rootdir: /Users/aminmatariyeh/sp26-team-05-moj
plugins: anyio-4.9.0
collected 1 item

tests/test_jokes_amatariy.py::test_submit_joke_valid PASSED [100%]

============================== 1 passed in 0.04s ==============================

## What Is Not Covered — and Why
This file only tests valid, non-empty jokes. Edge cases like whitespace-only text or maximum-length submissions are tested by teammates, and database error paths require mocking which is not in this cycle.

## What I Learned
Even a single happy-path test surfaces important behaviors like ensuring the text is stored correctly and an ID is generated.

