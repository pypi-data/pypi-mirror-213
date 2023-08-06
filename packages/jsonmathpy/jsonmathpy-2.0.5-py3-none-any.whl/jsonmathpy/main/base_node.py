class DefaultNode:

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

default_node_configuration = [
            {
                'node': '+',
                'handler': "add"
            },
            {
                'node': '-',
                'handler': "sub"
            },
            {
                'node': '*',
                'handler': "mul"
            },
            {
                'node': '^',
                'handler': "pow"
            },
            {
                'node': '/',
                'handler': "div"
            },
            {
                'node': 'array',
                'handler': "array"
            },
            {
                'node': 'integer',
                'handler': "int"
            },
            {
                'node': 'float',
                'handler': "float"
            },
            {
                'node': '&',
                'handler': "AND"
            },
            {
                'node': '|',
                'handler': "OR"
            },
            {
                'node': '==',
                'handler': "equal_equal"
            },
            {
                'node': '>',
                'handler': "greater"
            },
            {
                'node': '<',
                'handler': "less"
            },
            {
                'node': '>=',
                'handler': "greater_equal"
            },
            {
                'node': '<=',
                'handler': "less_equal"
            }
        ]