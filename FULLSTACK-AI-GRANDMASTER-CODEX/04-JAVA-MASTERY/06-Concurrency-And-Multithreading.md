# ☕ 06 — Concurrency & Multithreading ⭐

> *"Concurrency is the art of doing many things at once. It is also the art of debugging code that works 999 times and fails the 1,000th — on the customer's machine, never yours. Respect it."*

**Prev:** [`05-Exceptions-And-IO.md`](./05-Exceptions-And-IO.md) · **Next:** [`07-Spring-Boot-Essentials.md`](./07-Spring-Boot-Essentials.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. WHY CONCURRENCY

A **thread** is an independent path of execution within your program. With multiple threads you can:

- Keep an app responsive while work happens in the background (UI, servers).
- Use all CPU cores for parallel computation.
- Wait on many slow I/O operations (network, disk) at once instead of one at a time.

Java has had threads since day one, and the JVM maps them to OS threads. The catch: threads share memory, and shared mutable state is where bugs breed.

> **Concurrency vs parallelism.** *Concurrency* is dealing with many tasks at once (structure). *Parallelism* is executing many tasks at the same instant on multiple cores (execution). You can have concurrency on a single core (time-slicing); parallelism needs multiple cores.

---

## II. CREATING THREADS

### Runnable (preferred) and Thread

```java
public class CreatingThreads {
    public static void main(String[] args) throws InterruptedException {
        // 1) Implement Runnable (the task) — preferred: separates task from thread
        Runnable task = () -> {
            System.out.println("Running on: " + Thread.currentThread().getName());
        };
        Thread t1 = new Thread(task, "worker-1");
        t1.start();          // start() runs run() on a NEW thread. NEVER call run() directly.

        // 2) Subclass Thread (less flexible — you've used up your one inheritance slot)
        Thread t2 = new Thread() {
            @Override public void run() { System.out.println("Subclass thread"); }
        };
        t2.start();

        // join() — wait for a thread to finish before continuing
        t1.join();
        t2.join();
        System.out.println("All workers done");
    }
}
```

> **Gotcha — `start()` vs `run()`.** `start()` launches a new thread that then calls `run()`. Calling `run()` yourself just executes it on the *current* thread — no concurrency at all. This is a classic mistake.

> **Prefer `Runnable` over extending `Thread`.** `Runnable` is a task you can hand to any executor, schedule, or reuse. Extending `Thread` couples the task to the thread mechanism and wastes your single-inheritance slot.

---

## III. THE CORE PROBLEM — RACE CONDITIONS

When multiple threads read and write shared mutable state without coordination, operations interleave unpredictably.

```java
public class RaceCondition {
    static int counter = 0;          // shared mutable state — danger

    public static void main(String[] args) throws InterruptedException {
        Runnable increment = () -> {
            for (int i = 0; i < 100_000; i++) counter++;  // counter++ is NOT atomic
        };

        Thread a = new Thread(increment);
        Thread b = new Thread(increment);
        a.start(); b.start();
        a.join();  b.join();

        // Expected 200_000. Actual: some smaller, unpredictable number.
        System.out.println(counter);   // e.g. 137422 — lost updates
    }
}
```

Why? `counter++` is actually three steps: **read** counter, **add** 1, **write** back. Two threads can both read the same value, both add 1, and both write — two increments collapse into one. This is a **race condition**.

---

## IV. synchronized — MUTUAL EXCLUSION

`synchronized` ensures only one thread at a time runs a block guarded by a given lock (monitor). It also establishes a *happens-before* relationship, so changes by one thread become visible to the next.

```java
public class Synchronized {
    static int counter = 0;
    static final Object lock = new Object();

    public static void main(String[] args) throws InterruptedException {
        Runnable increment = () -> {
            for (int i = 0; i < 100_000; i++) {
                synchronized (lock) {        // only one thread in here at a time
                    counter++;
                }
            }
        };
        Thread a = new Thread(increment), b = new Thread(increment);
        a.start(); b.start(); a.join(); b.join();
        System.out.println(counter);   // 200000 — correct, every time
    }
}
```

### synchronized methods

```java
public class Counter {
    private int count = 0;

    public synchronized void increment() { count++; }     // locks on 'this'
    public synchronized int get() { return count; }

    // Static synchronized locks on the Class object, not an instance
    private static int globalCount = 0;
    public static synchronized void bump() { globalCount++; }
}
```

> **Gotcha — the `volatile` half-truth.** `volatile` guarantees *visibility* (one thread's write is seen by others) but **not atomicity**. `volatile int x; x++;` is still a race. Use `volatile` for simple flags (`volatile boolean running`), not for compound operations.

```java
public class VolatileFlag {
    static volatile boolean running = true;   // visibility guaranteed across threads

    public static void main(String[] args) throws InterruptedException {
        Thread worker = new Thread(() -> {
            while (running) { /* spin */ }      // without volatile, may loop FOREVER (cached value)
            System.out.println("stopped");
        });
        worker.start();
        Thread.sleep(100);
        running = false;        // worker sees this and exits
        worker.join();
    }
}
```

---

## V. ATOMICS AND CONCURRENT COLLECTIONS

Locking is correct but coarse. The `java.util.concurrent` package offers lock-free and fine-grained alternatives that are faster and easier to use correctly.

### Atomic variables — lock-free counters

```java
import java.util.concurrent.atomic.AtomicInteger;

public class Atomics {
    static AtomicInteger counter = new AtomicInteger(0);

    public static void main(String[] args) throws InterruptedException {
        Runnable inc = () -> { for (int i = 0; i < 100_000; i++) counter.incrementAndGet(); };
        Thread a = new Thread(inc), b = new Thread(inc);
        a.start(); b.start(); a.join(); b.join();
        System.out.println(counter.get());   // 200000 — atomic, no explicit lock
    }
}
```

### Concurrent collections — thread-safe by design

```java
import java.util.*;
import java.util.concurrent.*;

public class ConcurrentCollections {
    public static void main(String[] args) {
        // ConcurrentHashMap — high-performance thread-safe map (use this, NOT Hashtable)
        ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
        map.put("a", 1);
        map.merge("a", 1, Integer::sum);          // atomic update → 2
        map.computeIfAbsent("b", k -> 0);

        // CopyOnWriteArrayList — great for read-heavy, write-rare lists (listeners, configs)
        List<String> listeners = new CopyOnWriteArrayList<>();
        listeners.add("logger");

        // BlockingQueue — the backbone of producer/consumer; consumers block until items arrive
        BlockingQueue<String> queue = new LinkedBlockingQueue<>();
        // producer: queue.put("job");   consumer: queue.take();  (both block appropriately)

        System.out.println(map);   // {a=2, b=0}
    }
}
```

> **Don't synchronize a `HashMap` manually when `ConcurrentHashMap` exists.** It allows concurrent reads and segmented writes — far better throughput than wrapping a plain map in `synchronized`. Avoid the legacy `Hashtable`/`Vector`/`Stack` (globally synchronized, slow).

---

## VI. EXECUTORSERVICE — DON'T MANAGE THREADS BY HAND

Creating raw `Thread`s for every task is wasteful (threads are expensive) and unmanageable. An **`ExecutorService`** maintains a pool of reusable threads and a queue of tasks. This is how real applications do concurrency.

```java
import java.util.concurrent.*;
import java.util.*;

public class Executors_Demo {
    public static void main(String[] args) throws Exception {
        // A pool of 4 worker threads
        ExecutorService pool = Executors.newFixedThreadPool(4);

        // submit a Runnable (no result)
        pool.submit(() -> System.out.println("task on " + Thread.currentThread().getName()));

        // submit a Callable (returns a value) → get a Future
        Future<Integer> future = pool.submit(() -> {
            Thread.sleep(50);
            return 6 * 7;
        });
        System.out.println("Result: " + future.get());   // blocks until ready → 42

        // invokeAll — run many tasks, collect all results
        List<Callable<Integer>> tasks = List.of(() -> 1, () -> 2, () -> 3);
        List<Future<Integer>> results = pool.invokeAll(tasks);
        int sum = 0;
        for (Future<Integer> f : results) sum += f.get();
        System.out.println("Sum: " + sum);                // 6

        // ALWAYS shut down — otherwise the JVM won't exit (non-daemon threads linger)
        pool.shutdown();                                  // no new tasks; finish queued ones
        pool.awaitTermination(1, TimeUnit.SECONDS);
    }
}
```

### Choosing a pool

| Factory | Use when |
|---------|----------|
| `newFixedThreadPool(n)` | Steady, CPU-bound work; cap at ~#cores |
| `newCachedThreadPool()` | Many short-lived tasks; pool grows/shrinks |
| `newSingleThreadExecutor()` | Tasks must run sequentially in order |
| `newScheduledThreadPool(n)` | Delayed or periodic tasks |
| `newVirtualThreadPerTaskExecutor()` | (Java 21+) massive numbers of I/O-bound tasks |

> **Virtual threads (Java 21+).** Project Loom adds *virtual threads* — extremely lightweight threads you can spawn by the millions, ideal for blocking I/O. `Executors.newVirtualThreadPerTaskExecutor()` gives a thread per task cheaply. They make the classic "thread per request" model scale without async complexity.

```java
// Java 21+ : a million tasks, no sweat
// try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
//     for (int i = 0; i < 1_000_000; i++) {
//         executor.submit(() -> { Thread.sleep(1000); return null; });
//     }
// }   // try-with-resources shuts it down
```

---

## VII. CompletableFuture — COMPOSABLE ASYNC

`Future.get()` blocks. `CompletableFuture` lets you build non-blocking pipelines: run async work, transform results, combine futures, and handle errors — all without blocking a thread waiting.

```java
import java.util.concurrent.*;

public class CompletableFutures {
    static int fetchPrice(String item) {
        try { Thread.sleep(100); } catch (InterruptedException ignored) {}
        return item.length() * 10;     // pretend this is a slow network call
    }

    public static void main(String[] args) throws Exception {
        // Run async, then transform the result without blocking
        CompletableFuture<String> pipeline =
            CompletableFuture.supplyAsync(() -> fetchPrice("laptop"))   // async source
                .thenApply(price -> price * 2)                          // transform (map)
                .thenApply(price -> "Total: $" + price);                // transform again

        System.out.println(pipeline.get());   // Total: $120

        // Combine two independent async calls
        CompletableFuture<Integer> a = CompletableFuture.supplyAsync(() -> fetchPrice("phone"));
        CompletableFuture<Integer> b = CompletableFuture.supplyAsync(() -> fetchPrice("case"));
        CompletableFuture<Integer> combined = a.thenCombine(b, Integer::sum);
        System.out.println("Combined: " + combined.get());

        // Error handling without try/catch around get()
        CompletableFuture<Integer> safe =
            CompletableFuture.<Integer>supplyAsync(() -> { throw new RuntimeException("boom"); })
                .exceptionally(ex -> {
                    System.out.println("Recovered from: " + ex.getMessage());
                    return -1;     // fallback value
                });
        System.out.println(safe.get());   // -1

        // Fire-and-forget side effect when done
        CompletableFuture.supplyAsync(() -> fetchPrice("mouse"))
            .thenAccept(p -> System.out.println("Mouse price: " + p))
            .join();   // wait for the whole chain
    }
}
```

Key methods:

- `supplyAsync` — start async work that returns a value (`runAsync` for no value).
- `thenApply` — transform the result (like `map`).
- `thenCompose` — chain another future (like `flatMap`) — avoids nested futures.
- `thenCombine` — merge two independent futures.
- `exceptionally` / `handle` — recover from failures.
- `thenAccept` / `thenRun` — terminal side effects.

> **Gotcha — exceptions in a CompletableFuture are deferred.** A failure inside `supplyAsync` doesn't throw immediately; it surfaces when you call `get()` (wrapped in `ExecutionException`) or in `exceptionally`/`handle`. Always attach error handling to async pipelines.

---

## VIII. EXPLICIT LOCKS — WHEN synchronized ISN'T ENOUGH

`java.util.concurrent.locks.ReentrantLock` gives you what `synchronized` can't: timeouts, interruptibility, fairness, and try-without-blocking.

```java
import java.util.concurrent.locks.*;

public class ExplicitLocks {
    private final ReentrantLock lock = new ReentrantLock();
    private int balance = 100;

    void withdraw(int amount) {
        lock.lock();                 // acquire
        try {
            if (balance >= amount) balance -= amount;
        } finally {
            lock.unlock();           // ALWAYS unlock in finally — or you deadlock forever
        }
    }

    boolean tryWithdraw(int amount) {
        // tryLock — don't block; give up if the lock is busy
        if (lock.tryLock()) {
            try { balance -= amount; return true; }
            finally { lock.unlock(); }
        }
        return false;   // couldn't get the lock right now
    }
}
```

`ReadWriteLock` allows many concurrent readers but exclusive writers — ideal for read-heavy data:

```java
import java.util.concurrent.locks.*;

public class CachedConfig {
    private final ReadWriteLock rw = new ReentrantReadWriteLock();
    private String config = "default";

    String read() {
        rw.readLock().lock();        // multiple readers allowed simultaneously
        try { return config; } finally { rw.readLock().unlock(); }
    }
    void write(String c) {
        rw.writeLock().lock();       // exclusive — blocks all readers and writers
        try { config = c; } finally { rw.writeLock().unlock(); }
    }
}
```

---

## IX. DEADLOCK AND OTHER HAZARDS

A **deadlock**: thread A holds lock 1 and wants lock 2; thread B holds lock 2 and wants lock 1. Both wait forever.

```java
public class Deadlock {
    static final Object lockA = new Object(), lockB = new Object();

    public static void main(String[] args) {
        Thread t1 = new Thread(() -> {
            synchronized (lockA) {
                sleep();
                synchronized (lockB) { System.out.println("t1 got both"); }  // waits for lockB
            }
        });
        Thread t2 = new Thread(() -> {
            synchronized (lockB) {                                            // opposite order!
                sleep();
                synchronized (lockA) { System.out.println("t2 got both"); }  // waits for lockA
            }
        });
        t1.start(); t2.start();   // likely DEADLOCK — neither finishes
    }
    static void sleep() { try { Thread.sleep(50); } catch (InterruptedException ignored) {} }
}
```

> **Deadlock prevention — lock ordering.** If every thread always acquires locks in the *same global order* (e.g., always lockA before lockB), the cycle is impossible. Other tactics: use `tryLock` with a timeout, hold locks briefly, and avoid calling foreign code while holding a lock.

The four concurrency hazards to know:

- **Race condition** — unsynchronized access to shared mutable state → corrupted data.
- **Deadlock** — threads wait on each other in a cycle → frozen.
- **Livelock** — threads keep responding to each other and make no progress.
- **Starvation** — a thread never gets CPU/lock time because others monopolize it.

---

## X. A COMPLETE EXAMPLE — PARALLEL DOWNLOADER

```java
import java.util.*;
import java.util.concurrent.*;

public class ParallelDownloader {

    // Simulate downloading a URL (a slow I/O operation)
    static String download(String url) {
        try { Thread.sleep(200); } catch (InterruptedException ignored) {}
        return url + " (" + (url.length() * 100) + " bytes)";
    }

    public static void main(String[] args) throws Exception {
        List<String> urls = List.of(
            "http://a.com", "http://bb.com", "http://ccc.com", "http://dddd.com");

        ExecutorService pool = Executors.newFixedThreadPool(4);
        long start = System.currentTimeMillis();

        // Kick off all downloads concurrently as CompletableFutures
        List<CompletableFuture<String>> futures = urls.stream()
            .map(url -> CompletableFuture.supplyAsync(() -> download(url), pool)
                                         .exceptionally(ex -> url + " FAILED: " + ex.getMessage()))
            .toList();

        // Wait for ALL of them, then gather results
        CompletableFuture.allOf(futures.toArray(new CompletableFuture[0])).join();
        List<String> results = futures.stream().map(CompletableFuture::join).toList();

        long elapsed = System.currentTimeMillis() - start;
        results.forEach(System.out::println);
        // 4 downloads of 200ms each finish in ~200ms (parallel), not 800ms (sequential)
        System.out.println("Done in ~" + elapsed + "ms");

        pool.shutdown();
        pool.awaitTermination(1, TimeUnit.SECONDS);
    }
}
```

---

## XI. COMMON PITFALLS

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| Calling `run()` instead of `start()` | No new thread; runs serially | Use `start()` |
| Unsynchronized shared mutable state | Race conditions, lost updates | `synchronized`, atomics, or immutability |
| Using `volatile` for `count++` | Still races (not atomic) | `AtomicInteger` or a lock |
| Forgetting `lock.unlock()` | Permanent deadlock | Unlock in a `finally` block |
| Inconsistent lock ordering | Deadlock | Acquire locks in one global order |
| Not shutting down an ExecutorService | JVM hangs on exit; thread leak | `shutdown()` + `awaitTermination` |
| Ignoring `CompletableFuture` exceptions | Silent failures | `exceptionally`/`handle` |
| `Hashtable`/`Vector`/synchronized map | Poor throughput | `ConcurrentHashMap` |
| Catching/ignoring `InterruptedException` | Breaks cancellation | Restore the interrupt or propagate |
| Oversized thread pools | Context-switch thrash | Size to workload (~#cores for CPU-bound) |

---

## 🧠 KEY TAKEAWAYS

- A **thread** is an independent execution path; threads share memory, and **shared mutable state** is the root of concurrency bugs.
- Prefer **`Runnable`** tasks, and `start()` (never `run()`) to actually go parallel.
- **Race conditions** come from non-atomic access; fix with **`synchronized`**, **atomics** (`AtomicInteger`), explicit **locks**, or — best — **immutability** and not sharing state.
- `volatile` gives **visibility, not atomicity** — only for simple flags.
- Don't hand-manage threads: use an **`ExecutorService`** thread pool, and always **shut it down**. On Java 21+, **virtual threads** scale blocking I/O to millions of tasks.
- **`CompletableFuture`** builds non-blocking async pipelines (`thenApply`/`thenCompose`/`thenCombine`); attach `exceptionally`/`handle` for errors.
- Know the hazards — **race, deadlock, livelock, starvation** — and prevent deadlock with consistent **lock ordering**. Reach for **concurrent collections** (`ConcurrentHashMap`) over manual synchronization.

---

**Prev:** [`05-Exceptions-And-IO.md`](./05-Exceptions-And-IO.md) · **Next:** [`07-Spring-Boot-Essentials.md`](./07-Spring-Boot-Essentials.md) · **Index:** [`00-Index.md`](./00-Index.md)
