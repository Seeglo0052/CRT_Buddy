"""
CRT Buddy - Text Effects
Y2K风格文字特效生成器
"""
from PIL import Image, ImageDraw, ImageFont
import random


class TextEffects:
    """Y2K风格文字特效"""
    
    @staticmethod
    def create_gradient_text(text, size=(800, 400), font_size=60):
        """创建渐变文字图像"""
        img = Image.new('RGB', size, '#000000')
        draw = ImageDraw.Draw(img)
        
        # 尝试加载字体（使用系统默认）
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # 获取文字边界框
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # 居中位置
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2
        
        # 创建渐变背景
        for i in range(size[1]):
            ratio = i / size[1]
            r = int(255 * (1 - ratio))
            g = int(255 * ratio * 0.5)
            b = int(255 * ratio)
            draw.line([(0, i), (size[0], i)], fill=(r, g, b))
        
        # 绘制文字（带阴影）
        shadow_offset = 3
        draw.text((x + shadow_offset, y + shadow_offset), text, 
                 fill='#000000', font=font)
        draw.text((x, y), text, fill='#00ffff', font=font)
        
        return img
    
    @staticmethod
    def create_glitch_text(text, size=(800, 400), font_size=60):
        """创建故障艺术文字"""
        img = Image.new('RGB', size, '#000000')
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2
        
        # 绘制RGB分离效果
        offsets = [(-3, 0, '#ff0000'), (0, 0, '#00ff00'), (3, 0, '#0000ff')]
        for dx, dy, color in offsets:
            draw.text((x + dx, y + dy), text, fill=color, font=font)
        
        # 添加随机干扰线
        for _ in range(10):
            y_line = random.randint(0, size[1])
            draw.line([(0, y_line), (size[0], y_line)], 
                     fill=(random.randint(0, 255), random.randint(0, 255), 
                           random.randint(0, 255)), width=2)
        
        return img
    
    @staticmethod
    def create_neon_text(text, size=(800, 400), font_size=60):
        """创建霓虹灯文字效果"""
        img = Image.new('RGB', size, '#0a0a0a')
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2
        
        # 绘制多层辉光效果
        glow_layers = [
            (12, '#ff00ff', 30),
            (8, '#ff66ff', 60),
            (4, '#ffaaff', 120),
            (0, '#ffffff', 255)
        ]
        
        for offset, color, alpha in glow_layers:
            # 创建临时图层
            temp = Image.new('RGBA', size, (0, 0, 0, 0))
            temp_draw = ImageDraw.Draw(temp)
            
            # 解析颜色
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            
            temp_draw.text((x + offset, y + offset), text, 
                         fill=(r, g, b, alpha), font=font)
            
            img = Image.alpha_composite(img.convert('RGBA'), temp).convert('RGB')
        
        return img
    
    @staticmethod
    def create_chrome_text(text, size=(800, 400), font_size=60):
        """创建金属镀铬文字"""
        img = Image.new('RGB', size, '#000000')
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2
        
        # 绘制金属效果（多层渐变）
        layers = [
            (4, '#666666'),
            (3, '#999999'),
            (2, '#cccccc'),
            (1, '#eeeeee'),
            (0, '#ffffff')
        ]
        
        for offset, color in layers:
            draw.text((x, y + offset), text, fill=color, font=font)
        
        return img
    
    @staticmethod
    def create_retro_text(text, size=(800, 400), font_size=60):
        """创建复古Y2K文字（带星星和装饰）"""
        img = Image.new('RGB', size, '#000033')
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # 添加星星背景
        for _ in range(50):
            x_star = random.randint(0, size[0])
            y_star = random.randint(0, size[1])
            star_size = random.randint(1, 3)
            color = random.choice(['#ffff00', '#00ffff', '#ff00ff', '#ffffff'])
            draw.ellipse([x_star, y_star, x_star + star_size, y_star + star_size],
                        fill=color)
        
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2
        
        # 绘制文字（彩虹效果）
        colors = ['#ff0000', '#ff7700', '#ffff00', '#00ff00', '#0000ff', '#8800ff']
        for i, char in enumerate(text):
            color = colors[i % len(colors)]
            char_bbox = draw.textbbox((0, 0), char, font=font)
            char_width = char_bbox[2] - char_bbox[0]
            
            # 阴影
            draw.text((x + 2, y + 2), char, fill='#000000', font=font)
            # 主文字
            draw.text((x, y), char, fill=color, font=font)
            
            x += char_width
        
        return img
    
    @staticmethod
    def add_y2k_decorations(img):
        """添加Y2K装饰元素（星星、闪光等）"""
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        # 添加角落装饰
        decorations = ['?', '?', '??', '?', '?']
        positions = [
            (20, 20), (width - 60, 20),
            (20, height - 40), (width - 60, height - 40)
        ]
        
        try:
            deco_font = ImageFont.truetype("seguiemj.ttf", 30)
        except:
            deco_font = ImageFont.load_default()
        
        for pos in positions:
            deco = random.choice(decorations)
            draw.text(pos, deco, fill='#ffff00', font=deco_font)
        
        return img
    
    @staticmethod
    def create_meme_text(text, style='gradient'):
        """根据风格创建Meme文字"""
        styles = {
            'gradient': TextEffects.create_gradient_text,
            'glitch': TextEffects.create_glitch_text,
            'neon': TextEffects.create_neon_text,
            'chrome': TextEffects.create_chrome_text,
            'retro': TextEffects.create_retro_text
        }
        
        creator = styles.get(style, TextEffects.create_gradient_text)
        img = creator(text)
        
        # 随机添加装饰
        if random.random() < 0.5:
            img = TextEffects.add_y2k_decorations(img)
        
        return img
