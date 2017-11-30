# -*- coding: utf-8 -*-
# vi: set ft=python sw=4 :
"""GPG interface controller.

This module provides a way to encrypt and decrypt data with GPG using a
single GPG key. All data is padded to the same length before being encrypted.
The length can be specified on creation of GPGController class instance.

Todo:
    - implement methods
"""
import gnupg
import logging
from slrd import comlogstr


class GPGController(object):
    """Encrypt and decrypt data with GnuPG."""

    def __init__(self, gpg_key_id, gpg_home_dir='~/.gnupg/', pt_length=1000):
        """Initialization method.

        :param gpg_key_id:   ID of GPG key to use for encryption/decryption
        :param gpg_home_dir: path to GnuPG home directory
        :param pt_length:    length of a plain text block to feed to GPG.
                             Default is 1000.

        :type gpg_key_id: str
        :type gpg_home_dir: str
        :type pt_length: int

        :raise: <???>
        """
        self.logger = logging.getLogger(__name__)
        self.logger.debug(comlogstr.LOG_INIT_START)

        self.gpg_key_id = gpg_key_id
        self.gpg = gnupg.GPG(gnupghome='???')  # TODO

        self.logger.debug(comlogstr.LOG_INIT_END)

    def pad(self, data):
        """Pad data to the length equal to len(self.pt_length).

        :param data: data to pad
        :type data: str

        :return: padded data
        :rtype: str

        :raise: <???>
        """

    def encrypt(self, data):
        """Encrypt data with GPG.

        :param data: data to encrypt
        :type data: str

        :return: encrypted data
        :rtype: <???> # TODO: what type?

        :raise: <???>
        """

        # Make sure len(data) < self.pt_length

        # Pad data first
        # self.pad(data)

    def decrypt(self, data):
        """Decrypt data with PGP.

        :param data: data to decrypt
        :type data: str

        :return: decrypted data
        :rtype: <???> # TODO: what type?

        :raise: <???>
        """

        # Make sure len(data) == len(pt_length) + GPG overhead
