import os

def fix_file(path):
    print(f"Fixing {path}...")
    try:
        # Read as binary to handle any encoding
        with open(path, 'rb') as f:
            raw = f.read()
            
        # Remove BOM if present
        if raw.startswith(b'\xef\xbb\xbf'):
            raw = raw[3:]
        elif raw.startswith(b'\xff\xfe'):
            raw = raw[2:].decode('utf-16le').encode('utf-8')
        elif raw.startswith(b'\xfe\xff'):
            raw = raw[2:].decode('utf-16be').encode('utf-8')
            
        # Try decoding as utf-8, then fallback
        try:
            content = raw.decode('utf-8')
        except UnicodeDecodeError:
            content = raw.decode('ascii', errors='ignore')
            
        # Normalize line endings to \n
        content = content.replace('\r\n', '\n').replace('\r', '\n')
        
        # Write back as clean UTF-8
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
        print(f"Successfully fixed {path}")
            
    except Exception as e:
        print(f"Error fixing {path}: {str(e)}")

def traverse_and_fix(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py') or file.endswith('.md') or file.endswith('.txt'):
                fix_file(os.path.join(root, file))

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    traverse_and_fix(os.path.join(current_dir, 'src'))
    if os.path.exists(os.path.join(current_dir, 'tests')):
        traverse_and_fix(os.path.join(current_dir, 'tests'))
    # Also fix files in root
    for f in os.listdir(current_dir):
        if f.endswith('.py') or f.endswith('.md'):
            # fix_file requires file path
            path = os.path.join(current_dir, f)
            if os.path.isfile(path):
                fix_file(path)
