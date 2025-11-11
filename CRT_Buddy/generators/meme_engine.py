"""
CRT Buddy - Meme Generator Engine
Y2K风格Meme生成引擎
"""
from PIL import Image, ImageDraw, ImageFont
import random
import os
from effects.y2k_styles import Y2KEffects
from effects.text_effects import TextEffects


class MemeEngine:
    """Meme生成引擎"""
    
    # Y2K经典模板文案
    Y2K_TEMPLATES = [
        "UNDER CONSTRUCTION ??",
        "BEST VIEWED IN NETSCAPE ??",
        "WELCOME TO MY WEBSITE ?",
        "LOADING... ?",
        "YOU ARE VISITOR #999999 ??",
        "WEBMASTER: {text} ??",
        "POWERED BY GEOCITIES ??",
        "ENTER IF YOU DARE ??",
        "CYBERPUNK VIBES ONLY ??",
        "Y2K AESTHETIC ?",
    ]
    
    # Y2K贴纸元素
    Y2K_STICKERS = [
        "?", "?", "??", "??", "?", "?", "?", "??",
        "??", "??", "??", "???", "??", "??", "??",
        "??", "??", "??", "??", "??", "??", "??"
    ]
    
    def __init__(self, output_dir="output"):
        """初始化Meme引擎"""
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_text_meme(self, text, style='random'):
        """生成纯文字Meme"""
        if not text:
            text = random.choice(self.Y2K_TEMPLATES).replace("{text}", "CRT BUDDY")
        
        # 选择风格
        if style == 'random':
            style = random.choice(['gradient', 'glitch', 'neon', 'chrome', 'retro'])
        
        # 生成文字图像
        img = TextEffects.create_meme_text(text, style)
        
        # 应用随机Y2K特效
        if random.random() < 0.4:
            img = Y2KEffects.apply_random_effect(img)
        
        return img
    
    def generate_image_meme(self, image_path, text="", effect='random'):
        """生成图片+文字Meme"""
        try:
            # 加载图片
            img = Image.open(image_path)
            img = img.convert('RGB')
            
            # 调整大小
            max_size = 800
            if img.width > max_size or img.height > max_size:
                ratio = min(max_size / img.width, max_size / img.height)
                new_size = (int(img.width * ratio), int(img.height * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # 应用Y2K特效
            if effect == 'random':
                img = Y2KEffects.apply_random_effect(img)
            else:
                effect_map = {
                    'crt': Y2KEffects.apply_crt_effect,
                    'vhs': Y2KEffects.apply_vhs_glitch,
                    'holographic': Y2KEffects.apply_holographic_effect,
                    'chrome': Y2KEffects.apply_chrome_effect,
                    'neon': Y2KEffects.apply_neon_glow,
                    'pixelate': lambda x: Y2KEffects.apply_pixelate(x, 8)
                }
                effect_func = effect_map.get(effect, Y2KEffects.apply_crt_effect)
                img = effect_func(img)
            
            # 如果有文字，添加文字叠加层
            if text:
                img = self._add_text_overlay(img, text)
            
            # 添加Y2K贴纸
            img = self._add_stickers(img)
            
            return img
            
        except Exception as e:
            print(f"Error generating image meme: {e}")
            return None
    
    def _add_text_overlay(self, img, text):
        """在图片上添加文字叠加层"""
        width, height = img.size
        
        # 创建半透明背景条
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # 顶部文字条
        bar_height = 80
        draw.rectangle([(0, 0), (width, bar_height)], 
                      fill=(0, 0, 0, 180))
        
        # 底部文字条
        draw.rectangle([(0, height - bar_height), (width, height)], 
                      fill=(0, 0, 0, 180))
        
        # 合并叠加层
        img = img.convert('RGBA')
        img = Image.alpha_composite(img, overlay)
        
        # 添加文字
        draw = ImageDraw.Draw(img)
        
        try:
            font_size = 40
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # 分割文字到顶部和底部
        words = text.split()
        mid = len(words) // 2
        top_text = " ".join(words[:mid]) if mid > 0 else text
        bottom_text = " ".join(words[mid:]) if mid > 0 else ""
        
        # 绘制顶部文字
        if top_text:
            bbox = draw.textbbox((0, 0), top_text, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y = (bar_height - (bbox[3] - bbox[1])) // 2
            
            # 阴影
            draw.text((x + 2, y + 2), top_text, fill='#000000', font=font)
            # 主文字
            draw.text((x, y), top_text, fill='#00ffff', font=font)
        
        # 绘制底部文字
        if bottom_text:
            bbox = draw.textbbox((0, 0), bottom_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (width - text_width) // 2
            y = height - bar_height + (bar_height - text_height) // 2
            
            # 阴影
            draw.text((x + 2, y + 2), bottom_text, fill='#000000', font=font)
            # 主文字
            draw.text((x, y), bottom_text, fill='#ff00ff', font=font)
        
        return img.convert('RGB')
    
    def _add_stickers(self, img, num_stickers=5):
        """添加随机Y2K贴纸"""
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        try:
            sticker_font = ImageFont.truetype("seguiemj.ttf", 40)
        except:
            try:
                sticker_font = ImageFont.truetype("arial.ttf", 30)
            except:
                sticker_font = ImageFont.load_default()
        
        for _ in range(num_stickers):
            sticker = random.choice(self.Y2K_STICKERS)
            x = random.randint(20, width - 60)
            y = random.randint(20, height - 60)
            color = random.choice(['#ff00ff', '#00ffff', '#ffff00', '#00ff00'])
            
            # 添加阴影
            draw.text((x + 2, y + 2), sticker, fill='#000000', font=sticker_font)
            # 添加贴纸
            draw.text((x, y), sticker, fill=color, font=sticker_font)
        
        return img
    
    def save_meme(self, img, filename="meme"):
        """保存Meme到输出目录"""
        if img is None:
            return None
        
        # 生成唯一文件名
        counter = 1
        while True:
            output_path = os.path.join(self.output_dir, f"{filename}_{counter}.png")
            if not os.path.exists(output_path):
                break
            counter += 1
        
        img.save(output_path, 'PNG')
        return output_path
    
    def generate_random_meme(self):
        """生成完全随机的Y2K Meme"""
        text = random.choice(self.Y2K_TEMPLATES).replace("{text}", "Y2K VIBES")
        return self.generate_text_meme(text, style='random')
