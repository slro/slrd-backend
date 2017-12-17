"""
GitContoller module
:developer vsmysle
:type human
"""
import logging
from git import Repo
from git.exc import InvalidGitRepositoryError
from git.exc import RepositoryDirtyError
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
        self.origin = None
        if self.init:
            try:
                self.logger.info(gitlogstr.LOGSTR_SET_REPO_STARTED % path)
                self.repo = Repo(path)
                self.logger.debug(gitlogstr.LOGSTR_SET_REPO_SUCCESS % path)
            except InvalidGitRepositoryError:
                self.logger.error(gitlogstr.LOGSTR_SET_REPO_ERROR)
            self.logger.info(gitlogstr.LOGSTR_SET_REPO_ENDED)
        else:
            try:
                self.logger.info(gitlogstr.LOGSTR_INIT_STARTED % path)
                self.repo = Repo.init(path, 'bare-repo', bare=True)
                self.logger.debug(gitlogstr.LOGSTR_INIT_ENDED % path)
            except:
                self.logger.error(gitlogstr.LOGSTR_INIT_ERROR)
            self.logger.info(gitlogstr.LOGSTR_INIT_ENDED)
        self.logger.debug(comlogstr.LOG_INIT_END)

    def commit(self, commit_message):
        """
        Git commit method.

        :param commit_message: commit message
        :type  commit_message: str
        """
        # Do we need to add files here? Or this is done by manager?
        try:
            self.logger.info(gitlogstr.LOGSTR_COMMIT_STARTED)
            self.repo.commit(commit_message)
            self.logger.info(gitlogstr.LOGSTR_COMMIT_SUCCESS)
        except RepositoryDirtyError:
            self.logger.error(gitlogstr.LOGSTR_ADD_ERROR)

            '''
            if the repository is dirty we add all untracked files using git add command
            and execute commit once again
            '''
            self.__add()
            self.commit(commit_message)
        self.logger.info(gitlogstr.LOGSTR_ADD_ENDED)

    def set_remote(self, url):
        """
        Set remote to git remote repository.

        :param url: url to a remote repository
        :type url:  str
        """
        try:
            self.logger.info(gitlogstr.LOGSTR_SET_REMOTE_STARTED)
            self.origin = self.repo.create_remote('origin', url)
            self.logger.info(gitlogstr.LOGSTR_SET_REMOTE_SUCCESS)
        except:
            self.logger.error(gitlogstr.LOGSTR_SET_REMOTE_ERROR)
        self.logger.info(gitlogstr.LOGSTR_SET_REMOTE_ENDED)

    def pull(self):
        """
        Pull from git remote repository.
        """
        if self.origin:
            try:
                self.logger.info(gitlogstr.LOGSTR_PULL_STARTED)
                self.origin.pull()
                self.logger.info(gitlogstr.LOGSTR_PULL_SUCCESS)
            except:
                self.logger.error(gitlogstr.LOGSTR_PULL_ERROR)
            self.logger.info(gitlogstr.LOGSTR_PULL_ENDED)
        else:
            self.logger.error(gitlogstr.LOGSTR_REMOTE_NOT_SET)

    def push(self):
        """
        Push to git remote repository.
        """
        if self.origin:
            try:
                self.logger.info(gitlogstr.LOGSTR_PUSH_STARTED)
                self.origin.push()
                self.logger.info(gitlogstr.LOGSTR_PUSH_SUCCESS)
            except:
                self.logger.error(gitlogstr.LOGSTR_PUSH_ERROR)
            self.logger.info(gitlogstr.LOGSTR_PUSH_ENDED)
        else:
            self.logger.error(gitlogstr.LOGSTR_REMOTE_NOT_SET)

    def rollback(self):
        """
        Rollbase to a previous commit.
        """
        pass

    def __add(self, files=None):
        """
        Git add.

        :param files: list of paths of the files to add
        :type files: list
        """
        if not files:
            try:
                self.logger.info(gitlogstr.LOGSTR_ADD_STARTED)
                self.repo.index.add(self.repo.untracked_files)
                self.logger.info(gitlogstr.LOGSTR_ADD_SUCCESS)
            except:
                self.logger.error(gitlogstr.LOGSTR_ADD_ERROR)
            self.logger.info(gitlogstr.LOGSTR_ADD_ENDED)
        else:
            self.repo.index.add(files)
