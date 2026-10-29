"""
Installation Verification Script
Run this to verify all dependencies are installed correctly
"""
import sys

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"[OK] Python version: {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("  [WARNING] Python 3.8+ recommended")
        return False
    return True

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = {
        'flask': 'Flask',
        'pandas': 'pandas',
        'openpyxl': 'openpyxl',
        'numpy': 'numpy',
        'werkzeug': 'Werkzeug'
    }
    
    all_installed = True
    
    for package, display_name in required_packages.items():
        try:
            __import__(package)
            print(f"[OK] {display_name} installed")
        except ImportError:
            print(f"[X] {display_name} NOT installed")
            all_installed = False
    
    return all_installed

def check_project_structure():
    """Check if project structure is correct"""
    import os
    
    required_dirs = [
        'app',
        'rules',
        'static/css',
        'static/js',
        'templates',
        'uploads',
        'outputs'
    ]
    
    required_files = [
        'config.py',
        'run.py',
        'requirements.txt',
        'app/__init__.py',
        'app/routes.py',
        'app/validation_engine.py',
        'app/rules_loader.py',
        'app/file_handler.py',
        'app/utils.py',
        'templates/index.html',
        'static/css/style.css',
        'static/js/main.js'
    ]
    
    all_present = True
    
    print("\nChecking project structure...")
    
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"[OK] Directory: {directory}")
        else:
            print(f"[X] Missing directory: {directory}")
            all_present = False
    
    for file in required_files:
        if os.path.exists(file):
            print(f"[OK] File: {file}")
        else:
            print(f"[X] Missing file: {file}")
            all_present = False
    
    return all_present

def check_rules_files():
    """Check if rules files exist"""
    import os
    
    rules_dir = 'rules'
    if not os.path.exists(rules_dir):
        print(f"\n[X] Rules directory not found")
        return False
    
    rules_files = [f for f in os.listdir(rules_dir) if f.endswith('.json')]
    
    if rules_files:
        print(f"\n[OK] Found {len(rules_files)} rules file(s):")
        for rule_file in rules_files:
            print(f"  - {rule_file}")
        return True
    else:
        print(f"\n[X] No rules files found in {rules_dir}")
        return False

def main():
    """Main verification function"""
    print("=" * 60)
    print("Timesheet Validator - Installation Verification")
    print("=" * 60)
    print()
    
    # Check Python version
    print("Checking Python version...")
    python_ok = check_python_version()
    print()
    
    # Check dependencies
    print("Checking dependencies...")
    deps_ok = check_dependencies()
    print()
    
    # Check project structure
    structure_ok = check_project_structure()
    print()
    
    # Check rules files
    rules_ok = check_rules_files()
    print()
    
    # Final verdict
    print("=" * 60)
    if python_ok and deps_ok and structure_ok and rules_ok:
        print("SUCCESS: All checks passed! Installation is complete.")
        print()
        print("You can now run the application:")
        print("  python run.py")
        print()
        print("Then open your browser to: http://localhost:5000")
    else:
        print("WARNING: Some checks failed. Please review the errors above.")
        print()
        if not deps_ok:
            print("To install dependencies, run:")
            print("  pip install -r requirements.txt")
    print("=" * 60)

if __name__ == '__main__':
    main()

# Made with Bob
