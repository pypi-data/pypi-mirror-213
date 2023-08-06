import rsa
from rsa.key import PublicKey, PrivateKey
from sometools.sync_tools.base import Base


class RsaMixIn(Base):

    def __init__(self, *args, **kwargs):
        super(RsaMixIn, self).__init__(*args, **kwargs)

    @staticmethod
    def rsa_get_key_pair() -> (PublicKey, PrivateKey):
        """生成密钥对"""
        pubkey, prikey = rsa.newkeys(1024)
        return pubkey, prikey

    @staticmethod
    def rsa_create_pub_key(self) -> (PublicKey, PrivateKey):
        """创建公钥"""
        # 公钥有两个值  n,e
        public_n = "e0b509f62a8fc9" * 4
        public_e = '010001'
        # n、e必须为整数
        # 将16进制的字符串转为整数
        rsa_n = int(public_n, 16)
        rsa_e = int(public_e, 16)
        print('n：{}\ne：{}'.format(rsa_n, rsa_e))
        # 创建公钥 rsa.PublicKey(n,e)
        pubkey = rsa.PublicKey(rsa_n, rsa_e)
        return pubkey

    @staticmethod
    def rsa_sign(content: bytes, pri_key: PrivateKey, sign_type: str = 'MD5') -> bytes:
        """加签    rsa.sign(原信息，私钥，加密方式)  生成加签过后的信息"""
        sign_message = rsa.sign(content, pri_key, sign_type)
        return sign_message

    @staticmethod
    def rsa_verify(content: bytes, pub_key: PublicKey, sign_message: bytes) -> (PublicKey, PrivateKey):
        """验签    rsa.verify(需要验证的信息，加签过后的信息，公钥),如果需要验证的信息，是原信息，返回加密方式"""
        try:
            veri_res = rsa.verify(content, sign_message, pub_key)
            print(f'校验通过无修改-加密方式{veri_res}')
            return True
        except rsa.pkcs1.VerificationError as e:
            print(f"校验未通过-信息被篡改过-{e}")
            return False

    @staticmethod
    def rsa_encryption(content: bytes, pubkey: PublicKey) -> bytes:
        """加密：使用公钥"""
        return rsa.encrypt(content, pubkey)

    @staticmethod
    def rsa_decryption(en_text: bytes, prikey: PrivateKey) -> bytes:
        """解密：使用私钥"""
        return rsa.decrypt(en_text, prikey)
