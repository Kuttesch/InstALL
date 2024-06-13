# InstALL

InstALL is a Script written in Python that you can use to install a smaller project with all its dependencies.  
It is built so that you can easily provide an installer for your small (right now preferable python) project.

## Table of Contents

- [Usage](#usage)
- [Features](#features)
- [Bugs](#bugs)
- [Contributing](#contributing)
- [License](#license)

## Usage

To utilize InstALL for your project, follow the steps below:

1. **Project Setup**: Ensure you have a project to work with.

2. **Clone and Copy**: Clone this repository and copy the `install.py` and `install.ini` files into your project's root folder. It's crucial that these two files reside in the same directory as the script you wish to install.

3. **Configuration**: Edit the `install.ini` file according to your project's requirements. The `install.ini` file is a straightforward ini file with the following structure:

    ```ini
    [General]
    Name = "Script"
    ScriptName = "Script.py"
    Alias = "Script"
    Version = "0.0.0.1"

    [Directory]
    InstallDir = "Script"

    [Libraries]
    Libraries = "lib1, lib2, lib3"
    ```

   Adjust the names, script names, aliases, versions, installation directories, and libraries as needed.
   For further information on the configuration file, refer to the `install,ini` file in this repository as it contains comments to guide you.  

4. **Execution**: Give the user information on how to execute the script. The user can run the script by executing the following command:

    ```bash
    python install.py
    ```

    The script will install the project and its dependencies to `C:\Users\%username%\Documents\%InstallDir%` on Windows and `/home/%username%/Documents/%InstallDir%` on Linux.  
    It will also add a `config.ini` to the install direction, containing the installed version. You may use this config file for your projects configurations too.

**Important Note**: The versioning format is consistent. If you wish to modify the versioning format, you will need to alter the `install.py` script.

## Features

- **Simple Configuration**: The configuration file is straightforward and easy to understand.
- **Dependency Installation**: InstALL installs all libaries specified in the configuration file.
- **Versioning**: InstALL supports versioning for your project.

## Bugs

Currently, there are no known bugs. If you encounter any issues, please open an issue on the GitHub repository.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
Please reference this repository if you use InstALL in your project.

[MIT](https://choosealicense.com/licenses/mit/)
