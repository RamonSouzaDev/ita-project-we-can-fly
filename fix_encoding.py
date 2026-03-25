import os

def convert_to_utf8(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                try:
                    # Try reading as UTF-16LE first (common source of null bytes)
                    with open(path, 'rb') as f:
                        raw = f.read()
                    
                    if b'\x00' in raw:
                        print(f"Detected null bytes in {path}. Attempting UTF-16LE to UTF-8 conversion.")
                        content = raw.decode('utf-16le')
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"Converted {path} to UTF-8.")
                    else:
                        print(f"No null bytes detected in {path}.")
                except Exception as e:
                    print(f"Error processing {path}: {str(e)}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    convert_to_utf8(os.path.join(current_dir, 'src'))
    if os.path.exists(os.path.join(current_dir, 'tests')):
        convert_to_utf8(os.path.join(current_dir, 'tests'))
    convert_to_utf8(current_dir)
