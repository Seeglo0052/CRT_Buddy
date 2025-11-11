# CRT Buddy - 完整打包指南

## ?? 问题诊断

如果EXE运行时报错 `ModuleNotFoundError: No module named 'XXX'`，说明PyInstaller没有正确打包某些依赖。

---

## ? 解决方案

### 方式1: 使用改进的打包脚本（推荐）

```bash
python build_improved.py
```

这个脚本会：
- 检查所有依赖是否安装
- 使用正确的hidden-import参数
- 自动收集所有PyQt6和PIL子模块

### 方式2: 手动打包（完整命令）

```bash
python -m PyInstaller ^
    --name=CRT_Buddy ^
    --onefile ^
    --windowed ^
    --noconsole ^
    --clean ^
    --hidden-import=PyQt6 ^
    --hidden-import=PyQt6.QtCore ^
    --hidden-import=PyQt6.QtGui ^
    --hidden-import=PyQt6.QtWidgets ^
    --hidden-import=PIL ^
    --hidden-import=PIL.Image ^
    --hidden-import=PIL.ImageDraw ^
    --hidden-import=PIL.ImageFont ^
    --hidden-import=PIL.ImageFilter ^
    --hidden-import=PIL.ImageEnhance ^
    --hidden-import=numpy ^
    --collect-all=PyQt6 ^
    --collect-all=PIL ^
    main.py
```

### 方式3: 使用spec文件

1. 创建 `CRT_Buddy_full.spec`:

```python
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'PIL',
        'PIL.Image',
        'PIL.ImageDraw',
        'PIL.ImageFont',
        'PIL.ImageFilter',
        'PIL.ImageEnhance',
        'numpy',
        'core.pet_window',
        'effects.y2k_styles',
        'effects.text_effects',
        'generators.meme_engine',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# Collect all PyQt6 files
a.datas += collect_all('PyQt6')[0]
a.binaries += collect_all('PyQt6')[1]

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CRT_Buddy',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```

2. 运行打包:
```bash
pyinstaller CRT_Buddy_full.spec
```

---

## ?? 测试打包结果

### 方式1: 使用测试脚本
```bash
python test_exe.py
```

### 方式2: 手动测试
```bash
cd dist
.\CRT_Buddy.exe
```

检查：
- [ ] 程序能启动（无错误弹窗）
- [ ] CRT窗口正常显示
- [ ] 可以输入文字
- [ ] 点击按钮有响应
- [ ] 可以拖拽图片

---

## ?? 常见问题排查

### 问题1: `ModuleNotFoundError: No module named 'PyQt6'`

**原因**: PyInstaller没有找到PyQt6

**解决**:
```bash
# 重新打包，添加 --collect-all=PyQt6
pyinstaller --name=CRT_Buddy --onefile --windowed --collect-all=PyQt6 main.py
```

### 问题2: `ModuleNotFoundError: No module named 'PIL'`

**原因**: Pillow模块未正确打包

**解决**:
```bash
# 添加 --collect-all=PIL
pyinstaller --name=CRT_Buddy --onefile --windowed --collect-all=PIL main.py
```

### 问题3: `ModuleNotFoundError: No module named 'cv2'`

**原因**: OpenCV导入方式特殊

**解决**:
```bash
# 先检查opencv是否安装
pip show opencv-python

# 如果已安装，添加hidden-import
pyinstaller --hidden-import=cv2 ...
```

**替代方案** (如果cv2无法打包):
修改代码，使cv2变为可选：

```python
# 在 y2k_styles.py 中
try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False
    print("Warning: OpenCV not available, some effects disabled")

# 然后在使用cv2的函数中检查
def apply_chrome_effect(image):
    if not HAS_CV2:
        # 返回替代效果或原图
        return image
    # ... 原有代码
```

### 问题4: EXE体积太大

**当前大小**: ~22MB（包含PyQt6, PIL, NumPy）

**减小体积**:
```bash
# 1. 使用文件夹模式而不是单文件
pyinstaller --name=CRT_Buddy --onedir --windowed main.py

# 2. 使用UPX压缩
pyinstaller --name=CRT_Buddy --onefile --upx-dir=path/to/upx main.py

# 3. 排除不需要的模块
pyinstaller --exclude-module=matplotlib --exclude-module=scipy ...
```

### 问题5: 启动很慢

**原因**: 单文件模式需要解压到临时目录

**解决**:
```bash
# 使用文件夹模式（启动更快）
pyinstaller --name=CRT_Buddy --onedir --windowed main.py
```

---

## ?? 打包模式对比

### 单文件模式 (--onefile)
```
优点:
? 分发方便（只有一个exe）
? 看起来专业

缺点:
? 启动较慢（2-5秒）
? 体积较大（20-30MB）
? 每次运行解压到临时目录
```

### 文件夹模式 (--onedir)
```
优点:
? 启动快速（<1秒）
? 总体积可能更小
? 易于调试

缺点:
? 需要分发整个文件夹
? 文件多，看起来不整洁
```

---

## ?? 推荐的最终打包流程

### 步骤1: 清理旧文件
```bash
Remove-Item build -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item dist -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item *.spec -Force -ErrorAction SilentlyContinue
```

### 步骤2: 运行改进脚本
```bash
python build_improved.py
```

### 步骤3: 测试
```bash
python test_exe.py
```

### 步骤4: 验证功能
手动测试所有功能：
- [ ] 文字Meme生成
- [ ] 图片上传和处理
- [ ] 随机生成
- [ ] 文件保存到output

### 步骤5: 创建发布包
```bash
# 创建发布文件夹
mkdir release
Copy-Item dist\CRT_Buddy.exe release\
Copy-Item dist\使用说明.txt release\

# 压缩
Compress-Archive -Path release\* -DestinationPath CRT_Buddy_v1.0.zip
```

---

## ?? 进阶技巧

### 添加图标
```bash
# 准备一个icon.ico文件
pyinstaller --icon=icon.ico ...
```

### 添加版本信息
```bash
# 创建version.txt
pyinstaller --version-file=version.txt ...
```

### 静默打包（无输出）
```bash
pyinstaller --log-level=WARN ...
```

### 调试模式打包
```bash
# 保留控制台窗口，查看错误信息
pyinstaller --console ...
```

---

## ?? 验证打包完整性

运行以下脚本检查所有依赖：

```python
# check_imports.py
import sys

modules = [
    'PyQt6',
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.QtWidgets',
    'PIL',
    'numpy',
]

print("Checking imports in built executable...")
for module in modules:
    try:
        __import__(module)
        print(f"? {module}")
    except ImportError as e:
        print(f"? {module}: {e}")
```

---

## ?? 最终检查清单

打包完成后验证：

- [ ] EXE文件存在于dist文件夹
- [ ] 双击可以启动
- [ ] 没有控制台窗口闪现
- [ ] CRT窗口正常显示
- [ ] 所有按钮可点击
- [ ] 文字生成功能正常
- [ ] 图片上传功能正常
- [ ] 文件保存到output文件夹
- [ ] 在另一台电脑测试（无Python环境）

---

## ?? 获取帮助

如果仍有问题：

1. 查看构建日志: `build\CRT_Buddy\warn-CRT_Buddy.txt`
2. 使用调试模式打包: `--console --debug=all`
3. 提交Issue到GitHub
4. 检查PyInstaller文档: https://pyinstaller.org

---

<div align="center">

**祝打包顺利！**

Made with ?? in Y2K Spirit

</div>
