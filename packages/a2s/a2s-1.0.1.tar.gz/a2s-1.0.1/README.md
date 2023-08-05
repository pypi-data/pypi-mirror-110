# a2s

Python async function to sync function, Convert python async function to a sync function for calling from a normal
function in an existing event loop

# Usage

```python
import asyncio
from a2s import sync


@sync
async def an_async_func():
    print("Hello World")


def a_sync_func():
    an_async_func()
    pass


async def main():
    a_sync_func()
    pass


if __name__ == '__main__':
    asyncio.run(main())
```