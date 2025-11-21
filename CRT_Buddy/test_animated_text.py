# -*- coding: utf-8 -*-
"""
Demo: Animated text GIF/WebP generation
"""
from effects.text_effects import TextEffects

def main():
    text = "Y2K VIBES! CRT Buddy 流光闪烁"
    size = (600, 200)
    frames = 32
    duration = 50  # ms per frame
    effects = TextEffects()
    # 流光渐变
    imgs, dur = effects.render_animated_text(text, size=size, style='gradient', frames=frames, duration=duration)
    effects.save_animated_text(imgs, "output/animated_gradient.gif", format='GIF', duration=duration)
    # 彩虹 retro
    imgs2, dur2 = effects.render_animated_text(text, size=size, style='retro', frames=frames, duration=duration)
    effects.save_animated_text(imgs2, "output/animated_rainbow.gif", format='GIF', duration=duration)
    # 流光+闪烁
    imgs3, dur3 = effects.render_animated_text(text, size=size, style='gradient', frames=frames, duration=duration, flicker=True)
    effects.save_animated_text(imgs3, "output/animated_flicker.gif", format='GIF', duration=duration)
    print("Animated GIFs saved to output/")

if __name__ == "__main__":
    main()
