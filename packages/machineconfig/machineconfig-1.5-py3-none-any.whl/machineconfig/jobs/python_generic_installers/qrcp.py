
from platform import system
from machineconfig.utils.utils import get_latest_release, find_move_delete_linux, find_move_delete_windows
import crocodile.toolbox as tb


def main(version=None):
    # =================================================== python's qr code to create qrcode on terminal from simple text.
    tb.Terminal().run("pip install qrcode", shell="pwsh")

    # =================================================== Go's qrcp to allow file transfer between computer and phone.
    url = get_latest_release("https://github.com/claudiodangelis/qrcp", download_n_extract=False, version=version)
    if system() == "Windows":
        downloaded = url.joinpath(f"qrcp_{url[-1].str.replace('v', '')}_Windows_x86_64.tar.gz").download().ungz_untar(inplace=True)
        find_move_delete_windows(downloaded, "qrcp")
    else:
        downloaded = url.joinpath(f"qrcp_{url[-1].str.replace('v', '')}_linux_x86_64.tar.gz").download().ungz_untar(inplace=True)
        find_move_delete_linux(downloaded, "qrcp")


if __name__ == '__main__':
    main()
