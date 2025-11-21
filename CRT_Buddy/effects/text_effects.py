# -*- coding: utf-8 -*-
"""
CRT Buddy - Text Effects
Y2K style text rendering effects
"""
from PIL import Image, ImageDraw, ImageFont
import random


class FontCache:
    """Cache for PIL ImageFont objects by (font_path, size)"""
    def __init__(self, default_path="arial.ttf"):
        self.cache = {}
        self.default_path = default_path

    def get_font(self, size, font_path=None):
        path = font_path or self.default_path
        key = (path, size)
        if key in self.cache:
            return self.cache[key]
        try:
            font = ImageFont.truetype(path, size)
        except Exception:
            font = ImageFont.load_default()
        self.cache[key] = font
        return font

class TextEffects:
    """Y2K style text effects"""
    font_cache = FontCache()

    def render_fitted_text(self, img, text, base_divisor=8, min_font=12, padding=20, line_spacing=0.9, ellipsis=True, font_path=None):
        """Render potentially long text centered, auto-scaling & wrapping.
        Steps:
          1. Choose initial font size = min(width,height)//base_divisor
          2. Reduce size until longest line width fits (after wrapping)
          3. Wrap text by greedy word packing respecting current font size
          4. Draw each line with vertical centering
        Returns: (lines, font, (start_x, start_y))
        """
        draw = ImageDraw.Draw(img)
        width, height = img.size
        # Split into words
        words = text.split()
        # If no spaces (e.g., long single token or CJK), fallback to per-character pseudo words
        if len(words) == 1 and len(text) > 15:  # heuristic threshold
            words = list(text)
        # Initial font size guess
        max_font = max(min_font, min(width, height) // base_divisor)
        min_font_size = min_font
        font = self.font_cache.get_font(max_font, font_path)

        def wrap_lines(fnt):
            lines = []
            current = []
            joiner = " " if any(w == "" or w == " " for w in words) or (" " in text) else ""
            for w in words:
                test = joiner.join(current + [w]) if current else w
                bbox = draw.textbbox((0,0), test, font=fnt)
                if bbox[2]-bbox[0] + padding*2 <= width:
                    current.append(w)
                else:
                    if current:
                        lines.append(joiner.join(current))
                    current = [w]
            if current:
                lines.append(joiner.join(current))
            return lines

        # Binary search for largest font size that fits
        left = min_font_size
        right = max_font
        best_size = min_font_size
        best_lines = None
        best_font = self.font_cache.get_font(min_font_size, font_path)
        while left <= right:
            mid = (left + right) // 2
            test_font = self.font_cache.get_font(mid, font_path)
            lines = wrap_lines(test_font)
            line_heights = []
            max_line_w = 0
            for ln in lines:
                bbox = draw.textbbox((0,0), ln, font=test_font)
                w = bbox[2]-bbox[0]
                h = bbox[3]-bbox[1]
                line_heights.append(h)
                max_line_w = max(max_line_w, w)
            total_h = int(sum(line_heights) + (len(lines)-1) * (line_heights[0]*line_spacing if line_heights else 0))
            if (max_line_w + padding*2 <= width) and (total_h + padding*2 <= height):
                best_size = mid
                best_lines = lines
                best_font = test_font
                left = mid + 1
            else:
                right = mid - 1
        # If no size fits, fallback to min_font and ellipsis
        if best_lines is None:
            font = self.font_cache.get_font(min_font_size, font_path)
            lines = wrap_lines(font)
            if ellipsis and lines:
                last = lines[-1]
                while True:
                    bbox_last = draw.textbbox((0,0), last + ("…" if last else ""), font=font)
                    if bbox_last[2]-bbox_last[0] + padding*2 <= width or len(last) <= 1:
                        lines[-1] = last + ("…" if bbox_last[2]-bbox_last[0] + padding*2 <= width else "")
                        break
                    last = last[:-1]
            best_lines = lines
            best_font = font
            best_size = min_font_size
        # Centering coordinates
        bbox_line = draw.textbbox((0,0), 'Ag', font=best_font)
        line_h = bbox_line[3]-bbox_line[1]
        total_h = int(len(best_lines)*line_h + (len(best_lines)-1)*line_h*line_spacing)
        start_y = (height - total_h)//2
        return best_lines, best_font, start_y, line_h

        # Centering coordinates
        bbox_line = draw.textbbox((0,0), 'Ag', font=font)
        line_h = bbox_line[3]-bbox_line[1]
        lines = wrap_lines(font)
        total_h = int(len(lines)*line_h + (len(lines)-1)*line_h*line_spacing)
        start_y = (height - total_h)//2
        return lines, font, start_y, line_h
    
    def apply_effect(self, img, text, style):
        """Apply specified text effect"""
        effects = {
            'gradient': self.gradient_text,
            'glitch': self.glitch_text,
            'neon': self.neon_text,
            'chrome': self.chrome_text,
            'retro': self.retro_text
        }
        
        effect_func = effects.get(style, self.gradient_text)
        return effect_func(img, text)
    
    def gradient_text(self, img, text):
        draw = ImageDraw.Draw(img)
        # Smooth gradient across entire line using HSV-like interpolation among key stops
        gradient_stops = [(255,0,255), (0,255,255), (255,255,0), (0,255,0)]
        lines, font, start_y, line_h = self.render_fitted_text(img, text)
        for ln in lines:
            bbox = draw.textbbox((0,0), ln, font=font)
            line_w = bbox[2]-bbox[0]
            x_start = (img.size[0]-line_w)//2
            # Precompute cumulative widths for normalized position
            widths = []
            for ch in ln:
                cb = draw.textbbox((0,0), ch, font=font)
                widths.append(cb[2]-cb[0])
            total = sum(widths)
            x_cursor = 0
            for idx, ch in enumerate(ln):
                t = (x_cursor + widths[idx]/2)/max(1,total)
                # Map t into segment
                seg_len = 1/(len(gradient_stops)-1)
                seg_index = min(len(gradient_stops)-2, int(t/seg_len))
                local_t = (t - seg_index*seg_len)/seg_len
                c1 = gradient_stops[seg_index]
                c2 = gradient_stops[seg_index+1]
                color = tuple(int(c1[i] + (c2[i]-c1[i])*local_t) for i in range(3))
                draw.text((x_start + x_cursor, start_y), ch, fill=color, font=font)
                x_cursor += widths[idx]
            start_y += int(line_h * 0.9)
        return img
    
    def glitch_text(self, img, text):
        draw = ImageDraw.Draw(img)
        lines, font, start_y, line_h = self.render_fitted_text(img, text)
        offsets = [(0, -3), (3, 0), (-3, 3)]
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        for ln in lines:
            bbox = draw.textbbox((0,0), ln, font=font)
            line_w = bbox[2]-bbox[0]
            x = (img.size[0]-line_w)//2
            for offset, color in zip(offsets, colors):
                draw.text((x + offset[0], start_y + offset[1]), ln, fill=color, font=font)
            start_y += int(line_h * 0.9)
        return img
    
    def neon_text(self, img, text):
        draw = ImageDraw.Draw(img)
        lines, font, start_y, line_h = self.render_fitted_text(img, text)
        glow_color = (255, 0, 255)
        for ln in lines:
            bbox = draw.textbbox((0,0), ln, font=font)
            line_w = bbox[2]-bbox[0]
            x = (img.size[0]-line_w)//2
            for i in range(10, 0, -2):
                alpha = int(255 * (i / 10))
                draw.text((x, start_y), ln, fill=glow_color, font=font)
            draw.text((x, start_y), ln, fill=(255,255,255), font=font)
            start_y += int(line_h * 0.9)
        return img
    
    def chrome_text(self, img, text):
        draw = ImageDraw.Draw(img)
        lines, font, start_y, line_h = self.render_fitted_text(img, text)
        for ln in lines:
            bbox = draw.textbbox((0,0), ln, font=font)
            line_w = bbox[2]-bbox[0]
            x = (img.size[0]-line_w)//2
            # Shadow
            draw.text((x+5, start_y+5), ln, fill=(0,0,0), font=font)
            # Vertical gradient simulation
            text_h = line_h
            for i in range(0, text_h, 2):
                shade = int(128 + 127 * (i / max(1,text_h)))
                draw.text((x, start_y + i), ln, fill=(shade, shade, min(255, shade+50)), font=font)
            # Highlight
            draw.text((x-1, start_y-1), ln, fill=(255,255,255), font=font)
            start_y += int(line_h * 0.9)
        return img
    
    def retro_text(self, img, text):
        draw = ImageDraw.Draw(img)
        rainbow = [
            (255,0,0),(255,127,0),(255,255,0),(0,255,0),(0,0,255),(75,0,130),(148,0,211)
        ]
        lines, font, start_y, line_h = self.render_fitted_text(img, text)
        for ln in lines:
            bbox = draw.textbbox((0,0), ln, font=font)
            line_w = bbox[2]-bbox[0]
            x_start = (img.size[0]-line_w)//2
            widths = []
            for ch in ln:
                cb = draw.textbbox((0,0), ch, font=font)
                widths.append(cb[2]-cb[0])
            total = sum(widths)
            x_cursor = 0
            for idx, ch in enumerate(ln):
                t = (x_cursor + widths[idx]/2)/max(1,total)
                seg_len = 1/(len(rainbow)-1)
                seg_index = min(len(rainbow)-2, int(t/seg_len))
                local_t = (t - seg_index*seg_len)/seg_len
                c1 = rainbow[seg_index]; c2 = rainbow[seg_index+1]
                color = tuple(int(c1[i] + (c2[i]-c1[i])*local_t) for i in range(3))
                draw.text((x_start + x_cursor, start_y), ch, fill=color, font=font)
                x_cursor += widths[idx]
            start_y += int(line_h * 0.9)
        return img
