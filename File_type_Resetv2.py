import os
import winreg
from pathlib import Path

# Replace with your desired file extension and application path
extension = ".sif"
application_path = r"%LOCALAPPDATA%\projectspec\ProjectSpec5.exe"

# Expand the application path
expanded_application_path = os.path.expandvars(application_path)

# Create the file type registry key if it doesn't exist
file_type_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\{}".format(extension))

# Set the file type association
winreg.SetValueEx(file_type_key, "", 0, winreg.REG_SZ, expanded_application_path)

# Remove the UserChoice entry if it exists, to force a new hash to be generated
file_exts_key_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\{}".format(extension)
user_choice_key_path = r"{}\UserChoice".format(file_exts_key_path)

try:
    user_choice_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, user_choice_key_path, 0, winreg.KEY_READ)
    winreg.DeleteKey(winreg.HKEY_CURRENT_USER, user_choice_key_path)
except FileNotFoundError:
    # UserChoice subkey does not exist, do nothing
    pass

# Set the ProgId to the desired application
file_exts_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, file_exts_key_path, 0, winreg.KEY_WRITE)
winreg.SetValueEx(file_exts_key, "ProgId", 0, winreg.REG_SZ, expanded_application_path)

# Close registry keys
winreg.CloseKey(file_type_key)
winreg.CloseKey(file_exts_key)
