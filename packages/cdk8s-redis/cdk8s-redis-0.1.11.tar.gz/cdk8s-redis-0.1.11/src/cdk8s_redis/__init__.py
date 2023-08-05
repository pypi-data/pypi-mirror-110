'''
# cdk8s-redis

> Redis constructs for cdk8s

Basic implementation of a Redis construct for cdk8s. Contributions are welcome!

## Usage

The following will define a Redis cluster with a master and 2 slave replicas:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk8s_redis import Redis

# inside your chart:
redis = Redis(self, "my-redis")
```

DNS names can be obtained from `redis.masterHost` and `redis.slaveHost`.

You can specify how many slave replicas to define:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
Redis(self, "my-redis",
    slave_replicas=4
)
```

Or, you can specify no slave:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
Redis(self, "my-redis",
    slave_replicas=0
)
```

## License

Distributed under the [Apache 2.0](./LICENSE) license.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *


class Hello(metaclass=jsii.JSIIMeta, jsii_type="cdk8s-redis.Hello"):
    '''
    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(Hello, self, [])

    @jsii.member(jsii_name="sayHello")
    def say_hello(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "sayHello", []))


__all__ = [
    "Hello",
]

publication.publish()
