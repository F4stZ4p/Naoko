# Naoko Updater By F4stZ4p (c) 2018
from utils.naoko_shell import shell


def _update(gitdir):
    return shell(
        f"cd {gitdir} && git reset -q --hard HEAD && git clean -f -x -d -q && git pull"
    )
