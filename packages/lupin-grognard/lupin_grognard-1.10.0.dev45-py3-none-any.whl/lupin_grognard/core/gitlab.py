import os

from lupin_grognard.core.tools.utils import die


def is_gitlab_ci() -> bool:
    return os.getenv("GITLAB_CI") == "true"


def is_gitlab_shallow_clone_disabled() -> bool:
    return os.getenv("GIT_DEPTH") == "0"


def assert_gitlab_shallow_clone_defined() -> None:
    """Check if GIT_DEPTH is defined to 0 in GitLab CI"""
    if is_gitlab_ci() and not is_gitlab_shallow_clone_disabled():
        die(msg="GitLab shallow clone detected, please define GIT_DEPTH to 0")
