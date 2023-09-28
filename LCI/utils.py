import shutil

def say_hi(name):
  print(f'Hi, {name}')

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

def copy_file(filename, src_path, dest_path):
    """
    Copy a file from a source path to a destination path.

    Args:
        filename (str): The name of the file to be copied.
        src_path (str): The source directory containing the file.
        dest_path (str): The destination directory where the file will be copied.

    Raises:
        FileNotFoundError: If the source file does not exist.
        PermissionError: If permission is denied to copy the file.
        Exception: For any other unexpected errors during the copy process.

    Returns:
        None: This function does not return a value.

    Example:
        copy_file("example.txt", "/source_directory/", "/destination_directory/")
    """
    try:
        # Copy the file from src_path to dest_path
        shutil.copy(src_path+filename, dest_path+filename)
        #print(f"File copied from '{src_path}' to '{dest_path}' successfully.")
    except FileNotFoundError:
        print("The source file does not exist.")
    except PermissionError:
        print("Permission denied. You may not have the required permissions. Try use the function 'drive_colab' after.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

#def move_files(file_name,src_folder,edst_folder):

