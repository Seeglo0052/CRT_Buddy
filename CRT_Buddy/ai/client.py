# -*- coding: utf-8 -*-
import os
import configparser
from typing import List, Optional

import requests


class AIConfig:
    """Configuration for AI API access."""

    # Doubao (Ark) setup guidance:
    # 1. Set environment variables:
    #    export ARK_API_KEY="sk-xxxxx"  (must match official key format)
    #    export ARK_BASE_URL="https://ark.cn-beijing.volces.com/api/v3"
    # 2. In UI select provider = doubao, choose correct model name.
    #    For chat try: doubao-lite or doubao-pro (verify from docs)
    #    For images use: doubaoseedream-3-0-t2i-250415 (example)
    # 3. Simple text chat uses /responses with 'input' field automatically.
    #    Rich (image+text) chat uses /chat/completions.
    # 4. If you see 401 AuthenticationError: check key prefix & region.
    # 5. If you see unknown field "messages": ensure ARK_BASE_URL points to /api/v3 (not /v1 or trailing /responses).

    def __init__(self,
                 api_key: Optional[str] = None,
                 base_url: Optional[str] = None,
                 chat_model: str = "gpt-4o-mini",
                 image_model: str = "gpt-image-1"):
        # Defaults
        self.api_key = None
        self.base_url = "https://api.openai.com/v1"
        self.chat_model = chat_model
        self.image_model = image_model
        self.chat_provider = "openai"  # informational (openai|deepseek|other compatible)
        # Image provider options (openai | stability)
        self.image_provider = "openai"
        self.stability_api_key = None
        self.stability_engine = "stable-diffusion-v1-6"
        self.stability_base_url = "https://api.stability.ai"
        self.image_api_key: Optional[str] = None
        self.image_base_url: Optional[str] = None

        # Load from config.ini if present
        self._load_from_config()

        # Environment overrides (Ark first if provided)
        env_api_key = os.getenv("ARK_API_KEY") or os.getenv("OPENAI_API_KEY") or os.getenv("AI_API_KEY")
        if env_api_key:
            self.api_key = env_api_key
        env_base = os.getenv("ARK_BASE_URL") or os.getenv("OPENAI_BASE_URL") or os.getenv("AI_BASE_URL")
        if env_base:
            self.base_url = env_base
        self.chat_model = os.getenv("AI_CHAT_MODEL", self.chat_model)
        self.image_model = os.getenv("AI_IMAGE_MODEL", self.image_model)
        self.chat_provider = os.getenv("AI_CHAT_PROVIDER", self.chat_provider)
        self.image_provider = os.getenv("AI_IMAGE_PROVIDER", self.image_provider)
        self.stability_api_key = os.getenv("STABILITY_API_KEY", self.stability_api_key)
        self.stability_engine = os.getenv("STABILITY_ENGINE", self.stability_engine)
        self.stability_base_url = os.getenv("STABILITY_BASE_URL", self.stability_base_url)
        self.image_api_key = os.getenv("IMAGE_API_KEY", self.image_api_key)
        self.image_base_url = os.getenv("IMAGE_BASE_URL", self.image_base_url)

        # Explicit arg overrides
        if api_key:
            self.api_key = api_key
        if base_url:
            self.base_url = base_url

    def _load_from_config(self):
        cfg = configparser.ConfigParser()
        cfg_path_candidates = [
            os.path.join(os.path.dirname(__file__), "..", "config.ini"),
            os.path.join(os.path.dirname(__file__), "..", "..", "config.ini"),
            os.path.join(os.getcwd(), "CRT_Buddy", "config.ini"),
            os.path.join(os.getcwd(), "config.ini"),
        ]
        for p in cfg_path_candidates:
            p = os.path.abspath(p)
            if os.path.exists(p):
                try:
                    cfg.read(p, encoding="utf-8")
                    if cfg.has_section("AI"):
                        self.api_key = cfg.get("AI", "api_key", fallback=self.api_key)
                        self.base_url = cfg.get("AI", "base_url", fallback=self.base_url) or self.base_url
                        self.chat_model = cfg.get("AI", "chat_model", fallback=self.chat_model)
                        self.image_model = cfg.get("AI", "image_model", fallback=self.image_model)
                        self.image_provider = cfg.get("AI", "image_provider", fallback=self.image_provider)
                        self.chat_provider = cfg.get("AI", "chat_provider", fallback=self.chat_provider)
                        self.stability_api_key = cfg.get("AI", "stability_api_key", fallback=self.stability_api_key)
                        self.stability_engine = cfg.get("AI", "stability_engine", fallback=self.stability_engine)
                        self.stability_base_url = cfg.get("AI", "stability_base_url", fallback=self.stability_base_url)
                        self.image_api_key = cfg.get("AI", "image_api_key", fallback=self.image_api_key)
                        self.image_base_url = cfg.get("AI", "image_base_url", fallback=self.image_base_url)
                    break
                except Exception:
                    # Ignore parse errors and continue
                    pass


class AIClient:
    """Minimal OpenAI-compatible client for chat and image generation.

    Supports OpenAI or any OpenAI-compatible server by customizing base_url.
    """

    def __init__(self, config: Optional[AIConfig] = None):
        self.config = config or AIConfig()
        if not self.config.api_key:
            # Allow running without key; callers should handle None outputs gracefully
            print("[AI] Warning: No API key set. Set OPENAI_API_KEY or AI_API_KEY.")

    def _log(self, message: str):
        try:
            log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output'))
            os.makedirs(log_dir, exist_ok=True)
            with open(os.path.join(log_dir, 'ai_log.txt'), 'a', encoding='utf-8') as f:
                from datetime import datetime
                f.write(f"[{datetime.now().isoformat()}] {message}\n")
        except Exception:
            pass

    # --------- Chat Completion ---------
    def chat(self, messages: List[dict], model: Optional[str] = None, temperature: float = 0.7, max_tokens: int = 512, reasoning_effort: Optional[str] = None) -> Optional[str]:
        if not self.config.api_key:
            return None
        provider = (self.config.chat_provider or '').lower()
        use_model = model or self.config.chat_model
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }

        # Doubao (Ark) uses OpenAI-compatible /chat/completions endpoint
        if provider == 'doubao':
            base = self.config.base_url.rstrip('/')
            url = f"{base}/chat/completions"
            self._log("doubao using /chat/completions")
            # Doubao uses standard OpenAI format but prefers max_output_tokens
            payload = {
                "model": use_model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }
            last_err = None
            for attempt in range(2):
                try:
                    resp = requests.post(url, headers=headers, json=payload, timeout=60)
                    if resp.status_code >= 400:
                        snippet = resp.text[:200].replace('\n', ' ').strip()
                        raise RuntimeError(f"HTTP {resp.status_code}: {snippet}")
                    data = resp.json()
                    # Standard OpenAI format
                    text = data.get("choices", [{}])[0].get("message", {}).get("content")
                    if text:
                        self._log("doubao chat success")
                        return text
                    last_err = 'Empty response'
                except Exception as e:
                    last_err = str(e)
                    body_part = ''
                    try:
                        body_part = resp.text[:160].replace('\n',' ') if 'resp' in locals() else ''
                    except Exception:
                        pass
                    self._log(f"doubao chat attempt {attempt+1} failed: {last_err} body={body_part}")
                import time
                time.sleep(0.5 * (attempt + 1))
            self._log(f"doubao chat failed: {last_err}")
            return f"(doubao chat error: {last_err})"

        # Default OpenAI-compatible path
        url = f"{self.config.base_url.rstrip('/')}/chat/completions"
        payload = {
            "model": use_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        last_err = None
        for attempt in range(3):
            try:
                resp = requests.post(url, headers=headers, json=payload, timeout=60)
                status = resp.status_code
                if status >= 400:
                    snippet = resp.text[:160].replace('\n', ' ').strip()
                    raise RuntimeError(f"HTTP {status}: {snippet}")
                data = resp.json()
                content = data.get("choices", [{}])[0].get("message", {}).get("content")
                if content:
                    return content
                last_err = "Empty response"
            except Exception as e:
                last_err = str(e)
                self._log(f"chat attempt {attempt+1} failed: {last_err}")
            import time
            time.sleep(0.6 * (attempt + 1))
        self._log(f"chat failed after retries: {last_err}")
        return f"(chat error: {last_err}. Possible network/proxy issue. Set HTTPS_PROXY if needed.)"

    # --------- Image Generation ---------
    def generate_image(self, prompt: str, model: Optional[str] = None, size: str = "1024x1024") -> Optional[bytes]:
        key = self.config.image_api_key or self.config.api_key
        base = self.config.image_base_url or self.config.base_url
        provider = (self.config.image_provider or '').lower()

        # Stability branch
        if provider == "stability":
            api_key = self.config.stability_api_key or self.config.api_key
            if not api_key:
                return None
            try:
                w, h = [int(x) for x in size.lower().split("x")[:2]]
            except Exception:
                w, h = 1024, 1024
            url = f"{self.config.stability_base_url}/v1/generation/{self.config.stability_engine}/text-to-image"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            payload = {
                "text_prompts": [{"text": prompt}],
                "cfg_scale": 7,
                "height": h,
                "width": w,
                "samples": 1,
            }
            try:
                resp = requests.post(url, headers=headers, json=payload, timeout=120)
                resp.raise_for_status()
                data = resp.json()
                arts = data.get("artifacts") or []
                if not arts:
                    return None
                b64 = arts[0].get("base64")
                if not b64:
                    return None
                import base64
                return base64.b64decode(b64)
            except Exception as e:
                print(f"[AI] Stability image error: {e}")
                return None

        if not key:
            return None

        # Doubao image endpoint: Uses OpenAI-compatible path /images/generations (not /generate)
        if provider == 'doubao':
            url = f"{base.rstrip('/')}/images/generations"
            headers = {
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": model or self.config.image_model,
                "prompt": prompt,
                "size": size,
                # Doubao supports both b64_json and url
                "response_format": "b64_json",
            }
            try:
                resp = requests.post(url, headers=headers, json=payload, timeout=180)
                if resp.status_code >= 400:
                    snippet = resp.text[:200].replace('\n', ' ').strip()
                    raise RuntimeError(f"HTTP {resp.status_code}: {snippet}")
                data = resp.json()
                b64 = None
                img_url = None
                if isinstance(data, dict):
                    # Native style
                    if 'data' in data:
                        first = (data.get('data') or [{}])[0]
                        b64 = first.get('b64_json')
                        img_url = first.get('url')
                    if not b64:
                        out = data.get('output') or {}
                        if isinstance(out, dict):
                            # Common doubao fields
                            b64 = out.get('image_base64') or out.get('b64_json')
                            img_url = img_url or out.get('url')
                            if not b64:
                                images = out.get('images') or []
                                if images and isinstance(images, list):
                                    # images could be array of {base64: ...} or {b64_json: ...}
                                    first = images[0] or {}
                                    b64 = first.get('base64') or first.get('b64_json')
                                    img_url = img_url or first.get('url')
                    if not b64:
                        # Some proxies wrap under result
                        result = data.get('result') or []
                        if isinstance(result, list) and result:
                            first = (result[0] or {})
                            b64 = first.get('image_base64') or first.get('b64_json')
                            img_url = img_url or first.get('url')
                if not b64 and img_url:
                    # Fetch the URL and return bytes
                    try:
                        r2 = requests.get(img_url, timeout=60)
                        r2.raise_for_status()
                        return r2.content
                    except Exception as e:
                        self._log(f"doubao image url fetch error: {e}")
                        return None
                if not b64:
                    self._log(f"doubao image missing b64; keys={list(data.keys()) if isinstance(data, dict) else 'non-dict'}")
                    return None
                import base64
                return base64.b64decode(b64)
            except Exception as e:
                body_part = ''
                try:
                    body_part = resp.text[:160].replace('\n',' ') if 'resp' in locals() else ''
                except Exception:
                    pass
                self._log(f"doubao image error: {e} body={body_part}")
                print(f"[AI] Doubao image error: {e}")
                return None

        # Default OpenAI-compatible image endpoint
        url = f"{base.rstrip('/')}/images/generations"
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model or self.config.image_model,
            "prompt": prompt,
            "size": size,
            "response_format": "b64_json",
        }
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=120)
            resp.raise_for_status()
            data = resp.json()
            b64 = data.get("data", [{}])[0].get("b64_json")
            if not b64:
                return None
            import base64
            return base64.b64decode(b64)
        except Exception as e:
            self._log(f"image error: {e}")
            print(f"[AI] Image error: {e}")
            return None
