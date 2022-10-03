#!/usr/bin/python

import os
import re
from dotenv import load_dotenv
from playwright.sync_api import Playwright, sync_playwright
import subprocess
import tempfile
from pathlib import Path

load_dotenv()	#looks for .env file & loads content as environment variables, when found. By default looks in the current directory. Else looks in parent directory

# username=os.getenv('USERNAME')
# password=os.getenv('PASSWORD')

project_directory_path = '/home/fiona/Projects/wallhaven-automator/'
password_file_path = '/home/fiona/Projects/wallhaven-automator/.env'

with open(password_file_path, mode="r") as file:
    variables_list : list[str] = file.readlines()

def remove_quotes_new_line(a_string:str) -> str:
    return a_string.replace("'",'').replace("\n",'')


def clean_variety_output_path(a_string:str) -> str:
    return a_string.replace("b'",'').replace("\\n",'').replace("'",'')

for variable in variables_list:
    if re.match(r"^USERNAME", variable):
        username = re.search(r"(^USERNAME=)(.*)",remove_quotes_new_line(variable)).group(2).strip()

    if re.match(r"^PASSWORD", variable):
        password = re.search(r"(^PASSWORD=)(.*)",remove_quotes_new_line(variable)).group(2).strip()


def run(playwright: Playwright) -> None:
    
    cmd = ['variety', '--get']  #command to run in terminal - prints path of the current wallpaper set by variety
    with tempfile.TemporaryFile() as tempf:
        proc = subprocess.Popen(cmd, stdout=tempf)
        proc.wait()
        tempf.seek(0)   # go to start of file
        command_output : list = tempf.readlines()  # outputs a list with 1 element
    
    # Example of command_output= b'/home/fiona/.config/variety/Downloaded/wallhaven_wallhaven_cc_search_q_like_3Ag7l5x3_categories_111_purity_100_sorting_relevance_order_desc/wallhaven-y8w9ex.jpg\n'
    wallpaper_id : str = re.search(r"(.*wallhaven-)(.*?)\..*", str(command_output[0])).group(2)
    wallpaper_path : str = clean_variety_output_path(str(command_output[0]))
    
    browser = playwright.chromium.launch(headless=False)
    
    if Path(f"{project_directory_path}/state.json").exists():   #checking if file exists
        # Create a new context with the saved storage state.
        context = browser.new_context(storage_state=f"{project_directory_path}/state.json")
        page = context.new_page()

    else:
        context = browser.new_context()
        # Open new page
        page = context.new_page()

        # Go to https://wallhaven.cc/
        page.goto("https://wallhaven.cc/login")

        # Click [placeholder="Username or Email"]
        page.locator("[placeholder=\"Username or Email\"]").click()

        # Fill [placeholder="Username or Email"]
        page.locator("[placeholder=\"Username or Email\"]").fill(f"{username}")

        # Click [placeholder="Password"]
        page.locator("[placeholder=\"Password\"]").click()

        # Fill [placeholder="Password"]
        page.locator("[placeholder=\"Password\"]").fill(f"{password}")

        # Click button:has-text("Login")
        page.locator("button:has-text(\"Login\")").click()
        page.wait_for_url(f"https://wallhaven.cc/user/{username}")


    # Save storage state into the file.
    storage = context.storage_state(path=f"{project_directory_path}/state.json") # save login state to file

    # Go to https://wallhaven.cc/w/k7j1qd
    page.goto(f"https://wallhaven.cc/w/{wallpaper_id}")      # wallpaper url that we want to favourite
    fav_button_text : str = page.locator('id=fav-button').inner_text()

    if fav_button_text == ' Add to Favorites':
        page.locator('id=fav-button').click()
        subprocess.run(['notify-send', 'Favorited :D', '--app-name=WallAuto', '-i', f'{wallpaper_path}'])
    elif fav_button_text == ' In Favorites':
        # ...
        subprocess.run(['notify-send', 'Already Favorited', '--app-name=WallAuto', '-i', f'{wallpaper_path}'])

    # ---------------------
    context.close()
    browser.close()

def main() -> None:
    with sync_playwright() as playwright:
        run(playwright)

if __name__ == "__main__":
    main()