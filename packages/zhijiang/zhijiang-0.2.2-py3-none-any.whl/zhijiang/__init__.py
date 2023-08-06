import os
from termcolor import cprint
import fire
import zhijiang as pkg


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
                os.system("sudo bash -c 'echo source ~/.alias >> ~/.bashrc' ")


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
    script_path = os.path.join(pkg_installed_path, "scripts/enhance_python.sh")
    os.system(f"bash {script_path}")


def info():
    """
    print help info;
    to enable tab completion >> zhijiang -- --completion > ~/.zhijiang; echo source  ~/.zhijiang >> ~/.bashrc; source ~/.bashrc
    """
    cprint("1. if you want tab completion, please 'zhijiang -- --completion > ~/.zhijiang; echo source  ~/.zhijiang >> ~/.bashrc; source ~/.bashrc'", "red")
    cprint("2. zhijiang subcommand-xx --help to see how to control subcommand", "red")
    cprint(f"3. you can modify the file before executing them, they are put at {pkg_installed_path}", "red")


def main():
    fire.Fire(
        {
            "setup_rc_files": setup_rc_files,
            "install_useful_tools": install_useful_tools,
            "enhance_python": enhance_python,
            "info": info,
        }
    )


if __name__ == "__main__":
    main()
