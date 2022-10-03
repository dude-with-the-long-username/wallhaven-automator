# Wallhaven-Automator

Automate repetitive wallpaper actions on [wallhaven.cc](https://wallhaven.cc)

## ✨ Features

- Automatically favourite your current desktop wallpaper (fetched from wallhaven site through [variety](https://github.com/varietywalls/variety))
- Notification on success
  - Thumbnail of favorited pic shown in the notification
- Notification on failure
- Cookie storage & usage for more performance (skips trying to login if cookie already exists)

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
- Add full path of project directory to the variable `project_directory_path` in the program.
### Run
- `pytest favouriter.py`
  - To run with GUI (browser window):
    - set value of `headless` variable to `False` in program

### Make Program executable from anywhere

- Add `#!/usr/bin/python` to the top of the file
- Make script executable
	- `chmod +x favouriter.py`
- Create a symbolic link to your script-name.py from `/usr/local/bin` 
	- `ln -s <full-path-to-favouriter.py> /usr/local/bin/wallauto`  (can replace `wallauto` with any command name you want)
- Call `wallauto` from terminal.

## Tips:

- If using KDE Desktop, set custom keyboard shortcut in settings to launch wallauto easily.
  - eg: `alt+f` as trigger and action as `variety -f && wallauto`
## 🏗 In the works

- Download all your favourited wallpapers
- async methods to click favorite button before the entire wallpaper is loaded on wallhaven (performance)
- Favorite current desktop wallpaper into specific collections on wallhaven
- Package as an executable & AUR package
- save wallpaper for future favoriting if Internet connection is currently unavailable