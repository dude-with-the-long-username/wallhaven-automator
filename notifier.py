import subprocess

def notify(summary, body=None, icon=None):
    """
    Send a desktop notification using notify-send.
    summary: Title of the notification
    body: Optional message body
    icon: Optional path to icon image
    """
    cmd = ['notify-send', summary]
    if body:
        cmd.append(body)
    cmd += ['--app-name=WallAuto']
    if icon:
        cmd += ['-i', icon]
    subprocess.run(cmd)
