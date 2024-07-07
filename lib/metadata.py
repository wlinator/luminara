import subprocess


def get_latest_git_tag():
    """
    Retrieves the latest git tag.
    """
    try:
        command = ["git", "describe", "--abbrev=0", "--tags"]
        return subprocess.check_output(command).decode().strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return "BETA"


__title__ = "Luminara"
__version__ = get_latest_git_tag()
__author__ = "wlinator"
__license__ = "MIT License"
