# Batch Get Subtitle
Designed to automate the process of getting & renaming each subtitle file downloaded from https://animetosho.org/

Can also be used to get the chapter files for each episode. 


## Limitations
- Only works with 1 file type at once, cannot mix and match file types in source directory. 


## Pre-requisite
Python 3 required


## Standard Usage
Run the script and follow instructions in program


# Input Redirection
Input redirection can also be used to speed up the process, 2 examples have been provided in "Input Redirection Examples".

Please use with a text file with the following details seperated by new line
## Expected structure 
- source directory
- output directory
- current file name (with file extension)
- new file name (no file extension needed)
- structure (can be left empty)
- episode starting number ie start number on episode 1


## Windows (Compiled Program)
Running inside Powershell
```powershell
Get-Content "subtitle details.txt" | ./"Main.exe"
Get-Content "chapter details.txt" | ./"Main.exe"
```

# Source File
Project can also be run by having all 3 source files "Main.py", "MoveAndRename.py" and "InputValidation.py" in the same directory.
## UNIX (Source file)
```shell
./Main.py < "subtitle details.txt"
./Main.py < "chapter details.txt"
```


# PyInstaller Compilation
```shell
python -m PyInstaller --hidden-import 'natsort' --onefile Main.py MoveAndRename.py InputValidation.py
```