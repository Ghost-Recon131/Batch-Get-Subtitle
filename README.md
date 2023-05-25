# Batch Get Subtitle
Designed to automate the process of getting & renaming each subtitle file downloaded from https://animetosho.org/

Can also be used to get the chapter files for each episode. 


## Limitations
- Will encounter errors if there are multiple files with the same name but different extensions in the same directory.


## Pre-requisite
Python 3 required


## Standard Usage
Add in details in "Batch-Get-Tool_config.ini". All fields for each section must be filled or the script will ignore the
whole section. 

If the config file does not exist it will be created automatically. 


## Windows (Compiled Program)
Running inside Powershell
```powershell
./"Main.exe"
```

# Source File
Project can also be run by having all 3 source files "Main.py", "ConfigHandler.py" and "FileOperation.py" in the same directory.
## UNIX (Source file)
```shell
./Main.py 
```


# PyInstaller Compilation
```shell
python -m PyInstaller --onefile Main.py ConfigHandler.py FileOperation.py
```