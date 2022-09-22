# Wallhaven-Automator

Automate repetitive wallpaper actions on [wallhaven.cc](https://wallhaven.cc)

## ✨ Features

- Automatically favourite your current desktop wallpaper (fetched from wallhaven site through [variety](https://github.com/varietywalls/variety))
- Notification on sucess/failure

## 🔰 Setup
### Pre-requisites

- Linux
- Python

### Steps

- Install project dependencies
  - `pip install -r requirements.txt`
- Install browsers required by playwright
  - `playwright install` 
- Create a file named `.env` in the root of your project folder
    - Add the following to the `.env` file (replace values with your password & username)
        ```
            USERNAME='your-username'
            PASSWORD='your-password'
        ```
- Add full path of `.env` file to the variable `password_file_path` in the program.
### Run
- `pytest favouriter.py`
  - To run with GUI (browser window):
    - set value of `headless` variable to `False` in program

## 🏗 In the works

- Download all your favourited wallpapers
- Favorite current desktop wallpaper into specific collections on wallhaven
- Cookie storage & usage for more performance
- Package as an executable & AUR package
- save wallpaper for future favoriting if Internet connection is currently unavailable