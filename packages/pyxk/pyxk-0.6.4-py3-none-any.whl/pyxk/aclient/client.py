import asyncio
import warnings
from typing import (
    Any,
    List,
    Tuple,
    Union,
    Optional,
    Mapping,
    Pattern,
    Callable
)
from types import MethodType
from itertools import zip_longest
from multidict import CIMultiDict

from pyxk.utils import (
    chardet,
    LazyLoader,
    get_user_agent,
    default_headers,
)
from pyxk.aclient.typedef import (
    StrOrURL,
    Session,
    Response,
    EventLoop,
    CIMDict,
    Timeout,
    URLS
)

_copy = LazyLoader("_copy", globals(), "copy")
_yarl = LazyLoader("_yarl", globals(), "yarl")
aiohttp = LazyLoader("aiohttp", globals(), "aiohttp")
_selector = LazyLoader("_selector", globals(), "parsel.selector")
aiohttp_client_exceptions = LazyLoader("aiohttp_client_exceptions", globals(), "aiohttp.client_exceptions")

__all__ = ["Client", "Response"]


class Client:
    """异步下载器

    explain:
    from pyxk import Client, Response

    class Download(Client):
        start_urls = ['http://www.baidu.com' for _ in range(10)]

        async def parse(self, response: Response, **kwargs):
            print(response.url)

    Download.run()
    """
    limit: Optional[int] = None
    timeout: Timeout = None
    req_kwargs: Optional[Union[dict, List[dict]]] = None
    async_sleep: Optional[int] = None
    maximum_retry: Optional[int] = None
    headers: Optional[Union[dict, CIMDict]] = None
    semaphore: Union[Optional[int], asyncio.Semaphore] = None
    verify: Optional[bool] = None
    start_urls: Union[List[str], List[Tuple[str, dict]]] = []
    user_agent: Optional[str] = None
    aiohttp_kwargs: Optional[dict] = None
    retry_status_code: Optional[list] = None
    error_status_code: Optional[list] = None
    until_request_succeed: Optional[Union[bool, List[int]]] = None

    ATTR = (
        ("limit", 100),
        ("timeout", 7),
        ("headers", CIMultiDict(default_headers())),
        ("semaphore", 16),
        ("verify", True),
        ("async_sleep", 1),
        ("maximum_retry", 20),
        ("user_agent", get_user_agent()),
        ("aiohttp_kwargs", {}),
        ("until_request_succeed", False),
    )

    def __init__(self, *, base_url: StrOrURL = None, **kwargs):
        """异步下载器 init

        :param limit: aiohttp 并发控制
        :param timeout: 请求超时时间
        :param req_kwargs: start_request请求参数
        :param async_sleep: 异步休眠时间
        :param maximum_retry: 异步请求最大重试次数
        :param headers: 请求头
        :param semaphore: asyncio并发控制
        :param verify: ssl验证
        :param start_urls: 请求入口urls
        :param user_agent: User-Agent
        :param aiohttp_kwargs: aiohttp.ClientSession 实例化参数
        :param retry_status_code: 请求状态码，包含在列表中的进行重新发送
        :param error_status_code: 请求状态码，包含在列表中直接抛出错误
        :param until_request_succeed: 请求状态码，直到请求响应成功(可自定义响应状态码)
        :param base_url: base_url 每个请求URL进行拼接
        :param kwargs: **kwargs 关键字参数进行实例化
        """
        for key, val in kwargs.items():
            setattr(self, key, val)
        # event loop
        self._loop: EventLoop = None
        # aiohttp session
        self._session: Session = None
        # base_url
        self._base_url: StrOrURL = self.set_base_url(base_url)

    @classmethod
    def run(cls, **kwargs):
        """程序运行入口 - 应该调用该方法运行

        :params: **kwargs: 类实例化关键字参数
        """
        self = cls(**kwargs)
        # 创建新的 event loop
        try:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            # 运行
            self._loop.run_until_complete(self.async_start())
        finally:
            asyncio.set_event_loop(None)
            if self._loop:
                # 关闭 event loop
                self._loop.close()
        return self

    @property
    def attr(self):
        """默认变量ATTR"""
        return dict(self.ATTR)

    async def async_start(self) -> None:
        """开启异步下载器"""
        try:
            # event loop
            if (
                not self._loop
                or not isinstance(self._loop, asyncio.AbstractEventLoop)
                or self._loop.is_closed()
            ):
                self._loop = asyncio.get_event_loop()
                asyncio.set_event_loop(self._loop)
            # semaphore
            if not isinstance(self.semaphore, (int, float)) or self.semaphore < 0:
                self.semaphore = self.attr["semaphore"]
            self.semaphore = asyncio.Semaphore(self.semaphore)
            # aiohttp kwargs
            aiohttp_kwargs = self.aiohttp_kwargs \
                if isinstance(self.aiohttp_kwargs, dict) \
                else self.attr["aiohttp_kwargs"]
            aiohttp_kwargs = _copy.deepcopy(aiohttp_kwargs)
            # timeout
            if not aiohttp_kwargs.__contains__("timeout"):
                if not isinstance(self.timeout, aiohttp.ClientTimeout):
                    timeout = aiohttp.ClientTimeout(
                        total=self.timeout
                        if isinstance(self.timeout, (int, float)) and self.timeout > 0
                        else self.attr["timeout"]
                    )
                else:
                    timeout = self.timeout
                aiohttp_kwargs["timeout"] = timeout
            # connector
            if not aiohttp_kwargs.__contains__("connector"):
                aiohttp_kwargs["connector"] = aiohttp.TCPConnector(
                    loop=self._loop,
                    limit=self.limit
                    if isinstance(self.limit, int) and self.limit > 0
                    else self.attr["limit"],
                    ssl=bool(self.verify)
                    if self.verify is not None
                    else self.attr["verify"],
                )
            # headers
            if aiohttp_kwargs.__contains__("headers"):
                headers = self.headers \
                    if self.headers \
                    else aiohttp_kwargs.pop("headers")
                if not isinstance(headers, (dict, CIMultiDict)):
                    headers = {}
            else:
                headers = self.headers \
                    if isinstance(self.headers, (dict, CIMultiDict)) \
                    else self.attr["headers"]
            headers = CIMultiDict(_copy.deepcopy(headers))
            # User Agent
            if self.user_agent and isinstance(self.user_agent, str):
                headers["User-Agent"] = self.user_agent
            else:
                headers.setdefault("User-Agent", self.attr["user_agent"])
            aiohttp_kwargs["headers"] = headers
            # 创建 aiohttp client_session
            self._session = aiohttp.ClientSession(loop=self._loop, **aiohttp_kwargs)
            # 开始运行
            await self.start()
            result = await self.start_request()
            await self.completed(result)
        finally:
            await self.async_close()

    async def async_close(self):
        """关闭异步下载器"""
        await self.close()
        # 关闭 aiohttp client session
        if isinstance(self._session, aiohttp.ClientSession) and self._session.closed is False:
            await self._session.close()

    async def start_request(self):
        """start_urls 默认运行方法"""
        if not self.start_urls or not isinstance(self.start_urls, (list, tuple)):
            raise NotImplementedError(f"{self.__class__.__name__}.start_urls is not available!")
        # req_kwargs
        req_kwargs = self.req_kwargs
        if not req_kwargs or not isinstance(req_kwargs, dict):
            req_kwargs = {}
        return await self.gather(
            self.start_urls,
            self.parse,
            cb_kwargs_list=req_kwargs,
            automatic_base_url=True
        )

    async def request(
        self,
        url: StrOrURL,
        callback: Optional[Callable] = None,
        *,
        method: str = "GET",
        cb_kwargs: Optional[dict] = None,
        **req_kwargs
    ) -> Union[Response, Any]:
        """异步请求发送以及回调

        :param url: URL
        :param callback: 响应response 回调函数(函数是异步的)
        :param method: 请求方法(default: GET)
        :param cb_kwargs: 传递给回调函数的关键字参数
        :param req_kwargs: 异步请求 request参数
        :return: Response, Any
        """
        retry, exc_count, ret, response = 0, 0, None, None
        maximum_retry = self.maximum_retry \
            if isinstance(self.maximum_retry, int) and self.maximum_retry > 0 \
            else self.attr["maximum_retry"]
        async with self.semaphore:
            url = self.build_url(url)
            while True:
                try:
                    response = await self._session.request(method=method, url=url, **req_kwargs)
                    # 抛出 error status_code
                    if isinstance(self.error_status_code, (list, tuple)) and response.status in self.error_status_code:
                        raise aiohttp.InvalidURL(f"<Response[{response.status}] {url}>")
                    # 重试 retry status_code
                    if isinstance(self.retry_status_code, (list, tuple)) and response.status in self.retry_status_code:
                        response.close()
                        retry += 1
                        if retry % 10 == 0:
                            warnings.warn(f"<Response[{response.status}] {url}>, Retry: {retry}", stacklevel=4)
                        await self.sleep()
                        continue
                    # 直到请求状态码200才返回 until_request_succeed
                    as_succeed = self.until_request_succeed \
                        if self.until_request_succeed is not None else self.attr["until_request_succeed"]
                    if not isinstance(as_succeed, (list, tuple)):
                        as_succeed = [200] if as_succeed else []
                    if as_succeed and response.status not in as_succeed:
                        response.close()
                        retry += 1
                        if retry % 10 == 0:
                            warnings.warn(f"<Response[{response.status}] {url}>, Retry: {retry}", stacklevel=4)
                        await self.sleep()
                        continue
                    # 添加自定义方法
                    add_method_to_response(response)
                    # 开启回调函数
                    if callable(callback):
                        cb_kwargs = dict(cb_kwargs or {})
                        ret = await callback(response, **cb_kwargs)
                        response.close()
                    else:
                        ret = response
                    break
                # 请求超时 重试
                except asyncio.exceptions.TimeoutError:
                    if response:
                        response.close()
                    exc_count += 1
                    if exc_count >= maximum_retry:
                        raise
                    # warnings.warn(f"<{url}> Timeout", stacklevel=4)
                    await self.sleep()
                # 连接错误 重试
                except (
                    aiohttp_client_exceptions.ClientOSError,
                    aiohttp_client_exceptions.ClientPayloadError,
                    aiohttp_client_exceptions.ClientConnectorError,
                ):
                    if response:
                        response.close()
                    exc_count += 1
                    if exc_count >= maximum_retry:
                        raise
                    # warnings.warn(f"<{url}> ConnectorError", stacklevel=4)
                    await self.sleep()
                # 服务器拒绝连接
                except aiohttp_client_exceptions.ServerDisconnectedError:
                    if response:
                        response.close()
                    exc_count += 1
                    if exc_count >= maximum_retry:
                        raise
                    # warnings.warn(f"<{url}> ServerDisconnectedError", stacklevel=4)
                    await self.sleep()
            return ret

    async def gather(
        self,
        urls: URLS,
        callback: Optional[Callable] = None,
        *,
        method: str = "GET",
        cb_kwargs_list: Optional[Union[List[dict], dict]] = None,
        return_exceptions: bool = False,
        automatic_base_url: bool = False,
        **req_kwargs
    ) -> list:
        """发送url列表，创建异步任务 并发发送

        :param urls: Url List
        :param callback: 响应response 回调函数(函数是异步的)
        :param method: 请求方法(default: GET)
        :param cb_kwargs_list: 回调函数关键字参数列表
        :param return_exceptions: 错误传递(default: False)
        :param req_kwargs: 异步请求 request参数
        :return: list
        """
        if not isinstance(urls, (list, tuple)):
            raise TypeError(f"urls must be 'tuple' or 'list', not {type(urls).__name__!r}")
        length = len(urls)
        # parse cb_kwargs_list
        if isinstance(cb_kwargs_list, dict):
            cb_kwargs_list = [cb_kwargs_list for _ in range(length)]
        elif isinstance(cb_kwargs_list, (list, tuple)):
            cb_kwargs_list = cb_kwargs_list[:length]
            if len(cb_kwargs_list) < length:
                cb_kwargs_list.extend([{} for _ in range(length-len(cb_kwargs_list))])
        else:
            cb_kwargs_list = [{} for _ in range(length)]
        # parse urls
        for index, item in enumerate(urls):
            url, cb_kwargs = None, None
            if isinstance(item, (list, tuple)) and len(item) >= 2:
                url, cb_kwargs = item[0], dict(item[1])
            else:
                url, cb_kwargs = item, {}
            urls[index] = url
            cb_kwargs.update(cb_kwargs_list[index])
            cb_kwargs_list[index] = cb_kwargs
        # 收集任务
        tasks = []
        for url, cb_kwargs in zip_longest(urls, cb_kwargs_list):
            # base url
            if automatic_base_url and not self.base_url:
                self.base_url = url
            task = self.request(
                url=url,
                callback=callback,
                method=method,
                cb_kwargs=cb_kwargs,
                **req_kwargs
            )
            tasks.append(task)
        result = await asyncio.gather(*tasks, return_exceptions=return_exceptions)
        return result

    async def sleep(self, delay: Optional[Union[int, float]] = None, result: Any = None):
        """异步休眠

        :param delay: 休眠时间
        :param result: 返回值
        :return: result
        """
        if not isinstance(delay, (int, float)) or delay < 0:
            delay = self.async_sleep \
                if isinstance(self.async_sleep, (int, float)) and self.async_sleep >= 0 \
                else self.attr["async_sleep"]
        return await asyncio.sleep(delay, result=result)

    def build_url(self, _url) -> StrOrURL:
        """构造完整url地址"""
        if not isinstance(_url, (str, _yarl.URL)):
            return _url
        _url = _yarl.URL(_url)
        if _url.is_absolute():
            return _url
        if self._base_url and isinstance(self._base_url, _yarl.URL):
            return self._base_url.join(_url)
        return _url

    @staticmethod
    def set_base_url(url: StrOrURL) -> StrOrURL:
        """设置 base_url"""
        if not url or not isinstance(url, (str, _yarl.URL)):
            return None
        url = _yarl.URL(url)
        if not url.is_absolute():
            # 不是绝对路径
            return None
        return url

    @property
    def loop(self) -> EventLoop:
        """event loop"""
        return self._loop

    @property
    def base_url(self) -> StrOrURL:
        """base_url"""
        return self._base_url

    @base_url.setter
    def base_url(self, _url: StrOrURL):
        self._base_url = self.set_base_url(_url)

    async def parse(self, response: Response, **kwargs):
        """默认解析函数"""
        raise NotImplementedError(f"'{self.__class__.__name__}.parse' not implemented!")

    async def completed(self, result: list):
        """运行完成结果回调函数"""

    async def start(self):
        """创建 aiohttp session 后调用"""

    async def close(self):
        """关闭 aiohttp session 前调用"""

async def xpath(
    self,
    query: str,
    namespaces: Optional[Mapping[str, str]] = None,
    encoding: Optional[str] = None,
    type: Optional[str] = None,
    root: Optional[Any] = None,
    base_url: Optional[str] = None,
    _expr: Optional[str] = None,
    huge_tree: Optional[bool] = None,
    errors: str = "strict",
    **kwargs
):
    """Response.xpath"""
    text = await self.text(encoding=encoding, errors=errors)
    selector = _selector.Selector(
        text=text,
        type=type,
        _expr=_expr,
        namespaces=namespaces,
        root=root or _selector._NOT_SET,
        base_url=base_url,
        huge_tree=huge_tree or _selector.LXML_SUPPORTS_HUGE_TREE,
    )
    return selector.xpath(query=query, **kwargs)

async def css(
    self,
    query: str,
    namespaces: Optional[Mapping[str, str]] = None,
    encoding: Optional[str] = None,
    type: Optional[str] = None,
    root: Optional[Any] = None,
    base_url: Optional[str] = None,
    _expr: Optional[str] = None,
    huge_tree: Optional[bool] = None,
    errors: str = "strict"
):
    """Response.css"""
    text = await self.text(encoding=encoding, errors=errors)
    selector = _selector.Selector(
        text=text,
        type=type,
        _expr=_expr,
        namespaces=namespaces,
        root=root or _selector._NOT_SET,
        base_url=base_url,
        huge_tree=huge_tree or _selector.LXML_SUPPORTS_HUGE_TREE,
    )
    return selector.css(query=query)

async def re(
    self,
    regex: Union[str, Pattern[str]],
    replace_entities: bool = True,
    namespaces: Optional[Mapping[str, str]] = None,
    encoding: Optional[str] = None,
    type: Optional[str] = None,
    root: Optional[Any] = None,
    base_url: Optional[str] = None,
    _expr: Optional[str] = None,
    huge_tree: Optional[bool] = None,
    errors: str = "strict",
):
    """Response.re"""
    text = await self.text(encoding=encoding, errors=errors)
    selector = _selector.Selector(
        text=text,
        type=type,
        _expr=_expr,
        namespaces=namespaces,
        root=root or _selector._NOT_SET,
        base_url=base_url,
        huge_tree=huge_tree or _selector.LXML_SUPPORTS_HUGE_TREE,
    )
    return selector.re(regex=regex, replace_entities=replace_entities)

def urljoin(self, _url):
    """Response.urljoin"""
    if isinstance(_url, str):
        _url = _yarl.URL(_url)
    elif not isinstance(_url, _yarl.URL):
        return _url
    if _url.is_absolute():
        return _url
    return self.url.join(_url)

async def apparent_encoding(self):
    """Response.apparent_encoding"""
    byte = await self.read()
    return chardet(byte)["encoding"]

def add_method_to_response(response):
    """为异步response添加实例方法"""
    response.re = MethodType(re, response)
    response.css = MethodType(css, response)
    response.xpath = MethodType(xpath, response)
    response.urljoin = MethodType(urljoin, response)
    response.apparent_encoding = MethodType(apparent_encoding, response)
