from .aes_tool import AesMixIn
from .rsa_tool import RsaMixIn


class EncryptionDecryptionMixIn(AesMixIn,RsaMixIn):
    def __init(self, *args, **kwargs):
        super(EncryptionDecryptionMixIn, self).__init__(*args, **kwargs)

__all__ = ["EncryptionDecryptionMixIn"]