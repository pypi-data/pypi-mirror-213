
from machineconfig.utils.utils import get_latest_release
from platform import system
# import crocodile.toolbox as tb


url = r"https://github.com/gopasspw/gopass"
__doc__ = """cli password manager"""

def main(version=None):
    if system() == "Windows":
        get_latest_release(url, suffix="windows-amd64", download_n_extract=True, strip_v=True, tool_name="gopass", delete=False, version=version)
    elif system() == "Linux":
        get_latest_release(url, suffix="linux-amd64", download_n_extract=True, linux=True, compression="tar.gz", strip_v=True, tool_name="gopass", delete=False, version=version)
    else: raise NotImplementedError(f"System {system()} is not supported")


if __name__ == '__main__':
    main()
