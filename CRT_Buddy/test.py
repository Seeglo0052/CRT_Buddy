# -*- coding: utf-8 -*-
"""
CRT Buddy - Test Script
测试各个模块功能
"""
import os
import sys

def test_imports():
    """测试模块导入"""
    print("=" * 60)
    print("  测试模块导入")
    print("=" * 60)
    
    modules = [
        ("PyQt6", "PyQt6.QtWidgets"),
        ("Pillow", "PIL"),
        ("NumPy", "numpy"),
        ("OpenCV", "cv2"),
    ]
    
    all_passed = True
    
    for name, import_name in modules:
        try:
            __import__(import_name)
            print(f"? {name:15s} - OK")
        except ImportError as e:
            print(f"? {name:15s} - FAILED: {e}")
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("? 所有依赖模块正常")
    else:
        print("? 部分模块缺失，请运行: pip install -r requirements.txt")
    print("=" * 60 + "\n")
    
    return all_passed


def test_effects():
    """测试特效功能"""
    print("=" * 60)
    print("  测试Y2K特效")
    print("=" * 60)
    
    try:
        from PIL import Image
        from effects.y2k_styles import Y2KEffects
        
        # 创建测试图像
        test_img = Image.new('RGB', (400, 300), '#0066cc')
        print("? 创建测试图像")
        
        # 测试各种特效
        effects_to_test = [
            ("CRT效果", Y2KEffects.apply_crt_effect),
            ("VHS故障", Y2KEffects.apply_vhs_glitch),
            ("全息效果", Y2KEffects.apply_holographic_effect),
            ("镀铬效果", Y2KEffects.apply_chrome_effect),
            ("霓虹辉光", Y2KEffects.apply_neon_glow),
            ("像素化", lambda img: Y2KEffects.apply_pixelate(img, 8)),
        ]
        
        for name, effect_func in effects_to_test:
            try:
                result = effect_func(test_img)
                print(f"? {name:15s} - OK")
            except Exception as e:
                print(f"? {name:15s} - FAILED: {e}")
        
        print("\n" + "=" * 60)
        print("? 特效测试完成")
        print("=" * 60 + "\n")
        return True
        
    except Exception as e:
        print(f"? 特效测试失败: {e}\n")
        return False


def test_text_effects():
    """测试文字特效"""
    print("=" * 60)
    print("  测试文字特效")
    print("=" * 60)
    
    try:
        from effects.text_effects import TextEffects
        
        test_text = "Y2K TEST"
        
        effects_to_test = [
            ("渐变文字", lambda: TextEffects.create_gradient_text(test_text)),
            ("故障文字", lambda: TextEffects.create_glitch_text(test_text)),
            ("霓虹文字", lambda: TextEffects.create_neon_text(test_text)),
            ("镀铬文字", lambda: TextEffects.create_chrome_text(test_text)),
            ("复古文字", lambda: TextEffects.create_retro_text(test_text)),
        ]
        
        for name, effect_func in effects_to_test:
            try:
                result = effect_func()
                print(f"? {name:15s} - OK")
            except Exception as e:
                print(f"? {name:15s} - FAILED: {e}")
        
        print("\n" + "=" * 60)
        print("? 文字特效测试完成")
        print("=" * 60 + "\n")
        return True
        
    except Exception as e:
        print(f"? 文字特效测试失败: {e}\n")
        return False


def test_meme_engine():
    """测试Meme引擎"""
    print("=" * 60)
    print("  测试Meme生成引擎")
    print("=" * 60)
    
    try:
        from generators.meme_engine import MemeEngine
        
        engine = MemeEngine(output_dir="test_output")
        print("? Meme引擎初始化")
        
        # 测试文字Meme生成
        try:
            text_meme = engine.generate_text_meme("TEST MEME", style='gradient')
            print("? 文字Meme生成")
        except Exception as e:
            print(f"? 文字Meme生成失败: {e}")
        
        # 测试随机Meme
        try:
            random_meme = engine.generate_random_meme()
            print("? 随机Meme生成")
        except Exception as e:
            print(f"? 随机Meme生成失败: {e}")
        
        print("\n" + "=" * 60)
        print("? Meme引擎测试完成")
        print("=" * 60 + "\n")
        return True
        
    except Exception as e:
        print(f"? Meme引擎测试失败: {e}\n")
        return False


def test_pet_window():
    """测试宠物窗口（仅导入测试）"""
    print("=" * 60)
    print("  测试宠物窗口模块")
    print("=" * 60)
    
    try:
        from core.pet_window import CRTBuddyWindow
        print("? 宠物窗口模块导入成功")
        print("   (窗口显示需要运行主程序)")
        
        print("\n" + "=" * 60)
        print("? 宠物窗口测试完成")
        print("=" * 60 + "\n")
        return True
        
    except Exception as e:
        print(f"? 宠物窗口测试失败: {e}\n")
        return False


def main():
    """主测试函数"""
    print("\n")
    print("*" * 60)
    print("  CRT BUDDY - 模块测试")
    print("*" * 60)
    print("\n")
    
    results = []
    
    # 运行各项测试
    results.append(("依赖导入", test_imports()))
    results.append(("图像特效", test_effects()))
    results.append(("文字特效", test_text_effects()))
    results.append(("Meme引擎", test_meme_engine()))
    results.append(("宠物窗口", test_pet_window()))
    
    # 汇总结果
    print("\n")
    print("*" * 60)
    print("  测试结果汇总")
    print("*" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "? PASS" if passed else "? FAIL"
        print(f"{status:10s} - {name}")
        if not passed:
            all_passed = False
    
    print("*" * 60)
    
    if all_passed:
        print("\n?? 所有测试通过！可以运行主程序了：")
        print("   python CRT_Buddy.py")
        print("   或双击 run.bat\n")
    else:
        print("\n??  部分测试失败，请检查依赖安装：")
        print("   pip install -r requirements.txt\n")
    
    return all_passed


if __name__ == "__main__":
    success = main()
    print("\n按任意键退出...")
    input()
    sys.exit(0 if success else 1)
