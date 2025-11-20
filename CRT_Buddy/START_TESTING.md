# ?? CRT Buddy - �����ɣ���������ָ��

## ? ���״̬��100% �ɹ�

���CRT Buddy�Ѿ��ɹ����Ϊ������Windows��ִ���ļ���

---

## ?? �������ԣ�3�ַ�ʽ��

### ��ʽ1: ʹ�ÿ��ٲ��Խű����Ƽ���
```
˫������: quick_test.bat

����:
# CRT Buddy — Start Testing

English-only testing and packaging checklist (Windows).

---

## Quick Smoke

1) Run quick_test.bat (if present)
	- Verify EXE launches
	- Buttons clickable
	- Text generation saves to output/
	- Pixel font loads

2) Direct run dist\CRT_Buddy.exe (if built)

3) Terminal run (source)
```powershell
python start.py
python CRT_Buddy.py
```

---

## Build meta

- Artifact: CRT_Buddy.exe (PyInstaller)
- Deps: PyQt6, Pillow, NumPy, OpenCV

---

## Manual checks

- [ ] Window shows without crash
- [ ] Text → saved to output/
- [ ] Image → import/apply/save OK
- [ ] Random → generated and saved
- [ ] Menu/drag/always-on-top OK

---

## Repro steps (examples)

Text → Meme:
1. Type “Y2K VIBES ONLY”
2. Click GENERATE MEME
3. View output\y2k_text_1.png

Image → Effect:
1. Drag or upload PNG/JPG
2. Apply CRT effect
3. Save to output\y2k_image_1.png

Random → Effect:
1. Click RANDOM Y2K EFFECT
2. Save to output\y2k_random_1.png

---

## EXE issues

Missing DLL → install VC++ runtime:
https://aka.ms/vs/17/release/vc_redist.x64.exe

Black screen/no response → run from terminal to see logs; ensure antivirus isn’t blocking.

---

## Performance (approx.)

- Cold start: < 1s
- Text gen: 1–3s
- First image import: < 1s

---

## Release tips

1) Artifacts
	- dist/CRT_Buddy.exe
	- README/USAGE/QUICKSTART

2) Archive
	- Include one example image + how-to

3) GitHub Release
	- Tag + release with notes

---

Made for Y2K lovers.


---
