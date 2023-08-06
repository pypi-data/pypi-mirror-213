import hashlib
from sometools.sync_tools.base import Base


class Md5Mixin(Base):
    def __init__(self, *args, **kwargs):
        super(Md5Mixin, self).__init__(*args, **kwargs)

    @staticmethod
    def get_md5_bytes(bytes_content: bytes) -> bytes:
        return hashlib.md5(bytes_content).digest()

    @staticmethod
    def get_md5_str(bytes_content: bytes) -> str:
        return hashlib.md5(bytes_content).hexdigest()
