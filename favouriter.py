#!/home/fiona/projects/wallhaven-automator/venv/bin/python3


#!/usr/bin/python


import os
import re
import sqlite3
from dotenv import load_dotenv
from playwright.sync_api import Playwright, sync_playwright
import subprocess
import tempfile
from pathlib import Path

load_dotenv()	#looks for .env file & loads content as environment variables, when found. By default looks in the current directory. Else looks in parent directory

# username=os.getenv('USERNAME')
# password=os.getenv('PASSWORD')


project_directory_path = '/home/fiona/projects/wallhaven-automator/'
password_file_path = f'{project_directory_path}.env'
db_path = f'{project_directory_path}wallpapers.db'

# --- DB SETUP ---
def init_db():
    print('[LOG] Initializing database...')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS wallpapers (
        id TEXT PRIMARY KEY,
        url TEXT,
        path TEXT,
        favourited INTEGER DEFAULT 0
    )''')
    conn.commit()
    conn.close()
    print('[LOG] Database ready.')

def get_wallpaper(wallpaper_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT id, url, path, favourited FROM wallpapers WHERE id=?', (wallpaper_id,))
    row = c.fetchone()
    conn.close()
    return row

def add_wallpaper(wallpaper_id, url, path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO wallpapers (id, url, path) VALUES (?, ?, ?)', (wallpaper_id, url, path))
    conn.commit()
    conn.close()

def set_favourited(wallpaper_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('UPDATE wallpapers SET favourited=1 WHERE id=?', (wallpaper_id,))
    conn.commit()
    conn.close()

def get_unfavourited_wallpapers():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT id, url, path FROM wallpapers WHERE favourited=0')
    rows = c.fetchall()
    conn.close()
    return rows

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

    # Get current wallpaper info from Variety
    print('[LOG] Fetching current wallpaper from Variety...')
    cmd = ['variety', '--get']
    with tempfile.TemporaryFile() as tempf:
        proc = subprocess.Popen(cmd, stdout=tempf)
        proc.wait()
        tempf.seek(0)   # go to start of file
        command_output : list = tempf.readlines()  # outputs a list with 1 element

    # Example of command_output= b'/home/fiona/.config/variety/Downloaded/wallhaven_wallhaven_cc_search_q_like_3Ag7l5x3_categories_111_purity_100_sorting_relevance_order_desc/wallhaven-y8w9ex.jpg\n'
    wallpaper_id : str = re.search(r"(.*wallhaven-)(.*?)\..*", str(command_output[0])).group(2)
    wallpaper_path : str = clean_variety_output_path(str(command_output[0]))
    wallpaper_url = f"https://wallhaven.cc/w/{wallpaper_id}"
    print(f'[LOG] Current wallpaper: id={wallpaper_id}, path={wallpaper_path}')

    # DB: ensure wallpaper is tracked
    row = get_wallpaper(wallpaper_id)
    if not row:
        print(f'[LOG] Wallpaper {wallpaper_id} not in DB. Adding...')
        add_wallpaper(wallpaper_id, wallpaper_url, wallpaper_path)
        favourited = 0
    else:
        favourited = row[3]
        print(f'[LOG] Wallpaper {wallpaper_id} found in DB. Favourited={bool(favourited)}')

    if favourited:
        print(f'[LOG] Wallpaper {wallpaper_id} already favourited. Skipping browser.')
        subprocess.run(['notify-send', 'Already Favorited (DB)', '--app-name=WallAuto', '-i', f'{wallpaper_path}'])
        return

    print('[LOG] Launching browser...')
    browser = playwright.chromium.launch(headless=True)

    if Path(f"{project_directory_path}/state.json").exists():   #checking if file exists
        # Create a new context with the saved storage state.
        print('[LOG] Using existing browser state.')
        context = browser.new_context(storage_state=f"{project_directory_path}/state.json")
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

    # Save storage state
    print('[LOG] Saving browser state...')
    context.storage_state(path=f"{project_directory_path}/state.json")

    # Only favorite the current wallpaper
    print(f'[LOG] Visiting {wallpaper_url} ...')
    page.goto(wallpaper_url)
    fav_button_text : str = page.locator('id=fav-button').inner_text()
    print(f'[LOG] fav-button text: "{fav_button_text}"')
    if fav_button_text == ' Add to Favorites':
        print(f'[LOG] Favoriting wallpaper {wallpaper_id}...')
        page.locator('id=fav-button').click()
        set_favourited(wallpaper_id)
        subprocess.run(['notify-send', f'Favorited: {wallpaper_id}', '--app-name=WallAuto', '-i', f'{wallpaper_path}'])
    elif fav_button_text == ' In Favorites':
        print(f'[LOG] Wallpaper {wallpaper_id} already in favorites on wallhaven. Marking as favorited in DB.')
        set_favourited(wallpaper_id)
        subprocess.run(['notify-send', f'Already Favorited: {wallpaper_id}', '--app-name=WallAuto', '-i', f'{wallpaper_path}'])

    print('[LOG] Closing browser...')
    context.close()
    browser.close()

def main() -> None:
    init_db()
    with sync_playwright() as playwright:
        run(playwright)

if __name__ == "__main__":
    import traceback
    try:
        main()
    except Exception as e:
        error_msg = f"{type(e).__name__}: {e}\n" + traceback.format_exc()
        print(error_msg)
        subprocess.run([
            'notify-send',
            'Failed Favoriting',
            f'Error Occurred! Check log.',
            '--app-name=WallAuto'
        ])