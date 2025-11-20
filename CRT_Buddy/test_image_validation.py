# -*- coding: utf-8 -*-
"""Quick tests for MemeEngine.validate_image.
Run: python test_image_validation.py
Creates temporary images and exercises validation paths.
"""
import os
from PIL import Image
from generators.meme_engine import MemeEngine

engine = MemeEngine()

def make_image(path, size=(800,600), color=(30,60,90)):
    Image.new('RGB', size, color).save(path, 'PNG')


def test_valid_image():
    path = 'tmp_valid.png'
    make_image(path)
    im = engine.validate_image(path)
    assert im.size == (800,600)
    print('✓ valid image test passed')
    os.remove(path)


def test_too_large_reject():
    path = 'tmp_large.png'
    make_image(path, size=(2500,2500))
    try:
        engine.validate_image(path)
    except engine.ImageValidationError as e:
        print('✓ large image rejected:', e)
    else:
        raise AssertionError('Large image should have been rejected')
    os.remove(path)


def test_auto_resize():
    path = 'tmp_resize.png'
    make_image(path, size=(1600,1000))
    im = engine.validate_image(path)
    assert max(im.size) <= 1200
    print('✓ auto resize applied:', im.size)
    os.remove(path)


def test_bad_file():
    path = 'tmp_corrupt.img'
    with open(path,'wb') as f:
        f.write(b'notarealimage')
    try:
        engine.validate_image(path)
    except engine.ImageValidationError as e:
        print('✓ corrupt file detected:', e)
    else:
        raise AssertionError('Corrupt file should have raised')
    os.remove(path)


def test_unsupported_format():
    path = 'tmp.bmp'
    # create BMP then restrict allowed formats artificially
    Image.new('RGB',(100,100),(0,0,0)).save(path,'BMP')
    try:
        engine.validate_image(path, allowed_formats={'PNG'})
    except engine.ImageValidationError as e:
        print('✓ unsupported format detected:', e)
    else:
        raise AssertionError('Unsupported format should have raised')
    os.remove(path)

if __name__ == '__main__':
    test_valid_image()
    test_too_large_reject()
    test_auto_resize()
    test_bad_file()
    test_unsupported_format()
    print('\nAll validation tests completed.')
