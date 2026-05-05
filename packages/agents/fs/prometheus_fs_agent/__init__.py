import os

def write_to_disk(filename: str, content: str):
    """
    Physically commits a string of code to a file.
    Ensures the 'output' directory exists.
    """
    output_dir = "artifacts"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    path = os.path.join(output_dir, filename)
    
    with open(path, "w") as f:
        f.write(content)
    
    return f"[FS] Artifact successfully committed to: {path}"

if __name__ == "__main__":
    # Test run
    print(write_to_disk("test.py", "print('Hello Prometheus')"))
