from jsonmathpy.core.types import TokenType
from jsonmathpy.interfaces.tokens import ITokenProvider
from jsonmathpy.models.token import Token


class TokenProvider(ITokenProvider):

    def __init__(self):
        self.tokens = []

    def new_token(self, type, value) -> None:
        token = Token(type, value)
        self.tokens.append(token)
    
    def get_tokens(self):
        return self.tokens

    def new_single_operation_token(self, c1):
        self.tokens.append({
            '*': Token(TokenType.STAR,          '*'),
            '-': Token(TokenType.MINUS,         '-'),
            '+': Token(TokenType.PLUS,          '+'),
            '=': Token(TokenType.EQUAL,         '='),
            '[': Token(TokenType.LSQB,          '['),
            ']': Token(TokenType.RSQB,          ']'),
            '(': Token(TokenType.LPAR,          '('),
            ')': Token(TokenType.RPAR,          ')'),
            '{': Token(TokenType.LBRACE,        '{'),
            '}': Token(TokenType.RBRACE,        '}'),
            '^': Token(TokenType.CIRCUMFLEX,    '^'),
            '/': Token(TokenType.SLASH,         '/'),
            '|': Token(TokenType.VBAR,          '|'),
            '&': Token(TokenType.AMPER,         '&'),
            '!': Token(TokenType.EXCLAMATION,   '!'),
            '~': Token(TokenType.TILDE,         '~'),
            '>': Token(TokenType.GREATER,       '>'),
            '<': Token(TokenType.LESS,          '<'),
            ':': Token(TokenType.COLON,         ':'),
            '.': Token(TokenType.DOT,           '.'),
            ',': Token(TokenType.COMMA,         ','),
            ';': Token(TokenType.SEMI,          ';'),
            '@': Token(TokenType.AT,            '@'),
            '%': Token(TokenType.PERCENT,       '%')
        }[c1])

    def new_double_operation_token(self, c1, c2) -> TokenType:
        try:
            self.tokens.append({
            '!': {'=': Token(TokenType.NOTEQUAL,        '!=')},
            '%': {'=': Token(TokenType.PERCENTEQUAL,    '%=')},
            '&': {'=': Token(TokenType.AMPEREQUAL,      '&=')},
            '+': {'=': Token(TokenType.PLUSEQUAL,       '+=')},
            ':': {'=': Token(TokenType.COLONEQUAL,      ':=')},
            '=': {'=': Token(TokenType.EQEQUAL,         '==')},
            '|': {'|': Token(TokenType.VBARVBAR,         '||')},
            '@': {'=': Token(TokenType.ATEQUAL,         '@=')},
            '^': {'=': Token(TokenType.CIRCUMFLEXEQUAL, '^=')},
            '|': {'=': Token(TokenType.VBAREQUAL,       '|=')},
            '*': {'*': Token(TokenType.DOUBLESTAR,      '**'), '=': Token(TokenType.STAREQUAL,      '*=')},
            '>': {'=': Token(TokenType.GREATEREQUAL,    '>='), '>': Token(TokenType.RIGHTSHIFT,     '>>')},
            '/': {'/': Token(TokenType.DOUBLESLASH,     '//'), '=': Token(TokenType.SLASHEQUAL,     '/=')},
            '-': {'=': Token(TokenType.MINEQUAL,        '-='), '>': Token(TokenType.RARROW,         '->')},
            '<': {'=': Token(TokenType.LESSEQUAL,       '<='), '<': Token(TokenType.LEFTSHIFTEQUAL, '<<'), '>': Token(TokenType.NOTEQUAL, '<>')},
            }[c1][c2])
        except:
            self.new_single_operation_token(c1)
            self.new_single_operation_token(c1)


    def new_tripple_operation_token(self, c1, c2, c3) -> TokenType:
        try:
            self.tokens.append({
                '*': {'*': {'=': Token(TokenType.DOUBLESTAREQUAL,   '**=')}},
                '.': {'.': {'.': Token(TokenType.ELLIPSIS,          '...')}},
                '/': {'/': {'=': Token(TokenType.DOUBLESLASHEQUAL,  '//=')}},
                '<': {'<': {'=': Token(TokenType.LEFTSHIFTEQUAL,    '<<=')}},
                '>': {'>': {'=': Token(TokenType.RIGHTSHIFTEQUAL,   '>>=')}}
            }[c1][c2][c3])
        except:
            self.new_single_operation_token(c1)
            self.new_single_operation_token(c1)
            self.new_single_operation_token(c1)
