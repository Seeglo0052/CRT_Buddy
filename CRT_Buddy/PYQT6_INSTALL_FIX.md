## PYQT6_INSTALL_FIX — Windows 下安装问题指北
聚焦解决 “pip 安装 PyQt6 失败 / 运行时报缺 DLL” 等问题。
---
### 1) 使用独立虚拟环境
- 在仓库根目录创建 .venv，并在 VS Code 选择该解释器
- 之后的 pip 都在 .venv 中执行，避免系统环境冲突
---
### 2) 安装正确的包集合
- 最小集合：PyQt6, PyQt6-Qt6, PyQt6-sip
- 若 pip 自动解析失败，可逐个安装上述三者
---
### 3) 轮子匹配（wheels）
- Windows x64 通常使用 win_amd64 的 .whl
- Python 3.13 对应 cp313；确保下载/解析到的 wheel 与版本匹配
---
### 4) 运行时报 Qt DLL 缺失
- 确认已安装 PyQt6-Qt6（其中包含 Qt6*.dll）
- ANGLE/OpenGL 渲染冲突时，尝试切换/更新显卡驱动
- 若提示 platform plugins，检查 PyQt6 的 plugins 目录是否被正确发现（打包时尤其需要）
---
### 5) 仍无法安装？
- 升级 pip 和 setuptools
- 切换到清华/阿里云镜像源重试
- 贴出完整错误日志以便进一步定位
# ?? PyQt6 ��װ����������

## ��������

��װPyQt6ʱ��������
```
[Errno 2] No such file or directory: '...pageindicatordelegate-indicator-delegate-current-hovered@2x.png'
```

����Windows��·�����ƣ�260�ַ������µ����⡣

---

## ?? �������

### ����1: ����Windows��·��֧�֣��Ƽ���

1. �Թ���Ա���ݴ�PowerShell
2. �����������

```powershell
# ���ó�·��֧��
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
-Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

3. ��������
4. ���°�װPyQt6��

```bash
pip install PyQt6
```

### ����2: ʹ��PySide6������Ƽ�����

PySide6��Qt�ٷ���Python�󶨣�������PyQt6��ͬ��

```bash
pip install PySide6
```

Ȼ���޸���Ŀ�е����е��룺
```python
# ������
from PyQt6 import ...

# ��Ϊ
from PySide6 import ...
```

### ����3: ʹ�����⻷������·����

��C�̸�Ŀ¼�������⻷����·�����̣���

```bash
# �������⻷��
python -m venv C:\venv

# �������⻷��
C:\venv\Scripts\activate

# ��װ����
pip install PyQt6 Pillow numpy opencv-python
```

### ����4: �޸�ע����༭��

1. �� Win+R������ `regedit`
2. �ҵ���`HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem`
3. �½�DWORDֵ��`LongPathsEnabled`������Ϊ`1`
4. ��������

---

## ?? ���CRT Buddy�Ŀ��ٽ������

�ҽ���ʹ��**PySide6**������PyQt6 API������ȫ��ͬ��

### ����1: ��װPySide6
```bash
pip install PySide6
```

### ����2: �������ݽű�

���� `run_pyside.py`��
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

### ����3: ����
```bash
python run_pyside.py
```

### ����4: ���
```bash
pyinstaller --name=CRT_Buddy_PySide ^
            --onefile ^
            --windowed ^
            --noconsole ^
            --collect-all=PySide6 ^
            run_pyside.py
```

---

## ?? ��������Ա�

| ���� | �ŵ� | ȱ�� |
|------|------|------|
| **���ó�·��** | һ������ | ��Ҫ����ԱȨ�ޡ����� |
| **PySide6** | ����Ȩ�ޡ���װ���� | ���޸��������� |
| **���⻷��** | ��Ӱ��ϵͳ | ·���Կ��ܹ��� |
| **ע���** | ������Ч | ��Ҫ����ԱȨ�� |

---

## ?? �Ƽ�����

1. **���԰�װPySide6**����򵥣�
2. ���PySide6Ҳʧ�� �� ���ó�·��֧��
3. ��������
4. ���°�װ

---

## ?? ��֤��·���Ƿ�����

��PowerShell�����У�
```powershell
Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled"
```

������� `1`��˵�������á�

---

## ?? ע������

- PySide6��PyQt6 API 99%��ͬ
- ��������������޸�
- PySide6��Qt�ٷ��Ƽ���Python��
- ����֤�Ѻã�LGPL��

---

<div align="center">

**���飺ֱ��ʹ��PySide6��**

�����ȶ���û��·�����⣬�����ǹٷ��Ƽ���ѡ��

</div>
