import typer
from typing import List
from rich.style import Style
from rich.console import Console
from rich.prompt import Prompt
from typing_extensions import Annotated
from gitease import GitHelper
from gitease.summrizer import Summarizer
from config import OPENAI_API_KEY_NAME, OPENAI_API_KEY

cli = typer.Typer(add_completion=False)

console = Console()
console.print("Welcome to GitEase", style=Style(color="green", blink=True, bold=True))

add_annotation = Annotated[List[str], typer.Option("--add", "-a", help="Files to add. All of not provided")]
message_annotation = Annotated[str, typer.Option("--message", "-m",
                                                 help=f"commit message - If not provided, Generate by AI (given {OPENAI_API_KEY_NAME} is set)")]
quiet_annotation = Annotated[
    bool, typer.Option("--quiet", "-q", help="If True - Quiet the the LLM thoughts and other messages")]
y_annotation = Annotated[bool, typer.Option("--yes", "-y", help="If True - Skips confirmation message")]


def _join_files(files):
    return '\n'.join(files)


def get_user_message(diff):
    if not diff:
        return None
    console.print("\nHere is the diff:\n", style=Style(color="red", blink=True, bold=True))
    diffs = diff.split("diff --git")
    for change in diffs:
        console.print("diff --git" + change, style=Style())
    console.print("Provide a commit message", style=Style(color="yellow"))
    console.print("Press CTRL+C to cancel", style=Style(color="red"))
    return Prompt.ask("Message")


def confirm_message(message):
    console.print(f"\nYour commit message is:\n{message}\n")
    console.print("To confirm, press Enter.", style=Style(color="green"))
    console.print("Otherwise, write your own message:", style=Style(color="yellow"))
    console.print("Press CTRL+C to cancel", style=Style(color="red"))
    return Prompt.ask("Response")


@cli.command()
def save(add: add_annotation = None,
         message: message_annotation = None,
         quiet: quiet_annotation = False,
         y: y_annotation = False):
    """
    Add and commit files to git.
    """
    helper = GitHelper(verbose=not quiet)
    if not add:
        add = helper._get_changes()
    if add:
        helper.repo.index.add(add)
    else:
        console.print("No changes files to add", style=Style(color="red", blink=True, bold=True))

    if message is None:
        diff = helper.get_diff(staged=True)
        if not diff:
            console.print("No message provided, skipping commit", style=Style(color="red", blink=True, bold=True))
            return
        response = None
        if OPENAI_API_KEY:
            message = Summarizer(verbose=not quiet).summarize(diff).lstrip()
            message = message + f"\n{_join_files(add)}"
            if not y:
                response = confirm_message(message)
            if response and len(response) > 0:  # new user commit message
                message = response
        else:
            message = get_user_message(diff)

    if message:
        helper.repo.index.commit(message)
        console.print(f"Committed with message: {message}")
    else:
        console.print("No message provided, skipping commit", style=Style(color="red", blink=True, bold=True))


@cli.command()
def share(add: add_annotation = None,
          message: message_annotation = None,
          quiet: quiet_annotation = False,
          y: y_annotation = False):
    """Share to remote: add, commit and push to git"""
    save(add=add, message=message, quiet=quiet, y=y)
    GitHelper().push()


@cli.command()
def load():
    """Pull recent updates from git"""
    GitHelper().pull()


@cli.command()
def message(quiet: quiet_annotation = False,
            copy: Annotated[bool, typer.Option("--copy", "-c", help="Copy to clipboard")] = False):
    """Generate commit message from diff using AI"""
    if not OPENAI_API_KEY:
        console.print(f"{OPENAI_API_KEY_NAME} not set", style=Style(color="red", blink=True, bold=True))
        return False
    diff = GitHelper(verbose=not quiet).get_diff(staged=True)
    message = Summarizer(verbose=not quiet).summarize(diff).lstrip()
    console.print("Commit message:\n", style=Style(color="red", blink=True, bold=True))
    console.print(message)
    if copy:
        try:
            import clipboard
            console.print("Copied to clipboard", style=Style(color="green"))
            clipboard.copy(message)
        except ImportError:
            console.print("Install clipboard to copy to clipboard: 'pip install clipboard'",
                          style=Style(color="red", blink=True, bold=True))
