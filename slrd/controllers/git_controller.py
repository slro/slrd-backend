"""
GitContoller module
:developer vsmysle
:type human
"""
import logging
from git import Repo
from slrd.strings import comlogstr
from slrd.strings import gitlogstr
class GitController(object):
    """
    Controller that operates with git
    """
    def __init__(self, path, init=False):
        """
        Initialization method.

        :param init: checks for existing git repo
        :type init: bool

        :param path: path for git repo
        :type path: str
        """
        self.logger = logging.getLogger(__name__)
        self.logger.debug(comlogstr.LOG_INIT_START)
        self.init = init
        self.remote_url = None
        if self.init:
            self.logger.info(gitlogstr.LOGSTR_SET_REPO % path)
            self.repo = Repo(path)
            self.logger.debug(gitlogstr.LOGSTR_SET_REPO_SUCCESSFUL % path)
        else:
            self.logger.info(gitlogstr.LOGSTR_INIT_BARE_REPO_STARTED % path)
            self.repo = Repo.init(path, 'bare-repo', bare=True)
            self.logger.debug(gitlogstr.LOGSTR_INIT_BARE_REPO_ENDED % path)          
        self.logger.debug(comlogstr.LOG_INIT_END)

    def commit(self, commit_message):
        """
        Git commit method.

        :param commit_message: commit message
        :type  commit_message: str
        """
        # git add started( TODO: logging )
        self.repo.index.add(self.repo.untracked_files)
        # git add ended ( TODO: logging)
        # git commit started ( TODO: logging)
        self.repo.commit(commit_message)
        # git commit ended (TODO: logging)

    def set_remote(self, url):
        """
        Set remote to git remote repository.

        :param url: url to a remote repository
        :type url:  str
        """
        self.remote_url = url
        # git remote add origin 'url' (TODO: logging)
        self.repo.create_remote('origin', url)
        # git remote adding was successful (TODO: logging)

    def pull(self):
        """
        Pull from git remote repository.
        """
        pass

    def rollback(self):
        """
        Rollbase to a previous commit.
        """
        pass
