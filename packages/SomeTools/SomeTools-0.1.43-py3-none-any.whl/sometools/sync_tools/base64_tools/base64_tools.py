import base64
from sometools.sync_tools.base import Base


class Base64Mixin(Base):
    """
    base64是一种用64个字符来表示任意二进制数据的方法（将二进制数据编码成ASCII字符）
    使用了A-Z、a-z、0-9、 + 、 / 这64个字符
    用来将非ASCII字符的数据转换成ASCII字符的一种方法
    常用于对URL的编码
    可以将不可打印的二进制数据转化为可打印的字符串
    """

    def __init__(self, *args, **kwargs):
        super(Base64Mixin, self).__init__(*args, **kwargs)

    @staticmethod
    def base64_encode(bytes_content: bytes) -> bytes:
        return base64.b64encode(bytes_content)

    @staticmethod
    def base64_decode(bytes_content: bytes) -> bytes:
        return base64.b64decode(bytes_content)

    @staticmethod
    def base64_encode_urlsafe(bytes_content: bytes) -> bytes:
        """Base64编码后的数据可能会含有 + / 两个符号，如果编码后的数据用于URL或文件的系统路径中，就可能导致Bug，所以base模块提供了专门编码url的方法"""
        return base64.urlsafe_b64encode(bytes_content)

    @staticmethod
    def base64_decode_urlsafe(bytes_content: bytes) -> bytes:
        """Base64编码后的数据可能会含有 + / 两个符号，如果编码后的数据用于URL或文件的系统路径中，就可能导致Bug，所以base模块提供了专门编码url的方法"""
        return base64.urlsafe_b64decode(bytes_content)
