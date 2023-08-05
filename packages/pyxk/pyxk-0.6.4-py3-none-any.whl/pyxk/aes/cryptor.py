"""AES 加解密"""
from typing import Union, Optional

from pyxk.utils import LazyLoader
from pyxk.aes._fmtdata import FormatData

copy = LazyLoader("copy", globals(), "copy")
AES = LazyLoader("AES", globals(), "Crypto.Cipher.AES")


def no_padding(data, remove=False, pad=b"\x00"):
    """NoPadding填充模式"""
    # 消除 padding 字符
    if remove:
        return data.rstrip(pad)
    remainder = len(data) % AES.block_size or AES.block_size
    data += pad * (AES.block_size - remainder)
    return data


def zero_padding(data, remove=False, pad=b"\x00"):
    """ZeroPadding填充模式"""
    # 消除 padding 字符
    if remove:
        return data.rstrip(pad)
    remainder = len(data) % AES.block_size
    # 不填充
    data += pad * (AES.block_size - remainder)
    return data


PADDING_ALL = {
    "Raw": lambda data, *args, **kwagrs: data,
    "NoPadding": no_padding,
    "ZeroPadding": zero_padding,
}


class Cryptor(FormatData):
    """AES加解密"""
    def __init__(
            self,
            key: Union[str, bytes],
            iv: Optional[Union[str, bytes]] = None,
            mode: Union[int, str] = "CBC",
            padding: Optional[str] = "NoPadding",
            **kwargs
    ):
        """AES加解密 init

        :param key: 秘钥
        :param iv: 偏移量(部分加密模式不需要偏移量)
        :param mode: 加解密模式
        :param padding: 填充模式(Raw, NoPadding, ZeroPadding)
        :param kwargs: **kwargs
        """
        self._cipher = None
        self._padding = padding
        self.__padding_fmt()
        super().__init__(key, iv, mode, **kwargs)

    def __padding_fmt(self):
        """加解密数据的填充方式"""
        padding = self._padding
        if padding is None:
            self._padding = "NoPadding"
            return
        if not isinstance(padding, str) or padding not in PADDING_ALL:
            raise ValueError(f"'padding' must exist in the {list(PADDING_ALL)}, not {padding!r}")

    def encrypt(self, plaintext: Union[str, bytes]) -> bytes:
        """AES 加密

        :param plaintext: 加密明文
        :return: bytes
        """
        if isinstance(plaintext, str):
            plaintext = plaintext.encode(self._encode)
        elif not isinstance(plaintext, bytes):
            raise TypeError(f"'plaintext' type must be 'str' or 'bytes', not {type(plaintext).__name__!r}")
        # 创建 cipher - 加密
        self.__create_cipher()
        padding_func = PADDING_ALL[self.padding]
        return self._cipher.encrypt(padding_func(plaintext))

    def decrypt(self, ciphertext: Union[str, bytes]) -> bytes:
        """AES 解密

        :param ciphertext: 解密密文
        :return: bytes
        """
        if isinstance(ciphertext, str):
            ciphertext = ciphertext.encode(self._encode)
        elif not isinstance(ciphertext, bytes):
            raise TypeError(f"'plaintext' type must be 'str' or 'bytes', not {type(ciphertext).__name__!r}")
        # 创建 cipher - 解密
        self.__create_cipher()
        padding_func = PADDING_ALL[self.padding]
        return padding_func(self._cipher.decrypt(ciphertext), True)

    def __create_cipher(self):
        """创建 cipher - 加解密工具"""
        state = copy.deepcopy(self._state)
        state["key"] = self.key
        state["mode"] = self.mode
        if self.iv is not None:
            state["iv"] = self._iv
        self._cipher = AES.new(**state)

    @property
    def padding(self):
        """padding"""
        return self._padding

    @padding.setter
    def padding(self, value):
        self._padding = value
        self.__padding_fmt()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            raise
        self._cipher = None


def encrypt(
    key: Union[str, bytes],
    plaintext: Union[str, bytes],
    mode: Union[int, str] = "CBC",
    iv: Optional[Union[str, bytes]] = None,
    **kwargs
) -> bytes:
    """AES 加密

    :param key: 密钥
    :param plaintext: 加密明文
    :param mode: 加解密模式
    :param iv: 偏移量(部分加密模式不需要偏移量)
    :param kwargs: **kwargs
    :return: bytes
    """
    with Cryptor(key=key, mode=mode, iv=iv, **kwargs) as _cipher:
        return _cipher.encrypt(plaintext)


def decrypt(
    key: Union[str, bytes],
    ciphertext: Union[str, bytes],
    mode: Union[int, str] = "CBC",
    iv: Optional[Union[str, bytes]] = None,
    **kwargs
) -> bytes:
    """AES 解密

    :param key: 密钥
    :param ciphertext: 解密密文
    :param mode: 加解密模式
    :param iv: 偏移量(部分加密模式不需要偏移量)
    :param kwargs: **kwargs
    :return: bytes
    """
    with Cryptor(key=key, mode=mode, iv=iv, **kwargs) as _cipher:
        return _cipher.decrypt(ciphertext)
