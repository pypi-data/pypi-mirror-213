import contextlib
from typing import List
from pathlib import Path
from tempfile import NamedTemporaryFile
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import TextLoader
from langchain.llms import OpenAI
import git
import os
import openai.error


class GitLLM:

    def __init__(self, path: str = '.', verbose: bool = True):
        self.repo = git.Repo(path)
        self.verbose = verbose
        self.summarizer = load_summarize_chain(llm=OpenAI(temperature=0),
                                               chain_type="stuff",
                                               verbose=verbose)

    def get_status(self):
        return self.repo.git.status(porcelain=True)

    def get_diff(self, ):
        return self.repo.git.diff()

    def push(self):
        return self.repo.git.push()

    def pull(self):
        return self.repo.git.pull()

    def _get_changes(self):
        new_files, changed_files = [], []
        status = self.get_status()
        for line in status.split('\n'):
            if line.startswith('??'):
                new_files.append(line[3:])
            elif line.startswith(' M'):
                changed_files.append(line[3:])
        return new_files, changed_files

    @staticmethod
    def _join_files(files):
        return '\n'.join(files)

    def add_commit(self, files: List[str], message: str):
        self.repo.index.add(files)
        message = message + f"\n{self._join_files(files)}"
        if self.verbose:
            print(message)
        self.repo.index.commit(message)
        return True

    def summarize_diff(self):
        tmp = NamedTemporaryFile()
        Path(tmp.name).write_text(self.get_diff())
        with contextlib.suppress(openai.error.InvalidRequestError):
            return self.summarizer.run(TextLoader(tmp.name).load())
        return "Diff too long to summarize."

    def summarize_commits(self):
        tmp = NamedTemporaryFile()
        for commit in self.repo.iter_commits():
            tmp.write(commit.message.encode())

        with contextlib.suppress(openai.error.InvalidRequestError):
            return self.summarizer.run(TextLoader(tmp.name).load())
        return "Commits messages are too long to summarize."

    def auto_add_commit(self):
        new_files, changed_files = self._get_changes()
        if not new_files and self.verbose:
            print("No new files to commit.")
        else:
            self.add_commit(new_files, f"Automated commit - {len(new_files)} files:")
        if not changed_files and self.verbose:
            print("No changed files to commit.")
        else:
            changes_message = self.summarize_diff()
            self.add_commit(changed_files, f"Automated commit - {len(changed_files)} files:\n{changes_message}")

    def undo(self):
        """https://github.blog/2015-06-08-how-to-undo-almost-anything-with-git/"""
        pass

    @staticmethod
    def has_git():
        return os.path.exists('.git')

    @staticmethod
    def has_gitignore():
        return os.path.exists('.gitignore')
