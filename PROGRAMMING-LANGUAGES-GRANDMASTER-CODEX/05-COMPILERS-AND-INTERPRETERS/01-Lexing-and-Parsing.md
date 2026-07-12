# 🔡 Lexing and Parsing (The Front End)

> *"The front end's job is to understand: to turn a meaningless string into a meaningful tree."*

This file deepens the parsing foundations from [`../01-LANGUAGE-FOUNDATIONS/03-Grammars-and-Parsing.md`](../01-LANGUAGE-FOUNDATIONS/03-Grammars-and-Parsing.md) with a compiler-builder's lens.

---

## I. LEXICAL ANALYSIS (THE LEXER)

The lexer scans raw characters and emits a stream of **tokens** — the atomic vocabulary. Each token has a *type* and often a *value* and *source position* (for error messages).

```
source:  let count = 42;
tokens:  KEYWORD("let")  IDENT("count")  OP("=")  NUMBER(42)  SEMICOLON
         @1:1            @1:5            @1:11   @1:13       @1:15
```

Implementation: tokens are described by **regular expressions**, and a lexer is essentially a **finite-state machine** that runs in linear time. Real lexers handle:
- **Keywords vs identifiers** — `if` is a keyword; `iffy` is an identifier (usually: lex as identifier, then check a keyword table).
- **Longest-match rule** — `>=` is one token, not `>` then `=`.
- **Whitespace & comments** — usually discarded (but Python tracks indentation as tokens!).
- **String/number literals** — with escapes, floats, hex, etc.
- **Error recovery** — reporting an illegal character with its line/column.

Tools: `lex`/`flex`, or hand-written (most production compilers hand-write for speed and better errors).

---

## II. SYNTACTIC ANALYSIS (THE PARSER)

The parser consumes tokens and builds the **AST** according to the grammar. Two broad families:

### Top-down (recursive descent, LL)
One function per grammar rule; the call stack mirrors the parse tree. Intuitive, hand-writable, great error messages. Used by GCC, Clang, and most modern compilers.

```
parse_statement()
  → parse_let()  →  expect("let"), parse_ident(), expect("="), parse_expr(), expect(";")
```

### Bottom-up (LR, LALR)
Builds the tree from the leaves up using a state machine and a stack, driven by generated tables. More powerful (handles more grammars), but generated tables are opaque and errors are cryptic. Used by `yacc`/`bison`.

**Pratt parsing** deserves special mention: an elegant technique for parsing expressions with precedence by associating "binding powers" with operators. It's what many real language parsers use for the expression sub-grammar because it handles precedence and associativity cleanly without deeply nested grammar rules.

---

## III. THE AST — DESIGNING THE TREE

The AST's node types mirror the language's constructs:

```
Program
 └─ FunctionDecl "main"
     └─ Block
         ├─ VarDecl "x" = BinaryExpr(+, Literal 3, Literal 4)
         └─ ReturnStmt(Identifier "x")
```

Good AST design matters: it's the interface between the front end and everything after. Each node typically stores its **source location** (so later stages can report "type error at line 12") and, after semantic analysis, its **resolved type** and **symbol references**.

Compilers often use the **visitor pattern** to walk the AST — a separate visitor for type checking, one for optimization, one for code generation — keeping each concern isolated.

---

## IV. ERROR HANDLING — THE MARK OF A GOOD COMPILER

Beginners think a compiler's job is to accept correct programs. Half its job is **rejecting incorrect ones helpfully.** The difference between a great and a terrible language experience is often error quality:

- **Error recovery** — after one syntax error, don't give up; resynchronize (e.g., skip to the next `;` or `}`) and keep parsing to report multiple errors in one run.
- **Precise locations** — "unexpected `}` at line 42, column 8" beats "syntax error."
- **Helpful messages** — Rust and Elm set the standard: they suggest fixes ("did you mean `foo`?", "add a semicolon here").

This is why parser construction cares so much about carrying source positions through every token and node.

---

## V. A COMPLETE MINI FRONT END (Python)

A calculator front end: lexer + recursive-descent parser producing an AST.

```python
import re

# --- LEXER ---
def lex(src):
    token_spec = [
        ('NUMBER', r'\d+(\.\d+)?'), ('PLUS', r'\+'), ('MINUS', r'-'),
        ('STAR', r'\*'), ('SLASH', r'/'), ('LPAREN', r'\('), ('RPAREN', r'\)'),
        ('SKIP', r'[ \t]+'),
    ]
    regex = '|'.join(f'(?P<{name}>{pat})' for name, pat in token_spec)
    for m in re.finditer(regex, src):
        kind = m.lastgroup
        if kind == 'SKIP': continue
        yield (kind, m.group())

# --- PARSER (recursive descent) ---
class Parser:
    def __init__(self, tokens): self.toks = list(tokens); self.i = 0
    def peek(self): return self.toks[self.i] if self.i < len(self.toks) else (None, None)
    def eat(self, kind):
        k, v = self.peek()
        if k != kind: raise SyntaxError(f'expected {kind}, got {k}')
        self.i += 1; return v
    def expr(self):                      # expr := term (('+'|'-') term)*
        node = self.term()
        while self.peek()[0] in ('PLUS', 'MINUS'):
            op = self.eat(self.peek()[0]); node = ('binop', op, node, self.term())
        return node
    def term(self):                      # term := factor (('*'|'/') factor)*
        node = self.factor()
        while self.peek()[0] in ('STAR', 'SLASH'):
            op = self.eat(self.peek()[0]); node = ('binop', op, node, self.factor())
        return node
    def factor(self):                    # factor := NUMBER | '(' expr ')'
        if self.peek()[0] == 'NUMBER': return ('num', float(self.eat('NUMBER')))
        self.eat('LPAREN'); node = self.expr(); self.eat('RPAREN'); return node

ast = Parser(lex("3 + 4 * (2 - 1)")).expr()
# ('binop','+',('num',3.0),('binop','*',('num',4.0),('binop','-',('num',2.0),('num',1.0))))
```

You now have a real, correct, precedence-aware front end in ~35 lines. In [`../10-LANGUAGE-DESIGN/02-Build-Your-Own-Language.md`](../10-LANGUAGE-DESIGN/02-Build-Your-Own-Language.md) you'll add an evaluator and turn this into a working language.

---

## 📌 Key Takeaways
- The **lexer** (a finite-state machine) turns characters into tokens via regexes; longest-match and keyword tables matter.
- The **parser** builds the AST; **recursive descent** (top-down) is the hand-writable default, **LR** (bottom-up) is more powerful, **Pratt** parsing handles operator precedence elegantly.
- The **AST** carries source positions and (later) types; compilers walk it with the **visitor pattern**.
- Great compilers excel at **error recovery and messages** — half the job is rejecting bad programs helpfully.

**Next:** [`02-Semantic-Analysis-and-IR.md`](./02-Semantic-Analysis-and-IR.md)
