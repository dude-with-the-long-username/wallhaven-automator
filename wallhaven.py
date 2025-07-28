from pathlib import Path
import sys
import time

def favourite_wallpaper(playwright, wallpaper_id, wallpaper_url, wallpaper_path, username, password, state_path, notifier, db, manual=False):
    """
    Automates the process of favoriting a wallpaper on wallhaven.cc using Playwright.
    Handles login, persistent state, and notification.
    If manual is True, launches browser in non-headless mode and waits for user input before closing.
    """

    print(f"[DEBUG] favourite_wallpaper() received manual={manual}")
    print(f'[LOG] Launching browser (firefox)... (manual={manual})')
    browser = playwright.firefox.launch(headless=not manual)

    if Path(state_path).exists():
        print('[LOG] Using existing browser state.')
        context = browser.new_context(storage_state=state_path)
        page = context.new_page()
    else:
        print('[LOG] Logging in to wallhaven.cc...')
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://wallhaven.cc/login")
        page.locator("[placeholder=\"Username or Email\"]").click()
        page.locator("[placeholder=\"Username or Email\"]").fill(f"{username}")
        page.locator("[placeholder=\"Password\"]").click()
        page.locator("[placeholder=\"Password\"]").fill(f"{password}")
        page.locator("button:has-text(\"Login\")").click()
        page.wait_for_url(f"https://wallhaven.cc/user/{username}")

    print('[LOG] Saving browser state...')
    context.storage_state(path=state_path)

    print(f'[LOG] Visiting {wallpaper_url} ...')
    page.goto(wallpaper_url)
    fav_button_text = page.locator('id=fav-button').inner_text()
    print(f'[LOG] fav-button text: "{fav_button_text}"')
    if fav_button_text == ' Add to Favorites':
        print(f'[LOG] Favoriting wallpaper {wallpaper_id}...')
        page.locator('id=fav-button').click()
        db.set_favourited(wallpaper_id)
        notifier.notify(f'Favorited: {wallpaper_id}', icon=wallpaper_path)
    elif fav_button_text == ' In Favorites':
        print(f'[LOG] Wallpaper {wallpaper_id} already in favorites on wallhaven. Marking as favorited in DB.')
        db.set_favourited(wallpaper_id)
        notifier.notify(f'Already Favorited: {wallpaper_id}', icon=wallpaper_path)

    if manual:
        print('[LOG] Manual mode enabled. The browser will remain open for inspection.')
        input('Press Enter in the terminal to close the browser and finish...')
        print('[LOG] Closing browser after manual inspection.')
    print('[LOG] Closing browser...')
    context.close()
    browser.close()
