# -*- coding: utf-8 -*-
"""Network helpers: timeout + retry + simple exponential backoff.
Designed to be dependency-light and safe for GUI usage.
"""
from __future__ import annotations
import time
import math
from typing import Callable, Dict, Optional, Any
import requests

DEFAULT_TIMEOUT = 10  # seconds
DEFAULT_RETRIES = 3
DEFAULT_BACKOFF_BASE = 0.5  # initial backoff delay
MAX_BACKOFF = 8.0  # cap a single sleep

RETRY_STATUS = {429, 500, 502, 503, 504}

class NetworkError(Exception):
    """Raised when all retry attempts fail or unrecoverable error occurs."""
    pass

def _should_retry(status_code: int) -> bool:
    return status_code in RETRY_STATUS

def fetch_with_retry(
    method: str,
    url: str,
    *,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    data: Optional[Any] = None,
    json: Optional[Any] = None,
    timeout: float = DEFAULT_TIMEOUT,
    retries: int = DEFAULT_RETRIES,
    backoff_base: float = DEFAULT_BACKOFF_BASE,
    backoff_factor: float = 2.0,
    status_retry: Callable[[int], bool] = _should_retry,
) -> requests.Response:
    """HTTP request with retry + exponential backoff.

    Retries on:
      - requests.exceptions.Timeout / ConnectionError
      - HTTP status codes in RETRY_STATUS (or custom via status_retry)

    Backoff progression: base * factor^(attempt-1), capped by MAX_BACKOFF.

    Raises NetworkError if all attempts fail.
    """
    attempt = 0
    last_exc: Optional[Exception] = None
    while attempt <= retries:
        try:
            resp = requests.request(
                method.upper(), url,
                headers=headers, params=params, data=data, json=json,
                timeout=timeout
            )
            if status_retry(resp.status_code):
                attempt += 1
                if attempt > retries:
                    raise NetworkError(f"Retry limit reached (HTTP {resp.status_code})")
                delay = min(backoff_base * (backoff_factor ** (attempt - 1)), MAX_BACKOFF)
                time.sleep(delay)
                continue
            return resp
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            attempt += 1
            last_exc = e
            if attempt > retries:
                raise NetworkError(f"Retry limit reached (network error): {e}") from e
            delay = min(backoff_base * (backoff_factor ** (attempt - 1)), MAX_BACKOFF)
            time.sleep(delay)
        except requests.exceptions.RequestException as e:
            # Non-retryable general request errors
            raise NetworkError(f"Unrecoverable request error: {e}") from e
    # Should not reach here normally
    raise NetworkError(f"Failed after retries; last exception: {last_exc}")

__all__ = ["fetch_with_retry", "NetworkError"]
