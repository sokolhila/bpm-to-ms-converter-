"""
Build script to create executable from the BPM converter application
"""
import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        return False
    return True

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building executable...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Create a single executable file
        "--windowed",  # Hide console window (GUI app)
        "--name=BPM-Converter",  # Name of the executable
        "--icon=NONE",  # No icon for now
        "bpm_converter.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("Executable built successfully!")
        print("You can find the executable in the 'dist' folder.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error building executable: {e}")
        return False

def main():
    """Main build process"""
    print("BPM Converter - Build Script")
    print("=" * 30)
    
    # Check if we're in the right directory
    if not os.path.exists("bpm_converter.py"):
        print("Error: bpm_converter.py not found in current directory")
        print("Please run this script from the project directory")
        return
    
    # Install requirements
    if not install_requirements():
        print("Failed to install requirements. Exiting.")
        return
    
    # Build executable
    if build_executable():
        print("\nBuild completed successfully!")
        print("The executable 'BPM-Converter.exe' is located in the 'dist' folder.")
    else:
        print("\nBuild failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
