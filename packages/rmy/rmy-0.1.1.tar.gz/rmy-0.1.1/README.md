A powerful PRC framework to build distributed applications easily in Python. 

## How to use it

One can expose a Python object through a server as follow.

``` python
class Demo:
    async def greet(self, name):
        return f"Hello {name}!"


if __name__ == "__main__":
    rmy.run_tcp_server(8080, Demo())
```

This object can then be remotely access to as follows.

``` python
if __name__ == "__main__":
    with rmy.create_sync_client("localhost", 8080) as client:
        proxy: Demo = client.fetch_remote_object()
        print(proxy.greet("world"))
```

The object returned `fetch_remote_object` call is an ad hoc object which has the same interface as the one that has been exposed. One can also remotely access to the object attributes and even iterate asynchronously through data returned by the shared object.
