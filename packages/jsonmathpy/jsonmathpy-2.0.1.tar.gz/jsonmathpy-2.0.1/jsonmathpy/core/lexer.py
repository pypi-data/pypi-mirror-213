from jsonmathpy.interfaces.iterator import IIterator
from jsonmathpy.interfaces.lexer import ILexer
from jsonmathpy.interfaces.tokens import ITokenProvider
from jsonmathpy.core.types import TokenSinglets, TokenType
from enum import Enum


class Characters(Enum):
    """An object containing the set of supported characters, keyd on a set name."""
    WHITESPACE          = ' \n\t'
    DIGITS              = '0987654321'
    LOWERCASECHARACTERS = 'abcdefghijklmnopqrstuvwxyz'
    UPPERCASECHARACTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    NONLETTERCHARACTERS = '_{}:^;'
    OPERATIONS          = '*-+=[](){}^/|&!~><:;.,@%'
    LETTERS             = LOWERCASECHARACTERS + UPPERCASECHARACTERS
    CHARACTERS          = LOWERCASECHARACTERS + UPPERCASECHARACTERS + NONLETTERCHARACTERS
    OBJECTCHARACTERS    = LOWERCASECHARACTERS + UPPERCASECHARACTERS + NONLETTERCHARACTERS + DIGITS


class Lexer(ILexer):
    def __init__(self, token_provider: ITokenProvider, characters: IIterator):
        self.token_provider = token_provider
        self.characters = characters
        self.characters.advance()

    def tokenize(self):
        # If the token is longer than a single character, we need to defined how to generate it.
        while self.characters.current() != None:

            if self.characters.current() in Characters.WHITESPACE.value:
                self.characters.advance()

            elif self.characters.current() in Characters.LETTERS.value:
                self._object()

            elif self.characters.current() in Characters.DIGITS.value:
                self._number()

            elif self.characters.current() in Characters.OPERATIONS.value:
                self._operation()

            else:
                raise Exception(f"Illegal Character '{self.characters.current()}'")
        return self.token_provider.get_tokens()

    def _number(self):
        number = ''
        while self.characters.current() != None and (self.characters.current() in Characters.DIGITS.value or self.characters.current() == '.'):
            number += self.characters.current()
            self.characters.advance()
        count = number.count('.')
        if count == 0:
            self.token_provider.new_token(TokenType.INTEGER, number)
        elif count == 1:
            self.token_provider.new_token(TokenType.FLOAT, number)
        else:
            raise Exception(f"Illegal Character '{number}'")

    def _operation(self):
        ops = []
        while self.characters.current() != None and self.characters.current() in Characters.OPERATIONS.value:
            ops.append(self.characters.current())
            self.characters.advance()
        if len(ops) == 1:
            self.token_provider.new_single_operation_token(*ops)
        elif len(ops) == 2:
            self.token_provider.new_double_operation_token(*ops)
        elif len(ops) == 3:
            self.token_provider.new_tripple_operation_token(*ops)
        else:
            for i in ops:
                self.token_provider.new_single_operation_token(i)

    def _object(self):
        obj = ''
        while self.characters.current() != None and self.characters.current() in Characters.OBJECTCHARACTERS.value:
            if self.characters.current() in Characters.CHARACTERS.value and self.characters.peek() == '(':
                obj += self.characters.current()
                self.characters.advance()
                self.token_provider.new_token(TokenType.FUNCTION, obj)
            elif self.characters.peek() not in Characters.OBJECTCHARACTERS.value + '(':
                obj += self.characters.current()
                self.characters.advance()
                self.token_provider.new_token(TokenType.OBJECT, obj)
            else:
                obj += self.characters.current()
                self.characters.advance()