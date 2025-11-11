# ?? PyQt6 安装问题解决方案

## 问题描述

安装PyQt6时遇到错误：
```
[Errno 2] No such file or directory: '...pageindicatordelegate-indicator-delegate-current-hovered@2x.png'
```

这是Windows长路径限制（260字符）导致的问题。

---

## ?? 解决方案

### 方案1: 启用Windows长路径支持（推荐）

1. 以管理员身份打开PowerShell
2. 运行以下命令：

```powershell
# 启用长路径支持
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
-Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

3. 重启电脑
4. 重新安装PyQt6：

```bash
pip install PyQt6
```

### 方案2: 使用PySide6替代（推荐！）

PySide6是Qt官方的Python绑定，功能与PyQt6相同：

```bash
pip install PySide6
```

然后修改项目中的所有导入：
```python
# 将所有
from PyQt6 import ...

# 改为
from PySide6 import ...
```

### 方案3: 使用虚拟环境（短路径）

在C盘根目录创建虚拟环境（路径更短）：

```bash
# 创建虚拟环境
python -m venv C:\venv

# 激活虚拟环境
C:\venv\Scripts\activate

# 安装依赖
pip install PyQt6 Pillow numpy opencv-python
```

### 方案4: 修改注册表编辑器

1. 按 Win+R，输入 `regedit`
2. 找到：`HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem`
3. 新建DWORD值：`LongPathsEnabled`，设置为`1`
4. 重启电脑

---

## ?? 针对CRT Buddy的快速解决方案

我建议使用**PySide6**，它与PyQt6 API几乎完全相同：

### 步骤1: 安装PySide6
```bash
pip install PySide6
```

### 步骤2: 创建兼容脚本

创建 `run_pyside.py`：
```python
"""
CRT Buddy with PySide6
Compatible version that works around Windows path limitations
"""
# Monkey patch to use PySide6
import sys

# Replace PyQt6 with PySide6
sys.modules['PyQt6'] = __import__('PySide6')
sys.modules['PyQt6.QtCore'] = __import__('PySide6.QtCore')
sys.modules['PyQt6.QtGui'] = __import__('PySide6.QtGui')
sys.modules['PyQt6.QtWidgets'] = __import__('PySide6.QtWidgets')

# Now import and run main
from main import main
main()
```

### 步骤3: 运行
```bash
python run_pyside.py
```

### 步骤4: 打包
```bash
pyinstaller --name=CRT_Buddy_PySide ^
            --onefile ^
            --windowed ^
            --noconsole ^
            --collect-all=PySide6 ^
            run_pyside.py
```

---

## ?? 替代方案对比

| 方案 | 优点 | 缺点 |
|------|------|------|
| **启用长路径** | 一劳永逸 | 需要管理员权限、重启 |
| **PySide6** | 无需权限、即装即用 | 需修改少量代码 |
| **虚拟环境** | 不影响系统 | 路径仍可能过长 |
| **注册表** | 永久生效 | 需要管理员权限 |

---

## ?? 推荐流程

1. **尝试安装PySide6**（最简单）
2. 如果PySide6也失败 → 启用长路径支持
3. 重启电脑
4. 重新安装

---

## ?? 验证长路径是否启用

在PowerShell中运行：
```powershell
Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled"
```

如果返回 `1`，说明已启用。

---

## ?? 注意事项

- PySide6和PyQt6 API 99%相同
- 大多数代码无需修改
- PySide6是Qt官方推荐的Python绑定
- 许可证友好（LGPL）

---

<div align="center">

**建议：直接使用PySide6！**

它更稳定，没有路径问题，而且是官方推荐的选择。

</div>
