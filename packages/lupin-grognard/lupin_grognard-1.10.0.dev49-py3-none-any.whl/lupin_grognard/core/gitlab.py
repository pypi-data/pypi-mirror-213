import os

from lupin_grognard.core.tools.utils import die, info, warn


def is_ci_mr_target_branch_main() -> bool:
    target_branch = os.getenv("CI_MERGE_REQUEST_TARGET_BRANCH_NAME")
    if target_branch == "main":
        info(msg="The merge result pipeline target branch is 'main'")
        return True
    else:
        warn(msg="The merge result pipeline target branch is not 'main'")
        return False


def is_gitlab_ci() -> bool:
    return os.getenv("GITLAB_CI") == "true"


def is_gitlab_shallow_clone_disabled() -> bool:
    return os.getenv("GIT_DEPTH") == "0"


def assert_gitlab_shallow_clone_defined() -> None:
    """Check if GIT_DEPTH is defined to 0 in GitLab CI"""
    if is_gitlab_ci() and not is_gitlab_shallow_clone_disabled():
        die(msg="GitLab shallow clone detected, please define GIT_DEPTH to 0")
