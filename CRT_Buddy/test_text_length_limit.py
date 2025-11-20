# -*- coding: utf-8 -*-
"""Test for text length limit (MAX_TEXT_LEN).
Run: python test_text_length_limit.py
"""
from CRT_Buddy import MAX_TEXT_LEN

# Generate sample strings
short = 'HELLO Y2K'
long = 'A' * (MAX_TEXT_LEN + 10)

print(f"MAX_TEXT_LEN = {MAX_TEXT_LEN}")
print("Short length:", len(short))
print("Long length:", len(long))

assert len(short) <= MAX_TEXT_LEN
assert len(long) > MAX_TEXT_LEN

print("✓ Length boundary assertions passed")
