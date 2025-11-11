"""
CRT Buddy - Y2K Style Effects
Y2K风格图像滤镜和特效
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np
import cv2
import random


class Y2KEffects:
    """Y2K风格特效处理器"""
    
    @staticmethod
    def apply_crt_effect(image):
        """应用CRT显示器效果：扫描线、色差"""
        img_array = np.array(image)
        height, width = img_array.shape[:2]
        
        # 添加扫描线
        for i in range(0, height, 3):
            img_array[i:i+1, :] = img_array[i:i+1, :] * 0.7
        
        # RGB色差效果
        if len(img_array.shape) == 3:
            shift = 3
            r_channel = np.roll(img_array[:, :, 0], shift, axis=1)
            g_channel = img_array[:, :, 1]
            b_channel = np.roll(img_array[:, :, 2], -shift, axis=1)
            img_array = np.stack([r_channel, g_channel, b_channel], axis=2)
        
        return Image.fromarray(img_array.astype('uint8'))
    
    @staticmethod
    def apply_vhs_glitch(image):
        """VHS故障艺术效果"""
        img_array = np.array(image)
        height, width = img_array.shape[:2]
        
        # 随机水平条带位移
        num_glitches = random.randint(3, 8)
        for _ in range(num_glitches):
            y_start = random.randint(0, height - 30)
            y_end = y_start + random.randint(5, 30)
            shift = random.randint(-20, 20)
            
            if shift > 0:
                img_array[y_start:y_end, shift:] = img_array[y_start:y_end, :-shift]
            elif shift < 0:
                img_array[y_start:y_end, :shift] = img_array[y_start:y_end, -shift:]
        
        # 添加色彩失真
        if len(img_array.shape) == 3:
            img_array[:, :, 0] = np.clip(img_array[:, :, 0] * 1.2, 0, 255)
            img_array[:, :, 2] = np.clip(img_array[:, :, 2] * 0.8, 0, 255)
        
        return Image.fromarray(img_array.astype('uint8'))
    
    @staticmethod
    def apply_holographic_effect(image):
        """全息/镭射效果"""
        img = image.convert('RGB')
        img_array = np.array(img, dtype=np.float32)
        
        # 创建彩虹渐变叠加
        height, width = img_array.shape[:2]
        rainbow = np.zeros_like(img_array)
        
        for i in range(height):
            hue = (i / height) * 255
            if hue < 85:
                rainbow[i, :] = [255, hue * 3, 0]
            elif hue < 170:
                rainbow[i, :] = [(255 - (hue - 85) * 3), 255, 0]
            else:
                rainbow[i, :] = [0, 255, (hue - 170) * 3]
        
        # 混合原图和彩虹效果
        result = img_array * 0.6 + rainbow * 0.4
        result = np.clip(result, 0, 255)
        
        # 添加金属光泽
        img_pil = Image.fromarray(result.astype('uint8'))
        enhancer = ImageEnhance.Contrast(img_pil)
        img_pil = enhancer.enhance(1.5)
        
        return img_pil
    
    @staticmethod
    def apply_chrome_effect(image):
        """金属镀铬效果"""
        img = image.convert('L')  # 转灰度
        img_array = np.array(img)
        
        # 增强对比度
        img_array = np.clip(img_array * 1.5, 0, 255).astype('uint8')
        
        # 应用渐变映射（银色到蓝色）
        colored = cv2.applyColorMap(img_array, cv2.COLORMAP_WINTER)
        colored = cv2.cvtColor(colored, cv2.COLOR_BGR2RGB)
        
        # 添加高光
        colored = cv2.addWeighted(colored, 0.8, np.full_like(colored, 50), 0.2, 0)
        
        return Image.fromarray(colored)
    
    @staticmethod
    def apply_neon_glow(image):
        """霓虹辉光效果"""
        img = image.convert('RGB')
        
        # 增强饱和度
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(2.0)
        
        # 创建辉光效果
        glow = img.filter(ImageFilter.GaussianBlur(15))
        
        # 混合原图和辉光
        result = Image.blend(img, glow, 0.5)
        
        # 增加亮度
        enhancer = ImageEnhance.Brightness(result)
        result = enhancer.enhance(1.3)
        
        return result
    
    @staticmethod
    def apply_pixelate(image, pixel_size=8):
        """像素化效果"""
        img = image.convert('RGB')
        width, height = img.size
        
        # 缩小再放大
        small = img.resize(
            (width // pixel_size, height // pixel_size),
            Image.Resampling.NEAREST
        )
        result = small.resize((width, height), Image.Resampling.NEAREST)
        
        return result
    
    @staticmethod
    def add_scanlines_overlay(image, line_spacing=4, opacity=0.3):
        """添加扫描线叠加层"""
        img = image.convert('RGBA')
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # 绘制扫描线
        for y in range(0, img.size[1], line_spacing):
            draw.line([(0, y), (img.size[0], y)], fill=(0, 0, 0, int(255 * opacity)))
        
        return Image.alpha_composite(img, overlay).convert('RGB')
    
    @staticmethod
    def add_y2k_border(image, border_color='#00ff00', border_width=10):
        """添加Y2K风格边框"""
        img = image.convert('RGB')
        width, height = img.size
        
        # 创建边框
        bordered = Image.new('RGB', 
            (width + border_width * 2, height + border_width * 2),
            border_color
        )
        bordered.paste(img, (border_width, border_width))
        
        # 在边框上添加装饰
        draw = ImageDraw.Draw(bordered)
        
        # 绘制角落装饰
        corner_size = 20
        corners = [
            (0, 0),
            (bordered.width - corner_size, 0),
            (0, bordered.height - corner_size),
            (bordered.width - corner_size, bordered.height - corner_size)
        ]
        
        for x, y in corners:
            draw.rectangle([x, y, x + corner_size, y + corner_size], 
                         fill='#ff00ff')
        
        return bordered
    
    @staticmethod
    def apply_random_effect(image):
        """应用随机Y2K效果"""
        effects = [
            Y2KEffects.apply_crt_effect,
            Y2KEffects.apply_vhs_glitch,
            Y2KEffects.apply_holographic_effect,
            Y2KEffects.apply_chrome_effect,
            Y2KEffects.apply_neon_glow,
            lambda img: Y2KEffects.apply_pixelate(img, random.randint(6, 12))
        ]
        
        effect = random.choice(effects)
        result = effect(image)
        
        # 随机添加扫描线
        if random.random() < 0.6:
            result = Y2KEffects.add_scanlines_overlay(result)
        
        # 随机添加边框
        if random.random() < 0.4:
            colors = ['#00ff00', '#ff00ff', '#00ffff', '#ffff00']
            result = Y2KEffects.add_y2k_border(result, random.choice(colors))
        
        return result
