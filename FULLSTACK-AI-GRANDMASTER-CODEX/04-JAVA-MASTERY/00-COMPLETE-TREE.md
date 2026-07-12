# 🌳 THE COMPLETE JAVA TREE — "Nothing Left" Edition

> *The full map of everything we will learn, in the exact order to learn it. This is our checklist, our syllabus, and our compass. Mark `[x]` as each topic is completed.*

**How to read this:** Phases (0–13) → Modules → Topics. Every topic becomes its own lesson file with **Theory + Practical + Questions + Pitfalls**. Nothing here is optional for true mastery — the order is designed so each topic rests on the previous ones.

**Progress legend:** `[ ]` not started · `[~]` in progress · `[x]` mastered

---

## ✅ COMPLETENESS PROMISE & SCOPE

**The bar:** reading every lesson in this section, in order, = complete Java mastery. No external book or video required for the language and the JDK.

**What this covers (in full):** the **Java language** (every keyword, syntax, semantics) + **Java SE / the JDK standard library** (collections, generics, streams, I/O, NIO, networking, concurrency, time, reflection, modules) + **the JVM** (class loading, memory, GC, JIT, bytecode) + **tooling** (build, test, package, profile) + **best practices/design** + a **bridge to Spring/JDBC** for real backends.

**What is intentionally elsewhere (not "Java" itself):** deep Spring/Jakarta EE frameworks (overviewed here, mastered in this codex's backend sections), Android, and DSA-in-Java (see [`../../DSA-Grandmaster-Codex/`](../../DSA-Grandmaster-Codex/README.md)). Language *theory* in the abstract (type theory, GC algorithms as CS) lives in [`../../PROGRAMMING-LANGUAGES-GRANDMASTER-CODEX/`](../../PROGRAMMING-LANGUAGES-GRANDMASTER-CODEX/README.md).

> If you ever find a Java-SE topic not on this tree, it's a bug — tell me and it gets added. This is a living "nothing left" map.

---

## 🧭 PHASE 0 — SETUP & MENTAL MODEL
*Goal: understand what Java is and get code running on your machine.*

### 0.1 What Java Is
- [ ] History and philosophy (1995, Gosling, Sun/Oracle, "write once, run anywhere")
- [ ] Java editions: SE (Standard), EE/Jakarta (Enterprise), ME (Micro)
- [ ] Where Java is used (backend, Android, big data, enterprise)
- [ ] Java's key traits: object-oriented, platform-independent, GC, statically typed

### 0.2 How Java Runs (the mental model)
- [ ] Source code (`.java`) → bytecode (`.class`) → JVM → machine code
- [ ] What is bytecode; why it enables portability
- [ ] **JVM vs JRE vs JDK** (the classic confusion, settled)
- [ ] The JIT compiler and HotSpot (interpret then compile hot paths)
- [ ] JVM languages (Kotlin, Scala, Groovy, Clojure all run on the JVM)

### 0.3 Installation & Toolchain
- [ ] Choosing a JDK (Oracle vs OpenJDK vs Temurin/Adoptium) and an **LTS** version (8, 11, 17, 21)
- [ ] Installing the JDK; setting `JAVA_HOME` and `PATH`
- [ ] Verifying: `java -version`, `javac -version`
- [ ] IDEs: IntelliJ IDEA (recommended), Eclipse, VS Code + Java extensions

### 0.4 Your First Programs
- [ ] Anatomy of `HelloWorld.java` (class, `main`, `public static void`)
- [ ] Compiling with `javac` and running with `java`
- [ ] Single-file source execution (`java Hello.java`, JDK 11+)
- [ ] **JShell** — the REPL for experimenting
- [ ] Command-line arguments (`String[] args`)

---

## 🧱 PHASE 1 — LANGUAGE FUNDAMENTALS
*Goal: write any basic program with confidence.*

### 1.1 Syntax & Structure
- [ ] Statements, expressions, blocks, semicolons
- [ ] Comments (line, block, Javadoc)
- [ ] Naming conventions & code style
- [ ] Keywords and reserved words (full list)
- [ ] Identifiers and Unicode

### 1.2 Variables & Data Types
- [ ] Variable declaration, initialization, assignment
- [ ] **Primitive types**: `byte`, `short`, `int`, `long`, `float`, `double`, `char`, `boolean` (sizes, ranges, defaults)
- [ ] Literals: integer (binary/octal/hex), floating, char, boolean, string, underscores in literals
- [ ] Reference types vs primitives (stack vs heap intuition)
- [ ] `var` — local variable type inference (Java 10+)
- [ ] Constants and `final`
- [ ] Default values and scope of variables

### 1.3 Type Conversion & Casting
- [ ] Widening (implicit) conversions
- [ ] Narrowing (explicit) casts
- [ ] Autoboxing / unboxing (primitive ↔ wrapper)
- [ ] Overflow, underflow, precision loss
- [ ] `char` ↔ `int` arithmetic

### 1.4 Operators
- [ ] Arithmetic (`+ - * / %`), integer vs float division
- [ ] Relational (`== != < > <= >=`)
- [ ] Logical (`&& || !`) and short-circuiting
- [ ] Bitwise & shift (`& | ^ ~ << >> >>>`)
- [ ] Assignment & compound (`= += -= ...`)
- [ ] Increment/decrement (pre vs post)
- [ ] Ternary `?:`
- [ ] `instanceof`
- [ ] Operator precedence & associativity

### 1.5 Strings
- [ ] `String` basics and **immutability**
- [ ] The **String constant pool** and `intern()`
- [ ] `==` vs `.equals()` for strings (critical!)
- [ ] Common `String` methods (length, charAt, substring, indexOf, split, replace, etc.)
- [ ] **`StringBuilder` vs `StringBuffer` vs `String`** (when and why)
- [ ] String formatting (`String.format`, `printf`, formatted)
- [ ] Text blocks (multi-line strings, Java 15+)

### 1.6 Input & Output Basics
- [ ] `System.out.print` / `println` / `printf`
- [ ] `Scanner` for console input
- [ ] `System.in`, `System.err`
- [ ] `BufferedReader` for input (intro)

### 1.7 Control Flow
- [ ] `if` / `else if` / `else`
- [ ] `switch` statement (classic, fall-through, `break`)
- [ ] `switch` **expressions** (arrow syntax, `yield`, Java 14+)
- [ ] `switch` **pattern matching** (Java 21+)
- [ ] `while` loop
- [ ] `do-while` loop
- [ ] `for` loop
- [ ] Enhanced `for` (for-each)
- [ ] `break`, `continue`, and **labeled** break/continue

### 1.8 Arrays
- [ ] Declaration, instantiation, initialization
- [ ] Indexing, `length`, `ArrayIndexOutOfBoundsException`
- [ ] Iterating arrays
- [ ] Multi-dimensional arrays (2D, jagged/ragged)
- [ ] `Arrays` utility class (sort, fill, copyOf, equals, toString, binarySearch)
- [ ] Arrays vs collections (preview)

### 1.9 Complete Keyword & Modifier Reference
- [ ] All 50+ reserved words grouped (control, types, modifiers, OOP, exceptions, etc.)
- [ ] Modifiers deep: `static`, `final`, `abstract`, `synchronized`, `volatile`, `transient`, `native`, `strictfp`, `default`
- [ ] Bit manipulation utilities (`Integer.bitCount`, `Long.numberOfLeadingZeros`, masks/flags)
- [ ] `assert` preview (full treatment in Phase 3)

---

## 🧩 PHASE 2 — OBJECT-ORIENTED JAVA
*Goal: model any domain with clean OOP.*

### 2.1 Classes & Objects
- [ ] Defining a class; fields and methods
- [ ] Creating objects with `new`; references
- [ ] Instance vs class members
- [ ] Methods: parameters, return types, `void`
- [ ] Method overloading
- [ ] Varargs (`String...`)
- [ ] Pass-by-value (Java is *always* pass-by-value — the truth)

### 2.2 Constructors & Initialization
- [ ] Default and parameterized constructors
- [ ] `this` reference and `this()` constructor chaining
- [ ] Constructor overloading
- [ ] Instance initializer blocks; field initialization order
- [ ] `static` initializer blocks

### 2.3 Encapsulation & Access Control
- [ ] Access modifiers: `public`, `private`, `protected`, default (package-private)
- [ ] Getters/setters and the JavaBean convention
- [ ] Encapsulation as invariant protection

### 2.4 `static`
- [ ] Static fields (class variables)
- [ ] Static methods (and why `main` is static)
- [ ] Static blocks
- [ ] Static nested classes
- [ ] When static is right (and the overuse anti-pattern)

### 2.5 Inheritance
- [ ] `extends`, the `Object` superclass
- [ ] `super` (fields, methods, constructors)
- [ ] Method **overriding** vs **overloading** (the key distinction)
- [ ] `@Override`, covariant return types
- [ ] Constructor calls up the hierarchy
- [ ] `final` classes/methods (preventing inheritance/override)
- [ ] Composition over inheritance (design lesson)

### 2.6 Polymorphism
- [ ] Compile-time (static) polymorphism — overloading
- [ ] Runtime (dynamic) polymorphism — overriding, dynamic dispatch
- [ ] Upcasting and downcasting; `ClassCastException`
- [ ] `instanceof` and pattern matching for `instanceof` (Java 16+)

### 2.7 Abstraction
- [ ] Abstract classes and abstract methods
- [ ] **Interfaces**: definition, implementing, multiple interfaces
- [ ] `default` and `static` interface methods (Java 8+)
- [ ] `private` interface methods (Java 9+)
- [ ] Functional interfaces (`@FunctionalInterface`) — preview to Phase 6
- [ ] Abstract class vs interface (when to use which)
- [ ] Marker interfaces

### 2.8 The `Object` Class
- [ ] `toString()`
- [ ] `equals()` and `hashCode()` — the **contract** (deep, critical)
- [ ] `getClass()`
- [ ] `clone()` and `Cloneable` (shallow vs deep copy)
- [ ] `finalize()` (deprecated — why)
- [ ] `wait`/`notify`/`notifyAll` (preview to concurrency)

### 2.9 Nested & Anonymous Classes
- [ ] Static nested classes
- [ ] Inner (non-static nested) classes
- [ ] Local classes
- [ ] Anonymous classes
- [ ] Lambdas as a replacement (preview)

### 2.10 Special Class Types
- [ ] **Enums**: basics, fields, constructors, methods, `values()`, `valueOf()`, `EnumMap`/`EnumSet`
- [ ] **Records** (Java 16+): compact data classes, components, canonical/compact constructors
- [ ] **Sealed classes/interfaces** (Java 17+): `sealed`, `permits`, `non-sealed`
- [ ] Nested/inner enums and records

### 2.11 Packages & Organization
- [ ] `package` declaration and directory structure
- [ ] `import` (single, wildcard, static imports)
- [ ] Fully-qualified names
- [ ] The **classpath** explained
- [ ] Access across packages

---

## 🛠️ PHASE 3 — CORE APIs & EXCEPTIONS
*Goal: handle errors and use the everyday standard library.*

### 3.1 Exception Handling
- [ ] What exceptions are; the `Throwable` hierarchy (`Error` vs `Exception`)
- [ ] **Checked vs unchecked** exceptions (and `RuntimeException`)
- [ ] `try` / `catch` / `finally`
- [ ] Multi-catch and catch order
- [ ] `throw` vs `throws`
- [ ] Custom exceptions
- [ ] **Try-with-resources** and `AutoCloseable`
- [ ] Exception chaining (cause), suppressed exceptions
- [ ] Stack traces; reading them
- [ ] Best practices (don't swallow, fail fast, specific over generic)

### 3.2 Wrapper Classes
- [ ] `Integer`, `Long`, `Double`, `Boolean`, `Character`, etc.
- [ ] Boxing/unboxing pitfalls (`NullPointerException`, `==` on wrappers, Integer cache)
- [ ] Parsing (`parseInt`, `valueOf`) and formatting
- [ ] Useful constants and methods (MAX_VALUE, compare, etc.)

### 3.3 Numbers & Math
- [ ] `Math` class (common methods)
- [ ] `Random` and `ThreadLocalRandom`
- [ ] `BigInteger` (arbitrary precision)
- [ ] `BigDecimal` (exact decimal — why not `double` for money)

### 3.4 Date & Time (java.time)
- [ ] `LocalDate`, `LocalTime`, `LocalDateTime`
- [ ] `Instant`, `Duration`, `Period`
- [ ] `ZonedDateTime`, time zones, `ZoneId`
- [ ] Formatting/parsing (`DateTimeFormatter`)
- [ ] Legacy `Date`/`Calendar` (and why to avoid)

### 3.5 Optional
- [ ] The null problem and what `Optional` solves
- [ ] Creating (`of`, `ofNullable`, `empty`)
- [ ] Using (`isPresent`, `get`, `orElse`, `orElseGet`, `orElseThrow`, `map`, `filter`, `ifPresent`)
- [ ] Optional anti-patterns (fields, parameters)

### 3.6 Regular Expressions
- [ ] `Pattern` and `Matcher`
- [ ] Common regex syntax
- [ ] `String` regex methods (`matches`, `replaceAll`, `split`)
- [ ] Groups and capturing

### 3.7 Assertions
- [ ] The `assert` statement (two forms), enabling with `-ea`
- [ ] Assertions vs exceptions (when each is appropriate)
- [ ] Design-by-contract intuition

### 3.8 Internationalization (i18n) & Formatting
- [ ] `Locale` and locale-sensitive behavior
- [ ] `ResourceBundle` (message catalogs, translations)
- [ ] `NumberFormat`, `DecimalFormat`, currency & percent formatting
- [ ] `MessageFormat`; locale-aware date/number formatting
- [ ] Character encodings & `Charset` (UTF-8, the encoding trap)

---

## 🔷 PHASE 4 — GENERICS
*Goal: write type-safe, reusable code.*

### 4.1 Generics Basics
- [ ] Why generics (type safety, no casts, the pre-generics pain)
- [ ] Generic classes
- [ ] Generic methods
- [ ] Generic interfaces
- [ ] Type parameter naming conventions (`T`, `E`, `K`, `V`, `?`)

### 4.2 Bounds & Wildcards
- [ ] Bounded type parameters (`<T extends Number>`)
- [ ] Multiple bounds
- [ ] Wildcards: unbounded `<?>`, upper `<? extends T>`, lower `<? super T>`
- [ ] **PECS** — Producer Extends, Consumer Super
- [ ] Wildcard capture

### 4.3 Under the Hood & Limits
- [ ] **Type erasure** (how generics really work)
- [ ] Limitations: no primitives, no `new T()`, no generic arrays, no `instanceof` with generics
- [ ] Bridge methods (brief)
- [ ] Heap pollution and `@SafeVarargs`
- [ ] Generic best practices

---

## 📦 PHASE 5 — COLLECTIONS FRAMEWORK
*Goal: choose and use the right data structure every time.*

### 5.1 Overview & Hierarchy
- [ ] The Collections Framework map (`Iterable` → `Collection` → `List`/`Set`/`Queue`; `Map` separate)
- [ ] `Iterable` and `Iterator`; `ListIterator`
- [ ] `Collection` core methods
- [ ] **Fail-fast vs fail-safe** iterators; `ConcurrentModificationException`

### 5.2 List
- [ ] `ArrayList` (internals: dynamic array, resizing, amortized cost)
- [ ] `LinkedList` (doubly-linked; when it actually helps)
- [ ] `Vector` and `Stack` (legacy; why avoid)
- [ ] List operations & complexity

### 5.3 Set
- [ ] `HashSet` (hashing, no order)
- [ ] `LinkedHashSet` (insertion order)
- [ ] `TreeSet` (sorted, `NavigableSet`)
- [ ] Set operations (union/intersection/difference)

### 5.4 Map
- [ ] `HashMap` — **internal working** (buckets, hashing, collisions, treeify at 8, load factor, resize)
- [ ] `LinkedHashMap` (order, LRU cache trick)
- [ ] `TreeMap` (sorted, `NavigableMap`)
- [ ] `Hashtable` (legacy) and `Properties`
- [ ] Iterating maps (`entrySet`, `keySet`, `values`, `forEach`)
- [ ] `getOrDefault`, `computeIfAbsent`, `merge`, `putIfAbsent`

### 5.5 Queue & Deque
- [ ] `Queue` interface
- [ ] `PriorityQueue` (heap-backed)
- [ ] `ArrayDeque` (stack + queue; preferred over `Stack`/`LinkedList`)

### 5.6 Sorting & Ordering
- [ ] `Comparable` (`compareTo`) — natural ordering
- [ ] `Comparator` — custom ordering, `comparing`, `thenComparing`, `reversed`
- [ ] `Collections.sort`, `List.sort`
- [ ] The `equals`/`hashCode`/`compareTo` consistency contract

### 5.7 Utilities & Immutability
- [ ] `Collections` utility (unmodifiable, synchronized, singleton, emptyList, frequency)
- [ ] Immutable collections (`List.of`, `Map.of`, `Set.of`, Java 9+)
- [ ] Choosing the right collection (a decision table + complexity cheat-sheet)

---

## λ PHASE 6 — FUNCTIONAL JAVA
*Goal: think and code in the modern functional style.*

### 6.1 Lambdas & Functional Interfaces
- [ ] Lambda expression syntax and semantics
- [ ] Functional interfaces & `@FunctionalInterface`
- [ ] Built-in functional interfaces: `Predicate`, `Function`, `BiFunction`, `Consumer`, `Supplier`, `UnaryOperator`, `BinaryOperator`
- [ ] Capturing variables (effectively final)
- [ ] Lambdas vs anonymous classes (differences, `this`)

### 6.2 Method References
- [ ] Static (`ClassName::method`)
- [ ] Instance of a particular object
- [ ] Instance of an arbitrary object of a type
- [ ] Constructor references (`ClassName::new`)

### 6.3 Streams API
- [ ] What streams are (not collections); lazy evaluation
- [ ] Creating streams (from collections, `Stream.of`, `IntStream.range`, generate/iterate)
- [ ] Intermediate ops (`filter`, `map`, `flatMap`, `distinct`, `sorted`, `peek`, `limit`, `skip`)
- [ ] Terminal ops (`forEach`, `collect`, `reduce`, `count`, `min`/`max`, `findFirst`, `anyMatch`/`allMatch`/`noneMatch`)
- [ ] `Collectors` (toList/toSet/toMap, joining, counting, summing, averaging)
- [ ] **Grouping** (`groupingBy`) and **partitioning** (`partitioningBy`)
- [ ] Primitive streams (`IntStream`, `LongStream`, `DoubleStream`) and boxing
- [ ] `Optional` in streams
- [ ] **Parallel streams** (when they help, when they hurt)
- [ ] Stream pitfalls (reuse, statefulness, side effects)

---

## 💾 PHASE 7 — I/O, NIO & NETWORKING
*Goal: read/write anything — console, files, network, objects.*

### 7.1 Classic I/O (java.io)
- [ ] Byte streams (`InputStream`/`OutputStream`)
- [ ] Character streams (`Reader`/`Writer`)
- [ ] Buffered streams (`BufferedReader`/`BufferedWriter`)
- [ ] `File` class basics
- [ ] Reading/writing text and binary files
- [ ] Try-with-resources for I/O

### 7.2 NIO.2 (java.nio.file)
- [ ] `Path` and `Paths`
- [ ] `Files` utility (read/write/copy/move/delete/walk)
- [ ] Reading all lines / streaming lines
- [ ] Directory operations and `DirectoryStream`

### 7.3 Serialization
- [ ] `Serializable`, `serialVersionUID`
- [ ] `ObjectOutputStream`/`ObjectInputStream`
- [ ] `transient` fields
- [ ] Serialization risks & alternatives (JSON, etc.)

### 7.4 Networking (java.net)
- [ ] IP, ports, TCP vs UDP (just enough theory)
- [ ] `InetAddress`, `URL`, `URLConnection`
- [ ] TCP sockets: `Socket`, `ServerSocket` (a tiny client + server)
- [ ] UDP: `DatagramSocket`, `DatagramPacket`
- [ ] The modern **`HttpClient`** (Java 11+): sync & async requests
- [ ] Reading/writing over the network with streams

---

## 🔀 PHASE 8 — CONCURRENCY & MULTITHREADING
*Goal: write correct, fast concurrent code.*

### 8.1 Thread Basics
- [ ] Processes vs threads
- [ ] Creating threads (`Thread`, `Runnable`)
- [ ] Thread lifecycle & states
- [ ] `start` vs `run`, `sleep`, `join`, `interrupt`
- [ ] Daemon threads, priorities

### 8.2 Synchronization
- [ ] Race conditions & the need for synchronization
- [ ] `synchronized` methods and blocks; intrinsic locks/monitors
- [ ] `volatile` and visibility
- [ ] `wait` / `notify` / `notifyAll`; producer–consumer
- [ ] Deadlock, livelock, starvation
- [ ] `Atomic` classes (`AtomicInteger`, CAS)
- [ ] Explicit locks (`ReentrantLock`, `ReadWriteLock`, `Condition`)

### 8.3 High-Level Concurrency (java.util.concurrent)
- [ ] `Executor`, `ExecutorService`, thread pools (`Executors` factory)
- [ ] `Callable` and `Future`
- [ ] `CompletableFuture` (async composition)
- [ ] Concurrent collections (`ConcurrentHashMap`, `CopyOnWriteArrayList`, `BlockingQueue`)
- [ ] `CountDownLatch`, `CyclicBarrier`, `Semaphore`, `Phaser`
- [ ] Fork/Join framework & work stealing
- [ ] `ThreadLocal` and `InheritableThreadLocal`
- [ ] Scoped values (Java 21+)

### 8.4 The Java Memory Model & Modern Threads
- [ ] The Java Memory Model (happens-before, visibility, reordering)
- [ ] **Virtual threads** (Project Loom, Java 21) — millions of cheap threads
- [ ] Structured concurrency (preview)
- [ ] Best practices & common concurrency bugs

---

## ⚙️ PHASE 9 — JVM INTERNALS & PERFORMANCE
*Goal: understand and tune what runs your code.*

### 9.1 Class Loading
- [ ] Class loaders (bootstrap, platform, application) & delegation
- [ ] Loading → Linking (verify/prepare/resolve) → Initialization
- [ ] Custom class loaders (concept)

### 9.2 JVM Memory
- [ ] Runtime data areas: heap, stacks, metaspace, PC register, native method stack
- [ ] Object layout, references, escape analysis
- [ ] Stack vs heap in depth

### 9.3 Garbage Collection
- [ ] Reachability & GC roots
- [ ] Generational GC (young/old, minor/major GC)
- [ ] Collectors: Serial, Parallel, **G1**, **ZGC**, Shenandoah
- [ ] GC tuning flags; reading GC logs
- [ ] Memory leaks in a GC'd language (yes, they happen)
- [ ] References: strong, soft, weak, phantom

### 9.4 Execution & Tooling
- [ ] Bytecode and `javap`
- [ ] Interpretation + JIT (C1/C2, tiered compilation)
- [ ] **Reflection** (Class, Field, Method, `setAccessible`)
- [ ] **Annotations** (built-in, custom, retention, targets, processing)
- [ ] Dynamic proxies
- [ ] Profiling (JFR, VisualVM), **JMH** microbenchmarking

### 9.5 Extensibility & Native Interop
- [ ] **SPI** and `ServiceLoader` (pluggable services)
- [ ] Instrumentation & Java agents (`-javaagent`, bytecode manipulation) — concept
- [ ] **Foreign Function & Memory API** (Project Panama, calling native code) — modern
- [ ] **JNI** (the legacy native interface) — concept
- [ ] Vector API (SIMD, incubator) — concept

---

## ✨ PHASE 10 — MODERN JAVA (8 → 21+)
*Goal: write idiomatic modern Java and know what changed when.*

- [ ] Recap: lambdas, streams, `Optional`, `java.time` (Java 8)
- [ ] `var` (10), `List.of`/`Map.of` (9), private interface methods (9)
- [ ] **Records** (16), **sealed** classes (17)
- [ ] **Pattern matching**: `instanceof` (16), `switch` patterns (21), record patterns (21)
- [ ] **Text blocks** (15)
- [ ] Enhanced `switch` expressions (14)
- [ ] **Virtual threads** & structured concurrency (21)
- [ ] **Modules (JPMS)**: `module-info.java`, `requires`/`exports`, modular JDK
- [ ] Version-by-version feature map (8, 11, 17, 21 LTS + notable in-between)

---

## 🧰 PHASE 11 — BUILD, TEST & TOOLING
*Goal: work like a professional Java engineer.*

### 11.1 Build Tools
- [ ] Why build tools; the classpath problem they solve
- [ ] **Maven** (POM, lifecycle, dependencies, repositories, plugins)
- [ ] **Gradle** (build.gradle, tasks, Kotlin/Groovy DSL)
- [ ] Dependency management & transitive dependencies

### 11.2 Testing
- [ ] **JUnit 5** (annotations, assertions, lifecycle, parameterized tests)
- [ ] **Mockito** (mocks, stubs, verify)
- [ ] AssertJ / Hamcrest (fluent assertions)
- [ ] Test-driven development basics; test coverage

### 11.3 Logging & Packaging
- [ ] Logging: `java.util.logging`, SLF4J + Logback/Log4j2
- [ ] Packaging: JAR, executable/fat JAR, `MANIFEST.MF`
- [ ] `jlink` (custom runtime), `jpackage`, GraalVM native image (intro)
- [ ] Debugging (breakpoints, watches, remote debug)
- [ ] **`javadoc`** — writing and generating API documentation
- [ ] Interacting with the OS: `ProcessBuilder`, `Runtime`, environment & system properties
- [ ] `java`/`javac` advanced flags; JShell for exploration

---

## 🏛️ PHASE 12 — BEST PRACTICES & DESIGN
*Goal: write code a senior engineer respects.*

- [ ] **Effective Java** essentials (Bloch): static factories, builders, immutability, prefer composition, minimize mutability, favor interfaces
- [ ] `equals`/`hashCode`/`toString` done right (revisited with rigor)
- [ ] **SOLID** principles in Java
- [ ] **Design patterns** in Java (Singleton, Factory, Builder, Strategy, Observer, Decorator, Adapter, etc.)
- [ ] Clean code idioms & naming
- [ ] Common anti-patterns & code smells
- [ ] Defensive copying, immutability, null-safety strategies

---

## 🌉 PHASE 13 — BEYOND CORE (BRIDGES)
*Goal: connect Java to the real world and to jobs.*

- [ ] **JDBC** — connecting to databases (Connection, Statement, PreparedStatement, ResultSet, transactions)
- [ ] Intro to **Spring / Spring Boot** → `08-Spring-Boot-Essentials.md` and `09-Spring-Boot-Data-And-JPA.md` (in this folder)
- [ ] **DSA in Java** → pair with [`../../DSA-Grandmaster-Codex/`](../../DSA-Grandmaster-Codex/README.md)
- [ ] Annotation processing & code generation (Lombok, MapStruct)
- [ ] **Interview mastery**: core-Java Q&A, tricky output questions, concurrency puzzles, JVM questions

---

## 🗺️ THE LEARNING ORDER (linear path)

Walk phases **0 → 13 in order**. Within a phase, walk modules top to bottom. Do not skip — Phase N assumes Phases 0…N-1.

```
0 Setup ─► 1 Fundamentals ─► 2 OOP ─► 3 Core APIs/Exceptions ─► 4 Generics
   └─► 5 Collections ─► 6 Functional ─► 7 I/O ─► 8 Concurrency
        └─► 9 JVM Internals ─► 10 Modern Java ─► 11 Tooling ─► 12 Best Practices ─► 13 Bridges
```

**Milestones:**
- After **Phase 2** → you can build small OOP programs.
- After **Phase 6** → you can write real, idiomatic modern Java.
- After **Phase 8** → you're job-ready for most Java backend roles.
- After **Phase 12** → you're a Java grandmaster.

---

## ⚙️ HOW WE PROCEED (the method)

For **each topic** in this tree, we create one lesson file with four layers:

1. **🧠 Theory** — every term defined, how it works under the hood, *why* it exists.
2. **⌨️ Practical** — complete, runnable code examples you type and run.
3. **❓ Questions** — self-check + interview questions, with answers.
4. **⚠️ Pitfalls** — the classic mistakes, so you avoid them.

Files live in phase folders, e.g. `01-LANGUAGE-FUNDAMENTALS/01-Syntax-And-Structure.md`.

**To begin a lesson, just say:** *"start Phase 0"* (or any specific topic like *"teach 1.5 Strings"*), and we build that lesson in full depth. Then mark it `[x]` here and move to the next.

---

*🌳 The tree is planted. Now we grow it, one leaf at a time, until nothing is left.*
