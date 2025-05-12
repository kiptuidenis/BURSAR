import os
import shutil
from pathlib import Path

def collect_static():
    print("Starting static files collection...")
    
    # Define directories
    base_dir = Path(__file__).resolve().parent
    static_dir = base_dir / "app" / "static"
    staticfiles_dir = base_dir / "staticfiles"
    
    # Create staticfiles directory if it doesn't exist
    if not os.path.exists(staticfiles_dir):
        os.makedirs(staticfiles_dir, exist_ok=True)
        print(f"Created staticfiles directory at {staticfiles_dir}")
    
    # Check if source static directory exists
    if not os.path.exists(static_dir):
        print(f"Warning: Static directory {static_dir} does not exist.")
        return
    
    # Copy static files
    for item in os.listdir(static_dir):
        s = os.path.join(static_dir, item)
        d = os.path.join(staticfiles_dir, item)
        
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
            print(f"Copied directory: {item}")
        else:
            shutil.copy2(s, d)
            print(f"Copied file: {item}")
    
    # Create a simple index.html in staticfiles for verification
    with open(os.path.join(staticfiles_dir, 'index.html'), 'w') as f:
        f.write('<html><body><h1>Static files collected successfully</h1></body></html>')
    
    print("Static files collection complete!")

if __name__ == "__main__":
    collect_static()