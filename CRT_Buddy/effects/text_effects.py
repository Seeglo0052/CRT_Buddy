# -*- coding: utf-8 -*-
"""
CRT Buddy - Text Effects
Y2K style text rendering effects
"""
from PIL import Image, ImageDraw, ImageFont
import random


class TextEffects:
    """Y2K style text effects"""

    def render_fitted_text(self, img, text, base_divisor=8, min_font=12, padding=20, line_spacing=0.9, ellipsis=True):
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
        size_guess = max(min_font, min(width, height) // base_divisor)
        try:
            font = ImageFont.truetype("arial.ttf", size_guess)
        except Exception:
            font = ImageFont.load_default()
            size_guess = font.size if hasattr(font, 'size') else min_font

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

        # Adjust font size downward until fits vertically & horizontally
        while True:
            lines = wrap_lines(font)
            line_heights = []
            max_line_w = 0
            for ln in lines:
                bbox = draw.textbbox((0,0), ln, font=font)
                w = bbox[2]-bbox[0]
                h = bbox[3]-bbox[1]
                line_heights.append(h)
                max_line_w = max(max_line_w, w)
            total_h = int(sum(line_heights) + (len(lines)-1) * (line_heights[0]*line_spacing if line_heights else 0))
            if (max_line_w + padding*2 <= width) and (total_h + padding*2 <= height):
                break
            # reduce size
            size_guess = int(size_guess * 0.9)
            if size_guess < min_font:
                # final attempt: wrap one more time and possibly truncate last line
                lines = wrap_lines(font)
                if ellipsis and lines:
                    # ensure last line fits horizontally; if not, truncate
                    last = lines[-1]
                    while True:
                        bbox_last = draw.textbbox((0,0), last + ("…" if last else ""), font=font)
                        if bbox_last[2]-bbox_last[0] + padding*2 <= width or len(last) <= 1:
                            lines[-1] = last + ("…" if bbox_last[2]-bbox_last[0] + padding*2 <= width else "")
                            break
                        last = last[:-1]
                break
            try:
                font = ImageFont.truetype("arial.ttf", size_guess)
            except Exception:
                font = ImageFont.load_default()
                break

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
