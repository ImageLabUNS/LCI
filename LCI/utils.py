import shutil
import os
from PIL import Image
from io import BytesIO
import base64
import zipfile



def drive_colab():
  """
    Mount Google Drive in a Google Colab environment and set up authentication.

    This function mounts the Google Drive file system in a Google Colab environment
    and sets up authentication to access Google Drive using PyDrive.

    Args:
        None

    Returns:
        None

    Example:
        drive_colab()
    """
  from pydrive.auth import GoogleAuth
  from pydrive.drive import GoogleDrive
  from google.colab import auth
  from oauth2client.client import GoogleCredentials
  from google.colab import drive
  drive.mount('/content/drive')

def copy_file(file_path, dest_path):
    """
    Copy a file from a source path to a destination path.

    Args:
        file_path (str): The path of the file to be copied.
        dest_path (str): The destination directory where the file will be copied.

    Raises:
        FileNotFoundError: If the source file does not exist.
        PermissionError: If permission is denied to copy the file.
        Exception: For any other unexpected errors during the copy process.

    Returns:
        None: This function does not return a value.

    Example:
        copy_file("/source_directory/example.txt", "/destination_directory/")
    """
    try:
        strt = file_path[::-1].find('/')
        filename = file_path[-strt:]
        # Copy the file from src_path to dest_path
        shutil.copy(file_path, dest_path+filename)
        #print(f"File copied from '{src_path}' to '{dest_path}' successfully.")
    except FileNotFoundError:
        print("The source file does not exist.")
    except PermissionError:
        print("Permission denied. You may not have the required permissions. Try use the function 'drive_colab' after.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def move_file(file_path, dst_path):
    """
    Move a file from the source path to the destination path.

    This function copies a file from the source path to the destination path using the
    'copy_file' function and then removes the file from the source path.

    Args:
        file_path (str): The path to the file to be moved.
        dst_path (str): The destination directory where the file will be moved.

    Returns:
        None

    Example:
        move_file("/source_directory/example.txt", "/destination_directory/")
    """
    copy_file(file_path,dst_path)
    os.remove(file_path)



def install_package(package_name):
    """
    Install a Python package if it is not already installed.

    This function attempts to import the specified package. If the package is not
    installed, it uses pip to install it. If the installation fails, it prompts
    the user to install the package manually.

    Args:
        package_name (str): The name of the Python package to be installed.

    Returns:
        None

    Example:
        install_package("numpy")
    """
    import subprocess
    import sys
    try:
        # Try to import the package
        __import__(package_name)
    except ImportError:
        # If the package is not installed, install it using pip
        print(f"{package_name} is not installed. Installing now...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"{package_name} has been successfully installed.")
        except subprocess.CalledProcessError:
            print(f"Failed to install {package_name}. Please install it manually.")

def decode_image(base64_image_data):
    """
    Decode a base64-encoded image data and return a PIL Image object.

    Args:
        base64_image_data (str): Base64-encoded image data.

    Returns:
        PIL.Image.Image: A PIL Image object.

    Example:
        image_data = "base64_encoded_image_data_here"\n
        image = decode_image(image_data)
    """
    if base64_image_data:
        image_bytes = base64.b64decode(base64_image_data)
        image = Image.open(BytesIO(image_bytes))
        return image

def encode_image():
    """
    Encode an image as base64.

    Args:
        image_path (str): The path to the image file to be encoded.

    Returns:
        str: Base64-encoded image data.

    Example:
        image_path = "path/to/your_image.jpg"\n
        base64_image_data = encode_image(image_path)
    """
    # Open the image using PIL
    image = Image.open('your_image.jpg')  # Replace 'your_image.jpg' with the path to your image file

    # Convert the image to a bytes-like object
    image_bytes = image.tobytes()

    # Encode the image bytes as base64
    base64_image_data = base64.b64encode(image_bytes).decode('utf-8')

    # Print or use the base64_image_data as needed
    return(base64_image_data)

def get_metadata(img_path):
    """
    Extract the metadata of an image at the specified path.

    Args:
        image_path (str): The path to the image file.

    Returns:
        dict: A dictionary containing the image metadata.

    Example:
        metadata = get_metadata("path/to/image.jpg")
    """
    install_package('exifread')
    import exifread
    metadata = {}
    with open(img_path, 'rb') as f:
        # Return Exif tags
        tags = exifread.process_file(f)
        for tag in tags.keys():
            metadata[tag] = str(tags[tag])
            #print(tag, tags[tag])
    return metadata

def unzip_files(origin_path,dest_path):
  """
    Unzip files from a specified origin path to a destination directory.

    Args:
        origin_path (str): Path to the zip file to be extracted.
        dest_path (str): Path to the directory where contents will be extracted.

    Returns:
        None: Extracts files from the zip archive to the specified directory.

    Example:
        unzip_files("path/to/zip_file.zip", "path/to/destination")
    """
  
  
  # Create directory if it doesn't exist

  os.makedirs(extract_to_dir, exist_ok=True)
 


  # Open the zip file
  with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
      # Extract all contents to the specified directory
      zip_ref.extractall(extract_to_dir)

  # List the extracted files
  extracted_files = os.listdir(extract_to_dir)
  print("Files extracted successfully:")
