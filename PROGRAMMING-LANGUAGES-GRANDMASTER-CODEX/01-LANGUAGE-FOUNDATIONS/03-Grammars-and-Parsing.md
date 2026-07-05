# 🌳 Grammars and Parsing

> *"Parsing is the act of discovering the tree hidden inside a flat string."*

---

## I. THE PROBLEM

Source code arrives as a **flat sequence of characters**:

```
"x = 3 + 4 * 2"
```

But its *meaning* is a **tree** — because `*` binds tighter than `+`:

```
      =
     / \
    x   +
       / \
      3   *
         / \
        4   2
```

Turning the string into that tree is **parsing**, and it happens in two stages: lexing (characters → tokens) and parsing (tokens → tree).

---

## II. STAGE 1 — LEXING (TOKENIZATION)

The **lexer** (scanner) groups characters into **tokens** — the words of the language:

```
"x = 3 + 4 * 2"
   ↓ lexer
[IDENT("x"), EQUALS, NUM(3), PLUS, NUM(4), STAR, NUM(2)]
```

Tokens are defined by **regular expressions** (regular grammars):
- identifier: `[a-zA-Z_][a-zA-Z0-9_]*`
- number: `[0-9]+(\.[0-9]+)?`
- whitespace/comments: usually discarded

Lexing removes noise (spaces, comments) and classifies each atom. It's a **finite automaton** — fast, linear time.

---

## III. STAGE 2 — PARSING (GRAMMAR)

The **parser** combines tokens into a tree according to a **grammar**. Grammars are written in **BNF** (Backus–Naur Form) or EBNF:

```bnf
expr   ::= term (("+" | "-") term)*
term   ::= factor (("*" | "/") factor)*
factor ::= NUMBER | "(" expr ")"
```

Read it as rules: an `expr` is a `term`, optionally followed by `+`/`-` and more terms. This *nesting* is what encodes precedence: because `term` (which handles `*`/`/`) is defined *inside* `expr` (which handles `+`/`-`), multiplication naturally binds tighter.

### The Chomsky hierarchy (grammar power)
```
Type 3  Regular          → tokens (lexing). Recognized by finite automata.
Type 2  Context-free     → most language syntax. Recognized by pushdown automata.
Type 1  Context-sensitive → rarely used directly.
Type 0  Unrestricted     → full Turing power.
```
Programming-language *syntax* is almost always **context-free (Type 2)**; the *semantics* (like "is this variable declared?") is context-sensitive and handled later, not by the grammar.

---

## IV. THE AST — ABSTRACT SYNTAX TREE

The parser's output is an **AST**: a tree with only the *meaningful* structure. It's "abstract" because it drops syntactic noise (parentheses, semicolons, commas) — those did their job guiding the parse and are no longer needed.

```
Concrete syntax:  (3 + 4) * 2
AST:              Multiply(Add(Num 3, Num 4), Num 2)
```

The AST is the **central data structure** of every compiler and interpreter. Everything downstream — type checking, optimization, code generation, interpretation — operates on the AST, not the text. (See [`../05-COMPILERS-AND-INTERPRETERS/00-Index.md`](../05-COMPILERS-AND-INTERPRETERS/00-Index.md).)

---

## V. AMBIGUITY — THE PARSER'S NIGHTMARE

A grammar is **ambiguous** if one string can produce more than one tree. The classic case:

```
if a then if b then x else y
```
Does the `else` attach to the first `if` or the second? This is the **dangling else** problem. Languages resolve it by a rule ("else binds to the nearest if") or by requiring braces.

Another: `3 - 4 - 5`. Left-associative → `(3-4)-5 = -6`. Right-associative → `3-(4-5) = 4`. The grammar (or explicit associativity rules) must decide. Ambiguity is why precedence and associativity exist as concepts.

---

## VI. PARSING STRATEGIES (a map)

| Strategy | Direction | Used by | Notes |
|----------|-----------|---------|-------|
| **Recursive descent** | top-down | hand-written parsers, many real compilers | one function per grammar rule; easy to write and debug |
| **LL(k)** | top-down | ANTLR | predicts using k tokens of lookahead |
| **LR / LALR** | bottom-up | yacc, Bison | powerful, handles more grammars; table-driven |
| **PEG / packrat** | top-down | modern parser generators | ordered choice, no ambiguity by construction |
| **Pratt parsing** | expression-focused | many real languages | elegant operator-precedence handling |

**Recursive descent** is the one to learn first and the one you'll most likely hand-write: each grammar rule becomes a function, and the call stack mirrors the tree. You'll build one in [`../10-LANGUAGE-DESIGN/02-Build-Your-Own-Language.md`](../10-LANGUAGE-DESIGN/02-Build-Your-Own-Language.md).

---

## VII. A TINY RECURSIVE-DESCENT PARSER (Python)

```python
# Grammar: expr ::= term (('+'|'-') term)*  ;  term ::= NUM
tokens = []  # e.g. ['3','+','4','-','5']
pos = 0

def peek():  return tokens[pos] if pos < len(tokens) else None
def advance():
    global pos; tok = tokens[pos]; pos += 1; return tok

def parse_term():
    return ('num', int(advance()))

def parse_expr():
    node = parse_term()
    while peek() in ('+', '-'):
        op = advance()
        right = parse_term()
        node = ('binop', op, node, right)   # build the tree left-associatively
    return node
```

Feed it `['3','+','4','-','5']` and you get `('binop','-',('binop','+',('num',3),('num',4)),('num',5))` — exactly `(3+4)-5`, correctly left-associative.

---

## 📌 Key Takeaways
- Parsing = lexing (chars → tokens) then parsing (tokens → AST).
- Grammars (BNF/EBNF) are usually **context-free**; nesting encodes precedence.
- The **AST** is the compiler's central data structure; everything downstream uses it.
- Ambiguity (dangling else, associativity) must be resolved by rules.
- **Recursive descent** is the parsing strategy to learn first — one function per rule.

**Next:** [`04-Values-Bindings-and-Scope.md`](./04-Values-Bindings-and-Scope.md)
