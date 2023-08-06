# imgbbpy
An Asynchronous and Synchronous API Wrapper for the Imgbb API.

## Installation
Install imgbbpy via `pip`.

```sh
pip install imgbbpy
```
imgbbpy requires Python 3.7+

## Quickstart
Asynchronous usage:
```py
import asyncio
import imgbbpy

async def main():
    client = imgbbpy.AsyncClient('API KEY')
    image = await client.upload(file='path/to/image.jpeg')
    print(image.url)

asyncio.run(main())
```

Synchronous usage:
```py
import imgbbpy

client = imgbbpy.SyncClient('API KEY')
image = client.upload(file='path/to/image.png')
print(image.url)
```

You can get an API Key from https://api.imgbb.com.

## Documentation
Documentation can be found in the `documentation.md` file.

## License
MIT, see LICENSE for more details.
