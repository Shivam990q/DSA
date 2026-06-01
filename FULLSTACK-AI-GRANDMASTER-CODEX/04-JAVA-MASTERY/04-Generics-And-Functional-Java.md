# ☕ 04 — Generics & Functional Java ⭐

> *"Generics make your code typesafe without repetition. Lambdas and streams make it read like the problem you're solving instead of the loops you're writing. Together they are modern Java."*

**Prev:** [`03-Collections-Framework.md`](./03-Collections-Framework.md) · **Next:** [`05-Exceptions-And-IO.md`](./05-Exceptions-And-IO.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

# PART A — GENERICS

## I. THE PROBLEM GENERICS SOLVE

Before generics (pre-Java 5), collections held `Object`, so you cast everything and got runtime crashes:

```java
import java.util.*;

public class WithoutGenerics {
    public static void main(String[] args) {
        List list = new ArrayList();   // raw type — holds anything
        list.add("hello");
        list.add(42);                  // oops, an Integer snuck in
        String s = (String) list.get(0); // manual cast
        String bad = (String) list.get(1); // ClassCastException at RUNTIME 💥
    }
}
```

Generics move that error to **compile time** and remove the casts:

```java
import java.util.*;

public class WithGenerics {
    public static void main(String[] args) {
        List<String> list = new ArrayList<>();  // <String> — only Strings allowed
        list.add("hello");
        // list.add(42);                         // COMPILE ERROR — caught immediately
        String s = list.get(0);                  // no cast needed
        System.out.println(s);
    }
}
```

> **The diamond `<>`.** On the right side, `new ArrayList<>()` infers the type from the left. Less typing, same safety.

---

## II. GENERIC CLASSES

A type parameter (conventionally `T`, `E`, `K`, `V`) is a placeholder filled in when you use the class.

```java
// A type-safe container parameterized by T
public class Box<T> {
    private T value;
    public void set(T value) { this.value = value; }
    public T get() { return value; }

    public static void main(String[] args) {
        Box<String> sb = new Box<>();
        sb.set("hi");
        String s = sb.get();          // typesafe, no cast

        Box<Integer> ib = new Box<>();
        ib.set(42);
        // ib.set("nope");            // COMPILE ERROR
        int n = ib.get();
        System.out.println(s + " " + n);
    }
}
```

A generic class with two parameters — a `Pair`:

```java
public class Pair<K, V> {
    private final K key;
    private final V value;
    public Pair(K key, V value) { this.key = key; this.value = value; }
    public K key()   { return key; }
    public V value() { return value; }
    @Override public String toString() { return "(" + key + ", " + value + ")"; }

    public static void main(String[] args) {
        Pair<String, Integer> age = new Pair<>("Ada", 36);
        System.out.println(age.key() + " is " + age.value()); // Ada is 36
    }
}
```

> **Naming conventions:** `T` = Type, `E` = Element, `K`/`V` = Key/Value, `N` = Number, `R` = Return. They're just conventions; any identifier works, but follow them so others read your code instantly.

---

## III. GENERIC METHODS

A method can declare its own type parameter, independent of its class. The `<T>` goes before the return type.

```java
import java.util.List;

public class GenericMethods {
    // <T> declares the type parameter for THIS method
    static <T> T firstOf(List<T> list) {
        return list.isEmpty() ? null : list.get(0);
    }

    static <T> void swap(T[] arr, int i, int j) {
        T tmp = arr[i]; arr[i] = arr[j]; arr[j] = tmp;
    }

    public static void main(String[] args) {
        String first = firstOf(List.of("a", "b", "c")); // T inferred as String
        Integer firstNum = firstOf(List.of(1, 2, 3));    // T inferred as Integer
        System.out.println(first + " " + firstNum);

        Integer[] nums = {1, 2, 3};
        swap(nums, 0, 2);
        System.out.println(java.util.Arrays.toString(nums)); // [3, 2, 1]
    }
}
```

---

## IV. BOUNDED TYPE PARAMETERS

You can constrain a type parameter to a supertype with `extends`. This unlocks methods of the bound.

```java
import java.util.List;

public class Bounds {
    // T must be a Number (or subclass) — so we can call doubleValue()
    static <T extends Number> double sum(List<T> nums) {
        double total = 0;
        for (T n : nums) total += n.doubleValue();  // legal because T is a Number
        return total;
    }

    // Multiple bounds: T must be BOTH Comparable AND CharSequence
    static <T extends Comparable<T> & CharSequence> T max(T a, T b) {
        return a.compareTo(b) >= 0 ? a : b;
    }

    public static void main(String[] args) {
        System.out.println(sum(List.of(1, 2, 3)));        // 6.0
        System.out.println(sum(List.of(1.5, 2.5)));        // 4.0
        System.out.println(max("apple", "banana"));        // banana
    }
}
```

> **`extends` in generics means "is-a"** for both classes and interfaces. `<T extends Number>` accepts `Integer`, `Double`, etc. `<T extends Comparable<T>>` means "T can be compared to itself."

---

## V. WILDCARDS — `?`, `extends`, `super`, AND PECS

Wildcards make generic *parameters* flexible. They answer: "this method accepts a list of *some* type — what can I do with it?"

```java
import java.util.*;

public class Wildcards {
    // Unbounded ? — "list of unknown type". Can read as Object, can't add (except null).
    static void printAll(List<?> list) {
        for (Object o : list) System.out.print(o + " ");
        System.out.println();
    }

    // Upper-bounded: PRODUCER — you READ Numbers out of it
    static double sumOf(List<? extends Number> nums) {
        double total = 0;
        for (Number n : nums) total += n.doubleValue();   // safe to read as Number
        // nums.add(1);  // COMPILE ERROR — can't add; we don't know the exact subtype
        return total;
    }

    // Lower-bounded: CONSUMER — you WRITE Integers into it
    static void addInts(List<? super Integer> sink) {
        sink.add(1);                                       // safe to add Integer
        sink.add(2);
        // Integer x = sink.get(0);  // can only read as Object
    }

    public static void main(String[] args) {
        printAll(List.of("a", "b"));
        printAll(List.of(1, 2, 3));

        System.out.println(sumOf(List.of(1, 2, 3)));       // 6.0
        System.out.println(sumOf(List.of(1.5, 2.5)));      // 4.0

        List<Number> nums = new ArrayList<>();
        addInts(nums);                                      // List<Number> accepts ? super Integer
        System.out.println(nums);                           // [1, 2]
    }
}
```

> **PECS — Producer Extends, Consumer Super.** If a parameter **produces** values you read out, use `? extends T`. If it **consumes** values you put in, use `? super T`. This mnemonic resolves almost every wildcard question. (Think of `Collections.copy(dest, src)`: `src` is the producer `? extends T`, `dest` is the consumer `? super T`.)

### Type erasure — the catch you must know

Generics exist only at compile time. At runtime the JVM "erases" them to raw types. Consequences:

```java
public class Erasure {
    public static void main(String[] args) {
        List<String> a = new java.util.ArrayList<>();
        List<Integer> b = new java.util.ArrayList<>();
        System.out.println(a.getClass() == b.getClass()); // true — both are just ArrayList at runtime

        // Cannot do: new T[10], T.class, or `obj instanceof List<String>`
        // because the type info is gone at runtime.
    }
}
```

> **Practical impact:** you cannot create generic arrays (`new T[]`), can't use `instanceof` with a parameterized type, and can't overload methods that differ only by generic type. Erasure is the price of backward compatibility.

---

# PART B — FUNCTIONAL JAVA

## VI. FUNCTIONAL INTERFACES AND LAMBDAS

A **functional interface** has exactly one abstract method. A **lambda** is a concise instance of one. This is the foundation of functional Java (Java 8+).

```java
public class LambdaBasics {
    @FunctionalInterface
    interface Greeting {              // one abstract method → functional interface
        String greet(String name);
    }

    public static void main(String[] args) {
        // Pre-lambda: anonymous class — verbose
        Greeting old = new Greeting() {
            @Override public String greet(String name) { return "Hi " + name; }
        };

        // Lambda — same thing, the noise removed
        Greeting g = name -> "Hi " + name;
        System.out.println(g.greet("Ada"));   // Hi Ada

        // Lambda syntax variants
        Runnable r = () -> System.out.println("no args");             // no params
        Greeting block = name -> {                                     // multi-statement body
            String trimmed = name.strip();
            return "Hello, " + trimmed;
        };
        r.run();
        System.out.println(block.greet("  Bob "));
    }
}
```

> **`@FunctionalInterface`** is optional but recommended: the compiler then errors if you accidentally add a second abstract method.

### The built-in functional interfaces (`java.util.function`)

You rarely write your own — the JDK ships the common shapes:

```java
import java.util.function.*;

public class BuiltInFunctions {
    public static void main(String[] args) {
        // Function<T,R> — takes a T, returns an R
        Function<String, Integer> length = s -> s.length();
        System.out.println(length.apply("hello"));     // 5

        // Predicate<T> — takes a T, returns boolean
        Predicate<Integer> isEven = n -> n % 2 == 0;
        System.out.println(isEven.test(4));             // true

        // Consumer<T> — takes a T, returns nothing (side effect)
        Consumer<String> printer = s -> System.out.println("-> " + s);
        printer.accept("logged");

        // Supplier<T> — takes nothing, produces a T
        Supplier<Double> random = () -> Math.random();
        System.out.println(random.get());

        // BiFunction<T,U,R> — two inputs, one output
        BiFunction<Integer, Integer, Integer> add = (a, b) -> a + b;
        System.out.println(add.apply(2, 3));            // 5

        // UnaryOperator<T> — Function where input & output are the same type
        UnaryOperator<String> shout = s -> s.toUpperCase();
        System.out.println(shout.apply("hi"));          // HI

        // Composition
        Function<Integer, Integer> doubler = n -> n * 2;
        Function<Integer, Integer> inc = n -> n + 1;
        System.out.println(doubler.andThen(inc).apply(5)); // (5*2)+1 = 11
        System.out.println(doubler.compose(inc).apply(5)); // (5+1)*2 = 12
    }
}
```

| Interface | Shape | Abstract method |
|-----------|-------|-----------------|
| `Function<T,R>` | T → R | `R apply(T)` |
| `Predicate<T>` | T → boolean | `boolean test(T)` |
| `Consumer<T>` | T → void | `void accept(T)` |
| `Supplier<T>` | () → T | `T get()` |
| `BiFunction<T,U,R>` | (T,U) → R | `R apply(T,U)` |
| `UnaryOperator<T>` | T → T | `T apply(T)` |
| `BinaryOperator<T>` | (T,T) → T | `T apply(T,T)` |

---

## VII. METHOD REFERENCES — LAMBDAS, SHORTER

When a lambda just calls an existing method, a **method reference** (`::`) says it more cleanly.

```java
import java.util.*;
import java.util.function.*;

public class MethodRefs {
    public static void main(String[] args) {
        // 1) Static method:    ClassName::staticMethod
        Function<String, Integer> parse = Integer::parseInt;     // s -> Integer.parseInt(s)
        System.out.println(parse.apply("42"));

        // 2) Instance method of a particular object:  obj::method
        String prefix = "LOG: ";
        Consumer<String> log = System.out::println;             // s -> System.out.println(s)
        log.accept("hello");

        // 3) Instance method of an arbitrary object of a type:  ClassName::method
        Function<String, String> upper = String::toUpperCase;    // s -> s.toUpperCase()
        System.out.println(upper.apply("hi"));

        // 4) Constructor reference:  ClassName::new
        Supplier<ArrayList<String>> maker = ArrayList::new;      // () -> new ArrayList<>()
        List<String> list = maker.get();

        // Real use: sort with a method reference
        List<String> names = new ArrayList<>(List.of("Charlie", "alice", "Bob"));
        names.sort(String::compareToIgnoreCase);
        System.out.println(names);   // [alice, Bob, Charlie]
    }
}
```

---

## VIII. THE STREAM API ⭐ — DECLARATIVE DATA PROCESSING

A **stream** is a pipeline that processes a sequence of elements. You describe *what* to do (filter, map, reduce) and the stream handles the *how*. Streams don't store data and don't mutate the source.

A pipeline has three parts: a **source** → zero or more **intermediate operations** (lazy) → one **terminal operation** (triggers execution).

```java
import java.util.*;
import java.util.stream.*;

public class StreamIntro {
    public static void main(String[] args) {
        List<String> names = List.of("Ada", "Bob", "Charlie", "Dan", "Eve");

        // Imperative (the old way)
        List<String> resultImperative = new ArrayList<>();
        for (String n : names) {
            if (n.length() <= 3) resultImperative.add(n.toUpperCase());
        }

        // Declarative (streams) — reads like the requirement
        List<String> result = names.stream()        // source
            .filter(n -> n.length() <= 3)            // intermediate (lazy)
            .map(String::toUpperCase)                // intermediate (lazy)
            .sorted()                                // intermediate (lazy)
            .collect(Collectors.toList());           // terminal (executes now)

        System.out.println(result);  // [ADA, BOB, DAN, EVE]
    }
}
```

### The essential operations

```java
import java.util.*;
import java.util.stream.*;

public class StreamOps {
    public static void main(String[] args) {
        List<Integer> nums = List.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

        // filter — keep matching elements
        System.out.println(nums.stream().filter(n -> n % 2 == 0).toList()); // [2,4,6,8,10]

        // map — transform each element
        System.out.println(nums.stream().map(n -> n * n).toList());         // [1,4,9,...,100]

        // reduce — fold into a single value
        int sum = nums.stream().reduce(0, Integer::sum);                     // 55
        System.out.println(sum);

        // count, anyMatch, allMatch, noneMatch
        System.out.println(nums.stream().filter(n -> n > 5).count());        // 5
        System.out.println(nums.stream().anyMatch(n -> n > 9));              // true
        System.out.println(nums.stream().allMatch(n -> n > 0));             // true

        // findFirst returns an Optional
        Optional<Integer> firstBig = nums.stream().filter(n -> n > 7).findFirst();
        System.out.println(firstBig.get());                                  // 8

        // limit, skip, distinct, sorted
        System.out.println(Stream.of(3,1,2,3,1).distinct().sorted().toList()); // [1,2,3]
        System.out.println(nums.stream().skip(2).limit(3).toList());          // [3,4,5]

        // Numeric streams avoid boxing and add sum()/average()/max()
        int total = IntStream.rangeClosed(1, 100).sum();                      // 5050
        System.out.println(total);
        OptionalDouble avg = nums.stream().mapToInt(Integer::intValue).average();
        System.out.println(avg.getAsDouble());                                // 5.5
    }
}
```

### Collectors — gathering results

`collect` with `Collectors` is where streams get powerful: group, partition, join, and summarize.

```java
import java.util.*;
import java.util.stream.*;

public class CollectorsDemo {
    record Person(String name, String city, int age) {}

    public static void main(String[] args) {
        List<Person> people = List.of(
            new Person("Ada", "London", 36),
            new Person("Bob", "Paris", 42),
            new Person("Cara", "London", 29),
            new Person("Dan", "Paris", 51)
        );

        // toList / toSet
        List<String> names = people.stream().map(Person::name).collect(Collectors.toList());

        // joining
        System.out.println(people.stream().map(Person::name).collect(Collectors.joining(", ")));
        // Ada, Bob, Cara, Dan

        // groupingBy — partition into a Map<key, List>
        Map<String, List<Person>> byCity =
            people.stream().collect(Collectors.groupingBy(Person::city));
        System.out.println(byCity.keySet());   // [Paris, London]

        // groupingBy + downstream collector: average age per city
        Map<String, Double> avgAgeByCity = people.stream()
            .collect(Collectors.groupingBy(Person::city, Collectors.averagingInt(Person::age)));
        System.out.println(avgAgeByCity);       // {Paris=46.5, London=32.5}

        // counting per group
        Map<String, Long> countByCity = people.stream()
            .collect(Collectors.groupingBy(Person::city, Collectors.counting()));
        System.out.println(countByCity);        // {Paris=2, London=2}

        // partitioningBy — split by a boolean predicate
        Map<Boolean, List<Person>> overForty = people.stream()
            .collect(Collectors.partitioningBy(p -> p.age() > 40));
        System.out.println(overForty.get(true).size()); // 2

        // toMap — build a lookup
        Map<String, Integer> nameToAge = people.stream()
            .collect(Collectors.toMap(Person::name, Person::age));
        System.out.println(nameToAge.get("Ada")); // 36
    }
}
```

> **Gotcha — streams are single-use.** Once a terminal operation runs, the stream is consumed. Reusing it throws `IllegalStateException`. Create a fresh stream each time.

> **Gotcha — no side effects in the middle.** Don't mutate external state inside `map`/`filter`. Streams may be reordered or parallelized; side effects make results unpredictable. Keep stream functions pure; do mutation in the terminal step.

> **Gotcha — `parallelStream()` is not free speed.** It splits work across threads, but has overhead and demands thread-safe, stateless operations. Only helps for large datasets and CPU-bound work. Measure before using it.

---

## IX. OPTIONAL — TAMING NULL

`Optional<T>` is a container that either holds a value or is empty. It makes "might be absent" explicit in the type, pushing you to handle the missing case instead of risking an NPE.

```java
import java.util.*;

public class OptionalDemo {
    static Optional<String> findUser(int id) {
        return id == 1 ? Optional.of("Ada") : Optional.empty();
    }

    public static void main(String[] args) {
        Optional<String> user = findUser(1);

        // Check and get
        if (user.isPresent()) System.out.println(user.get());

        // Better: provide a default
        String name = findUser(99).orElse("guest");
        System.out.println(name);                       // guest

        // Lazy default (only computed if empty)
        String n2 = findUser(99).orElseGet(() -> "computed-default");

        // Throw if absent
        // String n3 = findUser(99).orElseThrow(() -> new NoSuchElementException("no user"));

        // Transform safely — no null checks
        int len = findUser(1).map(String::length).orElse(0);
        System.out.println(len);                        // 3

        // Run code only if present
        findUser(1).ifPresent(u -> System.out.println("Found " + u));
        findUser(2).ifPresentOrElse(
            u -> System.out.println("Found " + u),
            () -> System.out.println("Not found"));     // Not found
    }
}
```

> **Use `Optional` as a return type**, signalling "this might not find anything." **Don't** use it for fields or method parameters (it adds overhead and isn't `Serializable`), and **never** call `.get()` without first checking presence — that just reinvents the NPE. Prefer `orElse`, `orElseGet`, `map`, and `ifPresent`.

---

## X. A COMPLETE FUNCTIONAL EXAMPLE

Order processing that combines generics, lambdas, and streams:

```java
import java.util.*;
import java.util.stream.*;

public class OrderAnalytics {
    record Order(String customer, String product, double amount, String status) {}

    public static void main(String[] args) {
        List<Order> orders = List.of(
            new Order("Ada", "Laptop", 1200, "PAID"),
            new Order("Bob", "Mouse", 25, "PAID"),
            new Order("Ada", "Monitor", 300, "PENDING"),
            new Order("Cara", "Laptop", 1200, "PAID"),
            new Order("Bob", "Keyboard", 75, "CANCELLED")
        );

        // Total revenue from PAID orders
        double revenue = orders.stream()
            .filter(o -> o.status().equals("PAID"))
            .mapToDouble(Order::amount)
            .sum();
        System.out.printf("Revenue: $%.2f%n", revenue);  // $2425.00

        // Revenue per customer (PAID only), sorted high → low
        orders.stream()
            .filter(o -> o.status().equals("PAID"))
            .collect(Collectors.groupingBy(Order::customer, Collectors.summingDouble(Order::amount)))
            .entrySet().stream()
            .sorted(Map.Entry.<String, Double>comparingByValue().reversed())
            .forEach(e -> System.out.printf("  %s: $%.2f%n", e.getKey(), e.getValue()));

        // Best-selling products by count
        Map<String, Long> productCounts = orders.stream()
            .collect(Collectors.groupingBy(Order::product, Collectors.counting()));
        System.out.println("Product counts: " + productCounts);

        // Most expensive order (Optional because the list could be empty)
        orders.stream()
            .max(Comparator.comparingDouble(Order::amount))
            .ifPresent(o -> System.out.println("Biggest order: " + o.product()));
    }
}
```

---

## XI. COMMON PITFALLS

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| Using raw types (`List` not `List<String>`) | Lose type safety, get warnings | Always parameterize |
| Expecting `new T[]` to work | Compile error (erasure) | Use `List<T>` or pass a `Class<T>` |
| Reusing a consumed stream | `IllegalStateException` | Build a new stream |
| Side effects inside `map`/`filter` | Nondeterministic results | Keep functions pure |
| `Optional.get()` without `isPresent()` | NPE-equivalent crash | `orElse`/`map`/`ifPresent` |
| `Optional` fields/params | Overhead, awkward API | Use for return types only |
| Reaching for `parallelStream()` reflexively | Often slower, race bugs | Measure; ensure thread-safety |
| Wrong wildcard direction | Won't compile or can't add/read | Apply PECS |
| Boxing in hot numeric loops | Slow, memory churn | `IntStream`/`int[]` |

---

## 🧠 KEY TAKEAWAYS

- **Generics** move type errors from runtime to compile time and remove casts. Use type parameters (`<T>`), generic methods (`<T> T foo(...)`), and **bounds** (`<T extends Number>`).
- **Wildcards** flex generic parameters: remember **PECS** — *Producer `extends`, Consumer `super`.* Generics are erased at runtime, so no `new T[]` and no parameterized `instanceof`.
- A **functional interface** has one abstract method; a **lambda** is a terse instance of it. Lean on the built-ins: `Function`, `Predicate`, `Consumer`, `Supplier`.
- **Method references** (`::`) shorten lambdas that just delegate to an existing method or constructor.
- The **Stream API** expresses data processing declaratively: source → lazy intermediates (`filter`/`map`/`sorted`) → terminal (`collect`/`reduce`/`forEach`). Master `Collectors.groupingBy` — it replaces mountains of loops.
- **`Optional`** makes absence explicit; use it for return types and resolve it with `orElse`/`map`/`ifPresent`, never a naked `.get()`.
- Streams are single-use and should be side-effect-free; `parallelStream` only pays off for large, CPU-bound, thread-safe work.

---

**Prev:** [`03-Collections-Framework.md`](./03-Collections-Framework.md) · **Next:** [`05-Exceptions-And-IO.md`](./05-Exceptions-And-IO.md) · **Index:** [`00-Index.md`](./00-Index.md)
