# -*- coding: utf-8 -*-
"""Tests for advanced text wrapping: character fallback, ellipsis, gradient interpolation.
Run: python test_wrap_ellipsis_gradient.py
"""
from generators.meme_engine import MemeEngine

engine = MemeEngine(output_dir='output')

cases = [
    ("CJK超长文本无空格应自动按字符断行并在达到最小字体时截断后加省略号" * 3, 'gradient'),
    ("SINGLEVERYVERYLONGWORDWITHOUTSPACESANDSHOULDBEWRAPPEDPROPERLYANDTRUNCATEDIFNECESSARY", 'retro'),
    ("NORMAL MULTI WORD LONG TEXT FOR GRADIENT COLOR INTERPOLATION TESTING PURPOSES HERE", 'gradient'),
]

for idx, (text, style) in enumerate(cases, start=1):
    img = engine.generate_text_meme(text, style=style, size=(640,480))
    path = engine.save_meme(img, f"wrap_case_{idx}")
    print(f"Generated {style} case {idx}: {path}")

print("All wrap/ellipsis/gradient tests completed.")
