# CRT Buddy - �������ָ��

## PACKAGING_GUIDE — Windows 下打包指引（PyInstaller）

本项目已提供 .spec 与脚本，推荐在 .venv 里打包。

---

### 1) 基础准备

- 安装 pyinstaller（在 .venv 中）
- 确认依赖已安装：PyQt6、Pillow、numpy、opencv-python 等

---

### 2) 使用提供的 spec

- 文件：CRT_Buddy_complete.spec
- 可直接使用，也可根据资源路径调整 datas/binaries

---

### 3) 资源与插件

- 字体等静态资源需打包进 datas（如 DinkieBitmap）
- Qt 插件（platforms）通常由 PyQt6-Qt6 带入，注意 qwindows.dll 存在
- OpenCV 运行期可能需要 opencv_world*.dll（由轮子提供）

---

### 4) 脚本与批处理

- 参考：build_exe.py / build_improved.py
- Windows 批处理：rebuild_exe.bat / test_exe.bat
- 报告：PACKAGING_REPORT.md / FINAL_SUCCESS.md / FINAL_BUILD_SUCCESS.md 等

---

### FAQ

Q: 启动后白屏/窗口未创建？
A: 检查 Qt 平台插件是否被包含（platforms/qwindows.dll）。

Q: 资源/字体丢失？
A: 在 spec 的 datas 中添加对应目录或文件。

Q: 缺少 OpenCV DLL？
A: 安装 VC++ 运行库；确保 wheel 已包含 opencv_world*.dll。
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

2. ���д��:
```bash
pyinstaller CRT_Buddy_full.spec
```

---

## ?? ���Դ�����

### ��ʽ1: ʹ�ò��Խű�
```bash
python test_exe.py
```

### ��ʽ2: �ֶ�����
```bash
cd dist
.\CRT_Buddy.exe
```

��飺
- [ ] �������������޴��󵯴���
- [ ] CRT����������ʾ
- [ ] ������������
- [ ] �����ť����Ӧ
- [ ] ������קͼƬ

---

## ?? ���������Ų�

### ����1: `ModuleNotFoundError: No module named 'PyQt6'`

**ԭ��**: PyInstallerû���ҵ�PyQt6

**���**:
```bash
# ���´�������� --collect-all=PyQt6
pyinstaller --name=CRT_Buddy --onefile --windowed --collect-all=PyQt6 main.py
```

### ����2: `ModuleNotFoundError: No module named 'PIL'`

**ԭ��**: Pillowģ��δ��ȷ���

**���**:
```bash
# ���� --collect-all=PIL
pyinstaller --name=CRT_Buddy --onefile --windowed --collect-all=PIL main.py
```

### ����3: `ModuleNotFoundError: No module named 'cv2'`

**ԭ��**: OpenCV���뷽ʽ����

**���**:
```bash
# �ȼ��opencv�Ƿ�װ
pip show opencv-python

# ����Ѱ�װ������hidden-import
pyinstaller --hidden-import=cv2 ...
```

**�������** (���cv2�޷����):
�޸Ĵ��룬ʹcv2��Ϊ��ѡ��

```python
# �� y2k_styles.py ��
try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False
    print("Warning: OpenCV not available, some effects disabled")

# Ȼ����ʹ��cv2�ĺ����м��
def apply_chrome_effect(image):
    if not HAS_CV2:
        # �������Ч����ԭͼ
        return image
    # ... ԭ�д���
```

### ����4: EXE���̫��

**��ǰ��С**: ~22MB������PyQt6, PIL, NumPy��

**��С���**:
```bash
# 1. ʹ���ļ���ģʽ�����ǵ��ļ�
pyinstaller --name=CRT_Buddy --onedir --windowed main.py

# 2. ʹ��UPXѹ��
pyinstaller --name=CRT_Buddy --onefile --upx-dir=path/to/upx main.py

# 3. �ų�����Ҫ��ģ��
pyinstaller --exclude-module=matplotlib --exclude-module=scipy ...
```

### ����5: ��������

**ԭ��**: ���ļ�ģʽ��Ҫ��ѹ����ʱĿ¼

**���**:
```bash
# ʹ���ļ���ģʽ���������죩
pyinstaller --name=CRT_Buddy --onedir --windowed main.py
```

---

## ?? ���ģʽ�Ա�

### ���ļ�ģʽ (--onefile)
```
�ŵ�:
? �ַ����㣨ֻ��һ��exe��
? ������רҵ

ȱ��:
? ����������2-5�룩
? ����ϴ�20-30MB��
? ÿ�����н�ѹ����ʱĿ¼
```

### �ļ���ģʽ (--onedir)
```
�ŵ�:
? �������٣�<1�룩
? ��������ܸ�С
? ���ڵ���

ȱ��:
? ��Ҫ�ַ������ļ���
? �ļ��࣬������������
```

---

## ?? �Ƽ������մ������

### ����1: �������ļ�
```bash
Remove-Item build -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item dist -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item *.spec -Force -ErrorAction SilentlyContinue
```

### ����2: ���иĽ��ű�
```bash
python build_improved.py
```

### ����3: ����
```bash
python test_exe.py
```

### ����4: ��֤����
�ֶ��������й��ܣ�
- [ ] ����Meme����
- [ ] ͼƬ�ϴ��ʹ���
- [ ] �������
- [ ] �ļ����浽output

### ����5: ����������
```bash
# ���������ļ���
mkdir release
Copy-Item dist\CRT_Buddy.exe release\
Copy-Item dist\ʹ��˵��.txt release\

# ѹ��
Compress-Archive -Path release\* -DestinationPath CRT_Buddy_v1.0.zip
```

---

## ?? ���׼���

### ����ͼ��
```bash
# ׼��һ��icon.ico�ļ�
pyinstaller --icon=icon.ico ...
```

### ���Ӱ汾��Ϣ
```bash
# ����version.txt
pyinstaller --version-file=version.txt ...
```

### ��Ĭ������������
```bash
pyinstaller --log-level=WARN ...
```

### ����ģʽ���
```bash
# ��������̨���ڣ��鿴������Ϣ
pyinstaller --console ...
```

---

## ?? ��֤���������

�������½ű��������������

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

## ?? ���ռ���嵥

�����ɺ���֤��

- [ ] EXE�ļ�������dist�ļ���
- [ ] ˫����������
- [ ] û�п���̨��������
- [ ] CRT����������ʾ
- [ ] ���а�ť�ɵ��
- [ ] �������ɹ�������
- [ ] ͼƬ�ϴ���������
- [ ] �ļ����浽output�ļ���
- [ ] ����һ̨���Բ��ԣ���Python������

---

## ?? ��ȡ����

����������⣺

1. �鿴������־: `build\CRT_Buddy\warn-CRT_Buddy.txt`
2. ʹ�õ���ģʽ���: `--console --debug=all`
3. �ύIssue��GitHub
4. ���PyInstaller�ĵ�: https://pyinstaller.org

---

<div align="center">

**ף���˳����**

Made with ?? in Y2K Spirit

</div>
