import os
import subprocess
import shutil
import sys
import re
import ast
import configparser
import subprocess

def getInstallParameters():
    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Read the install.ini file
    config.read('./install.ini')

    # Get the values from the .ini file
    name = config.get('General', 'Name')
    script_name = config.get('General', 'ScriptName')
    alias = config.get('General', 'Alias')
    new_version = config.get('General', 'Version')
    install_dir = config.get('Directory', 'InstallDir')
    libraries = config.get('Libraries', 'Libraries')

    Installer_Path = os.path.abspath(script_name)
    Install_Path_Windows = os.path.expanduser('~/' + install_dir)
    Install_Path_Linux = os.path.expanduser('~/.local/bin/' + install_dir)

    return Installer_Path, Install_Path_Windows, Install_Path_Linux, name, script_name, alias, new_version, install_dir, libraries

Installer_Path, Install_Path_Windows, Install_Path_Linux, name, script_name, alias, new_version, install_dir, libraries = getInstallParameters()

print(f"DEBUG: Installer Path: {Installer_Path}")
print(f"DEBUG: Install Path (Windows): {Install_Path_Windows}")
print(f"DEBUG: Install Path (Linux): {Install_Path_Linux}")
print(f"DEBUG: Name: {name}")
print(f"DEBUG: Script Name: {script_name}")
print(f"DEBUG: Alias: {alias}")
print(f"DEBUG: Version: {version}")
print(f"DEBUG: Install Directory: {install_dir}")
print(f"DEBUG: Libraries: {libraries}")

def getVersion(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    try:
        current_version = config.get('General', 'Version')
    except:
        current_version = None
    return current_version

# Function to check the OS
def osCheck():
    if sys.platform == 'win32':
        return 'Windows'
        print("DEBUG: Windows OS detected.")
        return 'python'
    elif sys.platform == 'linux':
        return 'Linux'
        print("DEBUG: Linux OS detected.")
        return 'python3'
    else:
        return None
        print("DEBUG: Unsupported OS detected.")

# Function to install the required libraries
def libInstall():
    # Determine the pip command
    pip_command = 'pip3' if python_version == 'python3' else 'pip'

    for library in libraries:
        try:
            result = subprocess.run([sys.executable, '-m', pip_command, 'install', '--upgrade', library], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            if 'Requirement already satisfied' in result.stdout:
                print(f"{library} already exists!")
            else:
                print(f"{library} has been installed successfully!")
        except subprocess.CalledProcessError:
            print(f"Failed to install {library}!")


def checkVersion(Install_Path):
    if os.path.exists(Install_Path):
        current_version = getVersion(Install_Path + '/config.ini')

        # Compare the version numbers
        if current_version == None or new_version == None or new_version > current_version:
            # Newer version
            return 1
                
        elif new_version < current_version:
            # Older version
            return 2
        else:
            # Same version
            return 3
    else:
        # No version
        return 0

def switchInstall(VersionStatus, OSVersion):
    InstallVersion = "install" + OSVersion + "()"
    if VersionStatus == 0:
        check = input("Do you want to install SysInfo? (y/n): ")
        if check.lower() == 'y':
            exec(InstallVersion)
        else:
            quitMessage()
    elif VersionStatus == 1:
        print("You have a newer version of SysInfo than the one you're trying to install.")
        check = input("Do you want to downgrade SysInfo? (y/n): ")
        if check.lower() == 'y':
            exec(InstallVersion)
        else:
            quitMessage()
    elif VersionStatus == 2:
        print("A newer version of SysInfo is available.")
        check = input("Do you want to update SysInfo? (y/n): ")
        if check.lower() == 'y':
            exec(InstallVersion)
        else:
            quitMessage()
    elif VersionStatus == 3:
        print("You already have the latest version of SysInfo.")
        check = input("Do you want to reinstall SysInfo? (y/n): ")
        if check.lower() == 'y':
            exec(InstallVersion)
        else:
            quitMessage()


def successMessage():
    print("Sysinfo has been installed successfully!")
    print("Please remove the installer directory manually: " + os.path.dirname(Installer_Path))
    print("Please restart your terminal for the changes to take effect.")

def quitMessage():
    print("Quitting installation...")
    sys.exit(0)


def installWindows():
    print("Installing Sysinfo for Windows...")

    # Create the folder
    if not os.path.exists(Install_Path_Windows):
        os.makedirs(Install_Path_Windows, exist_ok=True)

    # Check if the PowerShell profile exists
    profile_check = subprocess.run(['powershell', '-Command', 'Test-Path $PROFILE'], capture_output=True, text=True)
    if 'True' in profile_check.stdout:
        # Check if the alias already exists in the profile
        alias_check = subprocess.run(['powershell', '-Command', f'if (Get-Command {alias} -ErrorAction SilentlyContinue) {{ "True" }} else {{ "False" }}'], capture_output=True, text=True)
        if 'True' in alias_check.stdout:
            print("Alias already exists.")
        else:
            command = f'Add-Content -Path $PROFILE -Value "`nfunction {alias} {{ python {Install_Path_Windows} }}"'
            subprocess.run(['powershell', '-Command', command], check=True)
            print("DEBUG: Alias added to existing profile.")
    else:
        # If the profile doesn't exist, ask the user if they want to create it
        user_input = input("A PowerShell profile does not exist. Do you want to create one? (y/n): ")
        if user_input.lower() == 'y':
            subprocess.run(['powershell', '-Command', 'New-Item -path $PROFILE -type file -force'], check=True)
            command = f'Add-Content -Path $PROFILE -Value "`nfunction {alias} {{ python {Install_Path_Windows} }}"'
            subprocess.run(['powershell', '-Command', command], check=True)
            print("DEBUG: Profile created and alias added.")
        else:
            print("Quitting installation...")
            sys.exit(0)

    # Install the required libraries
    libInstall()

    # Copy the SystemInfo.py script to the folder
    shutil.copy(Installer_Path, Install_Path_Windows)
    # Change the version number in the config file
    try:
        config = configparser.ConfigParser()
        config.read(Install_Path_Windows + '/config.ini')
        config['General'] = {'Version': new_version}
        with open(Install_Path_Windows + '/config.ini', 'w') as configfile:
            config.write(configfile)
    except:
        print("Failed to write to config.ini file.")

    successMessage()

def installLinux():

    print("Installing Sysinfo for Linux...")

    # Create the folder
    if not os.path.exists(Install_Path_Linux):
        os.makedirs(Install_Path_Linux, exist_ok=True)

    # Check if the bash profile exists
    profile_check = subprocess.run(['bash', '-c', 'test -f ~/.bashrc && echo "True" || echo "False"'], capture_output=True, text=True)
    if 'True' in profile_check.stdout:
        # Check if the alias already exists in the profile
        alias_check = subprocess.run(['bash', '-c', f'alias | grep -q "{alias}=" && echo "True" || echo "False"'], capture_output=True, text=True)
        if 'True' in alias_check.stdout:
            print("Alias already exists.")
        else:
            command = f'echo "alias {alias}=\'python3 {Install_Path_Linux}\'" >> ~/.bashrc'
            subprocess.run(['bash', '-c', command], check=True)
    else:
        user_input = input("A bash profile does not exist. Do you want to create one? (y/n): ")
        if user_input.lower() == 'y':
            subprocess.run(['touch', '~/.bashrc'], check=True)
            command = f'echo "alias {alias}=\'python3 {Install_Path_Linux}\'" >> ~/.bashrc'
            subprocess.run(['bash', '-c', command], check=True)
            print("Profile created and alias added.")
        else:
            quitMessage()

    libInstall()

    # Copy the SystemInfo.py script to the folder
    shutil.copy(Installer_Path, Install_Path_Linux)
    # Change the version number in the config file
    try:
        config = configparser.ConfigParser()
        config.read(Install_Path_Windows + '/config.ini')
        config['General'] = {'Version': new_version}
        with open(Install_Path_Windows + '/config.ini', 'w') as configfile:
            config.write(configfile)
    except:
        print("Failed to write to config.ini file.")

    successMessage()

def main():
    os_type, python_version = osCheck()
    if os_type == 'Windows':
        VersionStatus = checkVersion(Install_Path_Windows)
        switchInstall(VersionStatus, 'Windows')
    elif os_type == 'Linux':
        VersionStatus = checkVersion(Install_Path_Linux)
        switchInstall(VersionStatus, 'Linux')
    else:
        print("Unsupported OS.")
        quitMessage()


if __name__ == "__main__":
    main()