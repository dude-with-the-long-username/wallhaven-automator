import os
import re
from dotenv import load_dotenv
from playwright.sync_api import Playwright, sync_playwright
import subprocess
import tempfile

load_dotenv()	#looks for .env file & loads content as environment variables, when found. By default looks in the current directory. Else looks in parent directory

username=os.getenv('USERNAME')
password=os.getenv('PASSWORD')


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
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

    cmd = ['variety', '--get']  #command to run in terminal - prints path of the current wallpaper set by variety
    with tempfile.TemporaryFile() as tempf:
        proc = subprocess.Popen(cmd, stdout=tempf)
        proc.wait()
        tempf.seek(0)   # go to start of file
        command_output : list = tempf.readlines()  # outputs a list
    
    # Example of command_output= b'/home/fiona/.config/variety/Downloaded/wallhaven_wallhaven_cc_search_q_like_3Ag7l5x3_categories_111_purity_100_sorting_relevance_order_desc/wallhaven-y8w9ex.jpg\n'
    wallpaper_id : str = re.search(r"(.*wallhaven-)(.*?)\..*", str(command_output[0])).group(2)
    
    # Go to https://wallhaven.cc/w/k7j1qd
    page.goto(f"https://wallhaven.cc/w/{wallpaper_id}")      # wallpaper url that we want to favourite
    fav_button_text : str = page.locator('id=fav-button').inner_text()

    if fav_button_text == ' Add to Favorites':
        page.locator('id=fav-button').click()
    elif fav_button_text == ' In Favorites':
        ...

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
