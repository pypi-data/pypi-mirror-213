
from machineconfig.utils.utils import get_latest_release, find_move_delete_linux
import crocodile.toolbox as tb


url = r'https://github.com/sorenisanerd/gotty'
suffix = 'linux_amd64'
__doc__ = """gotty is a simple command line tool that turns your CLI tools into web applications."""


def main(version=None):
    release = get_latest_release(url, suffix=suffix, version=version, download_n_extract=True, linux=True, compression="tar.gz")


if __name__ == '__main__':
    main()
