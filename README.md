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

- set up a virtual environment (optional but recommended)
  - `python3 -m venv venv`
  - Activate it with `source venv/bin/activate`
- Install project dependencies
  - `pip install -r requirements.txt`
- Install browsers required by playwright
  - `playwright install` or `python -m playwright install`
- Create a file named `.env` in the root of your project folder
    - Add the following to the `.env` file (replace values with your password & username)
        ```
            USERNAME='your-username'
            PASSWORD='your-password'
        ```
- Add full path of project directory to the variable `project_directory_path` in the file `main.py`(replace the value that already exists).

### Run & CLI Usage

 `python main.py [OPTIONS]`

#### CLI Options:

- `--favourite` : Favorite the current wallpaper (default action if no flag is given)
- `--show-db` : Show all wallpapers in the database (id, url, path, favourited)
- `--show-unfavourited` : Show id, url, path, and favourited for all wallpapers with favourited=0
- `--favourite-all` : Favorite all unfavourited wallpapers in the database (5s delay between each)
- `--remove-unfavourited` : Remove all unfavourited wallpapers from the database
- `--manual` : Run in manual mode, where the browser will remain open for inspection until there is a user input in the terminal.

  - To run with GUI (browser window):
    - set value of `headless` variable to `False` in program

### Make Program executable from anywhere

- Add the shebang line that points to your Python interpreter inside your virtual enviornment, e.g. `#!/home/fiona/projects/wallhaven-automator/venv/bin/python3`   (alternative to adding `#!/usr/bin/python` to the top of the file)
- Make script executable
  - `chmod +x main.py`
- Create a symbolic link to your script-name.py from `/usr/local/bin` 
  - `ln -s <full-path-to-main.py> /usr/local/bin/wallauto`  (can replace `wallauto` with any command name you want)
- Call `wallauto` from terminal.

## Tips:

- If using KDE Desktop, set custom keyboard shortcut in settings to launch wallauto easily.
  - eg: `alt+f` as trigger and action as `variety -f && wallauto`
    - or use command `variety -f & wallauto & wait` to run both commands in parallel
## 🏗 In the works

- Download all your favourited wallpapers
- async methods to click favorite button before the entire wallpaper is loaded on wallhaven (performance)
- Favorite current desktop wallpaper into specific collections on wallhaven
- Package as an executable & AUR package
- save wallpaper for future favoriting if Internet connection is currently unavailable
- When using `--manual`, exit the script when the browser is closed by the user