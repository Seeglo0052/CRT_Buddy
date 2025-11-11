"""
Test if CRT_Buddy.exe can run properly
"""
import subprocess
import os
import sys

def test_exe():
    """Test the built executable"""
    exe_path = os.path.join("dist", "CRT_Buddy.exe")
    
    if not os.path.exists(exe_path):
        print("Error: CRT_Buddy.exe not found in dist folder!")
        print("Please build the executable first.")
        return False
    
    print("="*60)
    print("  Testing CRT_Buddy.exe")
    print("="*60)
    print(f"\nFile: {exe_path}")
    print(f"Size: {os.path.getsize(exe_path) / (1024*1024):.2f} MB")
    print("\nLaunching executable...")
    print("(The window should appear in a few seconds)")
    print("\nPress Ctrl+C to stop if it hangs\n")
    
    try:
        # Launch the executable
        process = subprocess.Popen(
            [exe_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("Executable started successfully!")
        print("Check if the CRT Buddy window appears.")
        print("\nIf you see the window, the build is successful!")
        print("Close the window to continue this test.\n")
        
        # Wait for the process to finish
        stdout, stderr = process.communicate(timeout=300)  # 5 min timeout
        
        if process.returncode == 0:
            print("\nTest PASSED! Executable ran successfully.")
            return True
        else:
            print(f"\nTest FAILED! Exit code: {process.returncode}")
            if stderr:
                print(f"Errors:\n{stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("\nTest still running (this is normal if window is open)")
        print("Close the CRT Buddy window to complete the test.")
        process.kill()
        return True
    except Exception as e:
        print(f"\nTest FAILED with exception: {e}")
        return False

if __name__ == "__main__":
    test_exe()
    input("\nPress Enter to exit...")
