
# search for words in files.
from machineconfig.utils.utils import get_latest_release

url = r'https://github.com/Genivia/ugrep'
__doc__ = """A fast, portable, feature-rich command-line search tool"""

def main(version=None):
    f = get_latest_release(url, version=version).joinpath('ugrep.exe').download()
    f.move(folder=f.get_env().WindowsApps, overwrite=True)


if __name__ == '__main__':
    main()
