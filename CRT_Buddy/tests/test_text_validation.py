# -*- coding: utf-8 -*-
"""Basic tests for MemeEngine.validate_text

Covers:
1. Empty text rejection
2. Whitespace trimming & collapsing
3. Length limit enforcement
4. Control character removal
5. Allow empty override
"""
import os, sys
CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from generators.meme_engine import MemeEngine

engine = MemeEngine(output_dir="output")


def show(result):
    ok, cleaned, reason = result
    print(f"ok={ok} cleaned='{cleaned}' reason={reason}")

print("Test 1: Empty text")
show(engine.validate_text("   "))

print("Test 2: Basic text")
show(engine.validate_text("  Hello   World   "))

print("Test 3: Newlines preserved")
show(engine.validate_text("Line1\n   Line2\nLine3"))

print("Test 4: Length limit (short)")
show(engine.validate_text("A" * 10, max_len=20))

print("Test 5: Length limit (too long)")
show(engine.validate_text("B" * 25, max_len=20))

print("Test 6: Control chars removed")
control_text = "Hello\x01World\x02!"  # \x01 and \x02 should be stripped
show(engine.validate_text(control_text))

print("Test 7: Allow empty override")
show(engine.validate_text("   ", allow_empty=True))

print("Test 8: Tabs & multiple spaces collapse")
show(engine.validate_text("Hello\t\tWorld    2025"))

print("Test 9: Mixed whitespace and newlines")
show(engine.validate_text("  A   B\n\n   C   "))

print("Test 10: None input")
show(engine.validate_text(None))
