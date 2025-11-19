# ?? ��Ҫ��PyQt6��װʧ�� - �������

## ?? ����˵��

��Ŀ�������**ȱ��PyQt6**�������Ϊʲô��
1. �����޷�ֱ������
2. �����EXEҲ�޷�����

������Ϣ��
```
ModuleNotFoundError: No module named 'PyQt6.QtWidgets'
```

## ??? ����ԭ��

Windows·���������ƣ�260�ַ�������PyQt6��װʧ�ܡ�
����·��̫����
```
C:\Users\SEEGLO\AppData\Local\Packages\
  PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\
  LocalCache\local-packages\Python313\site-packages\
  PyQt6\Qt6\qml\QtQuick\Controls\FluentWinUI3\
  light\images\pageindicatordelegate-indicator-delegate-current-hovered@2x.png
```

---

## ? ���������3�ַ�����

### ����1�����ó�·��֧�֣��Ƽ���?

#### ����1���޸�ע���
```
1. �� Win + R
2. ����: regedit
3. �ҵ�: HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem
4. ˫��: LongPathsEnabled
## INSTALL_FIX — 安装与常见问题修复

面向 Windows 的快速排障与修复清单。

---

## 1) 无法导入 PyQt6（ModuleNotFoundError）

- 确认 VS Code 使用仓库内的 .venv 解释器
- 使用该解释器安装依赖：
   - PyQt6, Pillow, numpy, opencv-python, pygame, pywin32, requests
- 验证导入：通过 python -c 运行并看到 IMPORT_OK

---

## 2) 入口混乱/运行不了

- 源码入口：main.py 调用 CRT_Buddy.main()
- 批处理入口：run.bat / launch_v2.bat
- 终端直接：python CRT_Buddy.py

---

## 3) 运行 EXE 缺少 DLL

- 安装 VC++ 运行库（x64）：
   https://aka.ms/vs/17/release/vc_redist.x64.exe
- 常见缺失：opencv_world*.dll、Qt6*.dll

---

## 4) PATH 与终端环境

- 建议在 VS Code 终端中运行，确保 .venv\Scripts 已被激活
- 不要混用系统 Python 与 .venv

---

## 5) Python 版本

- 推荐 3.12/3.13
- 若旧版本（3.8-3.10）可能需要降级/升级部分依赖

---

## 6) EXE 无响应/被拦截

- 在命令行中运行 EXE 以查看输出日志
- 关闭或信任杀毒软件；将 EXE 加入白名单
- 避免路径包含中文或空格过多（临时移动到短路径试试）

---

## FAQ

Q: VS Code 里提示找不到 PyQt6？
A: 切换到 .venv 解释器并安装依赖，再次验证导入。

Q: EXE 打不开，说缺少 DLL？
A: 安装 VC++ 运行库（链接见上）；若仍报错请截图具体 DLL 名称。

Q: pip 装好了还是运行不了？
A: 可能在系统 Python 安装了依赖，但 VS Code 用的是别的解释器；统一到 .venv。
python -c "import numpy; print('NumPy OK')"
python -c "import cv2; print('OpenCV OK')"
```

Ԥ�������
```
PyQt6 OK
Pillow OK
NumPy OK
OpenCV OK
```

---

## ?? ������װ�ű�

�����ļ� `install_deps.bat`��

```batch
@echo off
echo ========================================
echo CRT Buddy - ������װ�ű�
echo ========================================
echo.

echo [1/5] �������⻷��...
python -m venv C:\crt
if errorlevel 1 (
    echo [����] ���⻷������ʧ��
    pause
    exit /b 1
)

echo [2/5] �������⻷��...
call C:\crt\Scripts\activate.bat

echo [3/5] ����pip...
python -m pip install --upgrade pip

echo [4/5] ��װ����...
pip install PyQt6==6.7.1 Pillow==11.0.0 numpy==2.2.1 opencv-python==4.10.0.84 pyinstaller==6.16.0

echo [5/5] ��֤��װ...
python -c "import PyQt6.QtWidgets; print('PyQt6 OK')"
python -c "import PIL; print('Pillow OK')"
python -c "import numpy; print('NumPy OK')"
python -c "import cv2; print('OpenCV OK')"

echo.
echo ========================================
echo ��װ��ɣ�
echo ========================================
echo.
echo ��һ��:
echo 1. �������⻷������״̬
echo 2. ����: python CRT_Buddy.py
echo ��
echo 3. ����: python -m PyInstaller CRT_Buddy_complete.spec
echo.
pause
```

---

## ?? ����Ĺ�������

### ����ʱ
```powershell
# 1. �������⻷��
C:\crt\Scripts\activate

# 2. ������ĿĿ¼
cd C:\GameDev\CRT_Buddy\CRT_Buddy\CRT_Buddy

# 3. ���г���
python CRT_Buddy.py

# ������main.py
python main.py
```

### ���ʱ
```powershell
# 1. ȷ�����⻷���Ѽ���
C:\crt\Scripts\activate

# 2. ������ĿĿ¼
cd C:\GameDev\CRT_Buddy\CRT_Buddy\CRT_Buddy

# 3. ����
Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue

# 4. ���
python -m PyInstaller CRT_Buddy_complete.spec

# 5. ����
cd dist
.\CRT_Buddy.exe
```

---

## ? ��������

### Q: Ϊʲô����ϵͳPython��
**A**: ϵͳPython��װ�ں����·���£���������Windows 260�ַ�·�����ơ�

### Q: ���⻷����ռ�ö��ٿռ䣿
**A**: Լ500-800 MB����������������

### Q: ������PyQt5������
**A**: ���Ƽ�����Ŀר��ΪPyQt6��ƣ�PyQt5�����м��������⡣

### Q: ��װʧ����ô�죿
**A**: 
1. ȷ���Թ���ԱȨ������PowerShell
2. �����������
3. ����ʹ�ù��ھ���
```powershell
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple PyQt6
```

---

## ?? �Ƽ��������

**��������������ǿ���Ƽ���**

1. ? ʹ�� **����1**�����ó�·��֧�֣�
   - һ������
   - ϵͳ������
   - ����Ҫ�������Python����

2. ? Ȼ��ʹ�� **���⻷���ڶ�·��** (C:\crt)
   - ��ɿ�
   - ��Ӱ��ϵͳPython
   - ��������

---

## ?? ��Ҫ������

�����װ��Ȼʧ�ܣ����ṩ��
1. Windows�汾
2. Python�汾 (`python --version`)
3. ����������Ϣ
4. PowerShell�����ͼ

---

<div align="center">

## ? �����ж�

ѡ��һ����������ʼ��װ��

**�Ƽ��������ճ������**

```powershell
# �������⻷��
python -m venv C:\crt

# ����
C:\crt\Scripts\activate

# ��װ����
pip install PyQt6 Pillow numpy opencv-python pyinstaller

# ��֤
python -c "import PyQt6.QtWidgets; print('Success!')"
```

</div>
