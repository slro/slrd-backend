class GPGController(object):
    """ Encrypt and decrypt data with GnuPG """

    def __init__(self, gpg_key_id, pt_length):
        """ Initialization method

        :param str gpg_key_id: ID of GPG key to use for encryption/decryption
        :param int pt_length:  length of a plain text block to feed to GPG (it
                               will be padded to this length and rejected if
                               it's longer)

        :raise: <???>

        """

        # self.gpg_key_id = gpg_key_id

    def pad(self, data):
        """ Pad data to self.pt_length

        :param str data: data to pad

        :return str: padded data

        """

    def encrypt(self, data):
        """ Encrypt data with GPG

        :param str data: data to encrypt

        :return <???>: encrypted data # TODO: what type?

        :raise: <???>

        """

        # make sure len(data) < self.pt_length

        # pad data first
        # self.pad(data)

    def decrypt(self, data):
        """ Decrypt data with PGP

        :param str data: data to decrypt

        :return <???>: decrypted data # TODO: what type?

        :raise: <???>

        """

        # make sure len(data) == len(pt_length) + GPG overhead
