import contextlib
from typing import List
from pathlib import Path

from config import OPENAI_API_KEY_NAME
from gitease.summrizer import Summarizer
import git
import os
import openai.error


class GitHelper:

    def __init__(self, path: str = '.', verbose: bool = True):
        self.repo = git.Repo(path)
        self.verbose = verbose
        if not Path(path).joinpath('.git').exists():
            raise ValueError(f"Path {path} is not a git repo")
        if not Path(path).joinpath('.gitignore').exists():
            raise ValueError(f"Path {path} does not have a .gitignore file")

    def get_status(self):
        return self.repo.git.status(porcelain=True)

    def get_diff(self, staged: bool = False):
        if staged:
            staged = '--staged'
        return self.repo.git.diff(staged)

    def push(self):
        return self.repo.git.push()

    def pull(self):
        return self.repo.git.pull()

    def _get_changes(self):
        files = []
        status = self.get_status()
        for line in status.split('\n'):
            if line.startswith('??') or line.strip().startswith('M'):
                files.append(line[3:])

        return files

    def add_commit(self, files: List[str] = None, message: str = None):
        if not files:
            new_files, changed_files = self._get_changes()
            files = new_files + changed_files
        if not files:
            print("No changes found")
            return False

        if message is None:
            message = self.summarize_diff(staged=True)
            message = message + f"\n{self._join_files(files)}"
        if self.verbose:
            print(f"Adding files to git: {files}")
        self.repo.index.add(files)
        if self.verbose:
            print(message)
        self.repo.index.commit(message)
        return True

    def summarize_diff(self, staged: bool = False):
        if os.getenv("OPENAI_API_KEY") is None:
            raise RuntimeError(
                f"{OPENAI_API_KEY_NAME} not set - please set it in your environment variables or provide a commit message manually.")
        with contextlib.suppress(openai.error.InvalidRequestError):
            return Summarizer(verbose=self.verbose).summarize(self.get_diff(staged=staged))
        return "Diff too long to summarize."

    def undo(self):
        """https://github.blog/2015-06-08-how-to-undo-almost-anything-with-git/"""
        pass
