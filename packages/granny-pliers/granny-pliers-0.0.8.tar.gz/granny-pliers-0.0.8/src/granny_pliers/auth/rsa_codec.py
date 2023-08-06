#  Copyright 2022 Dmytro Stepanenko, Granny Pliers
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""RSA"""

import hashlib
from typing import Tuple

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPrivateKey

from granny_pliers.logger import AbstractLogger

__all__ = ["RSACodec"]


class RSACodec(AbstractLogger):
    """RSACodec is the main class for operate with keys"""

    def __init__(
        self,
        key_password: str = None,
        private_key_pem: bytes = None,
        private_key_filename: str = None,
        public_key_pem: bytes = None,
        public_key_file_name: str = None,
        key_size=4096,
    ):
        """
        :param key_password: Private key password. If None you can not use private key, because it should be protected
            with password. In case f using only public key, you can keep it None
        :param private_key_pem: Private key. If not None private_key_filename will be ignored
        :param public_key_file_name: Private key file name. The private key will be loaded from file
        :param public_key_pem: Public key. If not None public_key_file_name will be ignored
        :param public_key_file_name: Public key file name. The public key will be loaded from file
        :param key_size: Private key size, default value 4096
        """
        super().__init__()
        self.backend = default_backend()
        self.key_size = key_size

        self._private_key = None
        self._public_key = None

        if key_password is not None:
            self.key_password = key_password.encode()

        if private_key_pem is not None:
            self._load_private_key(private_key_pem)
        elif private_key_filename is not None:
            self._load_private_key_from_file(private_key_filename)

        if public_key_pem is not None:
            self._load_public_key(public_key_pem)
        elif public_key_file_name is not None:
            self._load_public_key_from_file(public_key_file_name)

    @property
    def public_key(self) -> RSAPublicKey:
        """public_key"""
        return self._public_key

    @property
    def private_key(self) -> RSAPrivateKey:
        """private_key"""
        return self._private_key

    def generate_keys(self) -> Tuple[bytes, bytes]:
        """
        Generate RSA key pair

        :return: Tuple[private key: bytes, public key: bytes] in PEM format
        """
        if self.key_password is None:
            self.log.error("Can not generate private key, key_password is empty")
            raise ValueError("Can not generate private key, key_password is empty")

        self.log.info("Generating private key...")
        self._private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=self.key_size, backend=self.backend
        )
        self.log.debug("Private key has been generated")

        self.log.info("Generating public key...")
        self._public_key = self.private_key.public_key()
        self.log.debug(
            "Public key has been generated, fingerprint: %s",
            hashlib.md5(self._get_public_key_bytes()).hexdigest(),
        )

        return self._get_private_key_bytes(), self._get_public_key_bytes()

    def _get_private_key_bytes(self) -> bytes:
        if self.key_password is None:
            self.log.error("Can not serialize private key, key_password is empty")
            raise ValueError("Can not serialize private key, key_password is empty")
        return self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(self.key_password),
        )

    def _get_public_key_bytes(self):
        """_get_public_key_bytes"""
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

    def save_private_key_to_file(self, private_key_filename):
        """save_private_key_to_file"""
        self.log.info("Saving private key into %s...", private_key_filename)
        with open(private_key_filename, "wb") as pem_out:
            pem_out.write(self._get_private_key_bytes())
        self.log.debug("Private key has been saved %s...", private_key_filename)

    def save_public_key_to_file(self, public_key_filename):
        """save_public_key_to_file"""
        self.log.info("Saving public key into %s...", public_key_filename)
        with open(public_key_filename, "wb") as pem_out:
            pem_out.write(self._get_public_key_bytes())
        self.log.debug("Public key has been saved %s...", public_key_filename)

    def _load_private_key(self, private_key: bytes):
        """
        Loads private key from bytes buffer

        :param private_key: bytes PEM format
        """
        if self.key_password is None:
            self.log.error("Can not load private key, key_password is empty")
            raise ValueError("Can not load private key, key_password is empty")

        self.log.info("Loading private key...")
        self._private_key = serialization.load_pem_private_key(
            private_key, password=self.key_password, backend=self.backend
        )
        self.log.debug("Private key has been loaded")

    def _load_public_key(self, public_key: bytes):
        """
        Loads public key from bytes buffer

        :param public_key: bytes PEM format
        """
        self.log.info("Loading public key...")
        self._public_key = serialization.load_pem_public_key(public_key, backend=self.backend)
        self.log.debug(
            "Public key has been loaded, fingerprint:%s",
            hashlib.md5(self._get_public_key_bytes()).hexdigest(),
        )

    def _load_private_key_from_file(self, private_key_filename: str):
        """
        Loads private key from file

        :param private_key_filename: filename
        """
        self.log.info("Loading private key from file %s...", private_key_filename)
        with open(private_key_filename, "rb") as file:
            self._load_private_key(file.read())

    def _load_public_key_from_file(self, public_key_filename: str):
        """
        Loads private key from file

        :param public_key_filename: filename
        """
        self.log.info("Loading public key from file %s...", public_key_filename)
        with open(public_key_filename, "rb") as file:
            self._load_public_key(file.read())

    def encrypt(self, buffer: bytes) -> bytes:
        """
        Encrypts buffer

        :param buffer:
        :return: encrypted bytes
        """
        if self.public_key is None:
            raise ValueError("Can not encrypt buffer, public_key is empty")

        return self.public_key.encrypt(
            buffer,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA512()),
                algorithm=hashes.SHA512(),
                label=None,
            ),
        )

    def decrypt(self, buffer: bytes) -> bytes:
        """
        Decrypts buffer

        :param buffer:
        :return: decrypted bytes
        """
        if self.private_key is None:
            raise ValueError("Can not decrypt buffer, private_key is empty")

        return self.private_key.decrypt(
            buffer,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA512()),
                algorithm=hashes.SHA512(),
                label=None,
            ),
        )

    def sign(self, buffer: bytes) -> bytes:
        """
        Generates signature of input buffer

        :param buffer: byte to be signed
        :return: bytes signature
        """
        if self.private_key is None:
            raise ValueError("Can not sign buffer, private_key is empty")

        return self.private_key.sign(
            data=buffer,
            padding=padding.PSS(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            algorithm=hashes.SHA256(),
        )

    def verify(self, buffer: bytes, signature: bytes) -> bool:
        """
        Verifies signature

        :param buffer: was signet
        :param signature:
        :return: True if signature is correct, False if not
        """
        if self.public_key is None:
            raise ValueError("Can not verify signature, public_key is empty")
        try:
            self.public_key.verify(
                signature,
                buffer,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            )
            return True
        except InvalidSignature:
            self.log.warning("Signature verification failed, invalid signature")
            return False
