# -*- coding: utf-8 -*-
"""
CRT Buddy - Meme Generator Engine
Y2K style Meme generation engine
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, UnidentifiedImageError
import random
import os
from datetime import datetime
from effects.y2k_styles import Y2KStyles
from effects.text_effects import TextEffects


class MemeEngine:
    def generate_text_meme_animated(self, text, style='gradient', size=(800, 600), frames=32, duration=50, out_prefix="y2k_text_animated"):
        """Generate animated text meme and save as gif."""
        ok, cleaned, reason = self.validate_text(text)
        if not ok:
            raise self.TextValidationError(reason)
        # Use text effect animation
        imgs, frame_duration = self.text_effects.render_animated_text(
            cleaned,
            size=size,
            style=style,
            frames=frames,
            duration=duration,
            flicker=True,
            flicker_mode='breath',
            flicker_speed_multiplier=384,
            flicker_amplitude=2,
            background_change_interval=4,
            background_rotate=True,
        )
        # Save gif
        counter = 1
        while True:
            filename = f"{out_prefix}_{counter}.gif"
            filepath = os.path.join(self.output_dir, filename)
            if not os.path.exists(filepath):
                break
            counter += 1
        self.text_effects.save_animated_text(imgs, filepath, format='GIF', duration=duration)
        print(f"Animated GIF saved: {filepath}")
        return filepath
    """Y2K style Meme generation engine"""
    
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        self.y2k_styles = Y2KStyles()
        self.text_effects = TextEffects()
        
        # Create output directory
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Y2K phrases
        self.y2k_phrases = [
            "UNDER CONSTRUCTION",
            "WELCOME TO MY WEBSITE",
            "BEST VIEWED IN NETSCAPE",
            "Y2K AESTHETIC",
            "CYBER DREAMS 2000",
            "POWERED BY GEOCITIES",
            "ENTER IF YOU DARE",
            "LOADING... PLEASE WAIT",
            "404 PAGE NOT FOUND",
            "GUESTBOOK - SIGN IN!",
            "WEBMASTER",
            "HIT COUNTER",
            "EMAIL ME",
            "NEW! UPDATED!",
            "COOL SITE AWARD",
            "MIDI MUSIC PLAYING",
            "FRAMES VERSION",
            "TEXT ONLY VERSION",
            "OPTIMIZED FOR 800x600",
            "MILLENNIUM BUG FREE"
        ]
    
    def generate_text_meme(self, text, style='random', size=(800, 600)):
        """Generate text-based meme"""
        # Central text validation
        ok, cleaned, reason = self.validate_text(text)
        if not ok:
            raise self.TextValidationError(reason)
        text = cleaned
        # Create base image
        img = Image.new('RGB', size, color=(0, 0, 0))
        
        # Apply Y2K background
        img = self._apply_y2k_background(img)
        
        # Add text with effect
        if style == 'random':
            style = random.choice(['gradient', 'glitch', 'neon', 'chrome', 'retro'])
        
        img = self.text_effects.apply_effect(img, text, style)
        
        # Add decorations
        img = self._add_decorations(img)
        
        return img
    
    def generate_image_meme(self, image_path, text="", effect='random'):
        """Generate image-based meme with Y2K effects"""
        # Validate & load image (may auto-resize)
        img = self.validate_image(image_path)
        
        # Apply Y2K effect
        if effect == 'random':
            effect = random.choice(['crt', 'vhs', 'holographic', 'chrome', 'neon', 'pixelate'])
        
        img = self.y2k_styles.apply_effect(img, effect)
        
        # Add text if provided
        if text:
            ok, cleaned, reason = self.validate_text(text)
            if not ok:
                raise self.TextValidationError(reason)
            img = self._add_text_overlay(img, cleaned)
        
        return img
    
    def generate_random_meme(self):
        """Generate completely random meme"""
        # Random phrase
        phrase = random.choice(self.y2k_phrases)
        
        # Random size
        sizes = [(800, 600), (640, 480), (1024, 768)]
        size = random.choice(sizes)
        
        # Generate
        return self.generate_text_meme(phrase, 'random', size)
    
    def save_meme(self, img, prefix="meme"):
        """Save meme to output directory"""
        # Generate filename
        counter = 1
        while True:
            filename = f"{prefix}_{counter}.png"
            filepath = os.path.join(self.output_dir, filename)
            if not os.path.exists(filepath):
                break
            counter += 1
        
        # Save
        img.save(filepath, 'PNG')
        print(f"Saved: {filepath}")
        return filepath
    
    def _apply_y2k_background(self, img):
        """Apply Y2K style background"""
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        # Gradient background
        for y in range(height):
            r = int(128 + 127 * (y / height))
            g = int(0 + 128 * (y / height))
            b = int(128 - 128 * (y / height))
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Add grid
        for x in range(0, width, 50):
            draw.line([(x, 0), (x, height)], fill=(255, 0, 255, 30), width=1)
        for y in range(0, height, 50):
            draw.line([(0, y), (width, y)], fill=(255, 0, 255, 30), width=1)
        
        return img

    # ---------------- Image Validation -----------------
    class ImageValidationError(Exception):
        """Custom exception for image validation failures"""
        pass

    class TextValidationError(Exception):
        """Custom exception for text validation failures"""
        pass

    def validate_image(self, image_path, allowed_formats=None, max_side=2000, auto_resize_side=1200):
        """Validate image file before meme generation.
        Steps:
        1. Exists & readable
        2. Pillow can decode (catch UnidentifiedImageError)
        3. Format in allowed list (if provided)
        4. Size limits (reject if any side > max_side)
        5. Auto downscale if any side > auto_resize_side (LANCZOS)
        Returns: PIL.Image (RGB)
        Raises: ImageValidationError with user-friendly message
        """
        if allowed_formats is None:
            allowed_formats = {"PNG", "JPG", "JPEG", "BMP", "GIF"}
        if not os.path.exists(image_path):
            raise self.ImageValidationError(f"File not found: {image_path}")
        try:
            with Image.open(image_path) as im:
                im.load()  # force decode
                fmt = (im.format or '').upper()
                if fmt == 'JPG':  # normalize
                    fmt = 'JPEG'
                if fmt not in allowed_formats:
                    raise self.ImageValidationError(f"Unsupported format: {fmt}. Allowed: {', '.join(sorted(allowed_formats))}")
                w, h = im.size
                if w > max_side or h > max_side:
                    raise self.ImageValidationError(f"Image too large: {w}x{h} (limit {max_side}px). Please downscale before using.")
                # Auto resize if beyond soft threshold
                if max(w, h) > auto_resize_side:
                    ratio = auto_resize_side / max(w, h)
                    new_size = (int(w * ratio), int(h * ratio))
                    im = im.resize(new_size, Image.Resampling.LANCZOS)
                return im.convert('RGB')
        except UnidentifiedImageError:
            raise self.ImageValidationError("Pillow could not decode the image (corrupted or unsupported data).")
        except OSError as e:
            raise self.ImageValidationError(f"I/O error reading image: {e}")

    # ---------------- Text Validation -----------------
    def validate_text(self, text, max_len=200, allow_empty=False, normalize_whitespace=True):
        """Validate and normalize user provided text.
        Returns (ok: bool, cleaned_text: str, reason: str|None)
        Rules:
          1. Strip leading/trailing whitespace
          2. Optionally collapse internal whitespace sequences to single space
          3. Remove control characters (<32) except newline
          4. Enforce max length (after normalization)
          5. Empty disallowed unless allow_empty=True
        """
        if text is None:
            text = ""
        cleaned = text.strip()
        if normalize_whitespace and cleaned:
            # Collapse all whitespace sequences to single spaces preserving newlines
            # First replace newlines with placeholders to avoid collapsing across lines
            placeholder = "\uFFFF"  # unlikely char
            cleaned = cleaned.replace("\r", "")
            cleaned = cleaned.replace("\n", f"{placeholder}")
            parts = cleaned.split()
            cleaned = " ".join(parts)
            cleaned = cleaned.replace(placeholder, "\n")
        # Remove control chars except newline
        cleaned = "".join(ch for ch in cleaned if ch == "\n" or ord(ch) >= 32)
        if not cleaned and not allow_empty:
            return False, cleaned, "TEXT EMPTY"
        if len(cleaned) > max_len:
            return False, cleaned, f"TEXT TOO LONG (>{max_len} chars)"
        return True, cleaned, None

    
    def _add_text_overlay(self, img, text):
        """Add text overlay to image"""
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        # Try to use a nice font
        try:
            font_size = int(height * 0.1)
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Get text size
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Position (bottom center)
        x = (width - text_width) // 2
        y = height - text_height - 30
        
        # Draw shadow
        shadow_offset = 3
        draw.text((x + shadow_offset, y + shadow_offset), text, fill=(0, 0, 0), font=font)
        
        # Draw text
        draw.text((x, y), text, fill=(255, 255, 0), font=font)
        
        return img
    
    def _add_decorations(self, img):
        """Add Y2K style decorations"""
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        # Random stars
        for _ in range(20):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(2, 5)
            color = random.choice([(255, 0, 255), (0, 255, 255), (255, 255, 0)])
            draw.ellipse([x, y, x+size, y+size], fill=color)
        
        return img
