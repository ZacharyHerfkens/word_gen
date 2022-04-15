# Word Generator

A word generator for conlangs, written in Python3. The aim of this generator is to be as simple as possible to do the basics, 
while still providing the tools to produce extremely complicated word shapes with a minimal amount of work.

## Syntax

Here is an example file:
```
%phonemes: a e i j k l m n o p s t u w;

%classes {
    Cons: n m l s p t k w j;
    Vowel: a i e o u;
    Coda: n s m l;
}

%patterns {
    Mid: Cons Vowel Coda?;
    Start: Cons?90 Vowel Coda?;
}

%words {
    Start Mid{0..2};
}

%filters {
    j <(i, e)> => (a, o, u);
    w <(u, o)> => (a, i, e);
    (Cons Vowel)@CV CV{1..};
}
```

### The `%phonemes` Directive
Definies the space of phonemes that will be used in word generation, as well as their alphabetical ordering.

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

### The `%words` Directive
Defines a number of patterns that may be used to generate words. Words are selected from this list according to a Zipf
distribution.

### The `%filters` Directive
Defines a series of filters that will be searched for and potentially replaced within a word. There are two types of
filters: replacing and rejecting. 

Replacing filters are in the form `filt => repl`, where `filt` is a filter pattern,
and `repl` is a replacement pattern. Filter patterns contain an environment, and a replacement field. Where the
replacement field is everything between `<` and `>`, and the environment is everything outside of them. Only the pattern
within the replacement field will be replaced by the `repl` pattern. If a replacement filter does not have this, 
it is invalid.

Rejecting filters do not contain a pattern to replace, instead, if a word matches the filter, it is rejected from the
output entirely. This is useful if the pattern being filtered has no recovery options.