# -*- coding: utf-8 -*-
"""Generate a meme with a very long text to verify wrapping/centering.
Run: python test_long_text_meme.py
"""
from generators.meme_engine import MemeEngine

engine = MemeEngine(output_dir='output')
long_text = (
    "THIS IS A VERY LONG LINE OF Y2K RETRO MEME TEXT THAT SHOULD AUTOMATICALLY WRAP AND "
    "CENTER WITHOUT GETTING CUT OFF ON THE LEFT OR RIGHT SIDE EVEN IF IT IS REALLY REALLY LONG"
)
img = engine.generate_text_meme(long_text, style='retro', size=(800,600))
path = engine.save_meme(img, 'long_text_test')
print('Generated long text meme at:', path)
