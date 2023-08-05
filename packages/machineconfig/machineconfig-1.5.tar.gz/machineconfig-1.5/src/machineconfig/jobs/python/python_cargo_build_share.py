
import crocodile.toolbox as tb
import platform


def build_rust_executable(url=r"https://github.com/atanunq/viu"):
    tool_name = url.split('/')[-1]

    # move command is not required since tool will go to .cargo/bin which is in PATH by default.
    # move_command = f"mv {exe} {tb.get_env().WindowsApps.as_posix()}/" if platform.platform() == "Windows" else f"sudo mv {exe} /usr/local/bin/"
    # {move_command}

    script = f"""
cd ~
git clone --depth 1 {url} 
cd {tool_name}
cargo install --path .
"""
    print(f"Executing {script}")
    if platform.system() == "Windows":
        tb.Terminal(stdout=None).run(f". {tb.P.tmpfile(suffix='.ps1').write_text(script)}", shell="pwsh").print()
    else:
        tb.Terminal(stdout=None).run(script, shell="pwsh")

    exe = tb.P.home().joinpath(f".cargo/bin/{tool_name}" + (".exe" if platform.system() == "Windows" else ""))

    try:
        tb.P.home().joinpath(tool_name).delete(sure=True)
    except PermissionError:
        print(f"PermissionError, couldn't delete: {tb.P.home().joinpath(tool_name)}")

    if platform.system() == "Windows":
        exe = exe.move(folder=tb.get_env().WindowsApps)
    elif platform.system() == "Linux":
        tb.Terminal().run(f"sudo mv {exe} /usr/local/bin")
        exe = tb.P(r"/usr/local/bin").joinpath(exe.name)
    else:
        raise NotImplementedError(f"Platform {platform.system()} not supported.")
    share_link = exe.to_cloud("gdpo", share=True)
    return share_link


# after cargo install diskonaut
# then mv ~/.cargo/bin/diskonaut.exe ~/AppData/Local/Microsoft/WindowsApps/
# then bu_gdrive_sx.ps1 .\diskonaut.exe -sRz  # zipping is vital to avoid security layers and keep file metadata.
