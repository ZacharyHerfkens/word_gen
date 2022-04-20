# Word Generator

A word generator for conlangs, written in Python3. The aim of this generator is to be as simple as possible to do the basics, 
while still providing the tools to produce extremely complicated word shapes with a minimal amount of work.

## Syntax

Here is an example file:
```
%classes {
    Cons: n m l s p t k w j;
    Vowel: a i e o u;
    Coda: n s m l;
}

%patterns {
    Mid: Cons Vowel Coda?;
    Start: Cons?90 Vowel Coda?;
}

%replacements {
    j |(i, e)| => (a, o, u);
    w |(u, o)| => (a, i, e);
    %any@cpy cpy{1..} => cpy;
    Mid@cpy cpy{1..} => %reject;
}

%words {
    Start Mid{0..2};
}
```
### The `%classes` Directive
Defines all of the various classes of phonemes that will be used in word generation. Phonemes will be generated from
these classes in a Gusein-Zade distribution, which selects left-most phonemes more often than right most. The formula
for this rule is `(1/n)(ln(n+1)-ln(r))`, where `n` is the total number of phonemes in the class, and `r` is the position
of the phoneme in the class. This distribution is flatter with a larger number of phonemes, and steeper with less.

### The `%patterns` Directive
Defines a number of patterns that can be used to generate words, the syntax of these patterns are described below. Patterns
cannot be recursive, either directly or indirectly.

This is fine:
```
A: a B;
B: b c;
```

This is not:
```
A: a B;
B: b A;
```

### The `%replacements` Directive
Defines patterns that will be matched and replaced within words.

### The `%words` Directive
Defines a number of patterns that may be used to generate words. Words are selected from this list according to a Zipf
distribution.