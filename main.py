#!/home/fiona/projects/wallhaven-automator/venv/bin/python3


#!/usr/bin/python


import os
import db
import variety
from dotenv import load_dotenv
from playwright.sync_api import Playwright, sync_playwright
import notifier
import tempfile
from pathlib import Path
import argparse
import time


load_dotenv()	#looks for .env file & loads content as environment variables, when found. By default looks in the current directory. Else looks in parent directory

# username=os.getenv('USERNAME')
# password=os.getenv('PASSWORD')


project_directory_path = '/home/fiona/projects/wallhaven-automator/'
password_file_path = f'{project_directory_path}.env'




with open(password_file_path, mode="r") as file:
    variables_list : list[str] = file.readlines()

for variable in variables_list:
    if variable.startswith("USERNAME"):
        username = variable.split("=",1)[1].strip().replace("'","")
    if variable.startswith("PASSWORD"):
        password = variable.split("=",1)[1].strip().replace("'","")


def run(playwright: Playwright, manual=False) -> None:
    print(f"[DEBUG] run() received manual={manual}")

    # Get current wallpaper info from Variety using variety.py
    print('[LOG] Fetching current wallpaper from Variety...')
    wallpaper_id, wallpaper_path, wallpaper_url = variety.get_current_wallpaper()
    print(f'[LOG] Current wallpaper: id={wallpaper_id}, path={wallpaper_path}')

    # DB: ensure wallpaper is tracked
    row = db.get_wallpaper(wallpaper_id)
    if not row:
        print(f'[LOG] Wallpaper {wallpaper_id} not in DB. Adding...')
        db.add_wallpaper(wallpaper_id, wallpaper_url, wallpaper_path)
        favourited = 0
        notifier.notify('Added to DB', icon=wallpaper_path)
    else:
        favourited = row[3]
        print(f'[LOG] Wallpaper {wallpaper_id} found in DB. Favourited={bool(favourited)}')

    if favourited and manual==False:
        print(f'[LOG] Wallpaper {wallpaper_id} already favourited. Skipping browser.')
        notifier.notify('Already Favorited (DB)', icon=wallpaper_path)
        return

    # Use wallhaven.py for browser automation
    import wallhaven
    wallhaven.favourite_wallpaper(
        playwright=playwright,
        wallpaper_id=wallpaper_id,
        wallpaper_url=wallpaper_url,
        wallpaper_path=wallpaper_path,
        username=username,
        password=password,
        state_path=f"{project_directory_path}/state.json",
        notifier=notifier,
        db=db,
        manual=manual
    )



def main():
    parser = argparse.ArgumentParser(description="Wallhaven Automator CLI")
    parser.add_argument('--show-db', action='store_true', help='Show all wallpapers in the database')
    parser.add_argument('--show-unfavourited', action='store_true', help='Show IDs of all unfavourited wallpapers in the database')
    parser.add_argument('--favourite', action='store_true', help='Favorite the current wallpaper (default action)')
    parser.add_argument('--favourite-all', action='store_true', help='Favorite all unfavourited wallpapers in the database (5s delay between each)')
    parser.add_argument('--remove-unfavourited', action='store_true', help='Remove all unfavourited wallpapers from the database')
    parser.add_argument('--manual', action='store_true', help='Open browser in manual (non-headless) mode and wait for user action before closing')
    args = parser.parse_args()

    print(f"[DEBUG] args.manual: {args.manual}")

    # If --favourite is passed, or no action flags (except --manual) are given, run the main workflow
    action_flags = [args.favourite, args.favourite_all, args.show_db, args.show_unfavourited, args.remove_unfavourited]
    if args.favourite or not any(action_flags):
        db.init_db()
        with sync_playwright() as playwright:
            run(playwright, manual=args.manual)

    if args.show_db:
        db.show_db()
        return
    if args.show_unfavourited:
        db.show_unfavourited_ids()
        return
    # If --favourite-all is passed, favorite all unfavourited wallpapers with delay
    if args.favourite_all:
        db.init_db()
        unfavs = db.get_unfavourited_wallpapers()
        if not unfavs:
            print("No unfavourited wallpapers to process.")
            return
        for wid, wurl, wpath in unfavs:
            print(f"[CLI] Processing wallpaper {wid}...")
            with sync_playwright() as playwright:
                import wallhaven
                wallhaven.favourite_wallpaper(
                    playwright=playwright,
                    wallpaper_id=wid,
                    wallpaper_url=wurl,
                    wallpaper_path=wpath,
                    username=username,
                    password=password,
                    state_path=f"{project_directory_path}/state.json",
                    notifier=notifier,
                    db=db,
                    manual=args.manual
                )
            print("[CLI] Waiting 5 seconds before next wallpaper...")
            time.sleep(5)
        return
    
    if args.remove_unfavourited:
        db.remove_unfavourited()
        return
    
if __name__ == "__main__":
    import traceback
    try:
        main()
    except Exception as e:
        error_msg = f"{type(e).__name__}: {e}\n" + traceback.format_exc()
        print(error_msg)
        notifier.notify('Failed Favoriting', 'Error Occurred! Check log.')
