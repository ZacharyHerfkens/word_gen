class Token:
    def __init__(self, file: str, start: int, end: int, line: int, col: int) -> None:
        """Initialize a token in `file` with a start position `start`, and `end`,
        and a line, col position."""
        self.file = file
        self.start = start
        self.end = end
        self.line = line
        self.col = col
    
    @property
    def text(self) -> str:
        return self.file[self.start:self.end]
    
    @property
    def pos(self) -> tuple[int, int]:
        return (self.line, self.col)
    
    def __str__(self) -> str:
        return f"{type(self)}('{self.text}' <ln:{self.line}, col:{self.col}>)"


class LiteralToken(Token):
    """Tokens which will only match an exact string of characters"""
    lit: str = ""

class Colon(LiteralToken):
    lit = ":"

class SemiColon(LiteralToken):
    lit = ";"

class Range(LiteralToken):
    lit = ".."

class Arrow(LiteralToken):
    lit = "=>"

class Comma(LiteralToken):
    lit = ","

class QuestionMark(LiteralToken):
    lit = "?"

class At(LiteralToken):
    lit = "@"

class OpenAngle(LiteralToken):
    lit = "<"

class CloseAngle(LiteralToken):
    lit = ">"

class OpenParen(LiteralToken):
    lit = "("

class CloseParen(LiteralToken):
    lit = ")"

class OpenBrace(LiteralToken):
    lit = "{"

class CloseBrace(LiteralToken):
    lit = "}"


class StringToken(Token):
    """Tokens which may contain an arbitrary string of characters"""
    @classmethod
    def is_start(cls, char: str) -> bool:
        """Determine whether the token can start with this character, this will only ever be called on the first 
        character of a would-be token."""
        return cls.is_valid(char)
    
    @classmethod
    def is_valid(cls, char: str) -> bool:
        """Determine whether a character is valid within this token, this will only ever be called on characters
        after the first in the token."""
        return False


class Directive(StringToken):
    @classmethod
    def is_start(cls, char: str) -> bool:
        return char == '%'
    
    @classmethod
    def is_valid(cls, char: str) -> bool:
        return (
            (char.isalpha() and char.islower())
            or char == '_'
        )

class Phoneme(StringToken):
    @classmethod
    def is_valid(cls, char: str) -> bool:
        return char.isalpha() and not char.isupper()


class PatternID(StringToken):
    @classmethod
    def is_start(cls, char: str) -> bool:
        return char.isupper()
    
    @classmethod
    def is_valid(cls, char: str) ->bool:
        return char.isalnum() or char == '_'

class Number(StringToken):
    @classmethod
    def is_valid(cls, char: str) -> bool:
        return char.isnumeric()