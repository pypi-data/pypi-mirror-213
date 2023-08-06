# oldpyro

This is a fork of **Pyrogram v1** (Last: [v1.4.16](https://pypi.org/project/pyrogram/1.4.16)) which installs the library with name `oldpyro` so that you can use both major versions at the same time.

- Install this only if you need both version. If you only need major version 1, use `pip install pyrogram==1.*`.
- Please install this before the latest `pyrogram` version so that dependencies, if conflicting, can be overwritten.

This isn't exactly the right way, but it is the only way. Also, dependencies may (and `will` in the future) create a problem!

## Installation

### PyPI

```shell
pip install oldpyro
```

### Usage

Just change `pyrogram` to `oldpyro` in your imports. For example:

```shell
from oldpyro import Client
```

If you are using both clients in same file:

```shell
from oldpyro import Client as Client1
```

## Credits

Original Author - [Dan](https://github.com/delivrance)

Original Repository - [pyrogram](https://github.com/pyrogram/pyrogram)
