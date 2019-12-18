from luaparser import ast
from .parser import LUAParser


def lua_to_dict(src) -> dict:

    tree = ast.parse(src)
    parser = LUAParser()

    result = parser.visit(tree)

    return result
