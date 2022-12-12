import logging
from urllib.parse import urlparse

from collections import defaultdict
import os.path

from gitmultirepoupdater.data_types import CliArguments, RepoState
from gitmultirepoupdater.constants import CloningStates
from gitmultirepoupdater.utils.helpers import remove_suffix

logger = logging.getLogger()


def is_url_or_git(file_names_or_repo_url: str) -> bool:
    # TODO: use urlparse to verify if its url and use regexp for git url
    return ".com" in file_names_or_repo_url.lower()


def read_repositories_from_file(repos_filename) -> list[str]:
    """Reads a list of repositories from a file while ignoring commented out lines."""
    with open(repos_filename) as f:
        return [l.strip() for l in f.readlines() if not l.strip().startswith("#")]
    

access_token_var_names = {
    "gitlab.com": "GITLAB_ACCESS_TOKEN",
    "github.com": "GITHUB_OAUTH_TOKEN",
    "DEFAULT": "GIT_TOKEN",
}

def standardize_git_repo_url(url: str) -> str:
    """Converts repository url to url which is suitable for cloning"""
    parsed_url = urlparse(url)
    # https://gitlab.com/-/profile/personal_access_tokens
    # GITLAB_ACCESS_TOKEN
    # GITHUB_OAUTH_TOKEN
    # GIT_TOKEN

    domain = parsed_url.netloc.split("@")[-1].lower()
    access_token_var_name = access_token_var_names.get(domain, access_token_var_names["DEFAULT"])

    # TODO: add github.com support
    if access_token := os.getenv(access_token_var_name, ""):
        domain_with_access_token = f"api:{access_token}@{parsed_url.netloc.split('@')[-1]}"
        parsed_url = parsed_url._replace(netloc=domain_with_access_token, scheme="https")

    return parsed_url.geturl()


def get_repo_name(url: str) -> str:
    return remove_suffix(url.split("/")[-1], ".git")


def get_repository_states(args: CliArguments) -> dict[str, RepoState]:
    repo_urls = []
    for file_names_or_repo_url in args.repos:
        if not is_url_or_git(file_names_or_repo_url) and os.path.exists(file_names_or_repo_url):
            newly_read_repos = read_repositories_from_file(file_names_or_repo_url)
            repo_urls.extend(newly_read_repos)
        else:
            repo_urls.append(file_names_or_repo_url)

    repo_states = {}
    for repo_url in repo_urls:
        standardized_repo_url = standardize_git_repo_url(repo_url)
        repo_name = get_repo_name(repo_url)
        repo_states[repo_name] = RepoState(
            args=args,
            repo_name=repo_name,
            repo_url=standardized_repo_url
        )

    return repo_states
