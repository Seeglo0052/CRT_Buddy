# -*- coding: utf-8 -*-
"""
CRT Buddy - Build Script
打包脚本：将项目打包为独立的EXE文件
"""
import os
import subprocess
import sys


def build_exe():
    """构建EXE文件"""
    print("=" * 60)
    print("  CRT BUDDY - BUILD SCRIPT")
    print("  正在打包为Windows可执行文件...")
    print("=" * 60)
    
    # PyInstaller命令
    cmd = [
        "pyinstaller",
        "--name=CRT_Buddy",
        "--onefile",
        "--windowed",
        "--clean",
        "--noconfirm",
        # 添加数据文件（如果有）
        # "--add-data=assets;assets",
        # 隐藏控制台窗口
        "--noconsole",
        # 主文件
        "CRT_Buddy.py"
    ]
    
    print("\n执行命令:")
    print(" ".join(cmd))
    print("\n正在打包，请稍候...\n")
    
    try:
        # 运行PyInstaller
        result = subprocess.run(cmd, check=True)
        
        print("\n" + "=" * 60)
        print("  ? 打包成功！")
        print("=" * 60)
        print("\n可执行文件位置: dist/CRT_Buddy.exe")
        print("\n使用说明:")
        print("1. 双击运行 dist/CRT_Buddy.exe")
        print("2. 可以将整个dist文件夹分发给其他用户")
        print("3. 不需要安装Python环境即可运行\n")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 60)
        print("  ? 打包失败")
        print("=" * 60)
        print(f"\n错误信息: {e}")
        print("\n请确保已安装PyInstaller:")
        print("  pip install pyinstaller\n")
        return False
    
    except FileNotFoundError:
        print("\n" + "=" * 60)
        print("  ? 找不到PyInstaller")
        print("=" * 60)
        print("\n请先安装PyInstaller:")
        print("  pip install pyinstaller\n")
        return False


def clean_build_files():
    """清理构建文件"""
    print("\n清理构建临时文件...")
    
    dirs_to_remove = ["build", "__pycache__"]
    files_to_remove = ["CRT_Buddy.spec"]
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            print(f"  删除目录: {dir_name}")
            try:
                import shutil
                shutil.rmtree(dir_name)
            except Exception as e:
                print(f"  警告: 无法删除 {dir_name}: {e}")
    
    for file_name in files_to_remove:
        if os.path.exists(file_name):
            print(f"  删除文件: {file_name}")
            try:
                os.remove(file_name)
            except Exception as e:
                print(f"  警告: 无法删除 {file_name}: {e}")
    
    print("清理完成！\n")


if __name__ == "__main__":
    # 检查是否在正确的目录
    if not os.path.exists("CRT_Buddy.py"):
        print("? 错误: 请在项目根目录运行此脚本")
        sys.exit(1)
    
    # 构建EXE
    success = build_exe()
    
    # 询问是否清理临时文件
    if success:
        response = input("\n是否清理构建临时文件? (y/n): ").lower()
        if response in ['y', 'yes', '是']:
            clean_build_files()
    
    print("\n按任意键退出...")
    input()
