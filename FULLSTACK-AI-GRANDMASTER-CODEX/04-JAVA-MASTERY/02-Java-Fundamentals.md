# ☕ 01 — Java Fundamentals

> *"Before you can build cathedrals, you learn to lay a single brick true. The fundamentals are the brick."*

**Prev:** [`01-Getting-Started.md`](./01-Getting-Started.md) · **Next:** [`03-OOP-In-Java.md`](./03-OOP-In-Java.md) · **Index:** [`01-Getting-Started.md`](./01-Getting-Started.md)

---

## I. WHAT JAVA ACTUALLY IS (AND WHY IT WON)

Java is a **statically typed, compiled, object-oriented, garbage-collected** language that runs on the **JVM** (Java Virtual Machine). The defining idea, from 1995, was **"Write Once, Run Anywhere"**:

```
Your code (.java)
      │  javac (compiler)
      ▼
Bytecode (.class)  ← platform-INDEPENDENT instructions
      │  java (the JVM)
      ▼
Machine code  ← JVM translates bytecode to THIS machine's instructions at runtime
```

You compile to **bytecode**, an intermediate language. The JVM — a program that exists for Windows, macOS, Linux, etc. — runs that same bytecode anywhere. That is why a `.jar` built on your laptop runs unchanged on a Linux server.

**Why it dominates backends:** strong typing catches errors at compile time, the ecosystem (Spring, libraries, tooling) is enormous, the JVM is battle-tested and fast, and large teams can maintain large codebases because the type system documents intent.

### The compilation + execution pipeline in detail

1. **`javac` (compile time):** parses your source, type-checks it, and emits `.class` files of bytecode. Most of your mistakes are caught here.
2. **Class loading:** when you run `java MyApp`, the JVM loads the needed `.class` files into memory.
3. **Bytecode verification:** the JVM checks the bytecode is safe (no stack corruption, valid types).
4. **JIT compilation (Just-In-Time):** the JVM starts interpreting bytecode, but "hot" methods that run often get compiled to native machine code on the fly. This is why long-running Java programs get *faster* after warming up.
5. **Garbage collection:** you never `free()` memory. A background collector reclaims objects nothing references anymore.

> **Gotcha — JDK vs JRE vs JVM.** The **JVM** runs bytecode. The **JRE** = JVM + standard libraries (enough to *run* Java). The **JDK** = JRE + tools like `javac` (enough to *develop* Java). You need the JDK.

---

## II. ANATOMY OF A JAVA PROGRAM

Everything in Java lives inside a **class**. The JVM starts execution at a method with this exact signature: `public static void main(String[] args)`.

```java
// File MUST be named HelloWorld.java (public class name == file name)
public class HelloWorld {

    // The entry point. The JVM calls this to start the program.
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

Dissecting `public static void main(String[] args)` — memorize this, you will type it thousands of times:

| Token | Meaning |
|-------|---------|
| `public` | Access modifier — the JVM (outside this class) must be able to call it |
| `static` | Belongs to the class, not an instance — the JVM calls it without creating an object first |
| `void` | Returns nothing |
| `main` | The special name the JVM looks for |
| `String[] args` | Command-line arguments, as an array of strings |

```java
public class Greeter {
    public static void main(String[] args) {
        // Run: java Greeter Alice  →  args[0] is "Alice"
        if (args.length > 0) {
            System.out.println("Hello, " + args[0] + "!");
        } else {
            System.out.println("Hello, stranger! (pass a name as an argument)");
        }
    }
}
```

> **Convention — naming.** Classes use `PascalCase`, methods and variables use `camelCase`, constants use `UPPER_SNAKE_CASE`, packages use `lowercase`. Java enforces almost none of this, but every team does. Following convention is part of writing professional code.

---

## III. VARIABLES AND DATA TYPES

Java has two families of types: **primitives** (raw values) and **reference types** (objects).

### The 8 primitive types

```java
public class Primitives {
    public static void main(String[] args) {
        // Integer types (whole numbers)
        byte  b = 127;                 // 8-bit,  -128 to 127
        short s = 32000;               // 16-bit
        int   i = 2_000_000_000;       // 32-bit — the DEFAULT for whole numbers (underscores allowed for readability)
        long  big = 9_000_000_000L;    // 64-bit — note the L suffix (required when literal exceeds int range)

        // Floating-point types (decimals)
        float  f = 3.14f;              // 32-bit — note the f suffix
        double d = 3.141592653589793;  // 64-bit — the DEFAULT for decimals

        // Other
        char    c = 'A';               // 16-bit single Unicode character — single quotes
        boolean flag = true;           // true or false ONLY (not 0/1 like C)

        System.out.println(i + " " + big + " " + d + " " + c + " " + flag);
    }
}
```

| Type | Size | Range / notes | Default |
|------|------|---------------|---------|
| `byte` | 8-bit | -128..127 | 0 |
| `short` | 16-bit | ~±32K | 0 |
| `int` | 32-bit | ~±2.1 billion | 0 |
| `long` | 64-bit | ~±9.2 quintillion | 0L |
| `float` | 32-bit | ~7 decimal digits | 0.0f |
| `double` | 64-bit | ~15 decimal digits | 0.0d |
| `char` | 16-bit | one Unicode char | '\u0000' |
| `boolean` | JVM-dependent | true/false | false |

> **Gotcha — integer overflow is silent.** `int x = Integer.MAX_VALUE + 1;` wraps around to a large negative number with no error. For money or huge counts use `long`, or `BigInteger` / `BigDecimal` when exactness matters.

> **Gotcha — never use `double` for money.** `0.1 + 0.2` is `0.30000000000000004`. Floating point is binary and cannot represent most decimals exactly. Use `BigDecimal` for currency.

```java
import java.math.BigDecimal;

public class Money {
    public static void main(String[] args) {
        System.out.println(0.1 + 0.2);                               // 0.30000000000000004  ← wrong for money
        System.out.println(new BigDecimal("0.1").add(new BigDecimal("0.2"))); // 0.3  ← exact
        // Note: pass numbers to BigDecimal as STRINGS, not doubles, to stay exact.
    }
}
```

### Reference types

Anything that is not a primitive is a reference type: `String`, arrays, and every class/object. A reference variable holds a *reference* (a handle) to an object on the heap, not the object itself.

```java
public class References {
    public static void main(String[] args) {
        String name = "Grace Hopper";   // String is a reference type (an object)
        int[] scores = {90, 85, 100};   // arrays are reference types too

        String empty = null;            // reference types can be null (no object)
        // int x = null;                // ERROR — primitives can NEVER be null
    }
}
```

> **The null trap.** A reference can be `null`, meaning "points at nothing." Calling a method on `null` throws `NullPointerException` (the NPE) — the single most common Java runtime error. We tame it later with `Optional` (file 04) and careful design.

### `var` — local type inference (Java 10+)

```java
public class VarDemo {
    public static void main(String[] args) {
        var message = "Hello";          // inferred as String
        var count = 42;                 // inferred as int
        var list = new java.util.ArrayList<String>(); // inferred — less repetition

        // var ONLY works for local variables WITH an initializer.
        // var x;             // ERROR — nothing to infer from
        // It is NOT dynamic typing. message is still permanently a String.
    }
}
```

### `final` — constants

```java
public class Constants {
    static final double PI = 3.14159;   // class-level constant
    public static void main(String[] args) {
        final int MAX_USERS = 100;       // cannot be reassigned
        // MAX_USERS = 200;              // ERROR — final variable
        System.out.println(PI * MAX_USERS);
    }
}
```

---

## IV. OPERATORS

```java
public class Operators {
    public static void main(String[] args) {
        // Arithmetic
        int a = 17, b = 5;
        System.out.println(a + b);   // 22
        System.out.println(a - b);   // 12
        System.out.println(a * b);   // 85
        System.out.println(a / b);   // 3   ← INTEGER division truncates, not 3.4
        System.out.println(a % b);   // 2   ← modulo (remainder)
        System.out.println((double) a / b); // 3.4 ← cast one operand to get real division

        // Comparison → produce boolean
        System.out.println(a > b);   // true
        System.out.println(a == b);  // false

        // Logical (short-circuit)
        boolean t = true, f = false;
        System.out.println(t && f);  // false — && stops at first false
        System.out.println(t || f);  // true  — || stops at first true
        System.out.println(!t);      // false

        // Compound assignment
        int x = 10;
        x += 5;  // x = x + 5  → 15
        x *= 2;  // 30
        System.out.println(x);

        // Increment / decrement
        int i = 5;
        System.out.println(i++); // 5 (post: returns THEN increments) → i is now 6
        System.out.println(++i); // 7 (pre: increments THEN returns)
    }
}
```

> **Gotcha — integer division.** `5 / 2` is `2`, not `2.5`, because both operands are `int`. To get `2.5`, make at least one a `double`: `5 / 2.0` or `(double) 5 / 2`.

> **Gotcha — `&&` vs `&`.** `&&` short-circuits (stops evaluating once the result is known); `&` always evaluates both sides. Use `&&` and `||` for boolean logic — short-circuiting is what makes `if (obj != null && obj.isValid())` safe.

### `==` vs `.equals()` — the most important distinction in Java

For **primitives**, `==` compares values. For **objects**, `==` compares *references* (are these the same object in memory?), while `.equals()` compares *contents*.

```java
public class EqualityTrap {
    public static void main(String[] args) {
        String a = new String("hello");
        String b = new String("hello");

        System.out.println(a == b);        // false — two DIFFERENT objects
        System.out.println(a.equals(b));   // true  — same CONTENT

        Integer x = 1000, y = 1000;
        System.out.println(x == y);        // false (!) — different Integer objects
        System.out.println(x.equals(y));   // true
    }
}
```

> **Rule:** compare object content with `.equals()`. Reserve `==` for primitives and for "is this literally the same object / is it null." Forgetting this causes bugs that pass small tests and fail in production.

---

## V. STRINGS

`String` is an object, immutable (cannot be changed after creation), and so common it gets language-level support.

```java
public class Strings {
    public static void main(String[] args) {
        String name = "Ada";
        String greeting = "Hello, " + name + "!";  // concatenation with +

        System.out.println(greeting.length());          // 11
        System.out.println(greeting.toUpperCase());      // HELLO, ADA!
        System.out.println(greeting.substring(7, 10));   // Ada
        System.out.println(greeting.contains("Ada"));    // true
        System.out.println(greeting.replace("Ada", "Bob")); // Hello, Bob!
        System.out.println(greeting.indexOf("Ada"));     // 7
        System.out.println("  trim me  ".strip());       // "trim me"

        // Split and join
        String csv = "a,b,c";
        String[] parts = csv.split(",");                 // ["a", "b", "c"]
        System.out.println(String.join(" | ", parts));   // a | b | c

        // Text blocks (Java 15+) — multi-line strings
        String json = """
            {
              "name": "Ada",
              "role": "engineer"
            }""";
        System.out.println(json);
    }
}
```

> **Gotcha — String immutability and the `+` loop trap.** Because strings are immutable, `s = s + x` creates a *new* string every time. Doing that in a loop is O(n²). Use `StringBuilder` for building strings in loops:

```java
public class StringBuilding {
    public static void main(String[] args) {
        // BAD: O(n²) — allocates a new String every iteration
        String slow = "";
        for (int i = 0; i < 5; i++) slow += i;

        // GOOD: O(n) — mutates one buffer
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 5; i++) sb.append(i);
        String fast = sb.toString();   // "01234"
        System.out.println(fast);
    }
}
```

---

## VI. CONTROL FLOW

### Conditionals

```java
public class Conditionals {
    public static void main(String[] args) {
        int score = 82;

        if (score >= 90) {
            System.out.println("A");
        } else if (score >= 80) {
            System.out.println("B");
        } else if (score >= 70) {
            System.out.println("C");
        } else {
            System.out.println("F");
        }

        // Ternary operator: condition ? valueIfTrue : valueIfFalse
        String result = (score >= 60) ? "Pass" : "Fail";
        System.out.println(result);
    }
}
```

### switch — classic and modern

```java
public class SwitchDemo {
    public static void main(String[] args) {
        int day = 3;

        // Classic switch (note the break; — forget it and execution "falls through")
        switch (day) {
            case 1: System.out.println("Mon"); break;
            case 2: System.out.println("Tue"); break;
            case 3: System.out.println("Wed"); break;
            default: System.out.println("Other");
        }

        // Switch EXPRESSION (Java 14+) — arrow form, no fall-through, returns a value
        String name = switch (day) {
            case 1 -> "Monday";
            case 2 -> "Tuesday";
            case 3 -> "Wednesday";
            default -> "Unknown";
        };
        System.out.println(name);
    }
}
```

> **Gotcha — fall-through.** In the classic `switch`, forgetting `break` means execution continues into the next case. The modern arrow (`->`) form has no fall-through and is safer — prefer it.

### Loops

```java
public class Loops {
    public static void main(String[] args) {
        // for — when you know the count or need the index
        for (int i = 0; i < 5; i++) {
            System.out.print(i + " ");   // 0 1 2 3 4
        }
        System.out.println();

        // enhanced for ("for-each") — iterate a collection/array, no index needed
        int[] nums = {10, 20, 30};
        for (int n : nums) {
            System.out.print(n + " ");   // 10 20 30
        }
        System.out.println();

        // while — loop while a condition holds
        int count = 3;
        while (count > 0) {
            System.out.print(count + " "); // 3 2 1
            count--;
        }
        System.out.println();

        // do-while — runs the body AT LEAST ONCE
        int x = 0;
        do {
            System.out.print("run ");      // prints once even though 0 < 0 is false
        } while (x < 0);
        System.out.println();
    }
}
```

### break, continue, and labels

```java
public class LoopControl {
    public static void main(String[] args) {
        for (int i = 0; i < 10; i++) {
            if (i == 5) break;       // exit the loop entirely
            if (i % 2 == 0) continue; // skip to next iteration
            System.out.print(i + " "); // 1 3
        }
        System.out.println();

        // Labeled break — escape nested loops (use sparingly)
        outer:
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (i + j == 3) break outer; // breaks BOTH loops
                System.out.println(i + "," + j);
            }
        }
    }
}
```

---

## VII. ARRAYS

A fixed-size, indexed, contiguous container of one type.

```java
import java.util.Arrays;

public class ArraysDemo {
    public static void main(String[] args) {
        // Declaration + initialization
        int[] a = new int[5];           // {0, 0, 0, 0, 0} — primitives default to 0
        int[] b = {1, 2, 3, 4, 5};      // literal

        a[0] = 99;                       // assign by index (0-based)
        System.out.println(a[0]);        // 99
        System.out.println(b.length);    // 5 — note: a FIELD, not a method (no parentheses)

        // Iterate
        for (int i = 0; i < b.length; i++) System.out.print(b[i] + " ");
        System.out.println();

        // Helpful utilities from java.util.Arrays
        System.out.println(Arrays.toString(b));   // [1, 2, 3, 4, 5]
        Arrays.sort(b);                            // sorts in place
        int idx = Arrays.binarySearch(b, 3);       // 2 (requires sorted array)
        System.out.println(idx);

        // 2D array (array of arrays)
        int[][] grid = {
            {1, 2, 3},
            {4, 5, 6}
        };
        System.out.println(grid[1][2]);  // 6
        System.out.println(Arrays.deepToString(grid)); // [[1, 2, 3], [4, 5, 6]]
    }
}
```

> **Gotcha — `ArrayIndexOutOfBoundsException`.** Indices run `0` to `length - 1`. Accessing `b[b.length]` throws. Arrays are also **fixed-size**: once created, you cannot grow them. When you need a resizable list, reach for `ArrayList` (file 03).

---

## VIII. INPUT AND OUTPUT

### Output

```java
public class Output {
    public static void main(String[] args) {
        System.out.println("With newline");
        System.out.print("No newline. ");
        System.out.print("Same line.\n");

        // printf — formatted output
        String name = "Ada";
        int age = 36;
        System.out.printf("%s is %d years old.%n", name, age);
        System.out.printf("Pi ≈ %.2f%n", 3.14159);   // 2 decimal places → 3.14
        // Common specifiers: %s string, %d integer, %f float, %b boolean, %n platform newline
    }
}
```

### Input with Scanner

```java
import java.util.Scanner;

public class Input {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter your name: ");
        String name = sc.nextLine();          // reads a whole line

        System.out.print("Enter your age: ");
        int age = sc.nextInt();               // reads an int

        System.out.printf("Hi %s, next year you'll be %d.%n", name, age + 1);

        sc.close();   // release the resource
    }
}
```

> **Gotcha — `nextInt()` then `nextLine()`.** `nextInt()` reads the number but leaves the trailing newline in the buffer. A following `nextLine()` then reads an empty string. Fix by calling an extra `sc.nextLine()` after `nextInt()` to consume the leftover newline, or read everything as lines and parse with `Integer.parseInt`.

---

## IX. METHODS

A **method** is a named, reusable block of behavior.

```java
public class Methods {

    // static so main can call it without creating an object
    static int add(int a, int b) {
        return a + b;
    }

    static void greet(String name) {   // void = returns nothing
        System.out.println("Hi, " + name);
    }

    // Overloading: same name, different parameter lists
    static double add(double a, double b) {
        return a + b;
    }

    // Varargs: accept any number of arguments
    static int sum(int... numbers) {
        int total = 0;
        for (int n : numbers) total += n;
        return total;
    }

    public static void main(String[] args) {
        System.out.println(add(2, 3));        // 5   (int version)
        System.out.println(add(2.5, 3.5));    // 6.0 (double version — overloading)
        greet("Ada");
        System.out.println(sum(1, 2, 3, 4));  // 10  (varargs)
    }
}
```

> **Pass-by-value, always.** Java passes *copies*. For primitives, the value is copied (the original cannot change). For objects, the *reference* is copied — so the method can mutate the object it points to, but reassigning the parameter does not affect the caller's variable. This trips up nearly everyone once.

```java
public class PassByValue {
    static void tryReassign(int[] arr) {
        arr[0] = 99;             // mutates the shared object → caller SEES this
        arr = new int[]{-1};     // reassigns local copy of reference → caller does NOT see this
    }
    public static void main(String[] args) {
        int[] data = {1, 2, 3};
        tryReassign(data);
        System.out.println(data[0]); // 99
    }
}
```

---

## X. SCOPE, COMMENTS, AND STYLE

```java
public class Scope {
    static int classLevel = 10;   // accessible throughout the class

    public static void main(String[] args) {
        int methodLevel = 20;     // only inside main

        {
            int blockLevel = 30;  // only inside these braces
            System.out.println(classLevel + methodLevel + blockLevel);
        }
        // System.out.println(blockLevel); // ERROR — out of scope here

        // Single-line comment
        /* Multi-line
           comment */
        /**
         * Javadoc comment — used to generate API docs.
         * @param args command-line arguments
         */
    }
}
```

---

## XI. A COMPLETE LITTLE PROGRAM

Bringing it together — a number-guessing game using everything above:

```java
import java.util.Scanner;

public class GuessingGame {
    public static void main(String[] args) {
        int target = (int) (Math.random() * 100) + 1;  // 1..100
        Scanner sc = new Scanner(System.in);
        int guess = -1;
        int attempts = 0;

        System.out.println("I'm thinking of a number from 1 to 100.");

        while (guess != target) {
            System.out.print("Your guess: ");
            guess = sc.nextInt();
            attempts++;

            if (guess < target)      System.out.println("Too low.");
            else if (guess > target) System.out.println("Too high.");
            else System.out.printf("Correct! You got it in %d attempts.%n", attempts);
        }
        sc.close();
    }
}
```

---

## XII. COMMON PITFALLS — A CHECKLIST

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| `==` on Strings/objects | Comparison "randomly" false | Use `.equals()` |
| Integer division | `5/2 == 2` not `2.5` | Cast a side to `double` |
| `int` overflow | Huge negative numbers | Use `long` / `BigInteger` |
| `double` for money | Off-by-a-fraction-of-a-cent | Use `BigDecimal` (from String) |
| Forgetting `break` in classic switch | Wrong cases run | Use arrow `switch` expressions |
| NPE | `NullPointerException` at runtime | Null-check; prefer `Optional` (file 04) |
| `nextInt()` then `nextLine()` | Empty string read | Consume the leftover newline |
| Building strings with `+` in a loop | Slow on large input | `StringBuilder` |
| File name ≠ public class name | `javac` won't compile | Match them exactly |
| Array index out of bounds | Runtime crash | Indices are `0 .. length-1` |

---

## 🧠 KEY TAKEAWAYS

- Java compiles to **bytecode** that the **JVM** runs anywhere; `javac` catches most errors before your program ever runs.
- Every program starts at `public static void main(String[] args)`, and all code lives inside a **class**.
- Two type families: **8 primitives** (raw values) and **reference types** (objects, can be `null`).
- `==` compares values for primitives and *references* for objects; use **`.equals()`** for object content.
- Watch the classic traps: integer division, integer overflow, `double` for money, switch fall-through, and the NPE.
- Use `StringBuilder` to build strings in loops; arrays are fixed-size (use `ArrayList` when you need growth).
- Java is **pass-by-value** — for objects, the *reference* is copied, so methods can mutate but not reassign caller variables.

---

**Prev:** [`01-Getting-Started.md`](./01-Getting-Started.md) · **Next:** [`03-OOP-In-Java.md`](./03-OOP-In-Java.md) · **Index:** [`01-Getting-Started.md`](./01-Getting-Started.md)
