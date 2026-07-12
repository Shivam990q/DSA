# ☕ 03 — The Collections Framework ⭐

> *"Arrays are where you start. Collections are where you live. Pick the wrong one and your O(1) becomes O(n); pick the right one and the code writes itself."*

**Prev:** [`03-OOP-In-Java.md`](./03-OOP-In-Java.md) · **Next:** [`05-Generics-And-Functional.md`](./05-Generics-And-Functional.md) · **Index:** [`01-Getting-Started.md`](./01-Getting-Started.md)

---

## I. WHY COLLECTIONS EXIST

Arrays are fixed-size and low-level. Real programs need containers that **grow**, **look things up fast**, **prevent duplicates**, **stay sorted**, or **act like queues**. The **Java Collections Framework** (in `java.util`) is a set of interfaces and implementations that cover all of these, with consistent APIs.

The framework is organized around a few core interfaces:

```
                 Iterable
                    │
              Collection
        ┌───────────┼───────────┐
       List        Set        Queue
        │        ┌──┴──┐         │
   ArrayList   HashSet │      Deque
   LinkedList  Linked  │   ArrayDeque
               HashSet │   PriorityQueue
               TreeSet (SortedSet)

      Map   (NOT a Collection — separate hierarchy)
       │
   HashMap, LinkedHashMap, TreeMap (SortedMap)
```

> **`Map` is not a `Collection`.** It maps keys to values; it doesn't fit the single-element `Collection` model. It lives in its own branch but is part of the framework.

**Program to the interface, not the implementation.** Declare variables by the interface type and pick the implementation at construction:

```java
List<String> names = new ArrayList<>();   // ✅ flexible — swap to LinkedList without touching callers
Map<String, Integer> ages = new HashMap<>();
// ArrayList<String> names = new ArrayList<>();  // ❌ locks you to ArrayList everywhere
```

---

## II. LIST — ORDERED, INDEXED, ALLOWS DUPLICATES

A `List` keeps insertion order and lets you access elements by index. Duplicates are allowed.

### ArrayList — your default list

Backed by a resizable array. Fast random access; appends are amortized O(1). This is the list you use 90% of the time.

```java
import java.util.ArrayList;
import java.util.List;

public class ArrayListDemo {
    public static void main(String[] args) {
        List<String> fruits = new ArrayList<>();
        fruits.add("apple");
        fruits.add("banana");
        fruits.add("cherry");

        System.out.println(fruits.get(1));        // banana — O(1) random access
        fruits.set(1, "blueberry");               // replace at index
        fruits.add(1, "apricot");                 // insert at index — shifts the rest (O(n))
        fruits.remove("cherry");                  // remove by value
        fruits.remove(0);                         // remove by index

        System.out.println(fruits);               // [apricot, blueberry]
        System.out.println(fruits.size());        // 2
        System.out.println(fruits.contains("blueberry")); // true — O(n) scan
        System.out.println(fruits.indexOf("blueberry"));   // 1

        // Iterate (three ways)
        for (String f : fruits) System.out.println(f);                 // for-each
        fruits.forEach(System.out::println);                           // method reference
        for (int i = 0; i < fruits.size(); i++) System.out.println(fruits.get(i)); // index
    }
}
```

### LinkedList — doubly-linked nodes

Fast insertion/removal at the ends; slow random access (must walk the chain). Also implements `Deque`, so it works as a queue or stack. In practice `ArrayList` (for lists) and `ArrayDeque` (for queues) usually beat it — `LinkedList` is rarely the right choice despite its fame.

```java
import java.util.LinkedList;

public class LinkedListDemo {
    public static void main(String[] args) {
        LinkedList<Integer> dq = new LinkedList<>();
        dq.addFirst(1);   // O(1) at the head
        dq.addLast(2);    // O(1) at the tail
        dq.addFirst(0);
        System.out.println(dq);          // [0, 1, 2]
        System.out.println(dq.get(2));   // 2 — but O(n): it walks from an end
        dq.removeFirst();                // O(1)
        System.out.println(dq);          // [1, 2]
    }
}
```

### ArrayList vs LinkedList — the complexity that decides

| Operation | ArrayList | LinkedList |
|-----------|:---------:|:----------:|
| `get(i)` / `set(i)` random access | **O(1)** | O(n) |
| `add` at end (append) | O(1) amortized | O(1) |
| `add`/`remove` at front | O(n) (shifts) | **O(1)** |
| `add`/`remove` in middle | O(n) | O(n) (finding) + O(1) (relinking) |
| Memory | compact | higher (node + 2 pointers each) |
| Cache friendliness | excellent (contiguous) | poor (pointer chasing) |

> **Verdict:** default to `ArrayList`. Its contiguous memory makes it faster in practice even for many operations where `LinkedList` looks better on paper. Reach for `ArrayDeque` when you need fast front/back operations.

---

## III. SET — NO DUPLICATES

A `Set` models a mathematical set: each element appears at most once. `add` of a duplicate is a no-op. The three implementations differ in *ordering* and *performance*.

```java
import java.util.*;

public class SetDemo {
    public static void main(String[] args) {
        // HashSet — fastest, NO order guarantee
        Set<String> hash = new HashSet<>();
        hash.add("b"); hash.add("a"); hash.add("c"); hash.add("a"); // duplicate ignored
        System.out.println(hash);          // order unpredictable, e.g. [a, b, c]
        System.out.println(hash.size());   // 3 (not 4)
        System.out.println(hash.contains("a")); // true — O(1) average

        // LinkedHashSet — preserves INSERTION order
        Set<String> linked = new LinkedHashSet<>();
        linked.add("b"); linked.add("a"); linked.add("c");
        System.out.println(linked);        // [b, a, c] — insertion order kept

        // TreeSet — kept SORTED (natural order or a Comparator)
        Set<String> tree = new TreeSet<>();
        tree.add("b"); tree.add("a"); tree.add("c");
        System.out.println(tree);          // [a, b, c] — always sorted
    }
}
```

### Set operations (union, intersection, difference)

```java
import java.util.*;

public class SetAlgebra {
    public static void main(String[] args) {
        Set<Integer> a = new HashSet<>(List.of(1, 2, 3, 4));
        Set<Integer> b = new HashSet<>(List.of(3, 4, 5, 6));

        Set<Integer> union = new HashSet<>(a);
        union.addAll(b);                 // {1,2,3,4,5,6}

        Set<Integer> intersection = new HashSet<>(a);
        intersection.retainAll(b);       // {3,4}

        Set<Integer> difference = new HashSet<>(a);
        difference.removeAll(b);         // {1,2}

        System.out.println(union + " " + intersection + " " + difference);
    }
}
```

### TreeSet's superpower — navigation

A `TreeSet` (a red-black tree) keeps elements sorted, enabling range and neighbor queries in O(log n):

```java
import java.util.TreeSet;

public class TreeSetNav {
    public static void main(String[] args) {
        TreeSet<Integer> t = new TreeSet<>(java.util.List.of(10, 20, 30, 40, 50));
        System.out.println(t.first());      // 10
        System.out.println(t.last());       // 50
        System.out.println(t.floor(25));    // 20 — largest ≤ 25
        System.out.println(t.ceiling(25));  // 30 — smallest ≥ 25
        System.out.println(t.higher(30));   // 40 — strictly greater
        System.out.println(t.lower(30));    // 20 — strictly less
        System.out.println(t.headSet(30));  // [10, 20] — everything < 30
        System.out.println(t.tailSet(30));  // [30, 40, 50] — everything ≥ 30
    }
}
```

> **Gotcha — custom objects in a HashSet need `equals`/`hashCode`.** A `HashSet` decides "is this a duplicate?" using `hashCode()` then `equals()`. Put a class with the default identity-based `equals` in a set and two "equal" objects both get stored. Override both (or use a `record`). For `TreeSet`, the elements must be `Comparable` or you must supply a `Comparator`.

---

## IV. MAP — KEY → VALUE LOOKUPS

A `Map` associates unique keys with values. This is the workhorse for lookups, counting, caching, indexing — anything keyed.

```java
import java.util.*;

public class MapDemo {
    public static void main(String[] args) {
        Map<String, Integer> ages = new HashMap<>();
        ages.put("Ada", 36);
        ages.put("Bob", 42);
        ages.put("Ada", 37);                  // overwrites — keys are unique

        System.out.println(ages.get("Ada"));          // 37
        System.out.println(ages.get("Nobody"));        // null — key absent
        System.out.println(ages.getOrDefault("Nobody", -1)); // -1 — safe default
        System.out.println(ages.containsKey("Bob"));   // true
        System.out.println(ages.size());               // 2

        // Iterate over entries (the right way)
        for (Map.Entry<String, Integer> e : ages.entrySet()) {
            System.out.println(e.getKey() + " -> " + e.getValue());
        }
        // Or just keys / just values
        for (String name : ages.keySet())  System.out.println(name);
        for (int age : ages.values())      System.out.println(age);

        ages.remove("Bob");
        System.out.println(ages);                       // {Ada=37}
    }
}
```

### The modern Map methods that eliminate boilerplate

```java
import java.util.*;

public class MapPower {
    public static void main(String[] args) {
        // Word frequency count — the classic, done cleanly
        String text = "the cat sat on the mat the cat";
        Map<String, Integer> freq = new HashMap<>();
        for (String word : text.split(" ")) {
            freq.merge(word, 1, Integer::sum);   // if absent → 1; else add 1
        }
        System.out.println(freq);  // {cat=2, sat=1, on=1, mat=1, the=3}

        // computeIfAbsent — build a multimap (key → list)
        Map<Character, List<String>> byFirst = new HashMap<>();
        for (String w : List.of("apple", "avocado", "banana")) {
            byFirst.computeIfAbsent(w.charAt(0), k -> new ArrayList<>()).add(w);
        }
        System.out.println(byFirst); // {a=[apple, avocado], b=[banana]}

        // putIfAbsent, compute, replace
        Map<String, Integer> m = new HashMap<>();
        m.putIfAbsent("x", 0);                      // only sets if missing
        m.compute("x", (k, v) -> v + 10);           // transform existing value
        System.out.println(m);                       // {x=10}
    }
}
```

### HashMap vs LinkedHashMap vs TreeMap

```java
import java.util.*;

public class MapVariants {
    public static void main(String[] args) {
        Map<String, Integer> hash   = new HashMap<>();        // fastest, no order
        Map<String, Integer> linked = new LinkedHashMap<>();  // insertion order
        TreeMap<String, Integer> tree = new TreeMap<>();      // sorted by key

        for (Map<String, Integer> m : List.of(hash, linked)) {
            m.put("banana", 1); m.put("apple", 2); m.put("cherry", 3);
        }
        tree.put("banana", 1); tree.put("apple", 2); tree.put("cherry", 3);

        System.out.println(hash);    // order unpredictable
        System.out.println(linked);  // {banana=1, apple=2, cherry=3} insertion order
        System.out.println(tree);    // {apple=2, banana=1, cherry=3} sorted

        // TreeMap navigation (like TreeSet)
        System.out.println(tree.firstKey());        // apple
        System.out.println(tree.floorKey("c"));     // banana — largest key ≤ "c"
        System.out.println(tree.headMap("c"));      // {apple=2, banana=1}
    }
}
```

| Map | Ordering | get/put | When to use |
|-----|----------|:-------:|-------------|
| `HashMap` | none | **O(1)** avg | default; you just need fast lookups |
| `LinkedHashMap` | insertion (or access) order | O(1) avg | need predictable iteration order; LRU caches |
| `TreeMap` | sorted by key | O(log n) | need sorted keys or range queries |

> **Gotcha — keys need correct `hashCode`/`equals` (HashMap) or `Comparable`/`Comparator` (TreeMap).** Mutating a key after inserting it into a `HashMap` (so its hashCode changes) makes it unfindable. Use immutable keys — `String`, boxed numbers, and `record`s are ideal.

---

## V. QUEUE AND DEQUE — FIFO, LIFO, AND PRIORITIES

### Queue / Deque with ArrayDeque

`ArrayDeque` is the recommended implementation for both stacks and queues — faster than `LinkedList` and than the legacy `Stack` class.

```java
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.Queue;

public class QueueDeque {
    public static void main(String[] args) {
        // FIFO queue
        Queue<String> q = new ArrayDeque<>();
        q.offer("first"); q.offer("second"); q.offer("third");
        System.out.println(q.poll());  // first — removes & returns head
        System.out.println(q.peek());  // second — views head without removing

        // Stack (LIFO) — use a Deque, NOT the old Stack class
        Deque<Integer> stack = new ArrayDeque<>();
        stack.push(1); stack.push(2); stack.push(3);
        System.out.println(stack.pop());  // 3 — last in, first out
        System.out.println(stack.peek()); // 2

        // Double-ended: add/remove at both ends
        Deque<Integer> dq = new ArrayDeque<>();
        dq.offerFirst(1); dq.offerLast(2); dq.offerFirst(0);
        System.out.println(dq);            // [0, 1, 2]
    }
}
```

> **Gotcha — `add`/`remove` throw, `offer`/`poll`/`peek` return special values.** On a full or empty queue, `add`/`remove`/`element` throw exceptions; `offer` returns `false`, `poll`/`peek` return `null`. Prefer the non-throwing trio for normal flow control.

> **Avoid `java.util.Stack`.** It's a legacy class (extends `Vector`, synchronized, iterates in the wrong order). Use `ArrayDeque` as a stack instead.

### PriorityQueue — a binary heap

Always dequeues the *smallest* element (by natural order or a `Comparator`). The backbone of Dijkstra, scheduling, top-K problems.

```java
import java.util.PriorityQueue;
import java.util.Collections;

public class PriorityQueueDemo {
    public static void main(String[] args) {
        // Min-heap (default): smallest comes out first
        PriorityQueue<Integer> minHeap = new PriorityQueue<>();
        minHeap.offer(5); minHeap.offer(1); minHeap.offer(3);
        System.out.println(minHeap.poll());  // 1
        System.out.println(minHeap.poll());  // 3

        // Max-heap: reverse the comparator
        PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
        maxHeap.offer(5); maxHeap.offer(1); maxHeap.offer(3);
        System.out.println(maxHeap.poll());  // 5

        // Custom priority: shortest string first
        PriorityQueue<String> byLength = new PriorityQueue<>((a, b) -> a.length() - b.length());
        byLength.offer("ccc"); byLength.offer("a"); byLength.offer("bb");
        System.out.println(byLength.poll()); // "a"
    }
}
```

> **Gotcha — a PriorityQueue is NOT fully sorted.** Only the *head* is guaranteed to be the minimum. Iterating it does not yield sorted order — only repeated `poll()` does.

---

## VI. ITERATORS AND SAFE REMOVAL

The enhanced `for` loop uses an `Iterator` under the hood. Modifying a collection while iterating it with a for-each loop throws `ConcurrentModificationException`. To remove during iteration, use the iterator's own `remove()`.

```java
import java.util.*;

public class Iterating {
    public static void main(String[] args) {
        List<Integer> nums = new ArrayList<>(List.of(1, 2, 3, 4, 5, 6));

        // WRONG — throws ConcurrentModificationException
        // for (Integer n : nums) if (n % 2 == 0) nums.remove(n);

        // RIGHT — iterator.remove()
        Iterator<Integer> it = nums.iterator();
        while (it.hasNext()) {
            if (it.next() % 2 == 0) it.remove();   // safe
        }
        System.out.println(nums);   // [1, 3, 5]

        // EVEN BETTER (Java 8+) — removeIf
        List<Integer> more = new ArrayList<>(List.of(1, 2, 3, 4, 5, 6));
        more.removeIf(n -> n % 2 == 0);
        System.out.println(more);   // [1, 3, 5]
    }
}
```

---

## VII. UTILITIES, IMMUTABILITY, AND SORTING

```java
import java.util.*;

public class Utilities {
    public static void main(String[] args) {
        // Immutable collections (Java 9+) — concise, throw on modification attempts
        List<String> fixed = List.of("a", "b", "c");
        Map<String, Integer> fixedMap = Map.of("x", 1, "y", 2);
        // fixed.add("d");  // UnsupportedOperationException — it's immutable

        // To get a MUTABLE copy:
        List<String> mutable = new ArrayList<>(fixed);
        mutable.add("d");

        // Sorting a List
        List<Integer> nums = new ArrayList<>(List.of(3, 1, 4, 1, 5, 9, 2));
        Collections.sort(nums);                          // natural order → [1,1,2,3,4,5,9]
        nums.sort(Collections.reverseOrder());           // descending
        System.out.println(nums);

        // Comparator: sort strings by length, then alphabetically
        List<String> words = new ArrayList<>(List.of("banana", "fig", "apple", "kiwi"));
        words.sort(Comparator.comparingInt(String::length).thenComparing(Comparator.naturalOrder()));
        System.out.println(words);  // [fig, kiwi, apple, banana]

        // Handy Collections helpers
        System.out.println(Collections.max(nums));
        System.out.println(Collections.min(nums));
        Collections.reverse(nums);
        Collections.shuffle(nums);
    }
}
```

> **Gotcha — `Arrays.asList` and `List.of` are fixed-size/immutable.** `Arrays.asList(arr)` returns a fixed-size list backed by the array (can't add/remove); `List.of(...)` is fully immutable. To get a growable list, wrap it: `new ArrayList<>(List.of(...))`.

---

## VIII. AUTOBOXING — THE HIDDEN COST

Collections store *objects*, so primitives get auto-wrapped into their boxed types (`int` → `Integer`). This is convenient but has costs.

```java
public class Autoboxing {
    public static void main(String[] args) {
        java.util.List<Integer> list = new java.util.ArrayList<>();
        list.add(5);            // autoboxing: int 5 → Integer.valueOf(5)
        int x = list.get(0);    // unboxing: Integer → int

        Integer a = null;
        // int y = a;           // NullPointerException — unboxing null!

        // Performance: in tight numeric loops, boxing millions of values is slow & memory-heavy.
        // For hot numeric code, prefer primitive arrays (int[]) or IntStream (file 04).
    }
}
```

> **Gotcha — unboxing `null` throws NPE.** `Map<String,Integer>.get(missingKey)` returns `null`; assigning it to an `int` unboxes null and crashes. Use `getOrDefault` or check for null.

---

## IX. CHOOSING THE RIGHT COLLECTION — DECISION GUIDE

Ask these questions in order:

```
Need key → value lookups?            → MAP
   ├─ fastest, order doesn't matter   → HashMap
   ├─ remember insertion order        → LinkedHashMap
   └─ need sorted keys / ranges       → TreeMap

Need to forbid duplicates?           → SET
   ├─ fastest, order doesn't matter   → HashSet
   ├─ remember insertion order        → LinkedHashSet
   └─ need sorted / range queries     → TreeSet

Need ordered, indexed, dup-OK list?  → LIST
   ├─ default (random access, append) → ArrayList
   └─ heavy front/back add-remove     → ArrayDeque (or LinkedList)

Need FIFO / LIFO?                    → ArrayDeque (queue or stack)
Need "always smallest/largest next"? → PriorityQueue
```

### Big-O cheat sheet

| Structure | Access | Search | Insert | Delete | Ordering |
|-----------|:------:|:------:|:------:|:------:|----------|
| ArrayList | O(1) | O(n) | O(1)* end / O(n) mid | O(n) | insertion |
| LinkedList | O(n) | O(n) | O(1) ends | O(1) ends | insertion |
| HashSet / HashMap | — | O(1) avg | O(1) avg | O(1) avg | none |
| LinkedHashSet/Map | — | O(1) avg | O(1) avg | O(1) avg | insertion |
| TreeSet / TreeMap | — | O(log n) | O(log n) | O(log n) | sorted |
| ArrayDeque | O(1) ends | O(n) | O(1) ends | O(1) ends | insertion |
| PriorityQueue | O(1) peek | O(n) | O(log n) | O(log n) | heap (min/max) |

\*amortized

---

## X. A REALISTIC EXAMPLE — A TINY ANALYTICS PASS

```java
import java.util.*;

public class PageViewsReport {
    record View(String user, String page) {}

    public static void main(String[] args) {
        List<View> views = List.of(
            new View("ada", "/home"), new View("bob", "/home"),
            new View("ada", "/pricing"), new View("ada", "/home"),
            new View("cara", "/pricing"), new View("bob", "/pricing")
        );

        // 1) Count views per page  (HashMap + merge)
        Map<String, Integer> perPage = new HashMap<>();
        for (View v : views) perPage.merge(v.page(), 1, Integer::sum);

        // 2) Unique visitors per page  (Map of String -> Set)
        Map<String, Set<String>> visitors = new HashMap<>();
        for (View v : views)
            visitors.computeIfAbsent(v.page(), k -> new HashSet<>()).add(v.user());

        // 3) Pages sorted by view count, descending  (PriorityQueue)
        PriorityQueue<Map.Entry<String, Integer>> top =
            new PriorityQueue<>((a, b) -> b.getValue() - a.getValue());
        top.addAll(perPage.entrySet());

        System.out.println("Views per page: " + perPage);
        System.out.println("Unique visitors: " + visitors);
        System.out.print("Ranking: ");
        while (!top.isEmpty()) {
            var e = top.poll();
            System.out.print(e.getKey() + "(" + e.getValue() + ") ");
        }
        // e.g. Ranking: /home(3) /pricing(3)
    }
}
```

---

## XI. COMMON PITFALLS

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| Modifying a list inside a for-each loop | `ConcurrentModificationException` | `iterator.remove()` or `removeIf` |
| Custom object in HashSet/HashMap without `equals`/`hashCode` | Duplicates / lost lookups | Override both, or use `record` |
| Using `LinkedList` for indexed access | Silent O(n) gets | Use `ArrayList` |
| Unboxing a `null` Integer | `NullPointerException` | `getOrDefault`, null-check |
| Assuming `HashMap`/`HashSet` ordering | Flaky, env-dependent output | Use `LinkedHashMap`/`TreeMap` for order |
| Mutating a key already in a map | Entry becomes unfindable | Use immutable keys |
| `Arrays.asList(...).add(...)` | `UnsupportedOperationException` | Wrap in `new ArrayList<>(...)` |
| Using `java.util.Stack` | Legacy, slow, odd iteration order | `ArrayDeque` |
| Iterating a `PriorityQueue` expecting sorted order | Only head is min | `poll()` repeatedly |

---

## 🧠 KEY TAKEAWAYS

- The framework splits into **List** (ordered, indexed, dups), **Set** (no dups), **Map** (key→value), and **Queue/Deque** (FIFO/LIFO/priority). `Map` is its own branch, not a `Collection`.
- **Program to the interface** (`List`, `Map`, `Set`) and choose the implementation at construction.
- Defaults: **`ArrayList`** for lists, **`HashMap`**/**`HashSet`** for lookups/uniqueness, **`ArrayDeque`** for stacks/queues, **`PriorityQueue`** for "next smallest/largest."
- Use the **`Tree*`** variants when you need sorted order or range/neighbor queries (O(log n)); use **`Linked*`** when you need predictable iteration order.
- Hash-based collections demand correct **`hashCode`/`equals`**; tree-based ones demand **`Comparable`/`Comparator`**.
- Master the modern `Map` methods — **`merge`, `computeIfAbsent`, `getOrDefault`** — they replace piles of boilerplate.
- Beware **`ConcurrentModificationException`**, autoboxing **NPEs**, and fixed-size/immutable lists from `Arrays.asList`/`List.of`.

---

**Prev:** [`03-OOP-In-Java.md`](./03-OOP-In-Java.md) · **Next:** [`05-Generics-And-Functional.md`](./05-Generics-And-Functional.md) · **Index:** [`01-Getting-Started.md`](./01-Getting-Started.md)
