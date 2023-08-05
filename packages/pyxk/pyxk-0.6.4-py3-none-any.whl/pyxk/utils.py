from types import ModuleType
from importlib import import_module
from typing import Any, Union, Optional, Callable


__all__ = [
    "LazyLoader",
    "runtime",
    "coro_runtime",
    "make_open",
    "get_user_agent",
    "default_headers",
    "md5",
    "hash256",
    "is_base64_from_regex",
    "base64_conversion_bytes",
    "rename_file",
    "rename_folder",
    "string_conversion_digits",
    "human_playtime",
    "pycode_conversion_lazyloader",
    "pyfile_conversion_lazyloader",
    "units_conversion_from_byte",
    "download_column",
    "progress_column",
    "chardet"
]


class LazyLoader(ModuleType):
    """模块延迟加载"""

    def __init__(self, local_name, module_life_cycle, import_name=None):
        """模块延迟加载

        :param local_name: 模块引用名称
        :param module_life_cycle: 模块生命周期(建议使用全局变量 globals)
        :param import_name: 导入模块名称
        """
        self._local_name = local_name
        self._module_life_cycle = module_life_cycle
        super().__init__(import_name or local_name)

    def _loader(self):
        module = import_module(self.__name__)
        self._module_life_cycle[self._local_name] = module
        self.__dict__.update(module.__dict__)
        return module

    def __getattr__(self, name):
        module = self._loader()
        return getattr(module, name)

    def __dir__(self):
        module = self._loader()
        return dir(module)


# 计算函数运行时间
def runtime(func: Callable):
    """装饰器: 计算函数运行时间"""
    import functools

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        import time
        from rich import console as rich_console
        console = rich_console.Console()
        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
        finally:
            end_time = time.perf_counter()
            console.print(f"{func.__name__!r} [magenta]running time[/]: {end_time - start_time}")
        return result
    return wrapper


# 计算异步函数运行时间
def coro_runtime(func: Callable):
    """装饰器: 计算异步函数运行时间"""
    import functools

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        import time
        from rich import console as rich_console
        console = rich_console.Console()
        start_time = time.perf_counter()
        try:
            result = await func(*args, **kwargs)
        finally:
            end_time = time.perf_counter()
            console.print(f"{func.__name__!r} [magenta]coroutine running time[/]: {end_time - start_time}")
        return result
    return wrapper


# 内置方法 `open` 装饰器
def _make_open(func):
    """内置方法open装饰器 - 文件模式 w/a 下，创建不存在的目录"""
    import functools

    @functools.wraps(func)
    def wrapper(file, mode="r", buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
        if not isinstance(mode, str):
            raise TypeError(f"{func.__name__}() argument 'mode' must be str, not {type(mode).__name__!r}")
        import os
        import warnings
        import itertools
        import collections
        # collections.Counter 统计可迭代对象 每项出现的次数
        # itertools.product 求多个可迭代对象的笛卡尔积
        mode_list = [collections.Counter(i+j) for i, j in itertools.product("wa", ("b", "b+", "", "+"))]
        if collections.Counter(mode) in mode_list:
            os.makedirs(os.path.dirname(file), exist_ok=True)
        # 二进制模式下 encoding=None
        if mode.find("b") != -1 and encoding is not None:
            warnings.warn(
                "binary mode doesn't take an encoding argument",
                DeprecationWarning,
                stacklevel=4
            )
            encoding = None
        return func(file, mode, buffering, encoding, errors, newline, closefd, opener)
    return wrapper


make_open = _make_open(open)


# User Agent
def get_user_agent(ua: Optional[str] = None, overwrite: bool = False) -> Union[str, Any]:
    """获取 UserAgent，默认 Android

    :param ua: 模糊查找内置字典User-Agent (android, windows, mac, iphone, ipad, symbian, apad)
    :param overwrite: 若为True, 直接返回  User-Agent
    :return: "User-Agent"
    """
    # 重写 UserAgent
    if overwrite:
        return ua
    # UserAgent 全部字典
    user_agent_dict = {
        "android": "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36",
        "windows": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        "mac": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        "iphone": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        "ipad": "Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1",
        "symbian": "Mozilla/5.0 (Symbian/3; Series60/5.2 NokiaN8-00/012.002; Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/533.4 (KHTML, like Gecko) NokiaBrowser/7.3.0 Mobile Safari/533.4 3gpp-gba",
        "apad": "Mozilla/5.0 (Linux; Android 11; Phh-Treble vanilla Build/RQ3A.211001.001;) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/90.0.4430.91 Safari/537.36",
    }
    # 默认UserAgent
    if not ua or not isinstance(ua, str):
        return user_agent_dict["android"]
    # 模糊查找UserAgent
    import difflib
    ua = difflib.get_close_matches(ua.lower(), user_agent_dict.keys(), 1)
    if not ua:
        return user_agent_dict["android"]
    return user_agent_dict[ua[0]]


# Headers
def default_headers(ua: Optional[str] = None):
    """Headers

    :param ua: user-agent
    :return: {"User-Agent": str}
    """
    return {"User-Agent": get_user_agent(ua)}


# md5 加密
def md5(plaintext: Union[str, bytes], encoding: Optional[str] = None):
    """MD5加密

    :param plaintext: 需加密明文
    :param encoding: plaintext编码
    :return: {"plaintext": str, "ciphertext": str}
    """
    result = {"plaintext": None, "ciphertext": None}
    if isinstance(plaintext, str):
        plaintext = plaintext.encode(encoding=encoding or "utf-8")
    elif not isinstance(plaintext, bytes):
        result["plaintext"] = plaintext
        return result
    # md5加密
    import hashlib
    ciphertext = hashlib.md5(plaintext).hexdigest()
    result["plaintext"], result["ciphertext"] = plaintext, ciphertext
    return result


# hash256
def hash256(plaintext: Union[str, bytes], encoding: Optional[str] = None):
    """HASH_256加密

    :param plaintext: 需加密明文
    :param encoding: plaintext编码
    :return: {"plaintext": str, "ciphertext": str}
    """
    result = {"plaintext": None, "ciphertext": None}
    if isinstance(plaintext, str):
        plaintext = plaintext.encode(encoding=encoding or "utf-8")
    elif not isinstance(plaintext, bytes):
        result["plaintext"] = plaintext
        return result
    # hash256加密
    import hashlib
    ciphertext = hashlib.sha256(plaintext).hexdigest()
    result["plaintext"], result["ciphertext"] = plaintext, ciphertext
    return result


# 判断base64数据类型
def is_base64_from_regex(data: Union[str, bytes]) -> bool:
    """判断是否为base64数据类型

    :param data: 需检测的数据
    :return: bool
    """
    import re
    if isinstance(data, bytes):
        # base64 数据类型 正则表达式判断
        pattern_from_bytes = re.compile(rb"^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$")
        return bool(pattern_from_bytes.match(data))

    if isinstance(data, str):
        # base64 数据类型 正则表达式判断
        pattern_from_string = re.compile(r"^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$")
        return bool(pattern_from_string.match(data))
    # str 或 bytes 以外类型返回 False
    return False


# base64数据类型 转化为bytes
def base64_conversion_bytes(data: Union[str, bytes], encoding: str = "utf-8"):
    """base64数据类型 转化为bytes

    :param data: data: 需要 base64 解密的数据
    :param encoding: encoding: type(data) is 'str' 通过 encoding 转换为 bytes
    :return: Tuple(bool, data)
    """
    if (
        not isinstance(data, (str, bytes))
        or not is_base64_from_regex(data)
    ):
        return False, data
    if isinstance(data, str):
        data = data.encode(encoding)
    import base64
    return True, base64.b64decode(data)


# 重命名本地存在的文件
def rename_file(file: str, suffix: Optional[str] = None):
    """重命名本地存在的文件

    :param file: 文件路径
    :param suffix: 文件后缀名
    :return: Tuple(rename_file, dir_name, basename)
    """
    import os
    import itertools
    # 绝对路径
    file = os.path.normpath(os.path.abspath(file))
    # 后缀名解析
    if not isinstance(suffix, str) or not suffix:
        file_split, suffix = file.rsplit(".", 1), ""
        if len(file_split) == 2 and len(file_split[-1]) < 6:
            suffix = file_split[-1]
    suffix = "." + suffix.strip().removeprefix(".") if suffix.strip() else suffix.strip()
    # 完整文件路径
    if not file.endswith(suffix):
        file += suffix

    if not os.path.isfile(file):
        return file, *os.path.split(file)
    newfile = None
    for index in itertools.count(1):
        newfile = file.removesuffix(suffix) + f".{index}" + suffix
        if not os.path.isfile(newfile):
            break
    return newfile, *os.path.split(newfile)


# 重命名本地存在的文件夹
def rename_folder(folder: str):
    """重命名本地存在的文件夹

    :param folder: 文件夹路径
    :return: Tuple(rename_folder, dir_name, basename)
    """
    import os
    import itertools
    folder = os.path.abspath(folder)
    if not os.path.isdir(folder):
        return folder, *os.path.split(folder)
    new_folder = None
    for index in itertools.count(1):
        new_folder = folder + f".{index}"
        if not os.path.isdir(new_folder):
            break
    return new_folder, *os.path.split(new_folder)


# 字符串转换为数字
def string_conversion_digits(target: Union[str, int, float], default: Any = None):
    """字符串转换为数字

    :param target: 需要转换的目标
    :param default: 返回默认值
    :return: {"is_digits": bool, "original": Any, "converted": digits}
    """
    result = {"is_digits": False, "original": target, "converted": default}
    # target type = `int` or `float`
    if isinstance(target, (int, float)):
        result["is_digits"], result["converted"] = True, target
        return result
    # target type != `str`
    if not isinstance(target, str):
        return result

    # 判断字符串是否为数字
    def is_digits(string):
        import re
        pattern = re.compile(r"^(?P<symbol>-)?(?P<int>\d+)(?P<float>\.\d+)?$")
        ret = pattern.match(string)
        if not ret:
            return {"is_digits": False, "type": None}
        ret = ret.groupdict()
        return {"is_digits": True, "type": float if ret["float"] is not None else int}
    # 转换为数字
    ret = is_digits(target)
    if ret["is_digits"]:
        result["is_digits"], result["converted"] = True, ret["type"](target)
    return result


# 人类直观时间展示
def human_playtime(playtime: Union[str, int, float]):
    """人类直观时间展示

    :param playtime: 传入一个时间(秒), 返回人类能理解的时间格式
    :return: str
    """
    digits = string_conversion_digits(playtime)
    if not digits["is_digits"]:
        return None
    playtime = digits["converted"]
    symbol, playtime = "-" if playtime < 0 else "", round(abs(playtime))
    hour, second = divmod(playtime, 3600)
    minute, second = divmod(second, 60)
    return f"{symbol}{hour}:{minute:0>2}:{second:0>2}"


# python模块转换懒加载
def pycode_conversion_lazyloader(string: str):
    """python代码中的导入模块转换为懒加载

    :param string: python代码
    :return: str
    """
    import re
    pattern = re.compile(
        r"^from\s+?(?P<from_name>\S+)\s+?import\s+?(?P<from_import_name>\S+)\s*?(as\s+?(?P<from_import_alias>\S+))?$|^import\s+?(?P<import_name>\S+)(\s+?as\s+(?P<import_alias>\S+?))?\s*?$",
        flags=re.M
    )

    def repl_string(match):
        match_dict = match.groupdict()
        import_name, alias = None, None
        result = '{alias} = LazyLoader("{alias}", globals(), "{import_name}")'
        # from导入
        if match_dict["from_name"]:
            import_name = f'{match_dict["from_name"]}.{match_dict["from_import_name"]}'
            alias = match_dict["from_import_name"]
        else:
            import_name = f'{match_dict["import_name"]}'
            alias = match_dict["import_name"]
        # alias
        if match_dict["from_import_alias"]:
            alias = match_dict["from_import_alias"]
        elif match_dict["import_alias"]:
            alias = match_dict["import_alias"]
        return result.format(alias=alias, import_name=import_name)

    # 替换懒加载
    string = pattern.sub(repl=repl_string, string=string)
    return string


# python模块转换懒加载 从文件
def pyfile_conversion_lazyloader(read_file: str, write_file: str, encoding: Optional[str] = None):
    """python文件中的导入模块转换为懒加载

    :param read_file: 读取python代码文件
    :param write_file: 写入转换后的python代码文件
    :param encoding: 文件编码
    """
    with open(read_file, "r", encoding=encoding) as read_fileobj:
        content = pycode_conversion_lazyloader(read_fileobj.read())
    with open(write_file, "w", encoding=encoding) as write_fileobj:
        write_fileobj.write(content)


# 字节单位自动换算
def units_conversion_from_byte(target: Union[int, float]):
    """字节单位自动换算

    :param target: 换算目标(Bytes)
    :return: str
    """
    target = string_conversion_digits(target)
    if not target["is_digits"]:
        return None
    target, target_units = abs(target["converted"]), "Bytes"
    units_dict = {"Bytes": 1, "KB": 1024, "MB": 1024, "GB": 1024, "TB": 1024, "PB": 1024, "EB": 1024, "ZB": 1024, "YB": 1024, "BB": 1024}
    for units, rate in units_dict.items():
        if target >= rate:
            target, target_units = target/rate, units
            continue
        break
    return f"{round(target, 2)}{target_units}"


# 下载进度条
def download_column(
    *,
    start: bool = True,
    total: Optional[float] = None,
    console: Optional[object] = None,
    add_task: bool = False,
    progress: Optional[object] = None,
    completed: Optional[float] = None,
    transient: bool = False,
    description: Optional[str] = None,
    show_transfer_speed: bool = True,
):
    """rich.progress - 下载进度条

    :param start: 立即启动任务，如果为 False 则需要手动启动
    :param total: 进度总步数
    :param console: rich.console.Console
    :param add_task: 是否添加进度任务 默认False
    :param progress: rich.progress.Progress类 默认自动创建
    :param completed: task 已完成步数 默认为0
    :param transient: 转瞬即逝
    :param description: 任务描述
    :param show_transfer_speed: 显示任务速度
    :return:
        `add_task` is `True`  -> progress, task
        `add_task` is `False` -> progress
    """
    import rich.progress as rich_progress
    if not isinstance(progress, rich_progress.Progress):
        column = [
            rich_progress.TextColumn("[progress.description]{task.description}"),
            rich_progress.TaskProgressColumn("[progress.percentage]{task.percentage:>6.2f}%"),
            rich_progress.BarColumn(),
            rich_progress.DownloadColumn(),
            rich_progress.TimeElapsedColumn(),
        ]
        if show_transfer_speed:
            column.insert(-1, rich_progress.TransferSpeedColumn())
        progress = rich_progress.Progress(*column,transient=transient, console=console)
    # 添加任务
    if add_task or total is not None:
        task = progress.add_task(
            total=total,
            start=start,
            description=description or "",
            completed=completed or 0
        )
        return progress, task
    return progress


# 任务进度条
def progress_column(
    *,
    start: bool = True,
    total: Optional[float] = None,
    console: Optional[object] = None,
    add_task: bool = False,
    progress: Optional[object] = None,
    completed: Optional[float] = None,
    transient: bool = False,
    description: Optional[str] = None,
    show_transfer_speed: bool = False,
):
    """rich.progress - 任务进度条

    :param start: 立即启动任务，如果为 False 则需要手动启动
    :param total: 进度总步数
    :param console: rich.console.Console
    :param add_task: 是否添加进度任务 默认False
    :param progress: rich.progress.Progress类 默认自动创建
    :param completed: task 已完成步数 默认为0
    :param transient: 转瞬即逝
    :param description: 任务描述
    :param show_transfer_speed: 显示任务速度
    :return:
        `add_task` is `True`  -> progress, task
        `add_task` is `False` -> progress
    """
    import rich.progress as rich_progress
    if not isinstance(progress, rich_progress.Progress):
        column = [
            rich_progress.TextColumn("[progress.description]{task.description}"),
            rich_progress.TaskProgressColumn("[progress.percentage]{task.percentage:>6.2f}%"),
            rich_progress.BarColumn(),
            rich_progress.TaskProgressColumn("[cyan]{task.completed}/{task.total}[/]"),
            rich_progress.TimeElapsedColumn(),
        ]
        if show_transfer_speed:
            column.insert(-1, rich_progress.TransferSpeedColumn())
        progress = rich_progress.Progress(*column,transient=transient, console=console)
    # 添加任务
    if add_task or total is not None:
        task = progress.add_task(
            total=total,
            start=start,
            description=description or "",
            completed=completed or 0
        )
        return progress, task
    return progress


def chardet(byte: bytes):
    """字符编码判断

    :param byte: bytes数据
    :return: {'encoding': str, 'language': str, 'confidence': float}
    """
    try:
        import chardet as _chardet
    except ImportError:
        import charset_normalizer as _chardet
    return _chardet.detect(byte)
