from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from sometools.sync_tools.base import Base


class AesMixIn(Base):

    def __init__(self, *args, **kwargs):
        super(AesMixIn, self).__init__(*args, **kwargs)

    @staticmethod
    def aes_ecb_encryption(content, password: bytes) -> bytes:
        """
        ECB模式加密
        :param content:明文必须为16字节或者16字节的倍数的字节型数据，如果不够16字节需要进行补全
        :param password:秘钥必须为16字节或者16字节的倍数的字节型数据。
        :return: bytes
        """
        aes = AES.new(password, AES.MODE_ECB)  # 创建一个aes对象,aes 加密常用的有 ECB 和 CBC 模式,AES.MODE_ECB 表示模式是ECB模式
        en_text = aes.encrypt(content)  # 加密明文
        return en_text

    @staticmethod
    def aes_ecb_decryption(en_text, password: bytes) -> bytes:
        """
        ECB模式解密
        :param en_text 加密后的密文
        :param password:秘钥必须为16字节或者16字节的倍数的字节型数据。
        :return: bytes
        """
        aes = AES.new(password, AES.MODE_ECB)
        content = aes.decrypt(en_text)
        return content

    @staticmethod
    def aes_cbc_encryption(content, password, iv: bytes) -> bytes:
        """
        CBC模式的加密
        :param content:明文必须为16字节或者16字节的倍数的字节型数据，如果不够16字节需要进行补全
        :param password:秘钥必须为16字节或者16字节的倍数的字节型数据
        :param iv 偏移量，bytes类型
        :return: bytes
        """
        aes = AES.new(password, AES.MODE_CBC, iv)  # 创建一个aes对象  AES.MODE_CBC 表示模式是CBC模式
        en_text = aes.encrypt(content)  # 加密明文
        return en_text

    @staticmethod
    def aes_cbc_decryption(en_text, password, iv: bytes) -> bytes:
        """
        CBC模式解密
        :param en_text 加密后的密文
        :param password:秘钥必须为16字节或者16字节的倍数的字节型数据。
        :param iv 偏移量，bytes类型
        :return: bytes
        """
        aes = AES.new(password, AES.MODE_CBC,
                      iv)  # CBC模式与ECB模式的区别：AES.new() 解密和加密重新生成了aes对象，加密和解密不能调用同一个aes对象，否则会报错TypeError: decrypt() cannot be called after encrypt()
        content = aes.decrypt(en_text)
        return content

    @staticmethod
    def aes_pad(content) -> bytes:
        """
        填充
        """
        text = pad(content, AES.block_size)
        return text

    @staticmethod
    def aes_unpad(en_text) -> bytes:
        """
        去填充
        """
        text = unpad(en_text, AES.block_size)
        return text
