# ?? 重要：立即修复指南

## 问题

你的程序无法运行，因为**缺少PyQt6依赖**！

```
ModuleNotFoundError: No module named 'PyQt6.QtWidgets'
```

---

## ? 快速解决（5分钟）

### ?? 步骤1：运行自动安装脚本

**双击运行:**
```
auto_install.bat
```

这个脚本会自动：
- ? 创建虚拟环境（在C:\crt，避免路径问题）
- ? 安装所有依赖（PyQt6、Pillow、NumPy、OpenCV、PyInstaller）
- ? 验证安装
- ? 激活环境

---

### ?? 步骤2：测试程序

安装完成后，会自动激活虚拟环境。然后运行：

```powershell
python CRT_Buddy.py
```

或

```powershell
python main.py
```

---

### ?? 步骤3：重新打包EXE

```powershell
# 清理之前的构建
Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue

# 重新打包
python -m PyInstaller CRT_Buddy_complete.spec

# 测试
cd dist
.\CRT_Buddy.exe
```

---

## ?? 手动安装（如果自动脚本失败）

### 方法1：PowerShell命令

```powershell
# 创建虚拟环境
python -m venv C:\crt

# 激活
C:\crt\Scripts\activate

# 安装依赖
pip install PyQt6==6.7.1
pip install Pillow==11.0.0  
pip install numpy==2.2.1
pip install opencv-python==4.10.0.84
pip install pyinstaller==6.16.0

# 验证
python -c "import PyQt6.QtWidgets; print('Success!')"
```

### 方法2：使用requirements.txt

创建 `requirements.txt`:
```
PyQt6==6.7.1
Pillow==11.0.0
numpy==2.2.1
opencv-python==4.10.0.84
pyinstaller==6.16.0
```

安装:
```powershell
C:\crt\Scripts\activate
pip install -r requirements.txt
```

---

## ? 验证成功

运行以下命令，应该看到 "OK"：

```powershell
python -c "import PyQt6.QtWidgets; print('PyQt6 OK')"
python -c "import PIL; print('Pillow OK')"
python -c "import numpy; print('NumPy OK')"
python -c "import cv2; print('OpenCV OK')"
```

---

## ?? 完整工作流程

### 每次开发时：

```powershell
# 1. 激活虚拟环境
C:\crt\Scripts\activate

# 2. 进入项目目录  
cd C:\GameDev\CRT_Buddy\CRT_Buddy\CRT_Buddy

# 3. 运行程序
python CRT_Buddy.py
```

### 打包时：

```powershell
# 1. 激活环境（如果还没激活）
C:\crt\Scripts\activate

# 2. 进入项目目录
cd C:\GameDev\CRT_Buddy\CRT_Buddy\CRT_Buddy

# 3. 清理
Remove-Item -Recurse -Force build, dist

# 4. 打包
python -m PyInstaller CRT_Buddy_complete.spec

# 5. 测试EXE
dist\CRT_Buddy.exe
```

---

## ?? 文件说明

| 文件 | 用途 |
|------|------|
| `auto_install.bat` | ? 自动安装所有依赖 |
| `INSTALL_FIX.md` | 详细的安装说明和故障排除 |
| `CRT_Buddy_complete.spec` | PyInstaller打包配置 |
| `CRT_Buddy.py` | 原始主程序（UTF-8有问题） |
| `main.py` | 清理过的主程序（推荐使用） |

---

## ? 常见问题

### Q: 为什么要用虚拟环境？
**A**: 避免Windows路径长度限制（260字符），同时隔离依赖。

### Q: C:\crt会占用多大空间？
**A**: 约500-800 MB（包含所有Python库）。

### Q: 可以删除吗？
**A**: 可以，但需要重新安装。建议保留。

### Q: auto_install.bat失败怎么办？
**A**: 
1. 以管理员权限运行
2. 检查网络连接
3. 查看 INSTALL_FIX.md 的详细说明

---

## ?? 成功后

? 依赖安装完成  
? 程序可以运行  
? EXE可以打包  
? 功能完全正常  

---

<div align="center">

## ?? 立即开始

### 第一步

**双击运行:**
```
auto_install.bat
```

### 第二步  

等待安装完成（3-5分钟）

### 第三步

测试程序:
```
python CRT_Buddy.py
```

---

**就这么简单！**

如有问题，查看 `INSTALL_FIX.md`

</div>
