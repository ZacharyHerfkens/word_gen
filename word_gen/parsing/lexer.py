from .token import *

class LexException(Exception):
    pass

class UnexpectedCharExcpetion(LexException):
    def __init__(self, char: str, line: int, col: int):
        super().__init__(f"Unexpected Character '{char}' at <ln:{line}, col:{col}>")
        self.char = char
        self.line = line
        self.col = col

class UnexpectedEOFException(LexException):
    def __init__(self):
        super().__init__(f"Reached End Of File while Lexing")


class Lexer:
    def __init__(self, text: str) -> None:
        """Initialize a lexer at position 0 in `text`"""
        self.text = text
        self.cursor = 0
        self.line = 1
        self.col = 1

    @property
    def pos(self) -> tuple[int, int]:
        """Get the current position of the lexer in the text, by (line, col)."""
        return (self.line, self.col)
    
    @property
    def cur(self) -> str | None:
        """Get the current character at the cursor, or none if there are no more characters."""
        if self.cursor >= len(self.text):
            return None
        else:
            return self.text[self.cursor]
    
    def next(self) -> bool:
        """Advance to the next character, 
        or do nothing if there are no more characters, 
        return whether an advance was made or not."""
        if self.cursor >= len(self.text):
            return False
        
        cur = self.cur
        if cur == '\n':
            self.line += 1
            self.col = 0
        
        self.cursor += 1
        self.col += 1
        return True
    
    def skip_space(self) -> None:
        while self.cur is not None and self.cur.isspace():
            self.next()
    
    def skip_line(self) -> None:
        while self.cur is not None and self.cur != '\n':
            self.next()
        self.next()
    
    def skip_to_tok(self) -> None:
        while True:
            self.skip_space()
            if self.text.startswith("//", self.cursor):
                self.skip_line()    # skip comments
            else:
                break

    def get_str_tok(self, tok: type[StringToken]) -> Token:
        """Given a token type, parse it from the text. The token must be present."""
        start = self.cursor
        line, col = self.pos

        self.next()
        while self.cur is not None and tok.is_valid(self.cur):
            self.next()
        end = self.cursor
        
        return tok(self.text, start, end, line, col)
    
    def get_lit_tok(self, tok: type[LiteralToken]) -> Token:
        start = self.cursor
        line, col = self.pos
        for _ in tok.lit:
            self.next()
        end = self.cursor

        return tok(self.text, start, end, line, col)
    
    def next_tok(self) -> Token:
        self.skip_to_tok()
        if self.cur is None:
            raise UnexpectedEOFException()

        next = self.next_tok_type()
        if next is None:
            raise UnexpectedCharExcpetion(self.cur, self.line, self.col)
        elif issubclass(next, LiteralToken):
            return self.get_lit_tok(next)
        elif issubclass(next, StringToken):
            return self.get_str_tok(next)
            
    
    def next_tok_type(self) -> type[Token] | None:
        self.skip_to_tok()
        if self.cur is None:
            return None
        
        for tok in StringToken.__subclasses__():
            if tok.is_start(self.cur):
                return tok
        
        for tok in LiteralToken.__subclasses__():
            if self.text.startswith(tok.lit, self.cursor):
                return tok
        
        return None