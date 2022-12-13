from dataclasses import dataclass
from gitmultirepoupdater.constants import CloningStates, PullRequestStates, ModificationState


@dataclass
class CliArguments:
    repos: list[str]
    clone_to: str
    commands: list[str]
    commit_message: str
    verbose: bool


@dataclass
class RepoState:
    args: CliArguments  # Parsed command line arguments 

    source_branch: str = ""  # Branch name from which a new branch for changes will be created
    branch: str = ""  # Branch name in which changes will be made and commited
    target_branch: str = ""  # Base branch into which PR changes will be pulled into

    cloning_state: str = CloningStates.NOT_STARTED.value
    modification_state: str = ModificationState.NOT_STARTED.value
    pull_request_state: str = PullRequestStates.NOT_CREATED.value

    name: str = ""  # Short human readable repo identifier
    owner: str = ""  # Owner of this repo
    url: str = ""  # Url used to clone the repository
    domain: str = ""  # Domain where the remote repository is hosted at (parsed from url)
    pull_request_url: str = ""  # Link to created pull request
    directory: str = ""  # Repository path in the file system

    stdout: str = ""  # Standard output from command execution
    stderr: str = ""  # Standard error output from command execution


@dataclass
class HttpRequestParams:
    url: str
    headers: dict[str, str]
    data: dict[str, str]
