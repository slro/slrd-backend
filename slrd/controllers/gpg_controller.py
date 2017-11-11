"""This module contains a single class: GPGController.

See GPGController class documentation for additional details.
"""
import gnupg


class GPGController(object):
    """Encrypt and decrypt data with GnuPG."""

    def __init__(self, gpg_key_id, pt_length):
        """Initialization method.

        :param gpg_key_id: ID of GPG key to use for encryption/decryption
        :param pt_length: length of a plain text block to feed to GPG (it will
                          be padded to this length and rejected if it's longer)
        :type gpg_key_id: str
        :type pt_length: int

        :raise: <???>
        """
        self.gpg_key_id = gpg_key_id
        self.gpg = gnupg.GPG(gnupghome='???')

    def pad(self, data):
        """Pad data to the length equal to len(self.pt_length).

        :param data: data to pad
        :type data: str

        :return: padded data
        :rtype: str
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
