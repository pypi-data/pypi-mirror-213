class BaseNode:

    def add(self, *args):
        return args[0] + args[1]

    def sub(self, *args):
        return args[0] - args[1]

    def mul(self, *args):
        return args[0] * args[1]

    def div(self, *args):
        return args[0] / args[1]

    def pow(self, *args):
        return args[0] ** args[1]

    def AND(self, *args):
        return args[0] and args[1]

    def OR(self, *args):
        return args[0] or args[1]

    def less(self, *args):
        return args[0] < args[1]

    def greater(self, *args):
        return args[0] > args[1]

    def less_equal(self, *args):
        return args[0] <= args[1]

    def greater_equal(self, *args):
        return args[0] >= args[1]

    def equal_equal(self, *args):
        return args[0] == args[1]

    def float(self,  *args):
        return float(''.join(args))

    def int(self,  *args):
        return int(''.join(args))

    def array(self, *args):
        return [*args]

base_configuration = [
            {
                'node': '+',
                'node_key': "add"
            },
            {
                'node': '-',
                'node_key': "sub"
            },
            {
                'node': '*',
                'node_key': "mul"
            },
            {
                'node': '^',
                'node_key': "pow"
            },
            {
                'node': '/',
                'node_key': "div"
            },
            {
                'node': '==',
                'node_key': "equal_equal"
            },
            {
                'node': '<=',
                'node_key': "less_equal"
            },
            {
                'node': '>=',
                'node_key': "greater_equal"
            },
            {
                'node': '<',
                'node_key': "less"
            },
            {
                'node': '>',
                'node_key': "greater"
            },
            {
                'node': '&',
                'node_key': "AND"
            },
            {
                'node': '|',
                'node_key': "OR"
            },
            {
                'node': 'array',
                'node_key': "array"
            },
            {
                'node': 'integer',
                'node_key': "int"
            },
            {
                'node': 'float',
                'node_key': "float"
            },
            {
                'node': 'function',
                'node_key': 'cos'
            },
            {
                'node': 'function',
                'node_key': 'sin'
            },
            {
                'node': 'function',
                'node_key': 'tan'
            },
            {
                'node': 'object',
                'node_key': "tensor"
            },
            {
                'node': 'function',
                'node_key': 'myFunction'
            }
        ]