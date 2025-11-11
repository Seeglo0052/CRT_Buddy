"""
Improved Build Script for CRT Buddy
Handles all dependencies correctly
"""
import subprocess
import sys
import os

def check_dependencies():
    """Check if all required packages are installed"""
    print("Checking dependencies...")
    required = ['PyQt6', 'PIL', 'numpy', 'cv2']
    missing = []
    
    for package in required:
        try:
            if package == 'cv2':
                __import__('cv2')
            else:
                __import__(package)
            print(f"  [OK] {package}")
        except ImportError:
            print(f"  [MISSING] {package}")
            missing.append(package)
    
    if missing:
        print(f"\nMissing packages: {', '.join(missing)}")
        print("Please install: pip install -r requirements.txt")
        return False
    
    return True

def build_exe():
    """Build the executable with proper configuration"""
    print("\n" + "="*60)
    print("  CRT BUDDY - IMPROVED BUILD SCRIPT")
    print("="*60)
    
    if not check_dependencies():
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # PyInstaller command with all necessary options
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=CRT_Buddy",
        "--onefile",
        "--windowed",
        "--noconsole",
        "--clean",
        "--noconfirm",
        # Hidden imports for PyQt6
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",  
        "--hidden-import=PyQt6.QtWidgets",
        # Hidden imports for PIL
        "--hidden-import=PIL",
        "--hidden-import=PIL.Image",
        "--hidden-import=PIL.ImageDraw",
        "--hidden-import=PIL.ImageFont",
        "--hidden-import=PIL.ImageFilter",
        "--hidden-import=PIL.ImageEnhance",
        # Hidden imports for numpy
        "--hidden-import=numpy",
        # Collect all submodules
        "--collect-all=PyQt6",
        "--collect-all=PIL",
        # Main file
        "main.py"
    ]
    
    print("\nBuilding executable...")
    print("This may take a few minutes...\n")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        
        print("\n" + "="*60)
        print("  BUILD SUCCESSFUL!")
        print("="*60)
        print("\nExecutable location: dist\\CRT_Buddy.exe")
        print("\nYou can now:")
        print("  1. Test the executable")
        print("  2. Share dist\\CRT_Buddy.exe with others")
        print("  3. No Python installation needed to run!\n")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print("\n" + "="*60)
        print("  BUILD FAILED")
        print("="*60)
        print(f"\nError: {e}")
        print("\nPlease check the error messages above.")
        return False

def main():
    if not os.path.exists("main.py"):
        print("Error: main.py not found!")
        print("Please run this script from the CRT_Buddy directory.")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    success = build_exe()
    
    if success:
        print("\nWould you like to test the executable now? (y/n): ", end='')
        response = input().lower()
        if response in ['y', 'yes']:
            print("\nLaunching CRT_Buddy.exe...")
            try:
                subprocess.Popen(["dist\\CRT_Buddy.exe"])
            except Exception as e:
                print(f"Error launching: {e}")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
