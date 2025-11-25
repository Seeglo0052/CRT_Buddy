# -*- coding: utf-8 -*-
"""Minimal Doubao API diagnostic.
Run: python tests/test_doubao_api.py --key 8bcf64fb-36d0-43c8-8422-7919262d0c60 [--base https://ark.cn-beijing.volces.com/api/v3]
Reports:
  - Chat endpoint /responses
  - Image endpoint /images/generate
Classifies failures (auth / model / other) and prints response snippets.
"""
import json, argparse, time
import requests

DEFAULT_BASE = "https://ark.cn-beijing.volces.com/api/v3"
CHAT_MODEL = "doubao-seed-1-6-251015"
IMAGE_MODEL = "doubaoseedream-3-0-t2i-250415"


def snippet(text: str, n: int = 180) -> str:
    return (text or "").replace("\n", " ")[:n]


def test_chat(key: str, base: str) -> None:
    url = base.rstrip("/") + "/responses"
    payload = {
        "model": CHAT_MODEL,
        "messages": [{"role": "user", "content": "PING"}],
        "max_output_tokens": 32,
    }
    t0 = time.time()
    try:
        r = requests.post(url, headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}, json=payload, timeout=40)
        dt = time.time() - t0
        body = snippet(r.text)
        if r.status_code == 200:
            try:
                data = r.json()
                out = data.get("output", {})
                text = out.get("text") or data.get("choices", [{}])[0].get("message", {}).get("content")
                print(f"[CHAT] 200 OK ({dt:.1f}s) -> {snippet(text, 60)}")
            except Exception:
                print(f"[CHAT] 200 OK parse error body={body}")
        elif r.status_code in (401, 403):
            print(f"[CHAT] AUTH FAIL {r.status_code} body={body}")
        elif r.status_code == 400:
            print(f"[CHAT] PARAM ERROR 400 body={body}")
        else:
            print(f"[CHAT] HTTP {r.status_code} body={body}")
    except Exception as e:
        print(f"[CHAT] NETWORK/EXCEPTION {e}")


def test_image(key: str, base: str) -> None:
    url = base.rstrip("/") + "/images/generate"
    payload = {
        "model": IMAGE_MODEL,
        "prompt": "ping",
        "size": "512x512",
    }
    t0 = time.time()
    try:
        r = requests.post(url, headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}, json=payload, timeout=120)
        dt = time.time() - t0
        body = snippet(r.text)
        if r.status_code == 200:
            try:
                data = r.json()
                b64 = None
                if 'data' in data:
                    b64 = (data.get('data') or [{}])[0].get('b64_json')
                if not b64:
                    out = data.get('output') or {}
                    if isinstance(out, dict):
                        b64 = out.get('image_base64') or out.get('b64_json')
                if b64:
                    print(f"[IMAGE] 200 OK ({dt:.1f}s) bytes~{len(b64)}")
                else:
                    print(f"[IMAGE] 200 OK but missing b64 body={body}")
            except Exception:
                print(f"[IMAGE] 200 OK parse error body={body}")
        elif r.status_code in (401, 403):
            print(f"[IMAGE] AUTH FAIL {r.status_code} body={body}")
        elif r.status_code == 400:
            print(f"[IMAGE] PARAM ERROR 400 body={body}")
        else:
            print(f"[IMAGE] HTTP {r.status_code} body={body}")
    except Exception as e:
        print(f"[IMAGE] NETWORK/EXCEPTION {e}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--key', required=True, help='Doubao API key')
    ap.add_argument('--base', default=DEFAULT_BASE, help='Base URL')
    args = ap.parse_args()
    print(f"Testing Doubao base={args.base}")
    test_chat(args.key, args.base)
    test_image(args.key, args.base)

if __name__ == '__main__':
    main()
