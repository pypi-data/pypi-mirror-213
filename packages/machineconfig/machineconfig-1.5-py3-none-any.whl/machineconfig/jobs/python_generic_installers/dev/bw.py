

import crocodile.toolbox as tb
from machineconfig.utils.utils import find_move_delete_linux
from rich.console import Console
from platform import system


__doc__ = """Bitwarden (password manager) cli"""


def main(version=None):
    _ = version
    if system() == "Windows":
        console = Console()
        console.rule("Installing bitwarden")
        url = r'https://vault.bitwarden.com/download/?app=cli&platform=windows'
        dir_ = tb.P(url).download(name="file.zip").unzip(inplace=True)
        dir_.search(f"bw.exe", r=True)[0].move(folder=tb.get_env().WindowsApps, overwrite=True)
        dir_.delete(sure=True)
        console.rule("Completed Installation")
    else:
        url = r'https://vault.bitwarden.com/download/?app=cli&platform=linux'
        dir_ = tb.P(url).download(name="file.zip").unzip(inplace=True)
        find_move_delete_linux(dir_, "bw", delete=True)


if __name__ == '__main__':
    main()
