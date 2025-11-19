# ? CRT Buddy - ��Ŀ����嵥

## ?? ��Ŀ�ṹ
```
CRT_Buddy/
������ ? CRT_Buddy.py           # ���������
������ ? start.py               # ���������ű�
������ ? requirements.txt       # �����б�
������ ? config.ini            # �����ļ�
������ ? README.md             # ��Ŀ˵��
# CRT Buddy - Checklist 清单

面向开发与测试的核对清单，覆盖文件结构、功能点与质量保证。

---

## Files 主要文件
```
CRT_Buddy/
    CRT_Buddy.py        # 主入口
    start.py            # 依赖自检+启动
    requirements.txt    # 依赖（较旧，3.8–3.11）
    config.ini          # 可选配置
    README.md           # 项目说明
    USAGE.md            # 使用说明
    SHOWCASE.md         # 效果展示
    build_exe.py        # 打包脚本
    run_app.bat         # Windows 一键启动
    core/
        __init__.py
        pet_window.py     # 主窗口/像素字体/UI
    effects/
        __init__.py
        y2k_styles.py     # 图片效果
        text_effects.py   # 文字效果
    generators/
        __init__.py
        meme_engine.py    # 生成与保存逻辑
```

---

## Features 功能核对

### UI/交互
- [x] 无边框窗体（置顶）可拖动
- [x] 右键菜单/状态信息
- [x] 像素字体加载 OK（DinkieBitmap）
- [x] 情绪/状态展示 idle/happy/thinking/processing

### 效果（图片）
- [x] CRT（扫描线+RGB偏移）
- [x] VHS（抖动/拖影/噪点）
- [x] Holographic/Chrome/Neon 文字高光
- [x] Pixelate（8/16-bit）

### 生成与保存
- [x] 文字 → y2k_text_*.png
- [x] 图片 → y2k_image_*.png
- [x] 随机 → y2k_random_*.png
- [x] 递增命名，写入 output/

---

## Dev/Docs 开发与文档
```markdown
# CRT Buddy — Developer/QA Checklist

A focused checklist for files, features, and quality verification.

---

## Files
```
CRT_Buddy/
    CRT_Buddy.py        # main entry
    start.py            # self-check + launcher
    requirements.txt    # legacy constraints (3.8–3.11)
    config.ini          # optional config
    README.md           # overview
    USAGE.md            # usage/how-to
    SHOWCASE.md         # feature showcase
    build_exe.py        # packaging script
    run_app.bat         # Windows launcher
    core/
        __init__.py
        pet_window.py     # main window / pixel font / UI
    effects/
        __init__.py
        y2k_styles.py     # image effects
        text_effects.py   # text effects
    generators/
        __init__.py
        meme_engine.py    # generation + save logic
```

---

## Features

### UI/Interactions
- [x] Frameless, draggable, always-on-top window
- [x] Right-click menu / status text
- [x] Pixel font loads (DinkieBitmap)
- [x] Mood/status updates: idle/happy/processing

### Effects (images/text)
- [x] CRT (scanlines + RGB shift)
- [x] VHS (jitter/ghosting/noise)
- [x] Holographic / Chrome / Neon styling
- [x] Pixelate (8/16-bit)

### Generation & Save
- [x] Text → y2k_text_*.png
- [x] Image → y2k_image_*.png
- [x] Random → y2k_random_*.png
### ���ڣ�V3.0��
- [ ] ����ģ���̵�
- [ ] ������������
- [ ] ���ϵͳ
- [ ] ��Ƶ����

---

## ?? ��Ŀ״̬

```
�������: ����������������������������������������? 95%

���Ĺ���: ? ���
�ĵ�����: ? ���
������֤: ? ������
����ַ�: ? ׼����
```

### ���Խ���������
1. ? ������Դ����
2. ? ��ϸ���ĵ�
3. ? �����ű�
4. ? �������
5. ? ʹ��ָ��

### ʹ�÷�ʽ
```bash
# ��ʽ1: ֱ������
python CRT_Buddy.py

# ��ʽ2: �����ű�
python start.py

# ��ʽ3: Windows������
˫�� run.bat

# ��ʽ4: ���EXE
python build_exe.py
# Ȼ������ dist/CRT_Buddy.exe
```

---

## ?? ��л

��л��ѡ��CRT Buddy��Ŀ��

����һ������Y2K�����黳�Ĵ�����Ŀ��ϣ�����ܸ������ǧ��������û��䡣

**��Ŀ�ص㣺**
- ?? ������Y2K��ѧʵ��
- ?? �ɰ����������
- ? ǿ���Meme����
- ?? �꾡���ĵ�
- ?? ���伴��

**������ʼ��**
```bash
cd CRT_Buddy
python start.py
```

---

<div align="center">

**? ����Y2Kʱ�⣡?**

Made with ?? for Y2K Lovers

</div>
