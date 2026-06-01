# ☕ 05 — Exceptions & I/O

> *"Programs don't fail because the happy path is hard. They fail because the unhappy path was never written. Exceptions are how Java forces you to think about what goes wrong."*

**Prev:** [`04-Generics-And-Functional-Java.md`](./04-Generics-And-Functional-Java.md) · **Next:** [`06-Concurrency-And-Multithreading.md`](./06-Concurrency-And-Multithreading.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

# PART A — EXCEPTIONS

## I. WHAT AN EXCEPTION IS

When something goes wrong at runtime — a missing file, bad input, division by zero — Java creates an **exception object** and *throws* it. Execution stops and the JVM unwinds the call stack looking for a handler. If none catches it, the program crashes and prints a **stack trace**.

```java
public class FirstException {
    public static void main(String[] args) {
        int[] arr = {1, 2, 3};
        System.out.println(arr[5]);   // throws ArrayIndexOutOfBoundsException
        System.out.println("never reached");
    }
}
```

Reading a stack trace (top to bottom = innermost to outermost call):

```
Exception in thread "main" java.lang.ArrayIndexOutOfBoundsException: Index 5 out of bounds for length 3
        at FirstException.main(FirstException.java:4)   ← the exact line that threw
```

> **The stack trace is a gift, not noise.** It tells you the *exception type*, a *message*, and the *exact line*. Read it from the top. Most "I'm stuck" moments dissolve once you actually read the trace.

---

## II. THE EXCEPTION HIERARCHY

```
                Throwable
                /        \
           Error          Exception
        (don't catch)     /        \
                  RuntimeException   (checked exceptions)
                  (unchecked)         IOException, SQLException, ...
                  NullPointerException
                  IllegalArgumentException
                  ArithmeticException, ...
```

- **`Error`** — serious JVM problems (`OutOfMemoryError`, `StackOverflowError`). You generally do **not** catch these; the program is doomed.
- **`Exception`** — recoverable problems your code should handle.
  - **Checked exceptions** (direct subclasses of `Exception`, e.g. `IOException`): the compiler *forces* you to handle or declare them.
  - **Unchecked exceptions** (`RuntimeException` and subclasses, e.g. `NullPointerException`): the compiler doesn't force handling; they usually signal **programming bugs**.

### Checked vs unchecked — the crucial distinction

```java
import java.io.*;

public class CheckedVsUnchecked {

    // CHECKED: IOException must be declared (throws) or caught. Compiler enforces it.
    static void readFile() throws IOException {
        new FileReader("data.txt");   // FileReader's constructor can throw IOException
    }

    // UNCHECKED: no declaration needed. This is a bug to fix, not a condition to handle.
    static int divide(int a, int b) {
        return a / b;                 // throws ArithmeticException if b == 0 — unchecked
    }

    public static void main(String[] args) {
        // divide(10, 0);  // would throw ArithmeticException: / by zero
    }
}
```

| | Checked | Unchecked (RuntimeException) |
|---|---------|------------------------------|
| Examples | `IOException`, `SQLException` | `NullPointerException`, `IllegalArgumentException`, `ArithmeticException` |
| Compiler forces handling? | **Yes** (`throws` or `try/catch`) | No |
| Usually means | Expected external failure (file, network) | A bug in your code |
| Strategy | Handle or propagate deliberately | Fix the code; validate inputs |

> **Philosophy:** checked exceptions model conditions a *correct* program might still hit (the file genuinely isn't there). Unchecked exceptions model conditions a *correct* program never hits (you dereferenced null). Validate to prevent the unchecked ones; handle the checked ones.

---

## III. try / catch / finally

```java
public class TryCatchFinally {
    public static void main(String[] args) {
        try {
            int result = 10 / 0;                    // throws ArithmeticException
            System.out.println(result);             // skipped
        } catch (ArithmeticException e) {
            System.out.println("Caught: " + e.getMessage());  // Caught: / by zero
        } finally {
            System.out.println("Always runs");      // cleanup — runs whether or not we threw
        }
        System.out.println("Program continues");
    }
}
```

- **`try`** wraps code that might throw.
- **`catch`** handles a specific exception type (and its subclasses).
- **`finally`** always runs — exception or not, even after a `return`. Used for cleanup (closing resources).

### Multiple and multi-catch

```java
public class MultiCatch {
    public static void main(String[] args) {
        try {
            process(args);
        } catch (NumberFormatException e) {
            System.out.println("Not a number: " + e.getMessage());
        } catch (ArrayIndexOutOfBoundsException | NullPointerException e) {
            // multi-catch: handle several types the same way (Java 7+)
            System.out.println("Bad input: " + e.getClass().getSimpleName());
        } catch (Exception e) {
            // most general LAST — order matters: subclasses before superclasses
            System.out.println("Something else: " + e);
        }
    }
    static void process(String[] args) {
        int n = Integer.parseInt(args[0]);   // can throw both NFE and AIOOBE
        System.out.println(n);
    }
}
```

> **Gotcha — catch order matters.** A `catch (Exception e)` placed before `catch (IOException e)` makes the second unreachable (compile error): `Exception` already catches everything. Always order from most specific to most general.

---

## IV. throw AND throws

- **`throw`** (statement) actually raises an exception.
- **`throws`** (method clause) declares that a method may propagate a checked exception to its caller.

```java
public class ThrowAndThrows {

    // Validate input and throw if invalid — fail fast with a clear message
    static int parseAge(String input) {
        int age = Integer.parseInt(input);
        if (age < 0 || age > 150) {
            throw new IllegalArgumentException("Age out of range: " + age);  // throw
        }
        return age;
    }

    // Declare that we might propagate a checked exception
    static void riskyIO() throws java.io.IOException {
        throw new java.io.IOException("disk gone");
    }

    public static void main(String[] args) {
        try {
            System.out.println(parseAge("200"));
        } catch (IllegalArgumentException e) {
            System.out.println("Rejected: " + e.getMessage());
        }
    }
}
```

> **Fail fast.** Validate arguments at the top of a method and `throw IllegalArgumentException` immediately on bad input. A clear exception at the source beats a mysterious NPE three calls deeper.

---

## V. CUSTOM EXCEPTIONS

Define your own exception types to model your domain's failures. Extend `RuntimeException` for unchecked (the common modern choice) or `Exception` for checked.

```java
// Unchecked custom exception — for programming/domain errors callers usually can't recover from
public class InsufficientFundsException extends RuntimeException {
    private final double shortfall;

    public InsufficientFundsException(double shortfall) {
        super("Short by $" + shortfall);   // sets the message
        this.shortfall = shortfall;
    }
    public double getShortfall() { return shortfall; }
}
```

```java
public class Account {
    private double balance;
    public Account(double balance) { this.balance = balance; }

    public void withdraw(double amount) {
        if (amount > balance) {
            throw new InsufficientFundsException(amount - balance);  // rich, typed error
        }
        balance -= amount;
    }

    public static void main(String[] args) {
        Account acc = new Account(100);
        try {
            acc.withdraw(150);
        } catch (InsufficientFundsException e) {
            System.out.println(e.getMessage());          // Short by $50.0
            System.out.println("Need: $" + e.getShortfall());
        }
    }
}
```

### Exception chaining — preserve the cause

When you catch a low-level exception and rethrow a higher-level one, pass the original as the *cause* so the stack trace shows the full story.

```java
public class Chaining {
    static void loadConfig() {
        try {
            throw new java.io.IOException("config.yml not found");
        } catch (java.io.IOException e) {
            // Wrap, don't swallow — preserve the original cause
            throw new RuntimeException("Failed to start application", e);
        }
    }
    public static void main(String[] args) {
        try {
            loadConfig();
        } catch (RuntimeException e) {
            System.out.println(e.getMessage());            // Failed to start application
            System.out.println("Caused by: " + e.getCause()); // java.io.IOException: config.yml not found
        }
    }
}
```

---

## VI. EXCEPTION ANTI-PATTERNS

```java
public class AntiPatterns {
    public static void main(String[] args) {
        // ❌ 1. Swallowing — the worst. Errors vanish silently.
        try { risky(); } catch (Exception e) { /* nothing */ }

        // ❌ 2. Catching Throwable/Error — you can't recover from OutOfMemoryError
        // try { ... } catch (Throwable t) { ... }

        // ❌ 3. Using exceptions for control flow — slow and unclear
        // try { return list.get(i); } catch (IndexOutOfBoundsException e) { return null; }
        //   ↳ just check the index instead

        // ❌ 4. Logging AND rethrowing — produces duplicate noise; do one or the other
    }
    static void risky() throws Exception { throw new Exception("boom"); }
}
```

> **Never swallow.** An empty `catch` block is where bugs go to hide. At minimum log it (`e.printStackTrace()` while learning; a real logger in production). Catch the **narrowest** type you can actually handle, and let the rest propagate.

---

# PART B — INPUT / OUTPUT

## VII. THE I/O LANDSCAPE

Java has two I/O families:

- **`java.io`** (classic): streams (`InputStream`/`OutputStream` for bytes, `Reader`/`Writer` for characters). Verbose but everywhere.
- **`java.nio.file`** (modern, Java 7+): `Path` + `Files` — concise, the recommended default for most file work.

Start with `java.nio.file` — it does in one line what classic I/O does in ten.

## VIII. READING AND WRITING FILES (modern NIO)

```java
import java.nio.file.*;
import java.io.IOException;
import java.util.List;

public class ModernFileIO {
    public static void main(String[] args) throws IOException {
        Path path = Path.of("notes.txt");

        // WRITE a whole file (creates or overwrites)
        Files.writeString(path, "line one\nline two\nline three\n");

        // APPEND
        Files.writeString(path, "line four\n", StandardOpenOption.APPEND);

        // READ the whole file as one String
        String content = Files.readString(path);
        System.out.print(content);

        // READ all lines into a List
        List<String> lines = Files.readAllLines(path);
        System.out.println("Line count: " + lines.size());   // 4

        // Existence / metadata
        System.out.println(Files.exists(path));               // true
        System.out.println(Files.size(path) + " bytes");

        // Clean up
        Files.deleteIfExists(path);
    }
}
```

> **Gotcha — `readAllLines`/`readString` load the entire file into memory.** Fine for small files, dangerous for a 10GB log. For big files, stream them line by line (next section).

### Streaming a large file lazily

```java
import java.nio.file.*;
import java.io.IOException;
import java.util.stream.Stream;

public class StreamFile {
    public static void main(String[] args) throws IOException {
        Path path = Path.of("notes.txt");
        Files.writeString(path, "apple\nbanana\napricot\ncherry\n");

        // Files.lines returns a Stream — reads lazily, one line at a time
        try (Stream<String> lines = Files.lines(path)) {   // try-with-resources closes it
            long aWords = lines.filter(l -> l.startsWith("a")).count();
            System.out.println("Lines starting with 'a': " + aWords);  // 2
        }
        Files.deleteIfExists(path);
    }
}
```

---

## IX. try-with-resources — AUTOMATIC CLEANUP

Resources (files, sockets, DB connections) must be closed or you leak handles. Before Java 7 this meant a fragile `finally` block. **try-with-resources** closes anything implementing `AutoCloseable` automatically, in reverse order, even if an exception is thrown.

```java
import java.io.*;

public class TryWithResources {
    public static void main(String[] args) {
        // The OLD way — verbose, easy to get wrong
        BufferedReader reader = null;
        try {
            reader = new BufferedReader(new FileReader("data.txt"));
            System.out.println(reader.readLine());
        } catch (IOException e) {
            System.out.println("Error: " + e.getMessage());
        } finally {
            if (reader != null) {
                try { reader.close(); } catch (IOException ignored) {}   // ugh
            }
        }
    }
}
```

```java
import java.io.*;

public class CleanResources {
    public static void main(String[] args) {
        // The MODERN way — declare resources in the parens; they auto-close
        try (BufferedReader reader = new BufferedReader(new FileReader("data.txt"))) {
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
        } catch (FileNotFoundException e) {
            System.out.println("No such file");
        } catch (IOException e) {
            System.out.println("Read error: " + e.getMessage());
        }
        // reader.close() is called automatically — even on exception
    }

    // Multiple resources close in REVERSE order of declaration
    static void copy(String from, String to) throws IOException {
        try (var in  = new BufferedReader(new FileReader(from));
             var out = new BufferedWriter(new FileWriter(to))) {
            String line;
            while ((line = in.readLine()) != null) {
                out.write(line);
                out.newLine();
            }
        }   // out closes first, then in
    }
}
```

> **Always use try-with-resources for anything `AutoCloseable`.** It is shorter, correct, and handles the tricky case where both the body *and* `close()` throw (the close exception is "suppressed" and attached to the primary one). There is essentially no reason to hand-write resource cleanup anymore.

### Make your own class auto-closeable

```java
public class Connection implements AutoCloseable {
    public Connection() { System.out.println("opened"); }
    public void query() { System.out.println("querying"); }
    @Override public void close() { System.out.println("closed"); }  // called automatically

    public static void main(String[] args) {
        try (Connection c = new Connection()) {
            c.query();
        }
        // prints: opened / querying / closed
    }
}
```

---

## X. CLASSIC STREAMS — BYTES vs CHARACTERS

When you do need `java.io`, the key distinction is **byte streams** (raw binary: images, serialized data) vs **character streams** (text, with encoding).

```java
import java.io.*;
import java.nio.charset.StandardCharsets;

public class ByteVsChar {
    public static void main(String[] args) throws IOException {
        // CHARACTER stream — for text. ALWAYS specify the charset (UTF-8) to avoid platform bugs.
        try (Writer w = new OutputStreamWriter(
                 new FileOutputStream("hello.txt"), StandardCharsets.UTF_8)) {
            w.write("Héllo, wörld");          // non-ASCII chars handled correctly
        }

        // BYTE stream — for binary data
        byte[] data = {0x4A, 0x61, 0x76, 0x61};   // "Java"
        try (OutputStream os = new FileOutputStream("bytes.bin")) {
            os.write(data);
        }

        // Buffering wraps a stream to reduce expensive system calls — wrap for performance
        try (BufferedReader br = new BufferedReader(
                 new InputStreamReader(new FileInputStream("hello.txt"), StandardCharsets.UTF_8))) {
            System.out.println(br.readLine());     // Héllo, wörld
        }

        new File("hello.txt").delete();
        new File("bytes.bin").delete();
    }
}
```

> **Gotcha — always specify the charset.** Reading/writing text without specifying `StandardCharsets.UTF_8` uses the platform default, which differs across machines and corrupts non-ASCII text. The modern `Files.readString`/`writeString` default to UTF-8 — another reason to prefer NIO.

> **Gotcha — buffer your streams.** A raw `FileInputStream` does a system call per byte. Wrap it in a `BufferedInputStream`/`BufferedReader` to read in chunks — often a 10–100× speedup for line-by-line work.

---

## XI. A COMPLETE EXAMPLE — A ROBUST FILE PROCESSOR

```java
import java.nio.file.*;
import java.io.IOException;
import java.util.*;
import java.util.stream.*;

public class LogAnalyzer {

    // Custom exception for our domain
    static class LogParseException extends RuntimeException {
        LogParseException(String msg, Throwable cause) { super(msg, cause); }
    }

    static Map<String, Long> countLevels(Path logFile) {
        try (Stream<String> lines = Files.lines(logFile)) {   // auto-closed, memory-safe
            return lines
                .filter(l -> !l.isBlank())
                .map(l -> l.split(" ")[0])         // first token = level, e.g. "ERROR"
                .collect(Collectors.groupingBy(s -> s, Collectors.counting()));
        } catch (IOException e) {
            // wrap a checked IO failure in a domain exception, preserving the cause
            throw new LogParseException("Could not read " + logFile, e);
        }
    }

    public static void main(String[] args) throws IOException {
        Path log = Path.of("app.log");
        Files.writeString(log, """
            INFO server started
            WARN low memory
            ERROR null pointer
            INFO request handled
            ERROR timeout
            """);

        try {
            Map<String, Long> counts = countLevels(log);
            counts.forEach((level, count) -> System.out.println(level + ": " + count));
            // ERROR: 2, INFO: 2, WARN: 1
        } catch (LogParseException e) {
            System.err.println(e.getMessage() + " (cause: " + e.getCause() + ")");
        } finally {
            Files.deleteIfExists(log);
        }
    }
}
```

---

## XII. COMMON PITFALLS

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| Empty `catch` block | Bugs vanish silently | Log it; handle or rethrow |
| Catching `Exception`/`Throwable` broadly | Hides real problems, catches `Error` | Catch the narrowest type |
| Catch order: general before specific | Compile error / dead code | Specific first, general last |
| Not closing resources | File/connection leaks | try-with-resources |
| `readAllLines` on a huge file | `OutOfMemoryError` | `Files.lines` (stream) |
| No charset on text I/O | Corrupted non-ASCII text | Specify `UTF_8` / use NIO |
| Unbuffered byte-by-byte reads | Painfully slow | Wrap in `Buffered*` |
| Losing the cause when rethrowing | Useless stack trace | Chain with `new X(msg, cause)` |
| Using exceptions for control flow | Slow, unreadable | Check conditions instead |

---

## 🧠 KEY TAKEAWAYS

- An exception unwinds the stack until caught; the **stack trace** names the type, message, and exact line — read it first.
- **Checked** exceptions (compiler-enforced, e.g. `IOException`) model expected external failures; **unchecked** (`RuntimeException`) usually signal bugs — prevent them by validating.
- `try`/`catch`/`finally` handle and clean up; order catches **specific → general**; **never swallow** exceptions.
- Use `throw` to fail fast on bad input and define **custom exceptions** to model your domain; always **chain the cause** when wrapping.
- For files, prefer modern **`java.nio.file`** (`Path` + `Files`) — concise and UTF-8 by default; stream big files with `Files.lines`.
- **try-with-resources** is the only correct way to manage `AutoCloseable` resources — it closes them reliably, even on exceptions.
- With classic streams: distinguish **bytes vs characters**, always set the **charset**, and **buffer** for performance.

---

**Prev:** [`04-Generics-And-Functional-Java.md`](./04-Generics-And-Functional-Java.md) · **Next:** [`06-Concurrency-And-Multithreading.md`](./06-Concurrency-And-Multithreading.md) · **Index:** [`00-Index.md`](./00-Index.md)
