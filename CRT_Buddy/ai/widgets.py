"""Clean AI widgets module: Chat, Settings, Image, Typing Game.

Image section mirrors chat customization: selectable provider, model, base URL presets,
separate image API key. Stability provider does not lock other fields.
"""
from __future__ import annotations

import os, configparser, requests
from typing import Optional
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit,
    QPushButton, QFileDialog, QComboBox
)

from .client import AIClient, AIConfig
from util.net import fetch_with_retry, NetworkError


class AIChatWidget(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.client = AIClient()
        layout = QVBoxLayout(self)
        # History and input
        self.history = QTextEdit()
        self.history.setReadOnly(True)
        self.input = QTextEdit()
        self.input.setPlaceholderText("Enter message...")
        # Multimodal optional image URL
        self.image_url_input = QLineEdit()
        self.image_url_input.setPlaceholderText("Optional image URL (http/https) for multimodal")
        # Reasoning effort selector
        self.reasoning_select = QComboBox()
        self.reasoning_select.addItems(["auto", "none", "light", "medium", "heavy"])
        self.reasoning_select.setCurrentText("medium")
        # Buttons
        self.send_btn = QPushButton("Send")
        self.ping_btn = QPushButton("Ping")
        row = QHBoxLayout()
        row.addWidget(self.send_btn)
        row.addWidget(self.ping_btn)
        # Assemble layout
        layout.addWidget(QLabel("AI Chat"))
        layout.addWidget(self.history, 3)
        layout.addWidget(self.image_url_input)
        layout.addWidget(QLabel("Reasoning Effort"))
        layout.addWidget(self.reasoning_select)
        layout.addWidget(self.input, 1)
        layout.addLayout(row)
        # Signals
        self.send_btn.clicked.connect(self.on_send)
        self.ping_btn.clicked.connect(self.on_ping)
        # Provider info label
        self.provider_label = QLabel("Provider: " + (self.client.config.chat_provider or 'openai'))
        layout.addWidget(self.provider_label)

    def apply_settings(self, provider: str, base_url: str, model: str, api_key: str):
        # Update config in-place; no need to recreate client
        self.client.config.chat_provider = provider
        if api_key:
            self.client.config.api_key = api_key
        if base_url:
            self.client.config.base_url = base_url
        if model:
            self.client.config.chat_model = model
        self.provider_label.setText(f"Provider: {provider} | {model}")

    def _build_messages(self, user_text: str, image_url: Optional[str]) -> list:
        """Construct messages list; include image_url if provided and valid."""
        if image_url and (image_url.startswith("http://") or image_url.startswith("https://")):
            rich_user_content = [
                {"type": "image_url", "image_url": {"url": image_url}},
                {"type": "text", "text": user_text},
            ]
            return [
                {"role": "system", "content": [{"type": "text", "text": "You are a helpful assistant."}]},
                {"role": "user", "content": rich_user_content},
            ]
        # Text-only
        return [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_text},
        ]

    def on_send(self):
        text = self.input.toPlainText().strip()
        if not text:
            return
        img = self.image_url_input.text().strip()
        msgs = self._build_messages(text, img)
        effort = self.reasoning_select.currentText()
        effort_param = None if effort == "auto" else effort
        self.history.append(f"You: {text}" + (f" [img={img}]" if img else ""))
        ans = self.client.chat(msgs, reasoning_effort=effort_param)
        self.history.append("AI: " + (ans.strip() if ans else "(error)"))
        self.input.clear()

    def on_ping(self):
        msgs = [
            {"role": "system", "content": "Reply with PONG"},
            {"role": "user", "content": "PING"},
        ]
        ans = self.client.chat(msgs, max_tokens=8, temperature=0.0)
        self.history.append("Ping: " + (ans.strip() if ans else "(failed)"))


CHAT_PRESETS = {
    # provider: (base_url, default_model)
    "openai": ("https://api.openai.com/v1", "gpt-4o-mini"),
    "deepseek": ("https://api.deepseek.com/v1", "deepseek-chat"),
    "groq": ("https://api.groq.com/openai/v1", "llama3-8b-8192"),
    "moonshot": ("https://api.moonshot.cn/v1", "moonshot-v1-8k"),
    "siliconflow": ("https://api.siliconflow.cn/v1", "qwen2.5-7b-instruct"),
    "ollama": ("http://localhost:11434/v1", "llama3.2:latest"),
    "volcengine": ("https://ark.cn-beijing.volces.com/api/v3", "ep-claude-3-5-sonnet"),
    "doubao": ("https://ark.cn-beijing.volces.com/api/v3", "doubao-seed-1-6-251015"),
    # custom: no defaults
}

IMAGE_PRESETS = {
    "openai": ("https://api.openai.com/v1", "gpt-image-1"),
    "stability": ("https://api.stability.ai", "stable-diffusion-v1-6"),
    "ollama": ("http://localhost:11434/v1", "stable-diffusion:latest"),
    "fal": ("https://fal.run/v1", "fal-ai/flux/dev"),
    "replicate": ("https://api.replicate.com/v1", "black-forest-labs/flux-pro"),
    "doubao": ("https://ark.cn-beijing.volces.com/api/v3", "doubaoseedream-3-0-t2i-250415"),
}

class AISettingsWidget(QWidget):
    """Settings with extended provider choices and sensible defaults.

    Chat Providers: openai, deepseek, groq, moonshot, siliconflow, ollama, volcengine, custom
    Image Providers: openai, stability, ollama, fal, replicate, custom
    """
    from PyQt6.QtCore import pyqtSignal
    settings_updated = pyqtSignal(dict)
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        # Chat fields
        self.chat_provider = QComboBox(); self.chat_provider.addItems(["openai", "deepseek", "groq", "moonshot", "siliconflow", "ollama", "volcengine", "doubao", "custom"])
        self.chat_model = QLineEdit("gpt-4o-mini")  # will be replaced by defaults on provider selection
        self.base_url = QLineEdit(); self.base_url.setPlaceholderText("Chat Base URL (e.g. https://api.openai.com/v1)")
        self.api_key = QLineEdit(); self.api_key.setPlaceholderText("Chat API Key")

        # Image fields
        self.image_provider = QComboBox(); self.image_provider.addItems(["openai", "stability", "ollama", "fal", "replicate", "doubao", "custom"])
        self.image_model = QLineEdit("gpt-image-1")  # replaced by defaults
        self.image_base_url = QLineEdit(); self.image_base_url.setPlaceholderText("Image Base URL (optional)")
        self.image_api_key = QLineEdit(); self.image_api_key.setPlaceholderText("Image API Key (optional)")

        # Buttons
        self.save_btn = QPushButton("Save Settings")
        self.test_chat_btn = QPushButton("Test Chat")
        self.test_image_btn = QPushButton("Test Image")
        self.status = QLabel("")

        def add(label: str, w: QWidget):
            layout.addWidget(QLabel(label)); layout.addWidget(w)
        add("Chat Provider", self.chat_provider)
        add("Chat Model", self.chat_model)
        add("Chat Base URL", self.base_url)
        add("Chat API Key", self.api_key)
        add("Image Provider", self.image_provider)
        add("Image Model", self.image_model)
        add("Image Base URL", self.image_base_url)
        add("Image API Key", self.image_api_key)
        row = QHBoxLayout(); row.addWidget(self.save_btn); row.addWidget(self.test_chat_btn); row.addWidget(self.test_image_btn); layout.addLayout(row)
        layout.addWidget(self.status)

        # Signals
        self.save_btn.clicked.connect(self.on_save)
        self.test_chat_btn.clicked.connect(self.on_test_chat)
        self.test_image_btn.clicked.connect(self.on_test_image)
        self.chat_provider.currentTextChanged.connect(self._apply_chat_provider_defaults)
        self.image_provider.currentTextChanged.connect(self._apply_image_provider_defaults)

        # Load existing config
        self._load()
        self._apply_chat_provider_defaults(self.chat_provider.currentText())

    # ----- Config helpers -----
    def _cfg_path(self) -> str:
        here = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        p = os.path.join(here, "config.ini")
        if not os.path.exists(p): p = os.path.join(os.path.dirname(here), "config.ini")
        return p

    def _load(self):
        cfg = configparser.ConfigParser()
        try:
            cfg.read(self._cfg_path(), encoding="utf-8")
            if cfg.has_section("AI"):
                g = lambda k, d="": cfg.get("AI", k, fallback=d)
                self.chat_provider.setCurrentText(g("chat_provider", self.chat_provider.currentText()))
                self.chat_model.setText(g("chat_model", self.chat_model.text()))
                self.base_url.setText(g("base_url"))
                self.api_key.setText(g("api_key"))
                self.image_provider.setCurrentText(g("image_provider", self.image_provider.currentText()))
                self.image_model.setText(g("image_model", self.image_model.text()))
                self.image_base_url.setText(g("image_base_url"))
                self.image_api_key.setText(g("image_api_key"))
        except Exception:
            pass

    def on_save(self):
        cfg = configparser.ConfigParser(); path = self._cfg_path()
        try:
            cfg.read(path, encoding="utf-8")
        except Exception:
            pass
        if not cfg.has_section("AI"):
            cfg.add_section("AI")
        s = cfg.set
        s("AI", "chat_provider", self.chat_provider.currentText().strip())
        s("AI", "chat_model", self.chat_model.text().strip())
        s("AI", "base_url", self.base_url.text().strip())
        s("AI", "api_key", self.api_key.text().strip())
        s("AI", "image_provider", self.image_provider.currentText().strip())
        s("AI", "image_model", self.image_model.text().strip())
        s("AI", "image_base_url", self.image_base_url.text().strip())
        s("AI", "image_api_key", self.image_api_key.text().strip())
        with open(path, "w", encoding="utf-8") as f:
            cfg.write(f)
        self.status.setText(f"Saved -> {path}")
        self.settings_updated.emit({
            "chat_provider": self.chat_provider.currentText().strip(),
            "chat_model": self.chat_model.text().strip(),
            "base_url": self.base_url.text().strip(),
            "api_key": self.api_key.text().strip(),
        })

    # ----- Chat presets -----
    def _apply_chat_provider_defaults(self, provider: str):
        p = provider.lower()
        if p in CHAT_PRESETS:
            base, model = CHAT_PRESETS[p]
            # Only overwrite if field empty or previous provider's default
            if not self.base_url.text().strip() or any(self.base_url.text().strip().startswith(v[0]) for v in CHAT_PRESETS.values()):
                self.base_url.setText(base)
            # Overwrite chat model if blank or previous default
            if self.chat_model.text().strip() in ("", "gpt-4", "gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo", "deepseek-chat", "llama3-8b-8192", "moonshot-v1-8k", "qwen2.5-7b-instruct", "llama3.2:latest", "ep-claude-3-5-sonnet"):
                self.chat_model.setText(model)
        # custom => leave user values untouched

    def _apply_image_provider_defaults(self, provider: str):
        p = provider.lower()
        if p in IMAGE_PRESETS:
            base, model = IMAGE_PRESETS[p]
            if not self.image_base_url.text().strip() or any(self.image_base_url.text().strip().startswith(v[0]) for v in IMAGE_PRESETS.values()):
                self.image_base_url.setText(base)
            if self.image_model.text().strip() in ("", "gpt-image-1", "stable-diffusion-v1-6", "stable-diffusion:latest", "fal-ai/flux/dev", "black-forest-labs/flux-pro"):
                self.image_model.setText(model)

    # Removed preset syncing logic; user requested only explicit base URL field.

    # ----- Image presets -----
    def _on_image_provider_changed(self, provider: str):
        # Minimal hint: if switching to stability, replace default openai image model
        if provider.lower() == "stability" and self.image_model.text().strip() == "gpt-image-1":
            self.image_model.setText("stable-diffusion-v1-6")

    # ----- Tests -----
    def on_test_chat(self):
        key = self.api_key.text().strip(); base = self.base_url.text().strip().rstrip('/') or 'https://api.openai.com/v1'
        if not key: self.status.setText("Enter chat API key"); return
        client = AIClient(AIConfig(api_key=key, base_url=base, chat_model=self.chat_model.text().strip()))
        msg = [{"role": "system", "content": "Reply with PONG"}, {"role": "user", "content": "PING"}]
        ans = client.chat(msg, max_tokens=8, temperature=0.0)
        self.status.setText("Chat OK: " + ans.strip()[:32] if ans else "Chat failed")

    def on_test_image(self):
        provider = self.image_provider.currentText().strip().lower(); self.status.setText("Testing image...")
        key = (self.image_api_key.text().strip() or self.api_key.text().strip())
        if not key:
            self.status.setText("Enter image API key")
            return
        if provider == "doubao":
            base = self.image_base_url.text().strip().rstrip('/') or 'https://ark.cn-beijing.volces.com/api/v3'
            model = self.image_model.text().strip()
            url = f"{base}/images/generate"
            headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
            payload = {"model": model, "prompt": "ping", "size": "512x512"}
            try:
                r = fetch_with_retry('POST', url, headers=headers, json=payload, timeout=45, retries=0, backoff_base=0.3)
                snippet = r.text[:120].replace('\n', ' ').strip()
                if r.status_code == 200:
                    self.status.setText(f"Doubao OK /images/generate -> {snippet[:40]}")
                else:
                    self.status.setText(f"Doubao HTTP {r.status_code}: {snippet}")
                return
            except Exception as e:
                self.status.setText(f"Doubao error: {e}")
            return
        if provider == "stability":
            base = self.image_base_url.text().strip().rstrip('/') or 'https://api.stability.ai'
            try:
                r = fetch_with_retry('GET', f"{base}/v1/engines/list", headers={"Authorization": f"Bearer {key}"}, timeout=15, retries=2, backoff_base=0.5)
                self.status.setText("Stability OK" if r.status_code == 200 else f"Stability HTTP {r.status_code}")
            except Exception as e:
                self.status.setText(f"Stability error: {e}")
            return
        base = self.image_base_url.text().strip().rstrip('/') or (self.base_url.text().strip().rstrip('/') or 'https://api.openai.com/v1')
        for ep in ["/models", "/images/models", "/v1/models"]:
            url = f"{base}{ep}" if not base.endswith(ep) else base
            try:
                r = fetch_with_retry('GET', url, headers={"Authorization": f"Bearer {key}"}, timeout=12, retries=2, backoff_base=0.4)
                if r.status_code == 200:
                    self.status.setText(f"Image OK ({ep})")
                    return
            except Exception:
                continue
        self.status.setText("Image endpoint unreachable")


class WorkerImage(QThread):
    finished = pyqtSignal(bytes)
    def __init__(self, client: AIClient, prompt: str, parent: Optional[QWidget] = None):
        super().__init__(parent); self.client = client; self.prompt = prompt
    def run(self):
        try:
            data = self.client.generate_image(self.prompt) or b""
        except Exception:
            data = b""
        self.finished.emit(data)


class AIImageWidget(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.client = AIClient()
        layout = QVBoxLayout(self)
        self.prompt = QTextEdit(); self.prompt.setPlaceholderText("Describe the image...")
        self.gen_btn = QPushButton("Generate Image")
        self.preview = QLabel("Preview"); self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.save_btn = QPushButton("Save Image"); self.save_btn.setEnabled(False)
        self.image_key_input = QLineEdit(self.client.config.image_api_key or self.client.config.api_key or "")
        self.image_key_input.setPlaceholderText("Image API Key (session override)")
        self.apply_key_btn = QPushButton("Apply Key")
        layout.addWidget(QLabel("AI Image Generator"))
        layout.addWidget(self.prompt)
        layout.addWidget(self.gen_btn)
        layout.addWidget(self.preview, 1)
        layout.addWidget(self.save_btn)
        r = QHBoxLayout(); r.addWidget(self.image_key_input); r.addWidget(self.apply_key_btn); layout.addLayout(r)
        self.gen_btn.clicked.connect(self.on_generate)
        self.save_btn.clicked.connect(self.on_save)
        self.apply_key_btn.clicked.connect(self.on_apply_key)
        self._last: Optional[bytes] = None

    def on_apply_key(self):
        self.client.config.image_api_key = self.image_key_input.text().strip() or None
        self.preview.setText("Image key applied.")

    def on_generate(self):
        p = self.prompt.toPlainText().strip()
        if not p: return
        self.preview.setText("Generating...")
        self.worker = WorkerImage(self.client, p)
        self.worker.finished.connect(self.on_image)
        self.worker.start()

    def on_image(self, data: bytes):
        if not data:
            self.preview.setText("Generation failed (key/network)")
            self.save_btn.setEnabled(False); return
        self._last = data
        pm = QPixmap(); pm.loadFromData(data)
        self.preview.setPixmap(pm.scaled(512, 512, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.save_btn.setEnabled(True)

    def on_save(self):
        if not self._last: return
        fn, _ = QFileDialog.getSaveFileName(self, "Save Image", "ai_image.png", "PNG Files (*.png)")
        if not fn: return
        try:
            with open(fn, 'wb') as f: f.write(self._last)
        except Exception as e:
            self.preview.setText(f"Save error: {e}")


class TypingGameWidget(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.prompt_label = QLabel("Press Start for prompt")
        self.text = QTextEdit(); self.text.setPlaceholderText("Type here...")
        self.start_btn = QPushButton("Start")
        self.stats = QLabel("WPM: 0 | Accuracy: 100%")
        layout.addWidget(QLabel("Typing Game"))
        layout.addWidget(self.prompt_label); layout.addWidget(self.text); layout.addWidget(self.start_btn); layout.addWidget(self.stats)
        self.start_btn.clicked.connect(self.on_start); self.text.textChanged.connect(self.on_type)
        self._target = ""; self._start_ts = 0.0

    def on_start(self):
        import random, time
        samples = ["HELLO FROM CRT BUDDY", "RETRO FUTURE Y2K VIBES", "TYPING GAME START NOW", "GENERATE COOL MEMES"]
        self._target = random.choice(samples); self._start_ts = time.time()
        self.prompt_label.setText(self._target); self.text.clear(); self.stats.setText("WPM: 0 | Accuracy: 100%")

    def on_type(self):
        import time
        if not self._target or not self._start_ts: return
        typed = self.text.toPlainText(); elapsed = max(1e-6, time.time() - self._start_ts)
        wpm = (len(typed)/5.0)/(elapsed/60.0)
        correct = sum(1 for a,b in zip(typed, self._target) if a==b)
        acc = 100.0 * (correct / max(1, len(typed)))
        self.stats.setText(f"WPM: {int(wpm)} | Accuracy: {int(acc)}%")


__all__ = ["AIChatWidget", "AISettingsWidget", "AIImageWidget", "TypingGameWidget"]
