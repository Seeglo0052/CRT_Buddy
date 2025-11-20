or

# CRT Buddy — Y2K Desktop Pet & Meme Generator

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-ff00ff)
![Python](https://img.shields.io/badge/python-3.8+-00ffff)
![License](https://img.shields.io/badge/license-MIT-00ff00)

Tiny Y2K desktop pet and meme generator. Apply CRT scanlines, VHS jitter, holographic/chrome/neon glow, pixelation and more to text or images, then save to the output folder.

</div>

---

## Features

- Floating, frameless, always-on-top “desktop pet” window
- Y2K effects: CRT, VHS, holographic/chrome/neon, pixelate, and more
- Text/Image/Random meme generation flows
- Bundled pixel font: DinkieBitmap (9px, 7px)
- Simple save flow with auto-incrementing filenames in `output/`

---

## Install

```
pip install PyQt6 Pillow numpy opencv-python pygame pywin32 requests
```

---

## Run

Open `CRT_Buddy/CRT_Buddy/CRT_Buddy.py` in VS Code, select the correct interpreter (.venv), and click “Run Python File”.

Or use the command line:

```powershell
cd "C:\Users\Administrator\Desktop\SD5913(CREATIVE PROGRAMMING FOR DESIGNERS AND ARTISTS)\FP\CRT_Buddy\CRT_Buddy"
python CRT_Buddy.py
# Or: python start.py (runs dependency check first)
# Or: double-click/run run_app.bat (one-click launch)
```

On first launch, if you see “Starting CRT Buddy…” and the pixel font loads, setup is successful.

---

## Usage

Main interface offers three generation modes:

1) Text Meme Generation
   - Type a phrase like “Y2K VIBES ONLY” in the text box, click GENERATE MEME

2) Image Meme Generation
   - Click UPLOAD IMAGE to select PNG/JPG/GIF/BMP
   - Apply Y2K effects and save

3) Random Effect Generation
   - Click RANDOM Y2K EFFECT to generate and save

Output files are saved in the `output/` directory, named incrementally (e.g., y2k_text_1.png, y2k_image_1.png, y2k_random_1.png).

---

## Effects (Quick Overview)

- CRT: Scanlines + RGB offset, simulates CRT tube
- VHS: Jitter/noise/ghosting, tape flavor
- Holographic/Chrome/Neon: Holographic/chrome/neon text and highlights
- Pixelate: Pixelation and grid effects

Visual effect code is in `effects/` and `generators/meme_engine.py`.

---

## Project Structure

```
CRT_Buddy/
   CRT_Buddy.py        # main entry
   start.py            # dependency check + launcher
   run_app.bat         # one-click Windows launcher
   core/               # main window, pixel font, UI logic
   effects/            # Y2K visual effects
   generators/         # text/image/random generation engine
   output/             # output directory
```

---

## Build EXE (Optional)

Build a standalone executable with PyInstaller:

```powershell
pip install pyinstaller
pyinstaller --name "CRT_Buddy" --onefile --windowed CRT_Buddy.py
# Or use the script:
python build_exe.py
```

The executable will be in `dist/CRT_Buddy.exe`.

---

## Troubleshooting

- ModuleNotFoundError: Make sure VS Code uses the workspace `.venv` and install dependencies there.
- Qt plugin/window issues: Reinstall PyQt6, or use `run_app.bat` to launch.
- Font not loading: Check that `DinkieBitmap-v*/ttf/DinkieBitmap-9px.ttf` exists.
- Missing DLLs in EXE: Install Visual C++ Redistributable: https://aka.ms/vs/17/release/vc_redist.x64.exe
- Can’t find results: Check the `output/` folder next to your script or EXE.

---

## License & Credits

MIT License. Pixel font: DinkieBitmap (see `DinkieBitmap-v*/EULA.txt`).

Inspiration: early web, Geocities/Netscape aesthetics, CRT/arcade culture, Bonzi Buddy-era mascots.
