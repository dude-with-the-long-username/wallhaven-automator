# Copilot Instructions for Wallhaven-Automator

## Project Overview
- Automates favoriting the current desktop wallpaper on [wallhaven.cc](https://wallhaven.cc) using Playwright and the Variety wallpaper manager.
- Sends desktop notifications (with thumbnail) on success or failure.
- Uses persistent login state (via `state.json`) to avoid repeated logins.

## Key Files & Structure
- `favouriter.py`: Main script. Handles login, wallpaper detection, favoriting, and notifications.
- `.env`: Stores `USERNAME` and `PASSWORD` for wallhaven.cc (not checked in).
- `requirements.txt`: Python dependencies (`playwright`, `dotenv`).
- `state.json`: Stores Playwright browser state (created at runtime).

## Core Workflow
1. Fetches current wallpaper path using `variety --get` (requires Variety to be installed and running).
2. Extracts the wallhaven wallpaper ID from the file path.
3. Launches a headless Chromium browser via Playwright.
4. Loads login state from `state.json` if available; otherwise, logs in using credentials from `.env`.
5. Navigates to the wallpaper's wallhaven page and clicks the favorite button if not already favorited.
6. Sends a desktop notification using `notify-send` (Linux only).

## Developer Workflows
- **Setup:**
  - Create and activate a Python virtual environment.
  - Install dependencies: `pip install -r requirements.txt`
  - Install Playwright browsers: `python -m playwright install`
  - Create `.env` with `USERNAME` and `PASSWORD`.
- **Run:**
  - `python favouriter.py` (or make executable and symlink for CLI use)
- **Debugging:**
  - Set `headless=False` in `favouriter.py` to see browser actions.
- **Notifications:**
  - Uses `notify-send` for desktop notifications; ensure it's available on your system.

## Project-Specific Patterns
- Credentials are loaded from `.env` manually (not via `os.getenv` in main logic).
- Persistent browser state is stored in `state.json` in the project root.
- All main logic is in a single script; no test or module structure.
- Uses subprocess to interact with system tools (`variety`, `notify-send`).

## Integration Points
- **Variety:** Must be installed and managing wallpapers.
- **Wallhaven.cc:** Requires valid user credentials.
- **Linux Desktop:** Relies on `notify-send` for notifications.

## Example: Adding a New Notification
To add a new notification, use:
```python
subprocess.run(['notify-send', 'Your Message', '--app-name=WallAuto', '-i', wallpaper_path])
```

---

If any section is unclear or missing, please provide feedback for further refinement.
