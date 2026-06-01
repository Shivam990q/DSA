# ☕ Java Mastery

> *"Java is verbose on purpose. That verbosity is a contract: the compiler reads your intent and refuses to let you lie. Master Java and you master the discipline of large systems."*

> **Section 04 of the** [`FULLSTACK-AI-GRANDMASTER-CODEX`](../README.md). This module takes you from `public static void main` to a deployed Spring Boot REST API backed by a real database.

---

## 🎯 WHAT YOU WILL OWN AFTER THIS SECTION

- The **language**: syntax, types, control flow, and what the JVM actually does with your code
- **Object-oriented design** the way senior engineers actually use it (not just textbook definitions)
- The **Collections Framework** — the data structures you reach for every single day
- **Generics** and **functional Java** (lambdas, streams) — modern, expressive, safe code
- **Exceptions and I/O** — failing gracefully and talking to files
- **Concurrency** — threads, executors, and the pitfalls that cause 3 a.m. pages
- **Spring Boot** — the framework that runs a huge share of the world's backends
- **Spring Data JPA** — turning Java objects into database rows and back

---

## 📚 CONTENTS — LEARNING ORDER

> Read in order. Each file assumes the ones before it. The ⭐ files are the highest-leverage — do not skim them.

| # | File | What it covers | Priority |
|---|------|----------------|----------|
| 00 | [`00-Index.md`](./00-Index.md) | You are here | — |
| 01 | [`01-Java-Fundamentals.md`](./01-Java-Fundamentals.md) | Syntax, types, variables, operators, control flow, I/O, `main`, compilation & the JVM | Core |
| 02 | [`02-OOP-In-Java.md`](./02-OOP-In-Java.md) | Classes, objects, constructors, the 4 pillars, interfaces vs abstract classes | ⭐ |
| 03 | [`03-Collections-Framework.md`](./03-Collections-Framework.md) | List, Set, Map, Queue/Deque, iterators, choosing the right structure | ⭐ |
| 04 | [`04-Generics-And-Functional-Java.md`](./04-Generics-And-Functional-Java.md) | Generics, bounds, wildcards, lambdas, Stream API, Optional, method references | ⭐ |
| 05 | [`05-Exceptions-And-IO.md`](./05-Exceptions-And-IO.md) | try/catch/finally, checked vs unchecked, custom exceptions, file I/O, try-with-resources | Core |
| 06 | [`06-Concurrency-And-Multithreading.md`](./06-Concurrency-And-Multithreading.md) | Threads, Runnable, synchronized, locks, ExecutorService, CompletableFuture, pitfalls | ⭐ |
| 07 | [`07-Spring-Boot-Essentials.md`](./07-Spring-Boot-Essentials.md) | Spring/Spring Boot, DI, @RestController, REST APIs, @Service/@Repository, config | ⭐ |
| 08 | [`08-Spring-Boot-Data-And-JPA.md`](./08-Spring-Boot-Data-And-JPA.md) | Spring Data JPA, entities, repositories, relationships, databases, CRUD API | Core |

---

## 🛠️ SETUP — GET A WORKING JDK

You write `.java` source files; the JDK turns them into runnable programs. You need the **JDK** (Java Development Kit), not just the JRE.

### Which version?

Use a **Long-Term Support (LTS)** release. As of this writing the strong default is **Java 21 (LTS)**; **Java 17 (LTS)** is also everywhere in industry. Everything in this section runs on Java 17+. Where a feature is newer (records, switch expressions, virtual threads), it is called out.

### Install

| OS | Easiest path |
|----|--------------|
| Windows | Install [Eclipse Temurin (Adoptium)](https://adoptium.net) JDK 21, or use `winget install EclipseAdoptium.Temurin.21.JDK` |
| macOS | `brew install temurin` (Homebrew) or download from Adoptium |
| Linux | `sudo apt install openjdk-21-jdk` (Debian/Ubuntu) or your distro's package |

Verify the install:

```bash
java -version     # runtime
javac -version    # compiler — if this fails you installed the JRE, not the JDK
```

### Your first program — the manual way

```java
// File: Hello.java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Welcome to Java Mastery.");
    }
}
```

```bash
javac Hello.java     # compiles to Hello.class (bytecode)
java Hello           # runs it → "Welcome to Java Mastery."
```

> **Modern shortcut (Java 11+):** `java Hello.java` compiles and runs single-file programs in one step — great for learning. You still need real compilation for multi-file projects.

### The tools you will actually use

- **IDE:** IntelliJ IDEA (Community edition is free) is the industry standard. VS Code with the Java extension pack also works well.
- **Build tool:** **Maven** or **Gradle**. They manage dependencies (libraries) and the build lifecycle. Spring Boot projects use one of these. We use **Maven** in the Spring sections because its XML is explicit and easy to read.
- **Project starter:** [start.spring.io](https://start.spring.io) generates a ready-to-run Spring Boot project.

---

## 🧭 HOW TO STUDY THIS SECTION

1. **Type the code, don't copy-paste.** Muscle memory matters. Break the examples on purpose and read the error.
2. **Keep a scratch project open.** Have a `Scratch.java` with a `main` method you can paste experiments into.
3. **Read the compiler errors.** Java's errors are wordy but precise. The error is a teacher.
4. **Build something after each file.** A CLI tool after fundamentals, a small class hierarchy after OOP, a REST API after Spring.

---

## 🔗 RELATED SECTIONS

- Backend pairs with [`08-SQL-DATABASES`](../08-SQL-DATABASES/) — Spring Data JPA sits on top of SQL.
- For the algorithmic thinking behind the data structures here, see the [`DSA-Grandmaster-Codex`](../../DSA-Grandmaster-Codex/README.md).
- After this, [`11-FULLSTACK-ENGINEERING`](../11-FULLSTACK-ENGINEERING/) covers auth, testing, and deployment for the APIs you build here.

---

**→ Begin:** [`01-Java-Fundamentals.md`](./01-Java-Fundamentals.md) | Back to [`../README.md`](../README.md)
