from operator import le
import unittest
from word_gen.parsing.lexer import LexException, Lexer, UnexpectedCharExcpetion, UnexpectedEOFException
from word_gen.parsing.token import *

class LexerTests(unittest.TestCase):

    def test_reading(self):
        s = "A\nBC\nD"
        lex = Lexer(s)

        i = 0
        while lex.cur != None:
            self.assertEqual(lex.cur, s[i])
            if lex.cur == 'A':
                self.assertEqual(lex.pos, (1, 1))
            elif lex.cur == "C":
                self.assertEqual(lex.pos, (2, 2))
            i += 1
            lex.next()

    def test_invalid(self):
        s = "%sample n ^ n"
        lex = Lexer(s)
        lex.next_tok()
        lex.next_tok()
        self.assertRaises(UnexpectedCharExcpetion, lex.next_tok)
    
    def test_eof(self):
        s = "ch   "
        lex = Lexer(s)
        lex.next_tok()
        self.assertRaises(UnexpectedEOFException, lex.next_tok)
    
    def test_directive(self):
        s = "   \n%sample_directive{}"
        lex = Lexer(s)
        tok = lex.next_tok()
        self.assertIsInstance(tok, Directive)
        self.assertEqual(tok.text, "%sample_directive")
        self.assertEqual(tok.pos, (2, 1))
    
    def test_phoneme(self):
        s = "ch \n n p"
        lex = Lexer(s)
        tok = lex.next_tok()
        self.assertIsInstance(tok, Phoneme)
        self.assertEqual(tok.text, "ch")

        lex.next_tok()

        tok = lex.next_tok()
        self.assertIsInstance(tok, Phoneme)
        self.assertEqual(tok.text, "p")
        self.assertEqual(tok.pos, (2, 4))
    
    def test_patternid(self):
        s = "Cons \n  Vowel Cons"
        lex = Lexer(s)
        lex.next_tok()
        tok = lex.next_tok()
        self.assertIsInstance(tok, PatternID)
        self.assertEqual(tok.text, "Vowel")
        self.assertEqual(tok.pos, (2, 3))
        lex.next_tok()
    
    def test_lit_tok(self):
        s = "(){(})"
        lex = Lexer(s)
        lex.next_tok()
        tok = lex.next_tok()
        self.assertIsInstance(tok, CloseParen)
        lex.next_tok()
        lex.next_tok()
        tok = lex.next_tok()
        self.assertIsInstance(tok, CloseBrace)
        lex.next_tok()
    
    def test_lex_file(self):
        with open("tests/gen_files/sample.gen") as f:
            s = f.read()
        
        lex = Lexer(s)
        while True:
            try:
                lex.next_tok()
            except UnexpectedEOFException:
                break
            except UnexpectedCharExcpetion as e:
                self.fail(f"Encountered Unexpected Char with error {e}")
