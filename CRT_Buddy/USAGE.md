# CRT Buddy - ����ʹ��ָ��
# CRT Buddy Usage Guide 使用说明

本页介绍如何启动和使用 CRT Buddy 生成 Y2K 风格的文字/图片 Meme。

---

## Run 启动方式

方式 A（推荐，先做依赖检查）
```powershell
```markdown
# CRT Buddy — Usage Guide

This page shows how to start and use CRT Buddy to create Y2K-style text/image memes.

---

## Run

Recommended (performs a dependency self-check first):
```powershell
python start.py
```

Direct run:
```powershell
python CRT_Buddy.py
```

On Windows you can also double-click `run_app.bat`.

---

## Workflows

### 1) Text → Meme
1. Type a phrase (e.g., "Y2K VIBES ONLY")
2. Click GENERATE MEME
3. Check `output/` for the saved image (e.g., y2k_text_1.png)

Suggested prompts:
- WELCOME TO MY WEBSITE
- UNDER CONSTRUCTION
- BEST VIEWED IN NETSCAPE
- POWERED BY GEOCITIES

### 2) Image → Y2K Effects
Flow A (drag & drop)
1. Drag an image into the window
2. Apply CRT/VHS/Neon effects
3. Save to `output/` (e.g., y2k_image_1.png)

Flow B (upload)
1. Click UPLOAD IMAGE and pick a file
2. Apply effects
3. Save to `output/`

### 3) Random → Surprise
1. Click RANDOM Y2K EFFECT
2. Save to `output/` (e.g., y2k_random_1.png)

---

## Tips

- Use short phrases for bolder Y2K styling
- Try contrasting colors for retro vibes
- Drag the pet window anywhere; right-click for menu

---

## Troubleshooting

- If the app doesn’t start, ensure dependencies are installed in the workspace `.venv`
- For EXE builds that fail due to missing DLLs, install Visual C++ Redistributable (see README)
- Output images are saved next to the script/EXE in the `output/` folder
## Effects 效果简介
- CRT: 扫描线 + RGB 偏移
- VHS: 抖动/拖影/噪点
- Holographic/Chrome/Neon: 全息/镀铬/霓虹质感
- Pixelate: 像素化（8/16-bit 风格）

效果实现见 `effects/` 与 `generators/meme_engine.py`。

---

## Tips 小贴士

- 输出文件保存在 `output/`，按类型与编号自动递增命名。
- 建议图片宽度不小于 800px；文字 Meme 默认画布约 800x400。
- VS Code 运行请确认选择 `.venv` 解释器并已安装依赖。

---

## Troubleshooting 速查

Q: 运行时报 ModuleNotFoundError（如 PyQt6）
A: 切换到 `.venv` 解释器并安装依赖：`pip install PyQt6 Pillow numpy opencv-python pygame pywin32 requests`

Q: 窗口不显示/黑屏
A: 关闭残留进程，重装 PyQt6，或使用 `run_app.bat`。

Q: 输出没有出现
A: 检查 `output/` 是否存在，没有则手动创建或检查写入权限。

---

## Build EXE 打包（可选）

```powershell
pip install pyinstaller
python build_exe.py
```

成品位于 `dist/CRT_Buddy.exe`。
- **���** CD���桢��ֽ���
