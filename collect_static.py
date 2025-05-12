import os
import shutil

def collect_static():
    print("Starting static files collection...")
    
    # Define directories
    base_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(base_dir, "app", "static")
    staticfiles_dir = os.path.join(base_dir, "staticfiles")
    
    # Create staticfiles directory if it doesn't exist
    if not os.path.exists(staticfiles_dir):
        os.makedirs(staticfiles_dir, exist_ok=True)
        print("Created staticfiles directory")
    
    # Check if source static directory exists
    if not os.path.exists(static_dir):
        print("Warning: Static directory does not exist.")
        # Create a default file to ensure the directory isn't empty
        with open(os.path.join(staticfiles_dir, "index.html"), 'w') as f:
            f.write("<html><body>Static files will be served here</body></html>")
        print("Created default index.html in staticfiles directory")
        return
    
    # Copy static files
    for item in os.listdir(static_dir):
        s = os.path.join(static_dir, item)
        d = os.path.join(staticfiles_dir, item)
        
        try:
            if os.path.isdir(s):
                if os.path.exists(d):
                    shutil.rmtree(d)
                shutil.copytree(s, d)
                print(f"Copied directory: {item}")
            else:
                shutil.copy2(s, d)
                print(f"Copied file: {item}")
        except Exception as e:
            print(f"Error copying {item}: {str(e)}")
    
    print("Static files collection completed successfully")

if __name__ == "__main__":
    collect_static()