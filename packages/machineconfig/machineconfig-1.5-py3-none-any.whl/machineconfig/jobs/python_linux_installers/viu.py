

from machineconfig.utils.utils import get_latest_release
import crocodile.toolbox as tb


__doc__ = """A cli image viewer for the terminal"""

def main(version=None):
    repo_url = tb.P(r"https://github.com/atanunq/viu")
    release = get_latest_release(repo_url.as_url_str(), version=version)
    exe = release.joinpath(f"viu").download()
    exe.chmod(0o777)
    # exe.move(folder=r"/usr/local/bin", overwrite=False)
    tb.Terminal().run(f"sudo mv {exe} /usr/local/bin/").print_if_unsuccessful(desc="MOVING executable to /usr/local/bin", strict_err=True, strict_returncode=True)


if __name__ == '__main__':
    pass
