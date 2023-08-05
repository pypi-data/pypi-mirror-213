# Pyxk

### pyxk install
```console
$ python -m pip install pyxk
```

### pyxk.aclient
```python
from pprint import pprint
from pyxk import Client, Response

class Downloader(Client):
    start_urls = ['https://pypi.org' for _ in range(2)]

    async def parse(self, response: Response):
        title = await response.xpath('//title/text()')
        return title.get()

    async def completed(self, result: list):
        pprint(result)

Downloader.run()

>> ['PyPI · The Python Package Index', 'PyPI · The Python Package Index']
```

### pyxk.m3u8
```python
from pyxk.m3u8 import load_url, load_content

url = 'http://xxx.m3u8'
output = 'xxx/xxx'
load_url(url=url, output=output)
```

```console
$ m3u8 --help

Usage: m3u8 [OPTIONS] COMMAND [ARGS]...     
                                            
  m3u8下载器                                
                                            
Options:                                    
  -o, --output TEXT             M3U8存储路径
  --reload                      重载m3u8资源
  --reserve                     保留m3u8资源
  -h, --headers <TEXT TEXT>...  Request Headers
  --no-verify                   Request Verify
  -l, --limit INTEGER           下载并发量
  -ua, --user-agent TEXT        User-Agent
  --help                        Show this message and exit.

Commands:
  file  使用m3u8文件下载资源
  url   使用m3u8链接下载资源

# use m3u8 download
$ m3u8 file xxx/xxx.m3u8 -o xxx/xxx.mp4
$ m3u8 url https://xxx.m3u8 -o xxx/xxx.mp4
```
