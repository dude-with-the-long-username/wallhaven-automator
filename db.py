import sqlite3
from pathlib import Path

DB_PATH = str(Path(__file__).parent / 'wallpapers.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS wallpapers (
        id TEXT PRIMARY KEY,
        url TEXT,
        path TEXT,
        favourited INTEGER DEFAULT 0
    )''')
    conn.commit()
    conn.close()

def get_wallpaper(wallpaper_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, url, path, favourited FROM wallpapers WHERE id=?', (wallpaper_id,))
    row = c.fetchone()
    conn.close()
    return row

def add_wallpaper(wallpaper_id, url, path):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO wallpapers (id, url, path) VALUES (?, ?, ?)', (wallpaper_id, url, path))
    conn.commit()
    conn.close()

def set_favourited(wallpaper_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('UPDATE wallpapers SET favourited=1 WHERE id=?', (wallpaper_id,))
    conn.commit()
    conn.close()

def get_unfavourited_wallpapers():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, url, path FROM wallpapers WHERE favourited=0')
    rows = c.fetchall()
    conn.close()
    return rows
