import subprocess
import re
import tempfile

def clean_variety_output_path(a_string: str) -> str:
    return a_string.replace("b'", '').replace("\\n", '').replace("'", '')

def get_current_wallpaper():
    """
    Fetches the current wallpaper info from Variety.
    Returns (wallpaper_id, wallpaper_path, wallpaper_url)
    """
    cmd = ['variety', '--get']
    with tempfile.TemporaryFile() as tempf:
        proc = subprocess.Popen(cmd, stdout=tempf)
        proc.wait()
        tempf.seek(0)
        command_output = tempf.readlines()
    if not command_output:
        raise RuntimeError('No output from variety --get')
    wallpaper_id = re.search(r"(.*wallhaven-)(.*?)\..*", str(command_output[0])).group(2)
    wallpaper_path = clean_variety_output_path(str(command_output[0]))
    wallpaper_url = f"https://wallhaven.cc/w/{wallpaper_id}"
    return wallpaper_id, wallpaper_path, wallpaper_url
