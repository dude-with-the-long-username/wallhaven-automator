import os
from xml.dom import NotFoundErr
from dotenv import load_dotenv
from playwright.sync_api import Playwright, sync_playwright, expect

#TODO: add requirements.txt file

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

    # Go to https://wallhaven.cc/w/k7j1qd
    page.goto("https://wallhaven.cc/w/k7j1qd")      # wallpaper url that we want to favourite

    a= page.locator('id=fav-button').inner_text()
    if a == ' Add to Favorites':
        page.locator('id=fav-button').click()
    elif a == ' In Favorites':
        ...

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
