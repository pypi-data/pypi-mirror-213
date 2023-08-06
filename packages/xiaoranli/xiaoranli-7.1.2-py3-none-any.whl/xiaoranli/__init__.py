import os
from termcolor import cprint
import fire
import xiaoranli as pkg
import packaging.version
import subprocess


pkg_installed_path = pkg.__path__[0]


def setup_rc_files(dry_run=True, restore_rc=False):
    assert isinstance(
        dry_run, bool
    ), "dry_run should be a boolean, so its value can only by True or False"
    if dry_run:
        cprint(
            "you are in dry run mode, use '--dry_run=False' to disable dry run", "red"
        )

    rc_files_path = os.path.join(pkg_installed_path, "data/rc_files")
    for root, _, files in os.walk(rc_files_path):
        for f in files:
            rc_file = os.path.join(root, f)
            dst = f"~/.{f}"
            backup = f"{dst}.bk"
            # backup the file if backup file is not existed
            if not os.path.exists(os.path.expanduser(backup)):
                # when user is root, then the rc file is not existed
                if not os.path.exists(os.path.expanduser(dst)):
                    os.system(f"touch {dst}")
                os.system(f"cp {dst} {backup}")

            if restore_rc:
                cmd = f"cp {backup} {dst}"
            else:
                cmd = f"cp {rc_file} {dst}"
            print(cmd)
            if not dry_run:
                os.system(cmd)
                os.system("sudo bash -c 'echo source ~/.alias >> ~/.zshrc' ")


def setup_ls():
    current_ver = subprocess.check_output(["lsb_release", "-sr"]).decode().strip()
    target_ver = "20.10"
    current_ver = packaging.version.parse(current_ver)
    target_ver = packaging.version.parse(target_ver)
    if current_ver >= target_ver:
        print("Current version is larger or equal to 20.10, use exa instead of ls")
        os.system("sudo HOME=$HOME bash -c 'echo \"\\nalias ls=\\'exa --group-directories-first\\'\" >> ~/.alias'")
        os.system("sudo HOME=$HOME bash -c 'echo \"\\nalias ll=\\'exa -abghHliS\\'\" >> ~/.alias'")
        print("please run 'source ~/.zshrc' to enable the alias")
    else:
        print("Current version is smaller than 20.10, No need to use exa")
    


def install_zsh():
    zsh_path = os.path.join(pkg_installed_path, "scripts/install_zsh.sh")
    os.system(f"bash {zsh_path}")

def install_useful_tools():
    """
    install usefule shell commands and python pkg, e.g. profiling tools, debugging tools;
    """
    script_path = os.path.join(pkg_installed_path, "scripts/install_useful_tools.sh")
    os.system(f"bash {script_path}")

def enhance_python():
    """
    add useful functions to python site.py, so you can call them like built-in functions, they are prefixed with zhijxu
    """
    script_path = os.path.join(pkg_installed_path, "zhijiang/scripts/enhance_python.sh")
    os.system(f"bash {script_path}")


def info():
    """
    print help info;
    to enable tab completion >> zhijiang -- --completion > ~/.zhijiang; echo source  ~/.zhijiang >> ~/.bashrc; source ~/.bashrc
    """
    cprint("1. if you want tab completion, please 'xiaoranli -- --completion > ~/.xiaoranli; echo source  ~/.xiaoranli >> ~/.zshrc; source ~/.zshrc'", "red")
    cprint("2. xiaoranli subcommand-xx --help to see how to control subcommand", "red")
    cprint(f"3. you can modify the file before executing them, they are put at {pkg_installed_path}", "red")
    cprint(
        "4. you could also use 'xiaoranli zsh' to install zsh,then use 'xiaoranli tools' to install packages, then use 'xiaoranli rc' to setup rc files",
        "red",
    )


def main():
    fire.Fire(
        {
            "setup_rc_files": setup_rc_files,
            "install_useful_tools": install_useful_tools,
            "enhance_python": enhance_python,
            "info": info,
            "zsh": install_zsh,
            "setup_ls":setup_ls,
        }
    )


if __name__ == "__main__":
    main()
