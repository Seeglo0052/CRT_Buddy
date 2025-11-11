# ?? 重要：PyQt6安装失败 - 解决方案

## ?? 问题说明

你的开发环境**缺少PyQt6**，这就是为什么：
1. 程序无法直接运行
2. 打包的EXE也无法运行

错误信息：
```
ModuleNotFoundError: No module named 'PyQt6.QtWidgets'
```

## ??? 根本原因

Windows路径长度限制（260字符）导致PyQt6安装失败。
具体路径太长：
```
C:\Users\SEEGLO\AppData\Local\Packages\
  PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\
  LocalCache\local-packages\Python313\site-packages\
  PyQt6\Qt6\qml\QtQuick\Controls\FluentWinUI3\
  light\images\pageindicatordelegate-indicator-delegate-current-hovered@2x.png
```

---

## ? 解决方案（3种方法）

### 方法1：启用长路径支持（推荐）?

#### 步骤1：修改注册表
```
1. 按 Win + R
2. 输入: regedit
3. 找到: HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem
4. 双击: LongPathsEnabled
5. 改为: 1
6. 重启电脑
```

#### 步骤2：启用Git长路径
```powershell
git config --global core.longpaths true
```

#### 步骤3：重新安装PyQt6
```powershell
pip uninstall PyQt6 PyQt6-Qt6 PyQt6-sip -y
pip install PyQt6
pip install Pillow numpy opencv-python
```

---

### 方法2：使用虚拟环境在短路径

#### 创建虚拟环境（在C盘根目录）
```powershell
# 创建在C:\py_env（短路径）
python -m venv C:\py_env

# 激活
C:\py_env\Scripts\activate

# 安装依赖
pip install PyQt6 Pillow numpy opencv-python pyinstaller

# 进入项目目录
cd C:\GameDev\CRT_Buddy\CRT_Buddy\CRT_Buddy

# 打包
python -m PyInstaller CRT_Buddy_complete.spec
```

---

### 方法3：使用Conda环境

```powershell
# 安装Miniconda
# 下载: https://docs.conda.io/en/latest/miniconda.html

# 创建环境
conda create -n crtbuddy python=3.11

# 激活
conda activate crtbuddy

# 安装依赖
pip install PyQt6 Pillow numpy opencv-python pyinstaller

# 打包
cd C:\GameDev\CRT_Buddy\CRT_Buddy\CRT_Buddy
python -m PyInstaller CRT_Buddy_complete.spec
```

---

## ?? 快速解决方案（最简单）

如果你想立即测试，可以使用我已经创建的虚拟环境方案：

### 步骤1：创建简短路径的虚拟环境
```powershell
# 创建虚拟环境
python -m venv C:\crt

# 激活
C:\crt\Scripts\activate

# 验证
python --version
```

### 步骤2：安装所有依赖
```powershell
# 安装核心库
pip install PyQt6==6.7.1
pip install Pillow==11.0.0
pip install numpy==2.2.1
pip install opencv-python==4.10.0.84
pip install pyinstaller==6.16.0
```

### 步骤3：打包
```powershell
cd C:\GameDev\CRT_Buddy\CRT_Buddy\CRT_Buddy

# 清理之前的构建
Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue

# 使用spec文件打包
python -m PyInstaller CRT_Buddy_complete.spec
```

### 步骤4：测试
```powershell
# 运行EXE
cd dist
.\CRT_Buddy.exe
```

---

## ?? 验证安装

### 测试PyQt6是否正确安装
```powershell
python -c "import PyQt6.QtWidgets; print('PyQt6 OK')"
python -c "import PIL; print('Pillow OK')"
python -c "import numpy; print('NumPy OK')"
python -c "import cv2; print('OpenCV OK')"
```

预期输出：
```
PyQt6 OK
Pillow OK
NumPy OK
OpenCV OK
```

---

## ?? 完整安装脚本

创建文件 `install_deps.bat`：

```batch
@echo off
echo ========================================
echo CRT Buddy - 依赖安装脚本
echo ========================================
echo.

echo [1/5] 创建虚拟环境...
python -m venv C:\crt
if errorlevel 1 (
    echo [错误] 虚拟环境创建失败
    pause
    exit /b 1
)

echo [2/5] 激活虚拟环境...
call C:\crt\Scripts\activate.bat

echo [3/5] 升级pip...
python -m pip install --upgrade pip

echo [4/5] 安装依赖...
pip install PyQt6==6.7.1 Pillow==11.0.0 numpy==2.2.1 opencv-python==4.10.0.84 pyinstaller==6.16.0

echo [5/5] 验证安装...
python -c "import PyQt6.QtWidgets; print('PyQt6 OK')"
python -c "import PIL; print('Pillow OK')"
python -c "import numpy; print('NumPy OK')"
python -c "import cv2; print('OpenCV OK')"

echo.
echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 下一步:
echo 1. 保持虚拟环境激活状态
echo 2. 运行: python CRT_Buddy.py
echo 或
echo 3. 运行: python -m PyInstaller CRT_Buddy_complete.spec
echo.
pause
```

---

## ?? 建议的工作流程

### 开发时
```powershell
# 1. 激活虚拟环境
C:\crt\Scripts\activate

# 2. 进入项目目录
cd C:\GameDev\CRT_Buddy\CRT_Buddy\CRT_Buddy

# 3. 运行程序
python CRT_Buddy.py

# 或运行main.py
python main.py
```

### 打包时
```powershell
# 1. 确保虚拟环境已激活
C:\crt\Scripts\activate

# 2. 进入项目目录
cd C:\GameDev\CRT_Buddy\CRT_Buddy\CRT_Buddy

# 3. 清理
Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue

# 4. 打包
python -m PyInstaller CRT_Buddy_complete.spec

# 5. 测试
cd dist
.\CRT_Buddy.exe
```

---

## ? 常见问题

### Q: 为什么不用系统Python？
**A**: 系统Python安装在很深的路径下，容易遇到Windows 260字符路径限制。

### Q: 虚拟环境会占用多少空间？
**A**: 约500-800 MB（包含所有依赖）

### Q: 可以用PyQt5代替吗？
**A**: 不推荐。项目专门为PyQt6设计，PyQt5可能有兼容性问题。

### Q: 安装失败怎么办？
**A**: 
1. 确保以管理员权限运行PowerShell
2. 检查网络连接
3. 尝试使用国内镜像：
```powershell
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple PyQt6
```

---

## ?? 推荐解决方案

**对于你的情况，我强烈推荐：**

1. ? 使用 **方法1**（启用长路径支持）
   - 一劳永逸
   - 系统级别解决
   - 不需要管理多个Python环境

2. ? 然后使用 **虚拟环境在短路径** (C:\crt)
   - 最可靠
   - 不影响系统Python
   - 依赖隔离

---

## ?? 需要帮助？

如果安装仍然失败，请提供：
1. Windows版本
2. Python版本 (`python --version`)
3. 完整错误信息
4. PowerShell输出截图

---

<div align="center">

## ? 立即行动

选择一个方法，开始安装！

**推荐命令（复制粘贴）：**

```powershell
# 创建虚拟环境
python -m venv C:\crt

# 激活
C:\crt\Scripts\activate

# 安装依赖
pip install PyQt6 Pillow numpy opencv-python pyinstaller

# 验证
python -c "import PyQt6.QtWidgets; print('Success!')"
```

</div>
