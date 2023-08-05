# -*- coding:utf-8 -*-
# from Crypto.Cipher import AES
import base64

# from crypto.Cipher import AES
from crypto.Cipher import AES

'''
    Crypt Util
    Author: rzzhou
'''


class CryptUtil(object):
    """
    AES加解密
    """
    # 密钥(key), 偏移量(vi)
    def __init__(self, args=None):

        self.BLOCK_SIZE = 16
        self.pad = lambda s: s + (self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE) * chr(
            self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE)

        self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]

        if args is None:
            self.tool_vi = "This_is_t00l_vi="

        else:
            self.tool_vi = args

    '''
    encypt
    @:param 密码   
    '''

    def AES_Encrypt(self, data, key=None):
        """
        加密
        :param data: 待加密数据
        :param key:  加密秘钥
        :return: 加密结果
        """
        self._KEY = key
        if self._KEY is None:
            self._KEY = "@Default_Key2020"
        if len(str(self.tool_vi)) == self.BLOCK_SIZE and len(str(self._KEY)) == self.BLOCK_SIZE:
            data = self.pad(data)
            cipher = AES.new(self._KEY.encode('utf8'), AES.MODE_CBC, self.tool_vi.encode('utf8'))
            encryptedbytes = cipher.encrypt(data.encode('utf8'))
            encodestrs = base64.b64encode(encryptedbytes)
            # 对byte字符串按 utf-8进行解码
            enctext = encodestrs.decode('utf8')

        else:
            enctext = "error"
        return enctext

    def AES_Decrypt(self, data, key=None):
        """
        解密
        :param data: 待解密数据
        :param key:  解密秘钥
        :return: 解密结果
        """
        self._KEY = key
        if self._KEY is None:
            self._KEY = "@Default_Key2020"
        if len(str(self.tool_vi)) == self.BLOCK_SIZE and len(str(key)) == self.BLOCK_SIZE:
            data = data.encode('utf8')
            encodebytes = base64.decodebytes(data)
            cipher = AES.new(self._KEY.encode('utf8'), AES.MODE_CBC, self.tool_vi.encode('utf8'))
            text_decrypted = cipher.decrypt(encodebytes)

            text_decrypted = self.unpad(text_decrypted)
            text_decrypted = text_decrypted.decode('utf8')

        else:
            text_decrypted = "error"
        return text_decrypted
