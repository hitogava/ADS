import sys
import os
import subprocess as sp
from pathlib import Path


class DirContext:
    default_dir = None
    target_dir = None

    def __init__(self, default, target):
        self.default_dir = default
        self.target_dir = target

    def __enter__(self):
        os.chdir(self.target_dir)

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.default_dir)


class CommitsContext:
    head = None
    current = None

    def __init__(self, head, current):
        self.head = head
        self.current = current

    def __enter__(self):
        os.system(f'git reset --hard {self.current} > /dev/null')

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.system(f'git reset --hard {self.head} > /dev/null')


if __name__ == '__main__':
    repo_path = Path(sys.argv[1])
    start, finish = sys.argv[2], sys.argv[3]
    command = sys.argv[4]
    with DirContext(os.getcwd(), repo_path):
        commits = os.popen('git log -99 --pretty=format:"%H"').read().split('\n')[::-1]
        l, r = commits.index(start), commits.index(finish)
        head = commits[-1]
        while l <= r:
            pivot = (l + r) // 2
            with CommitsContext(head, commits[pivot]):
                child = sp.Popen(repo_path.joinpath(command))
                streamdata = child.communicate()[0]
                rc = child.returncode
                if rc == 0:
                    l = pivot + 1
                else:
                    r = pivot - 1
        print(f'First bad commit: {commits[l]}')
