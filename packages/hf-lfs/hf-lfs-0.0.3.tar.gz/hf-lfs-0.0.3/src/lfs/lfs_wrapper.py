import sys
import subprocess
import lfs

def main():
    arguments = sys.argv[1:]
    path_to_git_lfs = "/".join(lfs.__file__.split("/")[:-1]) + "/git-lfs"

    subprocess.run([path_to_git_lfs, *arguments])
