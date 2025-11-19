"""Thin entrypoint wrapper to avoid duplicating app logic.

Keeps backward compatibility for users who run `python main.py`.
Actual application code lives in `CRT_Buddy.py` (function `main`).
"""

from CRT_Buddy import main as run


if __name__ == "__main__":
    run()
