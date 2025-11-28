# CRT Buddy

CRT Buddy is a retro-inspired desktop mascot and meme generator that brings Y2K aesthetics and playful interactivity to your computer. Featuring pixel fonts, animated effects, and a customizable mascot, CRT Buddy is both a productivity companion and a creative tool for producing vintage-style memes.

## Features

- Desktop Mascot: An adorable, animated mascot that reacts to user actions and keeps you company.
- Meme Generator: Create Y2K-style memes with custom text and images.
- Input Visualization: Real-time keystroke tracking and visualization with stats and history.
- Retro UI: Uses DinkieBitmap pixel fonts and CRT-style effects for an authentic old-school look.
- Customizable Effects: Includes Y2K text effects, particle animations, and more.
- Cross-Platform: Runs on Windows, macOS, and Linux (Python 3.8+).
- AI Hub: Optional AI chat, image generation, and a typing game via an OpenAI-compatible API.

## Installation

1. Clone the repository:

```powershell
git clone https://github.com/Seeglo0052/CRT_Buddy.git
cd CRT_Buddy
```

2. Set up a Python virtual environment (recommended):

```powershell
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```powershell
pip install -r CRT_Buddy/requirements.txt
```

If you run into issues with Pillow or PyQt6, make sure pip and wheel are up to date:

```powershell
pip install --upgrade pip wheel
```

4. Run the application:

```powershell
cd CRT_Buddy
python main.py
```

### Optional: Enable AI features (AI Hub)

You can use multiple providers for Chat and Image separately. Configure via environment variables or `CRT_Buddy/config.ini` under the `[AI]` section.

Supported providers (Chat): `openai`, `deepseek`, `groq`, `moonshot`, `siliconflow`, `ollama`, `volcengine`, `doubao`, `custom`

Supported providers (Image): `openai`, `stability`, `ollama`, `fal`, `replicate`, `doubao`, `custom`

- Environment variables:
   - Ark (Doubao): `ARK_API_KEY`, `ARK_BASE_URL` (e.g. `https://ark.cn-beijing.volces.com/api/v3`)
   - OpenAI-compatible: `OPENAI_API_KEY`, `OPENAI_BASE_URL` (or generic `AI_API_KEY`, `AI_BASE_URL`)

- Config file (`CRT_Buddy/config.ini`):
   - `chat_provider = deepseek` (example)
   - `base_url = https://api.deepseek.com/v1`
   - `chat_model = deepseek-chat`
   - `api_key = sk-...` (your chat key)
   - `image_provider = doubao`
   - `image_base_url = https://ark.cn-beijing.volces.com/api/v3`
   - `image_model = doubao-seedream-3-0-t2i-250415`
   - `image_api_key = 8bcf64fb-...` (your Ark image key)

In the app, click the AI HUB button to access Chat, Image, and Typing Game. Settings persist across sessions.

## Usage

- Mascot Window: The mascot lives on your desktop. Drag it, interact with it, and watch it react to keystrokes.
- Meme Generation: Use the meme generator to create custom memes. Access it from the main window or call `generators/meme_engine.py` directly.
- Input Visualization: Keystrokes are tracked and visualized in real time. Stats and history are shown in the mascot window.
- Customization: Fonts, effects, and mascot behavior can be adjusted via `config.ini` and the core/effects modules.

## Project Structure

- `CRT_Buddy/`
   - `main.py`: Main application entry point.
   - `core/pet_window.py`, `core/pet_window_v5.py`, `core/pet_window_v6.py`: Mascot window implementations.
   - `generators/meme_engine.py`: Meme generation engine.
   - `effects/`: Visual effects and styles (Y2K filters, text effects).

## Architecture

High-level components:
- Core UI: `core/pet_window_v7.py` (v8 alias), creates the main window, AI Hub dialog (Chat/Image/Typing Game), timers, and event wiring.
- AI Client: `ai/client.py` provides OpenAI-compatible chat and image generation; Doubao (Ark) uses `/chat/completions` and `/images/generations`.
- AI Widgets: `ai/widgets.py` contains `AIChatWidget`, `AISettingsWidget`, `AIImageWidget`, and `TypingGameWidget`. Settings persist in `CRT_Buddy/config.ini` and emit live updates.
- Generators: `generators/meme_engine.py` implements meme creation APIs.
- Effects: `effects/text_effects.py`, `effects/y2k_styles.py` implement Y2K visual filters.
- Utilities: `util/net.py` provides robust `fetch_with_retry` network calls.

Configuration flow:
- Load: `ai/client.py` reads `CRT_Buddy/config.ini` then environment variables (Ark overrides first).
- Save: `AISettingsWidget.on_save()` writes the `[AI]` section and emits `settings_updated` to update Chat/Image.
- Live apply: `AIChatWidget.apply_settings()` and `AIImageWidget.apply_settings()` update provider/base/model/key without restart.

Endpoints:
- Chat (Doubao): `POST {ARK_BASE_URL}/chat/completions` with standard `messages`.
- Image (Doubao): `POST {ARK_BASE_URL}/images/generations` with `prompt`, `size`; supports `b64_json` or `url`.

Logging:
- `output/ai_log.txt` captures request snippets and errors to aid troubleshooting.

Entry points:
- `CRT_Buddy/main.py` default launcher; `CRT_Buddy/CRT_Buddy.py` alt launcher.
- v8 alias: `core/pet_window_v8.py` references v7 implementation.

Error handling:
- Network retries in image tests; defensive fallbacks for varying response shapes.

Persistence:
- `.gitattributes` treats virtualenv as vendored to fix GitHub language stats.

Known notes:
- Provider coexistence supported (e.g., DeepSeek for chat + Doubao for image).

## Version History (summary)

- v8 (alias): Route main to v8 while using v7 window; AI Hub restored after widget fixes; Doubao chat/image standardized.
- v7: AI Hub introduced with Chat/Image/Typing Game; provider presets and settings persistence; Y2K effects expanded.
- v6: Input visualization, CPM tracking, improved window layout; effects refinements.
- v5.2 / v5.1 / v5.0: Pixel font support, horizontal layout, metallic UI polish, bug fixes.
- v4 and earlier: Core meme engine and initial Y2K filters established.

See CHANGELOG and `V*` docs in `CRT_Buddy/` for detailed milestones.
---

## Custom theme

You can customize the color constants used by the app:

```python
screen_color = QColor(0, 40, 80)      # deep blue
scan_color = QColor(0, 255, 255)      # cyan

text_color = QColor(0, 255, 255)      # cyan
glow_color = QColor(255, 0, 255)      # magenta

metal_color = QColor(220, 230, 240)   # silver
```

---

## Troubleshooting
### AI — Doubao (Ark) endpoints

- Chat: uses OpenAI-compatible `POST {ARK_BASE_URL}/chat/completions`
- Image: uses OpenAI-compatible `POST {ARK_BASE_URL}/images/generations`

Common issues:
- 404: Base URL wrong. Use `https://ark.cn-beijing.volces.com/api/v3` (no extra path).
- 401: API key format/region mismatch. Use Ark key for Doubao, not OpenAI/DeepSeek keys.
- Empty response: Temporary service issue or payload mismatch; check `output/ai_log.txt`.

### AI — Provider coexistence

You can set DeepSeek for chat and Doubao for images simultaneously. Use the Settings tab in AI Hub:
- Save after editing, then Image tab Apply Key if needed.
- Changes apply immediately; config is stored in `CRT_Buddy/config.ini`.

### Font not rendering correctly

If the UI uses the system font instead of the pixel font:
1. Verify `DinkieBitmap-v1.5.0-KeDingKeMao/ttf/` exists
2. Look for "Loaded pixel font" output in the terminal
3. If necessary, correct the path used by `load_pixel_font()`

### Module import errors

If you see `ModuleNotFoundError: No module named 'effects'`:

```powershell
cd CRT_Buddy
python main.py
```

### Image processing failures

- Ensure the input image is in a supported format (PNG, JPG, JPEG, GIF, BMP)
- Verify the image is not corrupted
## Features (short)

- Desktop mascot with Y2K UI and pixel fonts
- Meme generator + Y2K effects
- Keystroke visualization (CPM, history)
- AI Hub: Chat, Image, Typing Game
self.anim_timer.start(100)  # increase from 50 to 100 to lower frame rate

## Changelog
### v7.0 (2025-11-21)
- Added 4 animated Y2K backgrounds and background rotation
- Added image validation and retry logic for network requests
- Added `background_change_interval` (default 4 frames) and `background_rotate` flags
- Defaulted text flicker to "breath" mode with adjustable period
- Implemented text length limiting and added a test case
- Refactored text validation in MemeEngine and added tests
- Fixed background rendering bug that sometimes produced black frames
### AI Hub (brief)

- Chat providers: openai, deepseek, groq, moonshot, siliconflow, ollama, volcengine, doubao
- Image providers: openai, stability, ollama, fal, replicate, doubao
- Doubao/Ark:
   - Base: `https://ark.cn-beijing.volces.com/api/v3`
   - Chat: `POST /chat/completions`
   - Image: `POST /images/generations`
- DeepSeek:
   - Base: `https://api.deepseek.com/v1`
   - Chat model: `deepseek-chat`

Configure in `CRT_Buddy/config.ini` under `[AI]` or via env vars (`ARK_API_KEY`, `ARK_BASE_URL`, `OPENAI_API_KEY`, `OPENAI_BASE_URL`). Click AI HUB to use Chat/Image/Typing Game.
### v6.0 (2025-11-18)
## Usage (short)

- Run mascot window; drag and interact
- Generate memes from the main UI
- Typing visualization with CPM and history
- Customize via `config.ini`
- Improved window layout (520x320)
- Fixed import path issues
## Architecture (short)

- Core UI: `core/pet_window_v7.py` (v8 alias)
- AI Client: `ai/client.py` (OpenAI-compatible; Doubao uses `/chat/completions` & `/images/generations`)
- AI Widgets: `ai/widgets.py` (Chat/Settings/Image/Typing)
- Generators: `generators/meme_engine.py`
- Effects: `effects/*`
- Report bugs via Issues
## Version History (short)

- v8: v7 alias with AI Hub fixes; Doubao endpoints standardized
- v7: AI Hub (Chat/Image/Typing), presets & persistence
- v6: Input visualization & layout improvements
- v5.x: Pixel fonts & Y2K UI polish
- v4-: Core engine & filters


## Troubleshooting (short)

- 404: Check Ark base URL (`https://ark.cn-beijing.volces.com/api/v3`)
- 401: Use the correct provider key (Ark vs DeepSeek/OpenAI)
- See `output/ai_log.txt` for error snippets
---


---

<div align="center">Made with ❤️ and Y2K energy</div>

## Highlights

- 🖥️ CRT display effects — realistic cathode-ray tube simulation with scanlines and RGB offset
- 🤖 Cute desktop mascot — blinks, tracks the mouse, and displays different expressions
- � Y2K meme generator — multiple retro filters (VHS, holographic, neon, pixelation, etc.)
- ⌨️ Input visualization — real-time keystroke display, CPM, and particle effects
- 💾 Pixel fonts — uses DinkieBitmap to recreate authentic pixelated type

---

## Animated usage example
engine = MemeEngine(output_dir='output')
<!-- Screenshots and long examples omitted for brevity -->
      frames=32,
      background_change_interval=4,
      background_rotate=True,
      flicker_mode='breath',
      flicker_speed_multiplier=1.0,
      flicker_amplitude=0.08,
      output_filename='y2k_forever.gif'
)
print('Saved animated meme to', path)
```

Low-level call example (useful for testing or custom pipelines):

```python
from effects.text_effects import TextEffects
from PIL import Image, ImageFont

# create a blank base image and draw animated frames with TextEffects
font = ImageFont.truetype('DinkieBitmap-v1.5.0-KeDingKeMao/ttf/DinkieBitmap-9px.ttf', 24)
effects = TextEffects()
frames = effects.render_animated_text(
      text='Y2K',
      font=font,
      size=(800, 600),
      frames=32,
      flicker_mode='breath'
)
# frames is a list of PIL.Image objects you can save as GIF

---

## Quickstart checklist

1. Ensure the pixel fonts under `DinkieBitmap-v1.5.0-KeDingKeMao/ttf/` are present.
2. Create and activate a virtual environment.
3. Install dependencies with `pip install -r CRT_Buddy/requirements.txt`.
4. Run `python main.py` from the `CRT_Buddy` folder.

---

If you'd like, I can now run a repository-wide check for any remaining non-ASCII CJK characters and fix them across docs as well.
   duration=60,
   flicker=True,
   flicker_mode='breath',
   flicker_speed_multiplier=384,
   flicker_amplitude=2,
   background_change_interval=4,
   background_rotate=True,
)
print('Saved:', path)
```

Or call the lower-level `TextEffects` directly for more control:

```python
from effects.text_effects import TextEffects

te = TextEffects()
images, duration = te.render_animated_text(
   'HELLO', size=(800,600), frames=24,
   flicker=True, flicker_mode='breath', flicker_speed_multiplier=192,
   background_change_interval=6, background_rotate=True
)
# then save with te.save_animated_text(images, 'out.gif', duration=duration)
```


Random generation

1. Click the RANDOM button
2. The app will:
   - Pick a classic Y2K phrase
   - Apply a random text effect
   - Choose a canvas size
3. The generated image is saved to the `output` folder

### Input visualization

1. Click the text box to start typing
2. Watch the CRT screen:
   - Large central display shows the current key
   - A key history list is displayed at the bottom
   - Particle effects appear on keypress
3. Viewing stats:
   - The top status bar shows total key count and typing speed (CPM)

### Shortcuts

- Drag window: click and drag anywhere on the window
- Close app: click the circular X button in the bottom-right
- View outputs: open the `output` folder to see generated images

---

## 📸 Screenshots

### Main interface (ASCII mockup)
```
┌─────────────────────────────────────────────┐
│  CRT BUDDY v7.0            [LED] ●          │
├───────────┬─────────────────────────────────┤
│           │  CRT BUDDY v7.0 - VISUALIZER    │
│           │  KEYS: 42 | SPEED: 180 CPM      │
│    CRT    │                                 │
│  ┌─────┐  │  ┌─────────────────────────┐   │
│  │ 👀  │  │  │ Type here...            │   │
│  │ 😊  │  │  └─────────────────────────┘   │
│  └─────┘  │                                 │
│  [keys]   │  [███ GENERATE ███]            │
│           │  [███  IMAGE   ███]            │
│           │  [███  RANDOM  ███]            │
│           │                    ⦿            │
└───────────┴─────────────────────────────────┘
```

### Effects showcase

**Text effect examples:**
- Gradient: rainbow gradient text
- Glitch: RGB separation glitch
- Neon: neon glow effect
- Chrome: metallic chrome shine
- Retro: classic rainbow stripes

**Image filter examples:**
- CRT: vintage monitor / scanline effect
- VHS: tape distortion and noise
- Holographic: rainbow holographic overlay
- Pixelate: 8-bit pixelation

---

## 🛠️ Development

### Project structure

```
CRT_Buddy/
├── CRT_Buddy/
│   ├── main.py                    # application entry point
│   ├── config.ini                 # configuration file
│   ├── requirements.txt           # dependency list
│   │
│   ├── core/                      # core modules
│   │   ├── __init__.py
│   │   ├── pet_window.py          # base window class
│   │   ├── pet_window_v5.py       # v5: horizontal layout
│   │   └── pet_window_v6.py       # v6: input visualizer
│   │
│   ├── effects/                   # visual effects
│   │   ├── __init__.py
│   │   ├── y2k_styles.py          # Y2K image filters
│   │   └── text_effects.py        # text effects
│   │
│   ├── generators/                # generators
│   │   ├── __init__.py
│   │   └── meme_engine.py         # meme generation engine
│   │
│   └── output/                    # output directory
│       └── (generated images)
│
├── DinkieBitmap-v1.5.0-KeDingKeMao/  # pixel fonts
│   └── ttf/
│       └── DinkieBitmap-9px.ttf
│
├── README.md                      # this file
└── LICENSE                        # license
```

### Technology stack

- **GUI framework**: PyQt6
- **Image processing**: Pillow (PIL)
- **Numerical computing**: NumPy
- **Computer vision**: OpenCV
- **Fonts**: DinkieBitmap pixel fonts

### Core classes

#### CRTBuddyWindow
Main window class responsible for UI rendering and interactions.

**Key methods:**
- `paintEvent()` - custom CRT drawing
- `draw_mascot()` - draw the mascot
- `on_keystroke()` - handle key input
- `animate()` - animation loop

#### MemeEngine
The meme generation engine.

**Key methods:**
- `generate_text_meme()` - generate text-only memes
- `generate_image_meme()` - process image-based memes
- `generate_random_meme()` - generate a random meme
- `save_meme()` - save output to file

#### Y2KStyles
A collection of Y2K-style image filters.

**Available effects:**
- `crt_effect()` - CRT display
- `vhs_effect()` - VHS tape distortion
- `holographic_effect()` - holographic rainbow overlay
- `chrome_effect()` - metallic chrome
- `neon_effect()` - neon glow
- `pixelate_effect()` - 8-bit pixelation

### Custom configuration

You can edit the following parameters to customize behavior:

```python
# In pet_window_v6.py

# Window geometry
self.setGeometry(100, 100, 520, 320)

# Key history length
self.key_history = deque(maxlen=10)  # set to 20 to show more

# Particle effects
for _ in range(3):  # use 5 for more particles

# Mascot reaction frequency
if self.total_keystrokes % 10 == 0:  # change to 5 for more frequent reactions
```

### Adding new filter effects

```python
# In effects/y2k_styles.py

def my_custom_effect(self, img):
   """My custom image effect"""
   # your image processing code
   return img

# register in apply_effect()
effects = {
   'crt': self.crt_effect,
   'vhs': self.vhs_effect,
   'my_custom': self.my_custom_effect,  # add this line
}
```

---

## 🎨 Custom theme

The app uses classic Y2K colors by default. Change the color constants as needed:

```python
# CRT screen colors
screen_color = QColor(0, 40, 80)      # deep blue
scan_color = QColor(0, 255, 255)      # cyan

# Text/glow colors
text_color = QColor(0, 255, 255)      # cyan
glow_color = QColor(255, 0, 255)      # magenta

# Metal body color
metal_color = QColor(220, 230, 240)   # silver
```

---

## 🐛 Troubleshooting

### Fonts not rendering correctly

Problem: UI uses system fonts instead of the pixel font.

Solution:
1. Ensure `DinkieBitmap-v1.5.0-KeDingKeMao/ttf/` exists
2. Check terminal output for "Loaded pixel font"
3. If path is wrong, correct the path in `load_pixel_font()`

### Module import errors

Problem: `ModuleNotFoundError: No module named 'effects'`

Solution:
```bash
# Run from the project subfolder
cd CRT_Buddy
python main.py
```

### Image processing failures

Problem: App crashes during image processing

Solution:
1. Ensure image format is supported (PNG, JPG, JPEG, GIF, BMP)
2. Check that the image is not corrupted
3. Try converting the image to PNG

### Performance issues

Problem: App is lagging

Solution:
```python
# Adjust frame rate in setup_animations()
self.anim_timer.start(100)  # increase from 50 to 100 to lower frame rate

# Reduce particle count
for _ in range(1):  # reduce from 3 to 1
```

---

## 📝 Changelog

### v8.0 (2025-11-24)
- ✨ Added timed 【Rest Reminder】function

### v7.0 (2025-11-21)
- ✨ Added 4 Y2K animated backgrounds and background rotation
- ✨ Added image validation and retry logic for network requests
- ✨ Added `background_change_interval` (now default 4 frames) and `background_rotate` flags
- 🔧 Default "breath" text flicker mode; breathing period is adjustable
- 🔧 Implemented text length limit and added corresponding test case
- 🐛 Refactored text validation in MemeEngine and implemented comprehensive tests
- 🐛 Fixed background rendering bug (black frames)

### v6.0 (2025-11-18)
- ✨ Added input visualization system
- ✨ Real-time key display and key history
- ✨ Typing speed (CPM) tracking
- ✨ Particle effects on keypress
- 🎨 Improved window layout (520x320)
- 🐛 Fixed import path issues

### v5.1 (2025-11-17)
- ✨ Added pixel font support
- 🎨 Improved horizontal layout design
- 🎨 Polished metal button styles
- 😊 Added richer mascot expressions

### v5.0 (2025-11-16)
- ✨ New Y2K desktop PC styling
- ✨ Metallic buttons and chassis
- ✨ Circular power button
- 🐛 Fixed eye-tracking bug

### v4.0 and earlier
- Core functionality implemented
- Meme generation engine
- Y2K filter effects

---

## 🤝 Contributing

Contributions welcome! Ways to help:
1. 🐛 Report bugs via Issues
2. 💡 Suggest new features via Issues
3. 🔧 Submit PRs
4. 📖 Improve documentation
5. 🎨 Share creations made with CRT Buddy

### Contribution guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to your branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details

---

## 👨‍💻 Authors & Contributors

Primary author:
- **Seeglo0052** — [@Seeglo0052](https://github.com/Seeglo0052)

Contributors:
- [@Yiyuan0104](https://github.com/Yiyuan0104)
- [@Zhexi7777777](https://github.com/Zhexi7777777)
- [@wangleru](https://github.com/wangleru)

Project: https://github.com/Seeglo0052/CRT_Buddy

---

## 🙏 Thanks

- **DinkieBitmap** — pixel font pack
- **PyQt6** — GUI framework
- **Pillow** — image processing library
- Everyone who loves Y2K aesthetics and retro design

---

## 🌟 Star History

If this project helped you, please give it a ⭐!

---

<div align="center">

Made with ❤️ and Y2K aesthetics

[Back to top](#-crt-buddy)

</div>
