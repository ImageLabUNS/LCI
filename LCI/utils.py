def say_hi(name):
  print(f'Hi, {name}')

def drive_colab():
  # This lines are for mount the drive and get the auth from google
  from pydrive.auth import GoogleAuth
  from pydrive.drive import GoogleDrive
  from google.colab import auth
  from oauth2client.client import GoogleCredentials
  from google.colab import drive
  drive.mount('/content/drive')
