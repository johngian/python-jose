
from jose.constants import ALGORITHMS
from jose.exceptions import JOSEError, JWKError

from jose.backends.ecdsa_backend import ECDSAECKey
from jose.backends.cryptography_backend import CryptographyECKey

import ecdsa
import pytest

private_key = """-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIOiSs10XnBlfykk5zsJRmzYybKdMlGniSJcssDvUcF6DoAoGCCqGSM49
AwEHoUQDQgAE7gb4edKJ7ul9IgomCdcOebQTZ8qktqtBfRKboa71CfEKzBruUi+D
WkG0HJWIORlPbvXME+DRh6G/yVOKnTm88Q==
-----END EC PRIVATE KEY-----"""


class TestECAlgorithm:

    def test_EC_key(self):
        key = ecdsa.SigningKey.from_pem(private_key)
        ECDSAECKey(key, ALGORITHMS.ES256)
        CryptographyECKey(key, ALGORITHMS.ES256)

        ECDSAECKey(private_key, ALGORITHMS.ES256)
        CryptographyECKey(private_key, ALGORITHMS.ES256)

    def test_string_secret(self):
        key = 'secret'
        with pytest.raises(JOSEError):
            ECDSAECKey(key, ALGORITHMS.ES256)

        with pytest.raises(JOSEError):
            CryptographyECKey(key, ALGORITHMS.ES256)

    def test_object(self):
        key = object()
        with pytest.raises(JOSEError):
            ECDSAECKey(key, ALGORITHMS.ES256)

        with pytest.raises(JOSEError):
            CryptographyECKey(key, ALGORITHMS.ES256)

    def test_invalid_algorithm(self):
        with pytest.raises(JWKError):
            ECDSAECKey({'kty': 'bla'}, ALGORITHMS.ES256)

    def test_verify(self):
        key = ECDSAECKey(private_key, ALGORITHMS.ES256)
        msg = b'test'
        signature = key.sign(msg)
        public_key = key.public_key()

        assert public_key.verify(msg, signature) == True
        assert public_key.verify(msg, b'not a signature') == False