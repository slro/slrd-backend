# -*- coding: utf-8 -*-
# vi: set ft=python sw=4 :
"""Write and read files from a file system.

This module provides an interface to read, write and modify files from/to a
file system as well as some FS-related checks (existance, access etc).

Todo:
    - implement check_mode() and match_mode_subtree()
    - add delete_link() method
    - consider moving OS compatibility check to a separate module
"""
from datetime import datetime
import logging
from importlib import import_module
from os import makedirs, remove, fdopen, O_CREAT, lstat, utime, supports_fd
from os import open as osopen
from os.path import isdir, isfile, islink, exists
from slrd import type_checker as tc
from slrd.exceptions import fsctrl_exceptions as ex
from slrd.strings import comlogstr
from shutil import rmtree


class FSController(object):
    """Read, write and modify files in a file system."""

    SUPPORTED_LOAD_FORMATS = ["yaml", "json"]

    LOGSTR_RET_PMODE = 'retrieved parent mode: %s, mode: %s'
    LOGSTR_RET_FILE = 'retrieved file content: %s'
    LOGSTR_PARSE_FILE = 'parsed file content: %s, format: %s'
    LOGSTR_MKDIR = 'created directory: %s, mode: %s'
    LOGSTR_DELDIR = 'deleted directory: %s'
    LOGSTR_NODIR_OK = 'directory do not exist -> nothing to delete: %s'
    LOGSTR_SYML_ATK_SUS = 'platform do not support fd-based functions: ' + \
                          'symlink attack is possible'
    LOGSTR_DELFILE = 'deleted file: %s'
    LOGSTR_NOFILE_OK = 'file do not exist -> nothing to delete: %s'
    LOGSTR_MODE_WEIRD = 'permissions mode seems to be weird: %s'
    LOGSTR_NABS_PATHS = 'no absolute path enforcement: some functionality' + \
                        'might break with relative paths'

    ERRMSG_UNSUP_FORMAT = 'unsupported load format passed : %s'
    ERRMSG_UNSUP_TYPE = 'unsupported delete type: %s: %s'
    ERRMSG_MKDIR_MODE_ERR = 'can\'t cast mode argument to integer: %s'
    ERRMSG_READ_ERR = 'failed to read a file content: %s: %s'
    ERRMSG_MKDIR_ERR = 'failed to create directory: %s with mode %s: %s'
    ERRMSG_MKDIR_EXISTS = 'directory already exists: %s with mode: %s'
    ERRMSG_MKDIR_NDIR = 'can\'t create directory: %s: file exists'
    ERRMSG_DELDIR_ERR = 'failed to remove subtree: %s: %s'
    ERRMSG_DELDIR_NDIR = 'failed to remove subtree: %s: not a directory'
    ERRMSG_DELFILE_ERR = 'failed to remove file: %s: %s'
    ERRMSG_DELFILE_NFILE = 'failed to remove file: %s: not a file'
    ERRMSG_FILE_EXISTS = 'can\'t write to file: %s: file exists, force=%s'
    ERRMSG_NSUPP_FD = 'system do not support file descriptions: won\'t write'
    ERRMSG_WRITE_NFILE = 'can\'t write to file: %s: not a regular file'
    ERRMSG_WRITE_FAIL = 'error writing to file: %s: %s'
    ERRMSG_PATH_NEXIST = 'path do not exist: %s'
    ERRMSG_PATH_NABS = 'path must be absolute: %s'
    ERRMSG_PMRET_FAIL = 'failed to retrieve parent perms mode: %s: %s'

    def __init__(self, enforce_abspath=True):
        """Initialization method."""
        self.logger = logging.getLogger(__name__)
        self.logger.debug(comlogstr.LOG_INIT_START)
        self.enforce_abspath = enforce_abspath
        if not self.enforce_abspath:
            self.logger.warning(self.LOGSTR_NABS_PATHS)
        self.logger.debug(comlogstr.LOG_INIT_END)

    def __enforce_absolute(self, path):
        """Check whether a given path is absolute.

        Do not check an actual existence of a path.

        :param path: path to check
        :type path:  str

        :raises: slrd.exceptions.common_exceptions.SLRDIllegalArgumentError
        """
        tc.check_types(str, *locals())
        if not path[0] == '/':
            errstr = self.ERRMSG_PATH_NABS % path
            self.logger.critical(errstr)
            raise ex.SLRDIllegalArgumentError(errstr)

    def __is_weird_perms_mode(self, mode):
        """Check whether permissions mode looks weird.

        By "weird" means that mode is outside of a range (0, 511] or in octal
        (000, 777].

        :param mode: mode to check
        :type mode:  int

        :return: whether mode is weird
        :rtype:  bool

        :raises: slrd.exceptions.common_exceptions.SLRDIllegalArgumentError
        """
        tc.check_types(int, *locals())
        if mode in range(0, 512):
            return True
        self.logger.warning(self.LOGSTR_MODE_WEIRD % oct(mode))
        return False

    def __it_exists(self, path, check_func):
        """Implementation of *_exists methods.

        :param path:       path to check an existence of
        :param check_func: function to check with

        :type path:       str
        :type check_func: function

        :return: result of a check
        :rtype:  bool

        :raises: slrd.exceptions.common_exceptions.SLRDIllegalArgumentError
        """
        if self.enforce_abspath:
            self.__enforce_absolute(path)
        tc.check_types(str, callable, *locals())
        result = check_func(path)
        self.logger.debug(comlogstr.LOG_CHECK_RESULT %
                          (check_func.__name__ + '(%s)' % path, result))
        return result

    def file_exists(self, path):
        """Check whether a file exists.

        :param path:         path to a file to check an existence of
        :type path:          str

        :return: result of a check
        :rtype:  bool

        :raises: slrd.exceptions.common_exceptions.SLRDIllegalArgumentError
        """
        return self.__it_exists(path, isfile)

    def dir_exists(self, path):
        """Check whether a directory exists.

        :param path:         path to a directory to check an existence of
        :type path:          str

        :return: result of a check
        :rtype:  bool

        :raises: slrd.exceptions.common_exceptions.SLRDIllegalArgumentError
        """
        return self.__it_exists(path, isdir)

    def link_exists(self, path):
        """Check whether a link exists.

        :param path:         path to a link to check an existence of
        :type path:          str

        :return: result of a check
        :rtype:  bool

        :raises: slrd.exceptions.common_exceptions.SLRDIllegalArgumentError
        """
        return self.__it_exists(path, islink)

    def it_exists(self, path):
        """Check whether path exists.

        :param path:         path to check an existence of
        :type path:          str

        :return: result of a check
        :rtype:  bool

        :raises: slrd.exceptions.common_exceptions.SLRDIllegalArgumentError
        """
        return self.__it_exists(path, exists)

    def create_dir(self, path, mode):
        """Create a directory.

        :param path: path to a directory to create
        :param mode: permissions with which to create a directory (hint:
                     use octal notation, like 0o700)

        :type path: str
        :type mode: int

        :raises: slrd.exceptions.common_exceptions.SLRDIllegalArgumentError,
                 slrd.exceptions.controller_exceptions.SLRDFSCtrlCreateException
        """
        if self.enforce_abspath:
            self.__enforce_absolute(path)
        tc.check_types(str, int, *locals())
        d_exists = self.dir_exists(path)
        if d_exists:
            errmsg = self.ERRMSG_MKDIR_EXISTS % path
            self.logger.error(errmsg)
            raise ex.SLRDFSCtrlCreateException(errmsg)
        elif not d_exists and self.it_exists(path):
            errmsg = self.ERRMSG_MKDIR_NDIR % path
            self.logger.error(errmsg)
            raise ex.SLRDFSCtrlCreateException(errmsg)
        try:
            self.__is_weird_perms_mode(mode)
            makedirs(path, mode)
        except OSError as e:
            errmsg = self.ERRMSG_MKDIR_ERR % (path, mode, e)
            self.logger.error(self.errmsg)
            raise ex.SLRDFSCtrlCreateException(errmsg)
        self.logger.info(self.LOGSTR_MKDIR % (path, mode))

    def __delete_it(self, path, del_func, dtype):
        """Implemetation of delete_* methods.

        :param path:     path to something that must be deleted
        :param del_func: function to use when deleting
        :param dtype: lowercase description of "something" (i.e. file, dir,
                         link). Will be used for determining what checks to run
                         and what logs to output.

        :type path:      str
        :type del_func:  function
        :type dtype:  str

        :raises: slrd.exceptions.common_exceptions.SLRDIllegalArgumentError,
                 slrd.exceptions.controller_exceptions.SLRDFSCtrlRmException
        """
        if self.enforce_abspath:
            self.__enforce_absolute(path)
        tc.check_types(str, callable, str, *locals())
        dtype_up = dtype.upper()
        try:
            it_exists = getattr(self, '%s_exists' % dtype)
            logstr_del_succ = getattr(self, 'LOGSTR_DEL%s' % dtype_up)
            logstr_del_ok = getattr(self, 'LOGSTR_NO%s_OK' % dtype_up)
            errstr_del_fail = getattr(self, 'ERRMSG_DEL%s_ERR' % dtype_up)
            errstr_del_wtype = getattr(self, 'ERRMSG_DEL%s_N%s' %
                                       (dtype_up, dtype_up))
        except AttributeError as e:
            errmsg = self.ERRMSG_UNSUP_TYPE % (dtype, e)
            self.logger.critical(errmsg)
            raise ex.SLRDIllegalArgumentError(errmsg)
        if it_exists(path):
            try:
                del_func(path)
                self.logger.debug(logstr_del_succ)
            except (OSError, PermissionError) as e:
                errmsg = errstr_del_fail % path
                self.logger.info(errmsg)
                raise ex.SLRDFSCtrlRmException(errmsg)
        elif self.it_exists(path):  # it still exists but not dtype requested
            errmsg = errstr_del_wtype % path
            self.logger.error(errmsg)
            raise ex.SLRDFSCtrlRmException(errmsg)
        self.logger.warning(logstr_del_ok % path)  # do not exist at all

    def delete_dir(self, path):
        """Delete a directory.

        Remove the directory with all files in it (force, best-effort).

        If directory do not exist the operation considered to be successful. If
        an input path leads to something that is not a directory the exception
        will be raised.

        :param path: path to a directory to delete
        :type path:  str

        :raises: slrd.exceptions.common_exceptions.SLRDIllegalArgumentError,
                 slrd.exceptions.controller_exceptions.SLRDFSCtrlRmException
        """
        if not rmtree.avoids_symlink_attacks:
            self.logger.warning(self.LOGSTR_SYML_ATK_SUS)
        self.__delete_it(path, rmtree, 'dir')

    def delete_file(self, path):
        """Delete a file.

        If file do not exist an operation considered to be successful. If path
        leads to something that is not a regular file the exception will be
        raised.

        :param path: path to a file to delete
        :type path:  str

        :raises: slrd.exceptions.common_exceptions.SLRDIllegalArgumentError,
                 slrd.exceptions.controller_exceptions.SLRDFSCtrlRmException
        """
        self.__delete_it(path, remove, 'file')

    def read_file(self, path):
        """Read content of a text file.

        :param path: path to a text file to read
        :type path:  str

        :return: content of a file
        :rtype:  str

        :raises: slrd.exceptions.common_exceptions.SLRDIllegalArgumentError,
                 slrd.exceptions.controller_exceptions.SLRDFSCtrlReadException
        """
        if self.enforce_abspath:
            self.__enforce_absolute(path)
        tc.check_types(str, *locals())
        try:
            with open(path) as f:
                cont = f.read()
                self.logger.debug(self.LOGSTR_RET_FILE % path)
                return cont
        except (OSError, PermissionError) as e:
            errmsg = self.ERRMSG_READ_ERR % (path, e)
            self.logger.error(errmsg)
            raise ex.SLRDFSCtrlReadException(errmsg)

    def load_formatted_file(self, path, lformat):
        """Load content of a specific format.

        Basically calls self.read_file() and then attempts to loads with a
        parser of a specified format (JSON, YAML etc).

        See self.SUPPORTED_LOAD_FORMATS for a list of formats that can be used.

        :param path:   path to a file to load
        :param format: format to use when parsing file content

        :rtype path:   str
        :rtype format: str

        :return: loaded content of a file
        :rtype:  dict

        :raises: slrd.exceptions.common_exceptions.SLRDIllegalArgumentError,
                 slrd.exceptions.controller_exceptions.SLRDFSCtrlReadException
        """
        if self.enforce_abspath:
            self.__enforce_absolute(path)
        tc.check_types(str, str, *locals())
        if lformat not in self.SUPPORTED_LOAD_FORMATS:
            errmsg = self.ERRMSG_UNSUP_FORMAT % lformat
            self.logger.critical(errmsg)
            raise ex.SLRDIllegalArgumentError(errmsg)
        file_content = self.read_file(path)
        try:
            parsed_cont = import_module(lformat).loads(file_content)
            self.logger.debug(self.LOGSTR_PARSE_FILE % (path, lformat))
            return parsed_cont
        except Exception as e:
            errmsg = self.ERRMSG_READ_ERR % (path, e)
            self.logger.error(errmsg)
            raise ex.SLRDFSCtrlReadException(errmsg)

    def write_to_file(
            self,
            data,
            path,
            mode=0o755,
            inherit_mode=False,
            timestamp=None,
            force=False
            ):
        """Write data to a file located at a specified path.

        Data is written in a text mode.

        :param data:         data to write to a file
        :param path:         path to a file to write to
        :param mode:         permissions with which to create a file
                             (hint: use octal notation, like 0o700)
        :param inherit_mode: inherit access mode from a parent directory
        :param timestamp:    timestamp to create a file with (local time)
        :param force:        override existing files

        :type data:         str
        :type path:         str
        :type mode:         int
        :type inherit_mode: bool
        :type timestamp:    datetime.datetime object
        :type force:        bool

        :raises: slrd.exceptions.common_exceptions.SLRDIllegalArgumentError
                 slrd.exceptions.controller_exceptions.SLRDFSCtrlWriteException
        """
        if self.enforce_abspath:
            self.__enforce_absolute(path)
        tc.check_types(str, str, int, bool, datetime, bool, *locals())
        f_exists = self.file_exists(path)
        if utime not in supports_fd:
            self.logger.critical(self.ERRMSG_NSUPP_FD)
            raise self.SLRDUnsupportedSystemError(self.ERRMSG_NSUPP_FD)
        elif f_exists and not force:
            errmsg = self.ERRMSG_FILE_EXISTS % (path, str(force))
            self.logger.error(errmsg)
            raise ex.SLRDFSCtrlWriteException(errmsg)
        elif not f_exists and self.it_exists(path):
            errmsg = self.ERRMSG_WRITE_NFILE % path
            self.logger.error(errmsg)
            raise ex.SLRDFSCtrlWriteException(errmsg)
        if inherit_mode:
            mode = self.get_parent_mode(path)
        self.__is_weird_perms_mode(mode)
        if not timestamp:
            timestamp = datetime.today()
        ts_seconds = timestamp.timestamp()
        try:
            with fdopen(osopen(path, flags=O_CREAT, mode=mode)) as f:
                f.write(data)
                utime(f.fileno(), times=(ts_seconds, ts_seconds))
        except Exception as e:
            errmsg = self.ERRMSG_WRITE_FAIL % (type(e).__name__, e)
            self.logger.error(errmsg)
            raise ex.SLRDFSCtrlWriteException(errmsg)

    def get_parent_mode(self, path):
        """Get permissions mode of a parent folder.

        :param path: path to a file
        :type path:  str

        :return: mode of a parent
        :rtype:  int

        :raises: slrd.exceptions.common_exceptions.SLRDIllegalArgumentError
                 slrd.exceptions.controller_exceptions.SLRDFSCtrlReadException
        """
        if self.enforce_abspath:
            self.__enforce_absolute(path)
        if not self.it_exists(path):
            errmsg = self.ERRMSG_PATH_NEXIST % path
            self.logger.error(errmsg)
            raise ex.SLRDFSCtrlReadException(errmsg)
        parent = path.rsplit('/', 1)[0]
        # NOTE: stat will give a "wrong" permission mode if a parent is a
        # symlink; lstat solves this problem though it's a good question what
        # is a right approach in this case (lstat is used AFN)
        try:
            pmode = lstat(parent).st_mode
        # NOTE: blindly guessing exception types
        except (IOError, PermissionError) as e:
            errmsg = self.ERRMSG_PMRET_FAIL % (path, e)
            self.logger.error(errmsg)
            raise ex.SLRDFSCtrlReadException(errmsg)
        self.logger.info(self.LOGSTR_RET_PMODE % (path, oct(pmode)))
        return pmode

    def check_mode(self, path):
        """Get permissions mode of a path.

        :param path: path to get permissions of
        :type:       str

        :return: mode string (string that represents octal *nix permissions)
        :rtype:  str

        :raises: <???>
        """
        # TODO: implement

    def match_mode_subtree(self, path, dir_mode, other_mode, fd_content=True):
        """Check whether subtree permissions match ones passed in.

        :param path:       path to a subtree to check
        :param dir_mode:   mode string that all directories permissions must
                           match
        :param other_mode: mode string that all other files must match
        :param fd_content: ensure content of a subtree consists only from files
                           or directories

        :type path:        str
        :type dir_mode:    str
        :type other_mode:  str
        :type fd_content:  bool

        :return: result of a check
        :rtype:  bool

        :raises: <???>
        """
        # TODO: implement
