
import crocodile.toolbox as tb
from machineconfig.utils.utils import display_options


descriptive_themes = ["cupcake", "doubletime", "zork", "slick", "powerline-multiline", "font"]


def main(new_theme=None):
    profile = tb.P.home().joinpath(".bashrc")
    current_theme = tb.L(profile.read_text().splitlines()).filter(lambda x: "OSH_THEME=" in x)[0].split("=")[1]
    themes = tb.P.home().joinpath(".oh-my-bash/themes").search("*", not_in=["THEMES.md"]).apply(lambda x: x.trunk)
    themes.list.sort()
    if new_theme is None:
        tail = "Recomm: "
        new_theme = display_options(msg=f"Choose a theme number from the list above: ", options=list(themes) + ["slick", "surprise me"], default="surprise me", tail=tail,
                                    prompt=f"Recommended descriptive ones are {descriptive_themes}")
    if new_theme == "surprise me": new_theme = themes.sample()[0]
    print("Current Theme:", current_theme)
    print("New theme: ", f'"{new_theme}"')  #
    profile.modify_text(txt_search=current_theme, txt_alt=f'"{new_theme}"', replace_line=False)


if __name__ == '__main__':
    pass
