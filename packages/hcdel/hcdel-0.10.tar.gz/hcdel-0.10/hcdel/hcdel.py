import os.path
import subprocess
import sys

from getfilenuitkapython import get_filepath
from escape_windows_filepath import escape_windows_path
from list_all_files_recursively import get_folder_file_complete_path
import re
from hackyargparser import add_sysargv

startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE
creationflags = subprocess.CREATE_NO_WINDOW
invisibledict = {
    "startupinfo": startupinfo,
    "creationflags": creationflags,
    "start_new_session": True,
}
movefilepath = get_filepath("movefile.exe")
pendmovesexe = get_filepath("pendmoves.exe")
hcdelcmd = get_filepath("hcdel.cmd")


def get_scheduled_files():
    try:
        proc = subprocess.run(
            [
                pendmovesexe,
                "-accepteula",
            ],
            capture_output=True,
            **invisibledict,
        )
        deletednextstartup = [
            x.decode("utf-8", "ignore").strip().splitlines()[0][8:]
            for x in set(
                re.findall(rb"[\n\r]+Source:[^\n]+[\n\r]+Target: DELETE", proc.stdout)
            )
        ]
    except Exception:
        deletednextstartup = []
    return deletednextstartup


def delfile(filepath):
    escapedpath = escape_windows_path(filepath)
    _ = subprocess.run(f'"{hcdelcmd}" {escapedpath}', **invisibledict)

    if os.path.exists(filepath):
        subprocess.run(f'"{movefilepath}" -accepteula "{filepath}" ""', **invisibledict)


@add_sysargv
def delallfiles(
    path: str | None = None, dryrun: int | bool = 1, print_files: int | bool = 1
):
    r"""
    Recursively deletes files and directories.

    Args:
        path (str | None, optional): The path to the directory or file to be deleted. If None or '', the script exits with code 1. Defaults to None.
        dryrun (int | bool, optional): If set to 1 or True, performs a dry run and only prints the files that would be deleted without actually deleting them. If set to 0 or False, deletes the files and directories. Defaults to 1.
        print_files (int | bool, optional): If set to 1 or True, prints the files and directories being deleted. Defaults to 1.

    Returns:
        None

    Raises:
        None

    """
    if not path:
        sys.exit(1)
    path = path.strip('" ')
    path = os.path.normpath(path)
    if os.path.exists(path):
        if os.path.isdir(path):
            allfiles = [x.path for x in get_folder_file_complete_path(path)]
        else:
            allfiles = [path]

        for filepath in allfiles:
            if dryrun:
                print(f"Would delete: {filepath}")
            else:
                if print_files:
                    print(f"Deleting: {filepath}")

                delfile(filepath)
        if print_files:
            deletednextstartup = get_scheduled_files()
            if deletednextstartup:
                print("The following files will be deleted the next reboot: ")
                for file in deletednextstartup:
                    print(file)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        delallfiles()
