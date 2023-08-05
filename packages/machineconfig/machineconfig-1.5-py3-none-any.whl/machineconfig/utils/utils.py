
from crocodile.file_management import P, randstr
from crocodile.meta import Terminal
from crocodile.core import install_n_import
# import crocodile.environment as env
import machineconfig
from rich.text import Text
from rich.panel import Panel
from rich.console import Console
from rich.syntax import Syntax
import platform


LIBRARY_ROOT = P(machineconfig.__file__).resolve().parent  # .replace(P.home().str.lower(), P.home().str)
REPO_ROOT = LIBRARY_ROOT.parent.parent
PROGRAM_PATH = P.tmp().joinpath("shells/python_return_command") + (".ps1" if platform.system() == "Windows" else ".sh")
CONFIG_PATH = P.home().joinpath(".config/machineconfig")
tmp_install_dir = P.tmp(folder="tmp_installers")


def display_options(msg, options: list, header="", tail="", prompt="", default=None, fzf=False, multi=False) -> str or list:
    tool_name = "fzf"
    if fzf and check_tool_exists(tool_name):
        install_n_import("pyfzf")
        from pyfzf.pyfzf import FzfPrompt
        fzf = FzfPrompt()
        nl = "\n"
        choice_idx = fzf.prompt(options, fzf_options=("--multi" if multi else "") + f" --prompt={prompt.replace(nl, ' ')} --border=rounded") # --border-label={msg.replace(nl, ' ')}")
    else:
        console = Console()
        if default is not None:
            assert default in options, f"Default `{default}` option not in options `{list(options)}`"
            default_msg = Text(f" <<<<-------- DEFAULT", style="bold red")
        else: default_msg = ""
        txt = Text("\n" + msg + "\n")
        for idx, key in enumerate(options):
            txt = txt + Text(f"{idx:2d} ", style="bold blue") + str(key) + (default_msg if default is not None and default == key else "") + "\n"
        txt = Panel(txt, title=header, subtitle=tail, border_style="bold red")
        console.print(txt)
        choice_idx = input(f"{prompt}\nEnter option *number* (or option name starting with space): ")

    if not fzf:
        if choice_idx.startswith(" "):
            choice_key = choice_idx.strip()
            assert choice_key in options, f"Choice `{choice_key}` not in options `{options}`"
            choice_idx = options.index(choice_key)
        else:
            if choice_idx == "":
                assert default is not None, f"Default option not available!"
                choice_idx = options.index(default)
            try:
                try: choice_idx = int(choice_idx)
                except ValueError:  # parsing error
                    raise IndexError
                choice_key = options[choice_idx]
            except IndexError:
                # many be user forgotten to start with a dash
                if choice_idx in options:
                    choice_key = choice_idx
                    choice_idx = options.index(choice_idx)
                else: raise ValueError(f"Unknown choice. {choice_idx}")
            except TypeError:
                raise TypeError(f"Unknown choice. {choice_idx}")
                # pass
        print(f"{choice_idx}: {choice_key}", f"<<<<-------- CHOICE MADE")
    else:
        if not multi and type(choice_idx) is list and len(choice_idx) == 1: choice_idx = choice_idx[0]
        choice_key = choice_idx
    return choice_key


def symlink(this: P, to_this: P, prioritize_to_this=True):
    """helper function. creates a symlink from `this` to `to_this`.
    What can go wrong?
    depending on this and to_this existence, one will be prioretized depending on overwrite value.
    True means this will potentially be overwritten (depending on whether to_this exists or not)
    False means to_this will potentially be overwittten."""
    this = P(this).expanduser().absolute()
    to_this = P(to_this).expanduser().absolute()
    if this.is_symlink(): this.delete(sure=True)  # delete if it exists as symblic link, not a concrete path.
    if this.exists():  # this is a problem. It will be resolved via `overwrite`
        if prioritize_to_this is True:  # it *can* be deleted, but let's look at target first.
            if to_this.exists():  # this exists, to_this as well. to_this is prioritized.
                this.append(f".orig_{randstr()}", inplace=True)  # rename is better than deletion
            else: this.move(path=to_this)  # this exists, to_this doesn't. to_this is prioritized.
        elif prioritize_to_this is False:  # don't sacrefice this, sacrefice to_this.
            if to_this.exists(): this.move(path=to_this, overwrite=True)  # this exists, to_this as well, this is prioritized.   # now we are readly to make the link
            else: this.move(path=to_this)  # this exists, to_this doesn't, this is prioritized.
    else:  # this doesn't exist.
        if not to_this.exists(): to_this.touch()  # we have to touch it (file) or create it (folder)
    if platform.system() == "Windows": _ = install_n_import("win32api", "pywin32")  # this is crucial for windows to pop up the concent window in case python was not run as admin.
    try:
        P(this).symlink_to(to_this, verbose=True, overwrite=True)
    except Exception as ex: print(f"Failed at linking {this} ==> {to_this}.\nReason: {ex}")


def find_move_delete_windows(downloaded, tool_name=None, delete=True):
    if tool_name is not None and ".exe" in tool_name: tool_name = tool_name.replace(".exe", "")
    if downloaded.is_file():
        exe = downloaded
    else:
        if tool_name is None: exe = downloaded.search("*.exe", r=True)[0]
        else:
            tmp = downloaded.search(f"{tool_name}.exe", r=True)
            if len(tmp) == 1: exe = tmp[0]
            else: exe = downloaded.search("*.exe", r=True)[0]
    exe.move(folder=P.get_env().WindowsApps, overwrite=True)  # latest version overwrites older installation.
    if delete: downloaded.delete(sure=True)
    return exe


def find_move_delete_linux(downloaded, tool_name, delete=True):
    if downloaded.is_file():
        exe = downloaded
    else:
        res = downloaded.search(f"*{tool_name}*", folders=False, r=True)
        if len(res) == 1: exe = res[0]
        else: exe = downloaded.search(tool_name, folders=False, r=True)[0]
    print(f"MOVING file `{repr(exe)}` to '/usr/local/bin'")
    exe.chmod(0o777)
    # exe.move(folder=r"/usr/local/bin", overwrite=False)
    Terminal().run(f"sudo mv {exe} /usr/local/bin/").print_if_unsuccessful(desc="MOVING executable to /usr/local/bin", strict_err=True, strict_returncode=True)
    if delete: downloaded.delete(sure=True)
    return None


def get_latest_release(repo_url, download_n_extract=False, suffix="x86_64-pc-windows-msvc", file_name=None, tool_name=None, exe_name=None, delete=True, strip_v=False, linux=False, compression=None, sep="-", version=None):
    console = Console()
    print("\n\n\n")
    print(f"Inspecting latest release @ {repo_url}   ...")
    # with console.status("Installing..."):  # makes troubles on linux when prompt asks for password to move file to /usr/bin

    if version is None:
        import requests  # https://docs.github.com/en/repositories/releasing-projects-on-github/linking-to-releases
        latest_version = requests.get(str(repo_url) + "/releases/latest").url.split("/")[-1]  # this is to resolve the redirection that occures: https://stackoverflow.com/questions/36070821/how-to-get-redirect-url-using-python-requests
    else: latest_version = version

    download_link = P(repo_url + "/releases/download/" + latest_version)
    compression = compression or ("zip" if not linux else "tar.gz")
    version = download_link[-1]
    version = str(version).replace("v", "") if strip_v else str(version)
    tool_name = tool_name or P(repo_url)[-1]
    P.home().joinpath(f"tmp_results/cli_tools_installers/versions/{tool_name}").create(parents_only=True).write_text(version)

    if not download_n_extract: return download_link
    console.rule(f"Installing {tool_name} version {version}")
    if file_name is None:  # it is not constant, so we compile it from parts as follows:
        file_name = f'{tool_name}{sep}{version}{sep}{suffix}.{compression}'
    download_link = download_link.joinpath(file_name)
    print("Downloading", download_link.as_url_str())
    downloaded = download_link.download(folder=tmp_install_dir)

    if "tar.gz" in download_link: downloaded = downloaded.ungz_untar(inplace=True)
    elif "zip" in download_link: downloaded = downloaded.unzip(inplace=True, overwrite=True)
    elif "tar.xz" in download_link: downloaded = downloaded.unxz_untar(inplace=True)
    else: pass  # no compression.

    if download_n_extract and not linux: return find_move_delete_windows(downloaded, exe_name or tool_name, delete)
    elif download_n_extract and linux: return find_move_delete_linux(downloaded, exe_name or tool_name, delete)

    # console.rule(f"Completed Installation")
    # return res


def get_shell_script_executing_pyscript(python_file, func=None, system=None, ve_name="ve"):
    if func is None: exec_line = f"""python {python_file}"""
    else: exec_line = f"""python -m fire {python_file} {func}"""
    return f"""
. ~/scripts/activate_ve {ve_name}
{exec_line}
deactivate
"""


def write_shell_script(program, desc="", preserve_cwd=True, display=True, execute=False):
    if preserve_cwd:
        if platform.system() == "Windows":
            program = "$orig_path = $pwd\n" + program + "\ncd $orig_path"
        else:
            program = 'orig_path=$(cd -- "." && pwd)\n' + program + '\ncd "$orig_path" || exit'
    if display:
        print(f"Executing {PROGRAM_PATH}")
        print_programming_script(program=program, lexer="shell", desc=desc)
    if platform.system() == 'Windows': PROGRAM_PATH.create(parents_only=True).write_text(program)
    else: PROGRAM_PATH.create(parents_only=True).write_text(f"{program}")

    if execute: Terminal().run(f". {PROGRAM_PATH}", shell="powershell").print_if_unsuccessful(desc="Executing shell script", strict_err=True, strict_returncode=True)
    return None


def print_programming_script(program: str, lexer: str, desc=""):
    if lexer == "shell":
        if platform.system() == "Windows": lexer = "powershell"
        elif platform.system() == "Linux": lexer = "sh"
        else: raise NotImplementedError(f"lexer {lexer} not implemented for system {platform.system()}")
    console = Console()
    console.print(Panel(Syntax(program, lexer=lexer), title=desc), style="bold red")


def get_latest_version(url):
    # not yet used, consider, using it.
    import requests
    import json
    url = f"https://api.github.com/repos/{url.split('github.com/')[1]}/releases/latest"
    # Replace {owner} and {repo} with the actual owner and repository name
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        latest_version = data["tag_name"]
        print("Latest release version:", latest_version)
    else: print("Error:", response.status_code)


def check_tool_exists(tool_name):
    if platform.system() == "Windows": tool_name = tool_name + ".exe"
    if platform.system() == "Windows": cmd = "where.exe"
    elif platform.system() == "Linux": cmd = "which"
    else: raise NotImplementedError(f"platform {platform.system()} not implemented")
    import subprocess
    try:
        subprocess.check_output([cmd, tool_name])
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_current_ve():
    import sys
    path = P(sys.executable)  # something like ~\\venvs\\ve\\Scripts\\python.exe'
    if P.home().joinpath("ve") in path:
        return path.parent.parent.stem
    else:
        raise NotImplementedError("Not a kind of virtual enviroment that I expected.")
        # return path.parent.parent.stem


def choose_ssh_host(multi=True):
    from paramiko import SSHConfig
    c = SSHConfig()
    c.parse(open(P.home().joinpath(".ssh/config").str))
    choices = list(c.get_hostnames())
    hosts = display_options(msg="", options=choices, multi=multi, fzf=True)
    return hosts


if __name__ == '__main__':
    # import typer
    # typer.run(check_tool_exists)
    pass
