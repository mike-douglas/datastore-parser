from luaparser.astnodes import Node

_methods = {}


def visitor(node_type=None):
    """Visitor decorator
    This decorator looks for _name attributes in passsed arguments (nodes),
    and if they match a known visitor impl, they use it. Otherwise, it uses
    _DEFAULT
    """

    def _visit(self, arg):
        """Visitor implementation"""

        if hasattr(arg, '_name') and arg._name in _methods:
            method = _methods[arg._name]
        else:
            method = _methods['_DEFAULT']

        return method(self, arg)

    def decorator(f):
        if node_type is None:
            _methods['_DEFAULT'] = f
        else:
            _methods[node_type] = f

        return _visit

    return decorator


class LUAParser:
    """Builds a dict from a LUA AST tree containing Assign directives
    """

    @visitor('String')
    def visit(self, node: Node) -> str:
        return node.s

    @visitor('Number')
    def visit(self, node: Node) -> int:
        return node.n

    @visitor('Name')
    def visit(self, node: Node) -> str:
        return node.id

    @visitor('Field')
    def visit(self, node: Node) -> dict:
        """Return a dict with the k/v for the field, to be collapsed by the Table"""
        f = {}
        f[self.visit(node.key)] = self.visit(node.value)
        return f

    @visitor('Table')
    def visit(self, node: Node) -> dict:
        """Return a dict of fields merged into one structure"""
        t = {}

        for row in node.fields:
            t.update(self.visit(row))
        return t

    @visitor('Assign')
    def visit(self, node: Node) -> dict:
        """Return a dict of variable assignments"""
        targets = [self.visit(t) for t in node.targets]
        values = [self.visit(v) for v in node.values]

        return dict((t, v) for t, v in zip(targets, values))

    @visitor('Chunk')
    def visit(self, node: Node) -> any:
        # Skips the Chunk.body.Block.body levels
        return self.visit(node.body)[0][0]

    @visitor('_DEFAULT')
    def visit(self, node: Node) -> list:
        """Default visitor that handles lists and unnamed Node types in the tree"""
        result = []

        if isinstance(node, list):
            result = []

            for item in node:
                result.append(self.visit(item))

            return result
        else:
            for attr, attrValue in node.__dict__.items():
                if not attr.startswith(('_', 'comments')):
                    if isinstance(attrValue, Node) or isinstance(attrValue, list):
                        result.append(self.visit(attrValue))
                    else:
                        if attrValue is not None:
                            result.append(self.visit(attrValue))
                            pass

        return result
