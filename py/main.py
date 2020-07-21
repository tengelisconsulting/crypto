#!/usr/bin/env python3
"""
  Usage:
    crypto/py/main.py <modname> <funcname> <args>

    - <args> are passed to the specified function.
      They should be of the form --key=val.
    - <args> are passed as bytes.

  Output:
    - prints result of called function as utf-8 string

  Example:
    crypto/py/main.py symmetric encrypt --key="big_key" --body="plain_text"
    will call function
    symmetric.encrypt(key=b"big_key", body=b"plain_text")
"""

import os
import pkgutil
import re
import sys
from typing import Callable
from typing import Optional


DIRNAME = os.path.dirname(os.path.realpath(__file__))
ARG_REGEX = re.compile(r"--(\w+)=(.+)")


def input_transformer(text: str) -> bytes:
    return text.encode("utf-8")


def output_transformer(b: bytes) -> str:
    return b.decode("utf-8")


def load_modules():
    mod_info = [mod for mod in pkgutil.walk_packages([DIRNAME])
                if mod.name != "main"]
    modules = [finder.find_module(name).load_module(name)
               for finder, name, _ispkg in mod_info]
    return list(modules)


def parse_args() -> Optional[Callable]:
    if len(sys.argv) < 3:
        return None
    modname = sys.argv[1]
    fn_name = sys.argv[2]
    modules = load_modules()
    module = [m for m in modules if m.__name__ == modname]
    if not module:
        return None
    module = module[0]
    fn = getattr(module, fn_name, None)
    if not fn:
        return None

    def parse_arg_param(s: str):
        match = re.match(ARG_REGEX, s)
        if not match:
            return None
        key, val = match.groups()
        return (key, input_transformer(val))
    params = [parse_arg_param(s) for s in sys.argv[3:]]
    params = [p for p in params if p]
    args = dict([(key, val) for key, val in params])

    def _run():
        return fn(**args)
    return _run


def main():
    fn = parse_args()
    if not fn:
        print(__doc__)
        sys.exit(1)
        return
    res = fn()
    print(output_transformer(res), end="")
    return


if __name__ == '__main__':
    main()
