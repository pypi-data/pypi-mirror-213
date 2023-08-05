"""m3u8资源下载器"""
import os
import shlex
import asyncio
import aiofiles
import subprocess
from concurrent.futures import ThreadPoolExecutor

from pyxk.aes import Cryptor
from pyxk.utils import make_open
from pyxk.aclient import Client


class Downloader(Client):
    """m3u8 - segments 下载器"""

    timeout = 30
    maximum_retry = 30
    error_status_code = list(range(404, 411))
    until_request_succeed = True

    def __init__(
        self, *, m3obj, m3u8keys=None, segments=None, progress=None, download=None, **kwargs
    ):
        """m3u8 - segments 下载器

        :param m3obj: pyxk.m3u8downloader.main.M3U8
        :param m3u8keys: m3u8资源加密密钥
        :param segments: m3u8 segments
        :param progress: rich.progress.Progress
        :param download: rich.progress.Progress
        :param kwargs: **kwargs
        """
        super().__init__(**kwargs)
        self.m3obj = m3obj
        self.limit = m3obj.limit
        self.cipher = {index: Cryptor(**cipher) for index, cipher in m3u8keys.items()} if m3u8keys else {}
        self.temp_file = os.path.join(self.m3obj.temp_file, "segments") if self.m3obj.temp_file else None
        self.semaphore = m3obj.limit
        self.start_urls: dict = segments
        self.task = None
        self.progress = progress
        self.download = download
        self.user_agent = m3obj.user_agent

    async def start_request(self):
        # 数据不齐全 不下载
        if (
            not self.start_urls
            or not self.temp_file
            or not self.m3obj.output
        ):
            return None
        os.makedirs(self.temp_file, exist_ok=True)
        # 添加进度条任务
        self.task = self.progress.add_task(description="", total=len(self.start_urls))
        # 收集异步任务
        tasks, result = [], []
        for index, item in self.start_urls.items():
            file = os.path.join(self.temp_file, f"{index}.ts")
            result.append(file)
            # 跳过已下载文件
            if os.path.isfile(file) and os.path.getsize(file) > 0:
                self.progress.update(self.task, advance=1)
                continue
            task = self.request(
                item["url"],
                cb_kwargs={"file": file, "key": item["key"]},
                callback=self.parse,
            )
            tasks.append(task)
        await asyncio.gather(*tasks)
        return result

    async def parse(self, response, file, key):
        content = await response.content.read()
        # 解密
        if key is not None and self.cipher:
            content = self.cipher[key].decrypt(content)
        async with aiofiles.open(file, "wb") as write_fileobj:
            await write_fileobj.write(content)
        # 更新进度条
        self.progress.update(self.task, advance=1)
        return file

    async def completed(self, result):
        self.cipher, self.start_urls = None, None
        if not result:
            return
        # 创建 filelist 文件
        filelist, filesize = os.path.join(self.temp_file, "filelist.txt"), 0
        with make_open(filelist, "w", encoding="utf-8") as write_fileobj:
            for file in result:
                write_fileobj.write(f"file '{file}'\n")
                filesize += (os.path.getsize(file) - 16400)

        # ffmpeg 视频合并代码, 监测合并完成状态
        args = shlex.split(
            f"ffmpeg -loglevel quiet -f concat -safe 0 -i {filelist} -c copy {self.m3obj.output} -y"
        )
        merge_completed = False

        # ffmpeg 合并函数
        def merge_segments():
            try:
                subprocess.run(args=args, check=True)
            except FileNotFoundError:
                self.m3obj._console.log("[red]ffmpeg is not available![/]")
                self.m3obj._reserve = True
            finally:
                nonlocal merge_completed
                merge_completed = True

        # 合并进度条
        def merge_progress():
            import time
            completed_filezise = os.path.getsize(self.m3obj.output) if os.path.isfile(self.m3obj.output) else 0
            task = self.download.add_task(description="", total=filesize)
            while True:
                self.download.update(task, completed=completed_filezise)
                if merge_completed:
                    if os.path.isfile(self.m3obj.output):
                        self.download.update(task, completed=filesize)
                    break
                time.sleep(0.25)
        # 开启多线程
        pool = ThreadPoolExecutor()
        pool.submit(merge_segments)
        pool.submit(merge_progress)
        pool.shutdown()
