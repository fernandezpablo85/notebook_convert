import pygit2
from pygit2 import GIT_STATUS_INDEX_NEW, GIT_STATUS_INDEX_MODIFIED


STAGED_STATUSES = {GIT_STATUS_INDEX_NEW, GIT_STATUS_INDEX_MODIFIED}


def is_staged(file):
    repo = pygit2.Repository(".")
    staged_files = [f for f, flag in repo.status().items() if flag in STAGED_STATUSES]
    return file in staged_files
