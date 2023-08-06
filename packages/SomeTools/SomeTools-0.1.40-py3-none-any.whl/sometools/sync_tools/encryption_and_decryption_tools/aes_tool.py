from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from sometools.sync_tools.base import Base

class EncryptionDecryptionMixIn(Base):

    def __init__(self, *args, **kwargs):
        super(EncryptionDecryptionMixIn, self).__init__(*args, **kwargs)

    @staticmethod
    def aes_ecb_encryption(content, password: bytes) -> bytes:
        """
        ECB模式加密
        :param content:明文必须为16字节或者16字节的倍数的字节型数据，如果不够16字节需要进行补全
        :param password:秘钥必须为16字节或者16字节的倍数的字节型数据。
        :return: bytes
        """
        print("ECB模式加密")
        print("明文：", content)  # 加密明文，bytes类型
        aes = AES.new(password, AES.MODE_ECB)  # 创建一个aes对象,aes 加密常用的有 ECB 和 CBC 模式,AES.MODE_ECB 表示模式是ECB模式
        en_text = aes.encrypt(content)  # 加密明文
        print("密文：", en_text)  # 加密明文，bytes类型
        return en_text

    @staticmethod
    def aes_ecb_decryption(en_text, password: bytes) -> bytes:
        """
        ECB模式解密
        :param en_text 加密后的密文
        :param password:秘钥必须为16字节或者16字节的倍数的字节型数据。
        :return: bytes
        """
        print("ECB模式解密")
        print("密文：", en_text)
        aes = AES.new(password, AES.MODE_ECB)
        content = aes.decrypt(en_text)
        print("明文：", content)
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
        print("CBC模式的加密")
        print("明文：", content)  # 加密明文，bytes类型
        aes = AES.new(password,AES.MODE_CBC,iv) #创建一个aes对象  AES.MODE_CBC 表示模式是CBC模式
        en_text = aes.encrypt(content)  # 加密明文
        print("密文：", en_text)  # 加密明文，bytes类型
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
        print("CBC模式解密")
        print("密文：", en_text)
        aes = AES.new(password,AES.MODE_CBC,iv)  # CBC模式与ECB模式的区别：AES.new() 解密和加密重新生成了aes对象，加密和解密不能调用同一个aes对象，否则会报错TypeError: decrypt() cannot be called after encrypt()
        content = aes.decrypt(en_text)
        print("明文：", content)
        return content

    @staticmethod
    def aes_pad(content) -> bytes:
        """
        填充
        """
        print(f"填充前：{content}")
        text = pad(content, AES.block_size)
        print(f"填充后：{text}")
        return text

    @staticmethod
    def aes_unpad(en_text) -> bytes:
        """
        去填充
        """
        print(f"去填充前：{en_text}")
        text = unpad(en_text, AES.block_size)
        print(f"去填充后：{text}")
        return text

if __name__ == '__main__':
    demo_ins = EncryptionDecryptionMixIn()
    content = b'abcdefghijklmnh'
    res_text = demo_ins.aes_pad(content)
    demo_ins.aes_unpad(res_text)
    # 加密解密
    password = b'1234567812345678'  # 秘钥，b就是表示为bytes类型，秘钥必须为16字节或者16字节的倍数的字节型数据。
    content = b'abcdefghijklmnhi'  # 需要加密的内容，bytes类型，明文必须为16字节或者16字节的倍数的字节型数据，如果不够16字节需要进行补全
    en_text = demo_ins.aes_ecb_encryption(content, password)
    demo_ins.aes_ecb_decryption(en_text, password)
    iv = b'1234567812345678'  # iv偏移量，bytes类型
    en_text = demo_ins.aes_cbc_encryption(content, password, iv)
    content = demo_ins.aes_cbc_decryption(en_text, password, iv)

    # 中文加密解密
    # 我们可以使用encode()函数进行编码，将字符串转换成bytes类型数据
    # 这里选择gbk编码，是为了正好能满足16字节
    # utf8编码是一个中文字符对应3个字节,utf8 和 gbk 编码，针对英文字符编码都是一个字符对应一个字节。这里为了举例所以才选择使用gbk编码
    # 在解密后，同样是需要decode()函数进行解码的，将字节型数据转换回中文字符（字符串类型）
    print("中文明文：好好学习天天向上 需要gbk编码")
    content = "好好学习天天向上".encode('gbk')  # gbk编码，是1个中文字符对应2个字节，8个中文正好16字节
    en_text = demo_ins.aes_ecb_encryption(content, password)
    content = demo_ins.aes_ecb_decryption(en_text, password)
    print("中文明文：", content.decode("gbk"),"解密后同样需要进行解码")  # 解密后同样需要进行解码