"""
Quick Start - CRT Buddy
Simple launcher to test if everything works
"""
import sys

print("=" * 60)
print("  CRT BUDDY - Quick Start")
print("=" * 60)
print("\nChecking dependencies...\n")

# Check required modules
required_modules = {
    'PyQt6': 'PyQt6',
    'PIL (Pillow)': 'PIL',
    'NumPy': 'numpy',
    'OpenCV': 'cv2'
}

missing = []
for name, module in required_modules.items():
    try:
        __import__(module)
        print(f"[OK] {name}")
    except ImportError:
        print(f"[MISSING] {name}")
        missing.append(name)

if missing:
    print(f"\n[ERROR] Missing dependencies: {', '.join(missing)}")
    print("\nPlease install:")
    print("  pip install -r requirements.txt")
    input("\nPress Enter to exit...")
    sys.exit(1)

print("\n[SUCCESS] All dependencies found!")
print("\nStarting CRT Buddy...\n")

# Import and run
try:
    from CRT_Buddy import main
    main()
except Exception as e:
    print(f"\n[ERROR] Failed to start: {e}")
    import traceback
    traceback.print_exc()
    input("\nPress Enter to exit...")
    sys.exit(1)
