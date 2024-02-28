import subprocess


def get_latest_git_tag():
    try:
        command = ['git', 'describe', '--abbrev=0', '--tags']
        output = subprocess.check_output(command).decode().strip()
        return output

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return "BETA"


__title__ = "Racu"
__version__ = get_latest_git_tag()
__author__ = "stupidbeaver"
__author_email__ = "dokimakimaki@gmail.com"
__license__ = "GNU GENERAL PUBLIC LICENSE v2"
