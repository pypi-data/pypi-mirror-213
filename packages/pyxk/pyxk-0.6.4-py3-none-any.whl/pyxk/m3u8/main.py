"""m3u8资源解析和下载"""
import os
from typing import Union, Optional

from pyxk.utils import (
    rename_file,
    hash256,
    make_open,
    LazyLoader,
    progress_column,
    download_column,
    human_playtime
)
from pyxk.m3u8.m3u8parse import M3U8Parse
from pyxk.m3u8.m3u8download import Downloader

_rich_box = LazyLoader("_rich_box", globals(), "rich.box")
_rich_live = LazyLoader("_rich_live", globals(), "rich.live")
_rich_table = LazyLoader("_rich_table", globals(), "rich.table")
_rich_panel = LazyLoader("_rich_panel", globals(), "rich.panel")
_rich_console = LazyLoader("_rich_console", globals(), "rich.console")
_requests = LazyLoader("_requests", globals(), "pyxk.requests")


class M3U8:
    """m3u8资源下载器"""
    def __init__(self):
        # m3u8文件输出
        self._output = None
        # m3u8下载存储路径
        self._temp_file = None
        # 重新下载
        self._reload = False
        # 下载完成后保留m3u8文件
        self._reserve = False
        # request - verify
        self._verify = True
        # request - headers
        self._headers = None
        # limit
        self._limit = 16
        # user agent
        self._user_agent = None
        self._session = None
        self._console = _rich_console.Console()

    @property
    def output(self):
        """output"""
        return self._output

    @output.setter
    def output(self, path: Optional[str]) -> None:
        if path and isinstance(path, str):
            path = "_".join(path.split(" "))
            path = os.path.normpath(os.path.abspath(path))
        else:
            self._output, self._temp_file = None, None
            return
        self._output, dir_name, basename = rename_file(path, suffix="mp4")
        self._temp_file = os.path.join(dir_name, f".{basename.removesuffix('.mp4')}_temp")

    def load_url(
        self,
        url: str,
        *,
        output: Optional[str] = None,
        reload: bool = False,
        reserve: bool = False,
        headers: Optional[dict] = None,
        verify: bool = True,
        limit: int = 16,
        user_agent: Optional[str] = None,
    ):
        """使用m3u8链接下载资源

        :param url: m3u8 url
        :param output: m3u8资源输出到文件
        :param reload: 重新从网络加载m3u8文件
        :param reserve: 下载完成后保留m3u8文件
        :param headers: request 请求头
        :param verify: request verify
        :param limit: 异步下载并发量
        :param user_agent: User-Agent
        """
        self.output, self._limit = output, limit if isinstance(limit, int) and limit > 0 else 16
        self._reload, self._reserve = bool(reload), bool(reserve)
        self._headers, self._verify = headers, bool(verify)
        self._user_agent = user_agent if user_agent and isinstance(user_agent, str) else None
        self._session = _requests.Session(user_agent=self._user_agent)
        # 关闭requests警告
        if self._verify is False:
            import urllib3
            urllib3.disable_warnings()
        content = self.get_m3u8_content(url)
        # 无效m3u8内容
        if not self._is_m3u8_content(content):
            self._console.print("[red b]m3u8 url is not available!")
            return None
        # 解析m3u8
        return self.start_parse(content=content, url=url)

    def load_content(
        self,
        content: str,
        url: Optional[str] = None,
        *,
        output: Optional[str] = None,
        reload: bool = False,
        reserve: bool = False,
        headers: Optional[dict] = None,
        verify: bool = True,
        limit: int = 16,
        user_agent: Optional[str] = None,
    ):
        """使用m3u8文件下载资源

        :param content: m3u8内容 或 m3u8本地文件路径
        :param url: m3u8 url
        :param output: m3u8资源输出到文件
        :param reload: 重新从网络加载m3u8文件
        :param reserve: 下载完成后保留m3u8文件
        :param headers: request 请求头
        :param verify: request verify
        :param limit: 异步下载并发量
        :param user_agent: User-Agent
        """
        self.output, self._limit = output, limit if isinstance(limit, int) and limit > 0 else 16
        self._reload, self._reserve = bool(reload), bool(reserve)
        self._headers, self._verify = headers, bool(verify)
        self._user_agent = user_agent if user_agent and isinstance(user_agent, str) else None
        self._session = _requests.Session(user_agent=self._user_agent)
        # 关闭requests警告
        if self._verify is False:
            import urllib3
            urllib3.disable_warnings()
        # 无效m3u8内容
        if not self._is_m3u8_content(content):
            m3u8file = os.path.normpath(os.path.abspath(content)) if isinstance(content, str) else None
            if m3u8file and os.path.isfile(m3u8file):
                with open(m3u8file, "r", encoding="utf-8") as read_fileobj:
                    content = read_fileobj.read()
                    if not self._is_m3u8_content(content):
                        self._console.print("[red b]m3u8 content is not available![/]")
                        return None
            else:
                self._console.print("[red b]m3u8 content is not available![/]")
                return None
        # 解析m3u8
        return self.start_parse(content=content, url=url)

    def start_parse(self, content: str, url: Optional[str]):
        """开始解析m3u8内容

        :param content: m3u8 内容
        :param url: m3u8 链接
        """
        m3u8parse = M3U8Parse.run(content=content, url=url, instance=self)
        # 可视化内容
        table = _rich_table.Table(show_header=False, box=_rich_box.SIMPLE_HEAD, padding=0)
        table.add_column(justify="left", overflow="fold")
        # table1 = _rich_table.Table(show_header=False, box=_rich_box.SIMPLE_HEAD, padding=0)
        # table1.add_column(justify="left", overflow="ellipsis")
        # table1.add_row(f"[yellow b]url[/]: [blue u]{url}[/]")
        table.add_row(f"[yellow b]url[/]: [blue u]{url}[/]")
        table.add_section()
        table.add_row(f"[yellow b]maximum[/]: {m3u8parse['maximum']}")
        table.add_row(f"[yellow b]duration[/]: {human_playtime(m3u8parse['duration'])}")
        table.add_row(f"[yellow b]encryption[/]: {bool(m3u8parse['m3u8keys'])}")
        table.add_row(f"[yellow b]output[/]: [blue]{self.output}[/]")
        # 添加进度条
        progress, download = None, None
        if m3u8parse["segments"] and self.output and self._temp_file:
            progress = progress_column(add_task=False)
            download = download_column(add_task=False, show_transfer_speed=False)
            table.add_section()
            table.add_row(progress)
            table.add_row(download)
        panel = _rich_panel.Panel(
            table,
            subtitle=f"[dim i]limit: {self._limit}[/]",
            subtitle_align="right",
            border_style="bright_blue",
            title="[red]M3U8 Download[/]",
            title_align="center",
        )
        # 下载 segments
        live = _rich_live.Live(panel, console=self._console)
        with live:
            Downloader.run(
                m3obj=self,
                m3u8keys=m3u8parse["m3u8keys"],
                segments=m3u8parse["segments"],
                progress=progress,
                download=download
            )
        # 删除m3u8文件
        if not self._reserve and self._temp_file:
            import shutil
            if os.path.isdir(self._temp_file):
                shutil.rmtree(self._temp_file)
            
    def get_m3u8_content(
        self, url: Optional[str], *, is_m3u8key: bool = False
    ) -> Optional[Union[str, bytes]]:
        """获取m3u8内容

        :param url: url
        :param is_m3u8key: m3u8 key(type: bool)
        :return: str, bytes
        """
        if not(url and isinstance(url, str)):
            return None
        # 文件完整路径
        file = self._generate_filename(url, is_m3u8key)
        mode, attr, encoding = "r", "text", "utf-8"
        if is_m3u8key:
            mode, attr, encoding = "rb", "content", None
        # 获取网络资源
        if self._reload or not file or not os.path.isfile(file):
            response = self._session.get(url, headers=self._headers, verify=self._verify, timeout=10)
            if response.status_code != 200:
                self._console.print(f"[red]<Response [{response.status_code}] {url}>[/]")
            content = getattr(response, attr)
        # 获取本地资源
        else:
            with open(file, mode, encoding=encoding) as read_fileobj:
                content = read_fileobj.read()
        return content

    def sava_m3u8_content(
        self,
        url: Optional[str],
        content: Union[str, bytes],
        *,
        is_m3u8key: bool = False
    ):
        """保存m3u8内容

        :param url: url
        :param content: 保存内容
        :param is_m3u8key: m3u8 key(type: bool)
        """
        # 文件完整路径
        file = self._generate_filename(url, is_m3u8key)
        mode, encoding = "w", "utf-8"
        if is_m3u8key:
            mode, encoding = "wb", None
        # 保存文件到本地
        if file and (self._reload or not os.path.isfile(file)):
            with make_open(file, mode, encoding=encoding) as write_fileobj:
                write_fileobj.write(content)

    def _generate_filename(
            self, url: Optional[str], is_m3u8key: bool = False
    ) -> Optional[str]:
        """生成完整文件路径

        :param url: url
        :param is_m3u8key:  m3u8 key(type: bool)
        :return: str
        """
        if not self._temp_file or not url or not isinstance(url, str):
            return None
        basename = hash256(url)["ciphertext"] + (".key" if is_m3u8key else ".m3u8")
        return os.path.join(self._temp_file, basename)

    @staticmethod
    def _is_m3u8_content(content: Optional[str], /) -> bool:
        """检查是否是m3u8内容

        :param content: 需要检查的数据
        :return: bool
        """
        if not(content and isinstance(content, str)):
            return False
        return content.startswith("#EXTM3U")

    @property
    def limit(self):
        """limit"""
        return self._limit

    @property
    def user_agent(self):
        """User_Agent"""
        return self._user_agent

    @property
    def temp_file(self):
        """temp_file"""
        return self._temp_file


def load_url(
    url: str,
    *,
    output: Optional[str] = None,
    reload: bool = False,
    reserve: bool = False,
    headers: Optional[dict] = None,
    verify: bool = True,
    limit: int = 16,
    user_agent: Optional[str] = None,
):
    """使用m3u8链接下载资源

    :param url: m3u8 url
    :param output: m3u8资源输出到文件
    :param reload: 重新从网络加载m3u8文件
    :param reserve: 下载完成后保留m3u8文件
    :param headers: request 请求头
    :param verify: request verify
    :param limit: 异步下载并发量
    :param user_agent: User-Agent
    """
    m3u8obj = M3U8()
    return m3u8obj.load_url(
        url,
        output=output,
        reload=reload,
        reserve=reserve,
        headers=headers,
        verify=verify,
        limit=limit,
        user_agent=user_agent
    )


def load_content(
    content: str,
    url: Optional[str] = None,
    *,
    output: Optional[str] = None,
    reload: bool = False,
    reserve: bool = False,
    headers: Optional[dict] = None,
    verify: bool = True,
    limit: int = 16,
    user_agent: Optional[str] = None,
):
    """使用m3u8文件下载资源

    :param content: m3u8 content 或 m3u8本地文件路径
    :param url: m3u8 url
    :param output: m3u8资源输出到文件
    :param reload: 重新从网络加载m3u8文件
    :param reserve: 下载完成后保留m3u8文件
    :param headers: request 请求头
    :param verify: request verify
    :param limit: 异步下载并发量
    :param user_agent: User-Agent
    """
    m3u8obj = M3U8()
    return m3u8obj.load_content(
        content,
        url,
        output=output,
        reload=reload,
        reserve=reserve,
        headers=headers,
        verify=verify,
        limit=limit,
        user_agent=user_agent
    )
