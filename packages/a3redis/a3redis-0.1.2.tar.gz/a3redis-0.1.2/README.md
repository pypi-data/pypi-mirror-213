# a3redis

It is just a thin wrapper of redis.

[History.](HISTORY.md)

## Install

```shell script
pip install a3redis

```

## Examples

## 1. conf

```json
{
    "standalone": {
        "mode": "standalone",
        "init": {
            "host": "standalone-redis-master",
            "port": 6379,
            "db": 0,
            "password": "standalone",
            "decode_responses": true
        }
    },
    "sentinel": {
        "mode": "sentinel",
        "init": {
            "sentinels": [
                ["sentinel-redis-node-0.sentinel-redis-headless", 26379],
                ["sentinel-redis-node-1.sentinel-redis-headless", 26379],
                ["sentinel-redis-node-2.sentinel-redis-headless", 26379]
            ],
            "sentinel_kwargs": {
                "password": "sentinel"
            },
            "password": "sentinel",
            "db": 1,
            "decode_responses": true
        },
        "runtime": {
            "service_name": "my-master"
        }
    },
    "cluster": {
        "mode": "cluster",
        "init": {
            "host": "cluster-redis-cluster",
            "port": 6379,
            "password": "cluster",
            "decode_responses": true
        }
    }
}
```

## 2. Structures

### 2.1 Hash

```python
from a3redis.structures import Hash

class User(Hash):
    main_key = 'user:{id}'
    _hkey_username = 'username'

    def get_username(self) -> str:
        return self.get_member_by_key(self._hkey_username)

    def set_username(self, username: str):
        self.set_member(self._hkey_username, username)

if __name__ == '__main__':
    # If the redis service configuration is not specified, the `redis://localhost:6379/0` will be used.
    user = User(id='123')
    user.set_username('xxx')
    
    user = User(id='234')
    user.get_username()


```

### 2.2 List

```python
from a3redis.structures import List
from a3redis.bases import RedisClientFactory

class MessageList(List):
    # Specified redis server by rdb_conf_name
    rdb_conf_name = "cluster"
    main_key = "message_list"

if __name__ == "__main__":
    RedisClientFactory.init_redis_clients(conf={"cluster": "Refer to the conf json above"})
    
    message_list = MessageList()
    message_list.right_push("......")

```

### 2.3 String

```python
from a3redis.structures import String
from a3redis.bases import RedisClientFactory

class DataCache(String):
    rdb_conf_name = "cache"
    main_key = "data:{id}"

if __name__ == "__main__":
    RedisClientFactory.init_redis_clients(conf={"sentinel": "Refer to the conf json above"})
    readwrite_rdb = RedisClientFactory.get_rdb("sentinel")
    DataCache(id=123, rdb=readwrite_rdb).set(".....")
    
    readonly_rdb = RedisClientFactory.get_rdb("sentinel", readonly=True)
    data = DataCache(id=123, rdb=readonly_rdb).get()

```

## 3. Different redis serve mode

```python
from a3redis.bases import RedisClientFactory, RedisMode
from a3redis.structures import Hash


class User(Hash):
    main_key = 'user:{id}'
    _hkey_username = 'username'

    def get_username(self) -> str:
        return self.get_member_by_key(self._hkey_username)

    def set_username(self, username: str):
        self.set_member(self._hkey_username, username)


if __name__ == '__main__':
    # load all redis server
    RedisClientFactory.init_redis_clients(conf={"...": "Refer to the conf json above"})

    localhost_anonymous_rdb = None
    standalone_rdb = RedisClientFactory.get_rdb(RedisMode.Standalone)
    sentinel_rdb = RedisClientFactory.get_rdb(RedisMode.Sentinel)
    cluster_rdb = RedisClientFactory.get_rdb(RedisMode.Cluster)
    
    for rdb in [localhost_anonymous_rdb, standalone_rdb, sentinel_rdb, cluster_rdb]:
        user = User(id="123", rdb=rdb)
        user.set_username("tom")
        user.get_username()
        user.delete()

```