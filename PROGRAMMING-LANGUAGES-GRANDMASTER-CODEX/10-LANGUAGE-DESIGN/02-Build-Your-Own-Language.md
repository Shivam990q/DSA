# 🛠️ Build Your Own Language (Project)

> *"In 200 lines of Python, you will build a real programming language — with variables, functions, closures, and conditionals. Then you will finally understand everything."*

This is the capstone. We build **"Mini"**, a small but *real* interpreted language, applying the whole codex: [grammar/parsing](../01-LANGUAGE-FOUNDATIONS/03-Grammars-and-Parsing.md), [scope/closures](../01-LANGUAGE-FOUNDATIONS/04-Values-Bindings-and-Scope.md), and [tree-walking interpretation](../05-COMPILERS-AND-INTERPRETERS/04-Interpreters-VMs-and-JIT.md).

---

## I. THE LANGUAGE WE'RE BUILDING

Mini supports: numbers, arithmetic, variables, `if/else` (as expressions), and **first-class functions with closures**. Target programs:

```
let x = 10;
let double = fn(n) { n * 2 };
let result = if (x > 5) { double(x) } else { 0 };
print(result);        # 20

let makeAdder = fn(a) { fn(b) { a + b } };   # a closure!
let add5 = makeAdder(5);
print(add5(3));       # 8
```

Our pipeline: **source → lexer → parser → evaluator → result.**

---

## II. STAGE 1 — THE LEXER (text → tokens)

```python
import re

TOKEN_SPEC = [
    ('NUMBER',  r'\d+(\.\d+)?'),
    ('ID',      r'[A-Za-z_]\w*'),
    ('OP',      r'==|!=|<=|>=|[+\-*/<>(){};,=]'),
    ('WS',      r'\s+'),
]
KEYWORDS = {'let', 'fn', 'if', 'else', 'print', 'true', 'false'}

def lex(src):
    regex = '|'.join(f'(?P<{n}>{p})' for n, p in TOKEN_SPEC)
    toks = []
    for m in re.finditer(regex, src):
        kind, val = m.lastgroup, m.group()
        if kind == 'WS':
            continue
        if kind == 'ID' and val in KEYWORDS:
            kind = val.upper()          # keywords get their own token type
        toks.append((kind, val))
    toks.append(('EOF', None))
    return toks
```

`let x = 10;` becomes `[('LET','let'),('ID','x'),('OP','='),('NUMBER','10'),('OP',';'),...]`.

---

## III. STAGE 2 — THE PARSER (tokens → AST)

A recursive-descent parser. AST nodes are simple tuples/dicts. Note the precedence ladder (`expr` → `comparison` → `term` → `factor` → `call` → `primary`).

```python
class Parser:
    def __init__(self, toks): self.toks = toks; self.i = 0
    def peek(self): return self.toks[self.i]
    def next(self): t = self.toks[self.i]; self.i += 1; return t
    def expect(self, val):
        k, v = self.next()
        if v != val: raise SyntaxError(f"expected '{val}', got '{v}'")

    def parse(self):                         # program := statement*
        stmts = []
        while self.peek()[0] != 'EOF':
            stmts.append(self.statement())
        return ('block', stmts)

    def statement(self):
        k, v = self.peek()
        if k == 'LET':
            self.next(); name = self.next()[1]; self.expect('=')
            val = self.expr(); self.expect(';')
            return ('let', name, val)
        if k == 'PRINT':
            self.next(); self.expect('('); arg = self.expr()
            self.expect(')'); self.expect(';')
            return ('print', arg)
        e = self.expr()
        if self.peek()[1] == ';': self.next()
        return e

    def expr(self):                          # comparison
        node = self.term()
        while self.peek()[1] in ('<','>','==','!=','<=','>='):
            op = self.next()[1]; node = ('binop', op, node, self.term())
        return node
    def term(self):                          # + -
        node = self.factor()
        while self.peek()[1] in ('+','-'):
            op = self.next()[1]; node = ('binop', op, node, self.factor())
        return node
    def factor(self):                        # * /
        node = self.call()
        while self.peek()[1] in ('*','/'):
            op = self.next()[1]; node = ('binop', op, node, self.call())
        return node
    def call(self):                          # function application: f(args)
        node = self.primary()
        while self.peek()[1] == '(':
            self.next(); args = []
            while self.peek()[1] != ')':
                args.append(self.expr())
                if self.peek()[1] == ',': self.next()
            self.next()
            node = ('call', node, args)
        return node
    def primary(self):
        k, v = self.peek()
        if k == 'NUMBER': self.next(); return ('num', float(v))
        if k == 'TRUE':   self.next(); return ('bool', True)
        if k == 'FALSE':  self.next(); return ('bool', False)
        if k == 'ID':     self.next(); return ('var', v)
        if k == 'FN':     return self.function()
        if k == 'IF':     return self.if_expr()
        if v == '(':      self.next(); e = self.expr(); self.expect(')'); return e
        raise SyntaxError(f"unexpected '{v}'")
    def function(self):                      # fn(params) { body }
        self.next(); self.expect('('); params = []
        while self.peek()[1] != ')':
            params.append(self.next()[1])
            if self.peek()[1] == ',': self.next()
        self.next(); self.expect('{'); body = self.expr(); self.expect('}')
        return ('fn', params, body)
    def if_expr(self):                       # if (cond) {..} else {..}  — an EXPRESSION
        self.next(); self.expect('('); cond = self.expr(); self.expect(')')
        self.expect('{'); then = self.expr(); self.expect('}')
        self.expect('ELSE') if self.peek()[0]=='ELSE' else self.expect('else')
        self.expect('{'); els = self.expr(); self.expect('}')
        return ('if', cond, then, els)
```

---

## IV. STAGE 3 — THE EVALUATOR (walk the AST)

Here's where [scope and closures](../01-LANGUAGE-FOUNDATIONS/04-Values-Bindings-and-Scope.md) come alive. An **environment** is a dict with a parent link (implementing lexical scope). A **closure** is literally `(params, body, defining_environment)`.

```python
class Env:
    def __init__(self, parent=None): self.vars = {}; self.parent = parent
    def get(self, name):
        if name in self.vars: return self.vars[name]
        if self.parent: return self.parent.get(name)     # search enclosing scope
        raise NameError(name)
    def set(self, name, val): self.vars[name] = val

class Closure:
    def __init__(self, params, body, env):
        self.params, self.body, self.env = params, body, env   # captures defining env!

def evaluate(node, env):
    kind = node[0]
    if kind == 'num':  return node[1]
    if kind == 'bool': return node[1]
    if kind == 'var':  return env.get(node[1])
    if kind == 'let':
        env.set(node[1], evaluate(node[2], env)); return None
    if kind == 'print':
        print(evaluate(node[1], env)); return None
    if kind == 'block':
        result = None
        for stmt in node[1]: result = evaluate(stmt, env)
        return result
    if kind == 'binop':
        _, op, a, b = node; l, r = evaluate(a, env), evaluate(b, env)
        return {'+':l+r,'-':l-r,'*':l*r,'/':l/r,'<':l<r,'>':l>r,
                '==':l==r,'!=':l!=r,'<=':l<=r,'>=':l>=r}[op]
    if kind == 'if':
        _, cond, then, els = node
        return evaluate(then, env) if evaluate(cond, env) else evaluate(els, env)
    if kind == 'fn':
        return Closure(node[1], node[2], env)     # capture the current env → closure
    if kind == 'call':
        _, fn_node, arg_nodes = node
        fn = evaluate(fn_node, env)
        args = [evaluate(a, env) for a in arg_nodes]
        call_env = Env(parent=fn.env)             # new scope, parent = where fn was DEFINED
        for p, a in zip(fn.params, args): call_env.set(p, a)
        return evaluate(fn.body, call_env)
    raise RuntimeError(f"unknown node {kind}")
```

---

## V. PUTTING IT TOGETHER

```python
def run(src):
    return evaluate(Parser(lex(src)).parse(), Env())

run('''
let x = 10;
let double = fn(n) { n * 2 };
let result = if (x > 5) { double(x) } else { 0 };
print(result);                       # 20

let makeAdder = fn(a) { fn(b) { a + b } };
let add5 = makeAdder(5);
print(add5(3));                      # 8  ← the closure remembers a=5!
''')
```

**You just built a programming language.** Run it — `add5(3)` prints `8`, proving closures work: `makeAdder(5)` returns an inner function that *captured* `a=5` in its environment, and it survives long after `makeAdder` returned. That's a closure, and you *implemented* it: it's the `Closure` object holding `fn.env`.

---

## VI. WHAT YOU JUST LEARNED (and where to go next)

By building this, you *implemented* the concepts the whole codex described:
- **Lexing & parsing** — text → tokens → AST (recursive descent, precedence ladder).
- **Scope & closures** — the `Env` chain *is* lexical scope; the `Closure` capturing `env` *is* how closures work in every language.
- **Expression-oriented evaluation** — `if` returns a value because we made it an expression.
- **Tree-walking interpretation** — the simplest execution strategy.

Extensions to make it a "real" language (each teaches more):
1. **Strings, lists, and more operators.**
2. **A type checker** — add [static semantics](../05-COMPILERS-AND-INTERPRETERS/02-Semantic-Analysis-and-IR.md) before evaluation.
3. **Compile to bytecode + a VM** — for speed (see [`../05-COMPILERS-AND-INTERPRETERS/04-Interpreters-VMs-and-JIT.md`](../05-COMPILERS-AND-INTERPRETERS/04-Interpreters-VMs-and-JIT.md)).
4. **A REPL** — read-eval-print loop for interactive use.
5. **Error messages with line numbers**, recursion, and a standard library.

For a book-length treatment, *Crafting Interpreters* (Nystrom) and *Writing an Interpreter in Go* (Ball) are the canonical guides — see [`../12-RESOURCES-AND-REFERENCES/00-Index.md`](../12-RESOURCES-AND-REFERENCES/00-Index.md).

---

## 📌 Key Takeaways
- A complete interpreter = **lexer → parser → evaluator**, buildable in ~200 lines.
- The **environment chain** implements lexical scope; a **closure is `(params, body, captured_env)`** — you implemented the concept, not just used it.
- Making `if`/`fn` return values gives an expression-oriented language.
- Tree-walking is the simplest execution model; bytecode/VM/JIT are optimizations on top.
- Building a language cements every concept in this codex and directly enables DSLs, config/query languages, and tooling.

**Next:** [`../11-CASE-STUDIES/00-Index.md`](../11-CASE-STUDIES/00-Index.md)
