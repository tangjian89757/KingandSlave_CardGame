#!/usr/bin/env python3
"""
King & Slave Card Game Dependency Installer
Automatically detects and installs required dependencies
"""

import sys
import subprocess
import importlib.util

def check_package(package_name, import_name=None):
    """Check if package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        spec = importlib.util.find_spec(import_name)
        return spec is not None
    except ImportError:
        return False

def install_package(package_name):
    """Install package"""
    try:
        print(f"Installing {package_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"✅ {package_name} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {package_name} installation failed: {e}")
        return False

def main():
    """Main installation function"""
    print("🎮 King & Slave Card Game Dependency Installer")
    print("=" * 50)
    
    # Dependency package list
    packages = [
        ("pygame>=2.1.0", "pygame"),
        ("opencv-python>=4.5.0", "cv2"),
        ("numpy>=1.21.0", "numpy")
    ]
    
    missing_packages = []
    
    # Check installed packages
    print("🔍 Checking dependencies...")
    for package, import_name in packages:
        if check_package(package, import_name):
            print(f"✅ {import_name} is installed")
        else:
            print(f"❌ {import_name} is not installed")
            missing_packages.append(package)
    
    if not missing_packages:
        print("\n🎉 All dependencies are already installed!")
        return True
    
    # Install missing packages
    print(f"\n📦 Need to install {len(missing_packages)} packages...")
    success_count = 0
    
    for package in missing_packages:
        if install_package(package):
            success_count += 1
    
    print(f"\n📊 Installation result: {success_count}/{len(missing_packages)} successful")
    
    if success_count == len(missing_packages):
        print("🎉 All dependencies installed successfully! You can now run the game.")
        print("Run command: python3 'King&Slave Game.py'")
        return True
    else:
        print("⚠️  Some packages failed to install. Please install manually or check your network connection.")
        return False

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Installation cancelled by user")
    except Exception as e:
        print(f"\n❌ Error occurred during installation: {e}")
