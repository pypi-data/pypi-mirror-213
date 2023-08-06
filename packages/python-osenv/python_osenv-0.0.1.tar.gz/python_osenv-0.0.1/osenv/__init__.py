import os
import dotenv as __dotenv


class dotdict(dict):
    def __getattr__(self, __key: str):
        if __key.replace("_", "").isupper():
            result = self[__key]
        else:
            result = dict.__getattribute__(self, __key)
        return result

    def __setattr__(self, __key: str, value):
        if __key.replace("_", "").isupper():
            self[__key] = value
        else:
            dict.__setattr__(self, __key, value)


__isdir = os.path.isdir
__exists = os.path.exists
__dirname = os.path.dirname
__join = os.path.join
__abspath = os.path.abspath


def __env_path(root: str = ""):
    if not root:
        root = __file__
    if not __isdir(root):
        root = __dirname(root)
    result = None
    while len(root) > 1:
        result = __join(root, ".env")
        if __exists(result):
            break
        root = __dirname(root)
    if result is None:
        raise FileExistsError("Unable to locate env file")
    result = __abspath(result)
    return result


def osenv(root: str = ""):
    env_path = __env_path(root=root)
    result = __dotenv.dotenv_values(env_path)
    return dotdict(result)
