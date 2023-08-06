import contextlib
import sys
from typing_extensions import Annotated
import typer
from gitllm import GitLLM, ServiceEnum
import os
import subprocess
import time
from collections import namedtuple

backgroundcli = typer.Typer(add_completion=False)
cli = typer.Typer(add_completion=False)

Process = namedtuple('Process', ['pid', 'service', 'interval', 'path'])


def run(key: str, interval: float, path: str = '.'):
    gitllm = GitLLM(path=path)
    while interval > 0:
        try:
            print(f"{key} every {interval} minute")
            if key == ServiceEnum.COMMIT:
                gitllm.auto_add_commit()
            elif key == ServiceEnum.PUSH:
                gitllm.push()
            else:
                raise ValueError(f"Invalid key: {key}")
            time.sleep(interval * 60)
        except KeyboardInterrupt:
            break


@backgroundcli.command()
def bstart(service: ServiceEnum = typer.Argument(help="Which automation to run"),
           interval: float = typer.Argument(help="The interval in minutes"),
           path: str = typer.Argument(help="The repository local path")):
    print(f"Starting auto-git for {service} every {interval} minutes on repo at {path}")
    run(service, interval, path)
    print('Stopped....')


@cli.command()
def share(message: Annotated[str, typer.Option("--message", "-m",
                                               help="commit message - default will be a summarization of the git diff by LLM")] = None):
    """Share to remote: add, commit and push to git"""
    # TODO add: Annotated[List[str], typer.Option("--add", "-a", help="files to add - default is '.'")] = [],
    commit(message)
    GitLLM().push()


@cli.command()
def save(message: Annotated[str, typer.Option("--message", "-m",
                                              help="commit message - default will be a summarization of the git diff by LLM")] = None):
    """
    Automatically add and commit files to git.
    """
    # TODO add: Annotated[List[str], typer.Option("--add", "-a", help="files to add - default is '.'")] = [],
    gitllm = GitLLM()
    new_files, changed_files = gitllm._get_changes()
    add = new_files + changed_files
    if message is None:
        message = gitllm.summarize_diff()
        message = f"Automated commit - {len(add)} files:\n{message}"
    gitllm.add_commit(add, message)

@cli.command()
def commit(message: Annotated[str, typer.Option("--message", "-m",
                                                help="commit message - default will be a summarization of the git diff by LLM")] = None):
    """
    Automatically commit files to git and generate a commit message if not provided.
    """
    gitllm = GitLLM()
    if message is None:
        message = gitllm.summarize_diff()
        message = f"Automated commit: \n{message}"
    gitllm.repo.index.commit(message)

# Automations
@cli.command()
def auto(service: ServiceEnum = typer.Argument(help="Which automation to run"),
         interval: float = typer.Argument(help="The interval in minutes"),
         detach: bool = typer.Option(False, '--detach', help="Detach and run in the background")):
    """Automatically add and commit files to git at an interval"""
    path = os.getcwd()  # TODO as an argument
    if not GitLLM.has_git():  # TODO adjust to path
        raise RuntimeError("Not a git repository")
    elif not GitLLM.has_gitignore():  # TODO adjust to path
        raise RuntimeError("No .gitignore file found")
    stdout = subprocess.PIPE if detach else None
    kill([process.pid for process in _list(service)])

    if not detach:
        print(f"Press Ctrl+C to stop...\n")
    process = subprocess.Popen(["bgitllm", service, str(interval), path], stdout=stdout)
    if detach:
        print(f"Running auto {service} every {interval} in the background")
        sys.exit()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        process.terminate()
        process.wait()


def _list(service: str = ''):
    command = ' | '.join(["ps aux", f"grep 'bgitllm {service}'"])
    output = subprocess.check_output(command, shell=True).decode("utf-8").strip().split('\n')
    processes = []
    for row in output:
        row = row.split(' ')
        if len(row) > 2 and 'grep' not in row:
            processes.append(Process(int(row[1]), row[-3], float(row[-2]), row[-1]))
    return processes


@cli.command()
def list(service: Annotated[str, typer.Argument(help="Which automation to list - default all")] = ''):
    """List all running automations"""
    processes = _list(service)
    for process in processes:
        print(f"Auto {process.service} every {process.interval} minutes on pid {process.pid}  in repo at {process.path}")
    return processes


def kill(pids):
    for pid in pids:
        with contextlib.suppress(ProcessLookupError):
            os.kill(int(pid), 15)  # Send SIGTERM signal
            print(f"Stopped auto {pid}...")


@cli.command()
def stop(service: ServiceEnum = typer.Argument(help="Which service to stop")):
    """Stop automation"""
    print(f"Stopping auto-git {service} - in {os.getcwd()}")
    processes = _list(service)
    if not processes:
        print("No processes found.")
    else:
        print(f"Stopping processes for {service}...")
        kill([process.pid for process in processes])
