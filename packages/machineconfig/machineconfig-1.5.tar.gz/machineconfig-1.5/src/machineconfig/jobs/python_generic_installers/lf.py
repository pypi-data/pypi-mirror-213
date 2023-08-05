
# LF (golang)
from machineconfig.utils.utils import get_latest_release
import crocodile.toolbox as tb
import platform

url = 'https://github.com/gokcehan/lf'
__doc__ = """lf is a terminal file manager written in go."""

def main(version=None):

    if platform.system() == 'Windows':
        # tb.Terminal().run("nu -c 'ps | where name == lf.exe | each { |it| kill $it.pid --force}'", shell="pwsh").print()
        tb.L(tb.install_n_import("psutil").process_iter()).filter(lambda x: x.name() == 'lf.exe').apply(lambda x: x.kill())
        get_latest_release(url, file_name='lf-windows-amd64.zip', download_n_extract=True, version=version)
    elif platform.system() == 'Linux':
        tb.Terminal().run("killall lf")
        get_latest_release(url, file_name='lf-linux-amd64.tar.gz', download_n_extract=True, linux=True, compression="tar.gz", version=version)
    else: raise NotImplementedError(f"Platform {platform.system()} not supported.")

    return f""


if __name__ == '__main__':
    main()
