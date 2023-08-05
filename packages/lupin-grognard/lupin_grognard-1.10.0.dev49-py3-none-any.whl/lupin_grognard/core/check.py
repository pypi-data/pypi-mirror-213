import sys
from typing import List

from lupin_grognard.core.commit.commit import Commit
from lupin_grognard.core.commit.commit_error import ErrorCount
from lupin_grognard.core.commit.commit_validator import CommitValidator


def check_max_allowed_major_commits(
    commits: List[Commit], major_commit_limit: int
) -> bool:
    """Check if the number of major commits in `commits` exceeds `major_commit_limit`.

    Args:
        commits (List[Commit]): The list of commit object.
        major_commit_limit (int): The maximum number of major commits allowed.

    Returns:
        bool: True if the number of major commits is within the limit, else False.
    """
    if major_commit_limit == 0:  # --all option
        return True

    major_commit_count = 0
    for commit in commits:
        if commit._is_major_commit():
            major_commit_count += 1

    if major_commit_count > major_commit_limit:
        print(
            f"Error: found {major_commit_count} major commits to check in the "
            f"current branch while the maximum allowed number is {major_commit_limit}"
        )
        sys.exit(1)
    return True


def check_commit(
    commits: List[Commit],
    merge_option: int,
    permissive_mode: bool = False,
    is_ci_mr_target_branch_main: bool = False,
) -> None:
    """
    check_commit performs validation checks on each commit.
    If merge_option is set to 0, the function checks that merge commits
    have approvers.
    If merge_option is 1, the function only validates the title for a merge,
    the title and the body of the commit if it is a simple commit.
    The function also calls the error_report method of the ErrorCount
    class to output any errors found during validation.
    If any errors are found, it will call sys.exit(1)
    Args:
        commits (List): List of commits to check
        merge_option (int): 0 or 1
    """
    error_counter = ErrorCount()
    commits = [
        CommitValidator(
            commit=c,
            error_counter=error_counter,
            is_ci_mr_target_branch_main=is_ci_mr_target_branch_main,
        )
        for c in commits
    ]

    for commit in commits:
        commit.perform_checks(merge_option)
    error_counter.error_report(permissive_mode=permissive_mode)
