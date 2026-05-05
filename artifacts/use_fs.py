import os

def create_directory(path: str) -> None:
    """
    Creates a directory at the specified path.

    :param path: The path where the directory should be created.
    """
    try:
        os.makedirs(path, exist_ok=True)
        print(f"Directory created or already exists at: {path}")
    except OSError as e:
        print(f"Error creating directory: {e}")

def write_to_disk(filename: str, content: str) -> None:
    """
    Writes content to a file at the specified filename.

    :param filename: The path where the file should be written.
    :param content: The content to be written to the file.
    """
    try:
        with open(filename, 'w') as file:
            file.write(content)
        print(f"Content written to: {filename}")
    except IOError as e:
        print(f"Error writing to file: {e}")

def save_hello_world():
    directory_path = "/path/to/your/directory"
    create_directory(directory_path)
    file_path = os.path.join(directory_path, "hello_world.txt")
    write_to_disk(file_path, "Hello, World!")

def save_custom_content(content: str):
    directory_path = "/path/to/your/directory"
    create_directory(directory_path)
    file_path = os.path.join(directory_path, "custom_content.txt")
    write_to_disk(file_path, content)

def main():
    directory_path = "/path/to/your/directory"
    create_directory(directory_path)
    data = "Sample data to write"
    write_to_disk(os.path.join(directory_path, "sample_file.txt"), data)

if __name__ == "__main__":
    main()