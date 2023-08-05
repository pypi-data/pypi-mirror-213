import logging
import os
import re
import sys
from typing import List

from lupin_grognard.core.commit.commit import Commit
from lupin_grognard.core.config import COMMIT_DELIMITER, INITIAL_COMMIT
from lupin_grognard.core.git import Git


def read_file(file: str) -> str:
    with open(f"{file}", "r", encoding="utf-8") as file:
        data = file.read()
        return data


def write_file(file: str, content: str):
    with open(f"{file}", "w", encoding="utf-8") as outfile:
        outfile.write(content)


def get_version():
    """get version from setup.cfg file and
    update __version__ in lupin_grognard.__init__.py
    """
    setup_cfg = read_file("setup.cfg")
    _version = re.search(
        r"(^version = )(\d{1,2}\.\d{1,2}\.\d{1,2})(\.[a-z]{1,})?(\d{1,2})?",
        setup_cfg,
        re.MULTILINE,
    )
    version = ""
    for group in _version.group(2, 3, 4):
        if group is not None:
            version = version + str(group)
    content = f'__version__ = "{version}"\n'
    write_file(file="lupin_grognard/__init__.py", content=content)
    return version


def get_current_branch_name() -> str:
    branch_name = Git().get_branch_name()
    # branch name can be messing if running in CI
    if not branch_name:
        branch_name = os.getenv("CI_COMMIT_BRANCH")
    if not branch_name:
        branch_name = os.getenv("CI_MERGE_REQUEST_SOURCE_BRANCH_NAME")
    if not branch_name:
        return ""
    return branch_name


def is_ci_mr_target_branch_main() -> bool:
    return os.getenv("CI_MERGE_REQUEST_TARGET_BRANCH_NAME") == 'main'


def display_supported_commit_types() -> None:
    commit_type = [
        "build(add|change|remove)",
        "bump",
        "ci",
        "deps(add|change|remove)",
        "docs",
        "enabler",
        "feat(add|change|remove)",
        "fix",
        "refactor",
        "test",
    ]
    print("Supported commit types: " + ", ".join(commit_type))
    print(
        'Only one major commit types allowed per branch: "enabler", "feat", "fix" or "refactor".'
    )


def display_number_of_commits_to_check(commit_list: List):
    number_commits_to_check = len(commit_list)
    if number_commits_to_check == 0:
        print("0 commit to check")
        sys.exit(0)
    elif number_commits_to_check == 1:
        print(f"Found {number_commits_to_check} commit to check:")
    else:
        print(f"Found {number_commits_to_check} commits to check:")


def generate_commit_list_obj(commit_string: str) -> List[Commit]:
    """Geneartes the list of commits from Git().get_log().stdout value"""
    return [Commit(commit) for commit in commit_string.split(COMMIT_DELIMITER) if len(commit) > 0]


def generate_commits_range_to_check(
    branch_list: List,
    commits: List[Commit],
    first_commit_merge_to_main: bool = False,
    initial_commits: List[str] = INITIAL_COMMIT,
) -> List:
    """generates a list of message ranges starting with INITIAL_COMMIT
    or the last merge into a branch contained in the branch list.
    if first_commit_merge_to_main is True, returns the list of commits
    until the second merge commit
    """

    merge_count = 0

    for i, commit in enumerate(commits):
        if first_commit_merge_to_main:
            if commit.title.startswith("Merge branch"):
                merge_count += 1
                if merge_count == 2:
                    return commits[:i]
        else:
            if commit.title.startswith("Merge branch"):
                for branch in branch_list:
                    if commit.title.endswith(f"into '{branch}'"):
                        return commits[:i]
            elif commit.title in initial_commits:
                return commits[:i]
    return list()


def is_first_commit_merge_to_main_branch(commits: List[Commit]) -> bool:
    """Checks if the first commit in the list is a merge to main branch"""
    if len(commits) == 0:
        return False
    return commits[0].title.startswith("Merge branch") and commits[0].title.endswith("into 'main'")



def die(msg: str) -> None:
    logging.error(msg)
    sys.exit(1)


def warn(msg: str) -> None:
    logging.warning(msg)


def info(msg: str) -> None:
    logging.info(msg)


def check_if_file_exists(file: str) -> bool:
    file_path = os.path.join(os.getcwd(), file)
    return os.path.isfile(file_path)


def configure_logging():
    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s", level=logging.INFO
    )


def is_main_branch(branch_name: str, main_branch_list: List) -> bool:
    return branch_name in main_branch_list
