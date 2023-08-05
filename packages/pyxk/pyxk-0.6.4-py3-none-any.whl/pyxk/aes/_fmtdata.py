"""AES加解密 数据初始化"""
from typing import Union, Optional
from pyxk.utils import LazyLoader

AES = LazyLoader("AES", globals(), "Crypto.Cipher.AES")


# 目前支持的模式
MODES = {
    "ECB": 1,
    "CBC": 2,
    "CFB": 3,
    "OFB": 5,
    "CTR": 6,
    "OPENPGP": 7,
    "EAX": 9,
    "CCM": 8,
    "SIV": 10,
    "GCM": 11,
    "OCB": 12
}


class FormatData:
    """AES数据初始化"""
    def __init__(
        self,
        key: Union[str, bytes],
        iv: Optional[Union[str, bytes]] = None,
        mode: Union[int, str] = "CBC",
        encode: Optional[str] = "UTF-8",
        **kwargs
    ):
        """AES数据初始化 init

        :param key: 秘钥
        :param iv: 偏移量(部分加密模式不需要偏移量)
        :param mode: 加解密模式
        :param encode: 编码
        :param kwargs: **kwargs
        """
        self._key = key
        self._mode = mode
        self._iv = iv
        self._encode = encode
        self._state = kwargs
        self.__initialization()

    def __initialization(self):
        """初始化 key mode iv"""
        self.__key_to_bytes()
        self.__mode_fmt()
        self.__iv_to_bytes()

    def __key_to_bytes(self):
        """key 转换为 bytes"""
        key = self.key
        if isinstance(key, str):
            key = key.encode(self._encode)
        elif not isinstance(key, bytes):
            raise TypeError(
                "'key' type must be 'str' or 'bytes',"
                f" not {type(key).__name__!r}"
            )
        # key 长度判断
        key_length = len(key)
        if key_length not in AES.key_size:
            raise ValueError(
                f"'key' length must be {AES.key_size},"
                f" not {key_length!r}"
            )
        self._key = key

    def __mode_fmt(self):
        """mode 判断"""
        mode = self.mode
        if isinstance(mode, str) and MODES.__contains__(mode.upper()):
            mode = MODES[mode.upper()]
        if not isinstance(mode, int) or mode not in MODES.values():
            mode_val = list(MODES.keys())
            mode_val.extend(list(MODES.values()))
            raise TypeError(f"mode must exist in the {mode_val!r}, not {mode!r}")
        self._mode = mode

    def __iv_to_bytes(self):
        """iv 转换为 bytes"""
        iv = self.iv
        if iv is None:
            if self._mode != MODES["CBC"]:
                return
            iv = self.key[:16]

        if isinstance(iv, str):
            iv = iv.encode(self._encode)
        elif not isinstance(iv, bytes):
            raise TypeError("'iv' type must be 'str' or 'bytes', not {type(iv).__name__!r}")
        # iv 长度判断
        iv_length = len(iv)
        if iv_length != AES.block_size:
            raise ValueError(f"'iv' length must be equal to {AES.block_size!r}, not {iv_length!r}")
        self._iv = iv

    @property
    def key(self):
        """key"""
        return self._key

    @key.setter
    def key(self, value):
        self._key = value
        self.__key_to_bytes()

    @property
    def mode(self):
        """mode"""
        return self._mode

    @mode.setter
    def mode(self, value):
        self._mode = value
        self.__mode_fmt()

    @property
    def iv(self):
        """iv"""
        return self._iv

    @iv.setter
    def iv(self, value):
        self._iv = value
        self.__iv_to_bytes()
