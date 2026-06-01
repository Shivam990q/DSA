# ☕ 07 — Spring Boot Essentials ⭐

> *"Spring Boot is the reason a Java backend that used to take a week of XML configuration now takes an afternoon. It handles the plumbing so you write business logic. A huge share of the world's APIs run on it."*

**Prev:** [`06-Concurrency-And-Multithreading.md`](./06-Concurrency-And-Multithreading.md) · **Next:** [`08-Spring-Boot-Data-And-JPA.md`](./08-Spring-Boot-Data-And-JPA.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. WHAT SPRING AND SPRING BOOT ACTUALLY ARE

**Spring Framework** is a giant toolkit for building Java applications. Its heart is the **IoC container** (Inversion of Control), which creates and wires your objects together for you. Around that core, Spring adds modules: web (REST APIs), data (databases), security, messaging, and more.

The problem: classic Spring needed mountains of XML and manual configuration. **Spring Boot** is a layer on top that takes an opinionated, convention-over-configuration approach:

- **Auto-configuration** — sees what's on your classpath and configures it sensibly. Add a database driver, and Spring Boot wires up a connection pool automatically.
- **Starters** — curated dependency bundles. `spring-boot-starter-web` pulls in everything for REST APIs in one line.
- **Embedded server** — an embedded Tomcat is built in, so your app is a runnable `.jar`, not a `.war` you deploy to a server. `java -jar app.jar` and you're live.
- **Production-ready** — health checks, metrics, and externalized config out of the box.

```
Without Spring Boot:                 With Spring Boot:
  configure DispatcherServlet          @SpringBootApplication
  set up Tomcat, web.xml               + spring-boot-starter-web
  wire beans in XML                    + a few annotations
  manage dependency versions     →     run.  it just works.
  deploy a WAR to a server
```

> **Mental model:** Spring is the engine; Spring Boot is the car built around it so you can just drive. You'll spend your time on `@RestController` and `@Service`, not on configuration.

---

## II. INVERSION OF CONTROL & DEPENDENCY INJECTION — THE CORE IDEA

This is the single most important concept in Spring. Understand it and everything else clicks.

**Normally**, an object creates its own dependencies:

```java
// TIGHT COUPLING — OrderService is welded to a specific EmailService
public class OrderService {
    private final EmailService email = new EmailService();  // creates its own dependency
    // Problems: can't swap EmailService for a test fake; can't share one instance; rigid.
}
```

**With Dependency Injection (DI)**, the object *declares* what it needs and the container *provides* it:

```java
// LOOSE COUPLING — the dependency is INJECTED from outside
public class OrderService {
    private final EmailService email;
    public OrderService(EmailService email) {   // "give me an EmailService"
        this.email = email;
    }
}
```

**Inversion of Control (IoC)** = you no longer control object creation; the **Spring container** does. It creates your objects (called **beans**), figures out their dependencies, and wires the whole graph together. This makes code testable (inject a mock), flexible (swap implementations), and free of `new` sprawl.

### The annotations that make it happen

```java
import org.springframework.stereotype.*;

// @Component (and its specializations) marks a class as a Spring-managed bean
@Service                       // a service-layer bean (specialization of @Component)
public class EmailService {
    public void send(String to, String msg) {
        System.out.println("Email to " + to + ": " + msg);
    }
}

@Service
public class OrderService {
    private final EmailService email;

    // Constructor injection: Spring sees this needs an EmailService and supplies the bean.
    // No @Autowired needed when there's a single constructor (Spring infers it).
    public OrderService(EmailService email) {
        this.email = email;
    }

    public void placeOrder(String customer) {
        // ... business logic ...
        email.send(customer, "Your order is confirmed!");
    }
}
```

**Stereotype annotations** (all are `@Component` under the hood, with semantic meaning):

| Annotation | Layer | Meaning |
|------------|-------|---------|
| `@Component` | any | generic Spring bean |
| `@Service` | business logic | service-layer bean |
| `@Repository` | data access | DAO bean; adds DB exception translation |
| `@RestController` | web | handles HTTP, returns data (JSON) |
| `@Configuration` | config | declares beans via `@Bean` methods |

> **Prefer constructor injection.** Inject dependencies through the constructor (as above), not via `@Autowired` on fields. It makes dependencies explicit, allows `final` fields (immutable), and lets you construct the object in tests without Spring. Field injection (`@Autowired private X x;`) is discouraged.

---

## III. YOUR FIRST SPRING BOOT APP

### Project setup

Generate a project at [start.spring.io](https://start.spring.io): choose **Maven**, **Java 17+**, and add the **Spring Web** dependency. You get this structure:

```
my-api/
├── pom.xml                      ← Maven build file (dependencies, plugins)
├── src/main/java/com/example/demo/
│   └── DemoApplication.java     ← the entry point
└── src/main/resources/
    └── application.properties   ← configuration
```

The key parts of `pom.xml`:

```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.3.0</version>     <!-- manages all dependency versions for you -->
</parent>

<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>  <!-- REST + embedded Tomcat -->
    </dependency>
</dependencies>
```

### The entry point

```java
package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication   // = @Configuration + @EnableAutoConfiguration + @ComponentScan
public class DemoApplication {
    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);  // boots the whole app
    }
}
```

`@SpringBootApplication` bundles three annotations:

- `@EnableAutoConfiguration` — turn on Boot's auto-config magic.
- `@ComponentScan` — scan this package (and sub-packages) for your beans.
- `@Configuration` — allow this class to define beans.

Run it: `mvn spring-boot:run` (or run `main` in your IDE). An embedded Tomcat starts on port 8080.

---

## IV. BUILDING A REST API WITH @RestController

A `@RestController` maps HTTP requests to Java methods and serializes return values to JSON automatically (via Jackson, included in the web starter).

```java
package com.example.demo;

import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/greetings")    // base path for all methods here
public class GreetingController {

    // GET /api/greetings/hello
    @GetMapping("/hello")
    public String hello() {
        return "Hello, World!";
    }

    // GET /api/greetings/hello/Ada  — @PathVariable pulls from the URL
    @GetMapping("/hello/{name}")
    public Greeting helloName(@PathVariable String name) {
        return new Greeting("Hello, " + name + "!");   // returned object → JSON
    }

    // GET /api/greetings/search?term=hi&lang=en  — @RequestParam reads query string
    @GetMapping("/search")
    public Greeting search(@RequestParam String term,
                           @RequestParam(defaultValue = "en") String lang) {
        return new Greeting("[" + lang + "] " + term);
    }

    // A record makes a clean JSON response shape
    record Greeting(String message) {}
}
```

Hit `GET http://localhost:8080/api/greetings/hello/Ada` and you get:

```json
{ "message": "Hello, Ada!" }
```

### The full set of HTTP verb mappings

```java
package com.example.demo;

import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import java.util.*;

@RestController
@RequestMapping("/api/tasks")
public class TaskController {

    // In-memory store for the example (a real app uses a database — see file 08)
    private final Map<Integer, Task> store = new HashMap<>();
    private int nextId = 1;

    record Task(int id, String title, boolean done) {}
    record CreateTaskRequest(String title) {}   // request body shape

    // READ all → GET /api/tasks
    @GetMapping
    public Collection<Task> all() {
        return store.values();
    }

    // READ one → GET /api/tasks/1  (404 if missing)
    @GetMapping("/{id}")
    public ResponseEntity<Task> one(@PathVariable int id) {
        Task t = store.get(id);
        return (t == null) ? ResponseEntity.notFound().build() : ResponseEntity.ok(t);
    }

    // CREATE → POST /api/tasks   with JSON body {"title": "..."}
    @PostMapping
    public ResponseEntity<Task> create(@RequestBody CreateTaskRequest req) {
        Task t = new Task(nextId++, req.title(), false);
        store.put(t.id(), t);
        return ResponseEntity.status(HttpStatus.CREATED).body(t);   // 201 Created
    }

    // UPDATE → PUT /api/tasks/1
    @PutMapping("/{id}")
    public ResponseEntity<Task> update(@PathVariable int id, @RequestBody Task updated) {
        if (!store.containsKey(id)) return ResponseEntity.notFound().build();
        Task t = new Task(id, updated.title(), updated.done());
        store.put(id, t);
        return ResponseEntity.ok(t);
    }

    // DELETE → DELETE /api/tasks/1
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable int id) {
        return (store.remove(id) != null)
            ? ResponseEntity.noContent().build()       // 204 No Content
            : ResponseEntity.notFound().build();        // 404
    }
}
```

| Annotation | HTTP method | Typical use |
|------------|-------------|-------------|
| `@GetMapping` | GET | read data |
| `@PostMapping` | POST | create |
| `@PutMapping` | PUT | full update / replace |
| `@PatchMapping` | PATCH | partial update |
| `@DeleteMapping` | DELETE | delete |
| `@RequestBody` | — | bind JSON request body to an object |
| `@PathVariable` | — | read a value from the URL path |
| `@RequestParam` | — | read a query-string parameter |

> **`ResponseEntity` gives you control over the status code and headers.** Returning a bare object always yields `200 OK`. Use `ResponseEntity` to return `201 Created`, `404 Not Found`, `204 No Content`, etc. Correct status codes are part of a good REST API.

---

## V. THE LAYERED ARCHITECTURE — Controller → Service → Repository

Real apps separate concerns into layers. This keeps controllers thin, business logic testable, and data access isolated.

```
HTTP request
    │
    ▼
@RestController   ← handles HTTP: parse request, return response. NO business logic.
    │  calls
    ▼
@Service          ← business logic, rules, orchestration. The "brain."
    │  calls
    ▼
@Repository       ← data access: talks to the database. NO business logic.
    │
    ▼
Database
```

```java
// --- Domain model ---
record Product(Long id, String name, double price) {}

// --- Repository layer: data access (in-memory here; real DB in file 08) ---
import org.springframework.stereotype.Repository;
import java.util.*;
import java.util.concurrent.atomic.AtomicLong;

@Repository
class ProductRepository {
    private final Map<Long, Product> db = new HashMap<>();
    private final AtomicLong ids = new AtomicLong();

    List<Product> findAll() { return new ArrayList<>(db.values()); }
    Optional<Product> findById(Long id) { return Optional.ofNullable(db.get(id)); }
    Product save(String name, double price) {
        long id = ids.incrementAndGet();
        Product p = new Product(id, name, price);
        db.put(id, p);
        return p;
    }
}
```

```java
// --- Service layer: business logic ---
import org.springframework.stereotype.Service;
import java.util.*;

@Service
class ProductService {
    private final ProductRepository repo;
    ProductService(ProductRepository repo) { this.repo = repo; }   // constructor injection

    List<Product> list() { return repo.findAll(); }

    Product create(String name, double price) {
        // business rules live HERE, not in the controller
        if (name == null || name.isBlank()) throw new IllegalArgumentException("Name required");
        if (price < 0) throw new IllegalArgumentException("Price cannot be negative");
        return repo.save(name.strip(), price);
    }

    Product get(Long id) {
        return repo.findById(id)
            .orElseThrow(() -> new NoSuchElementException("Product " + id + " not found"));
    }
}
```

```java
// --- Controller layer: HTTP only ---
import org.springframework.web.bind.annotation.*;
import org.springframework.http.*;
import java.util.List;

@RestController
@RequestMapping("/api/products")
class ProductController {
    private final ProductService service;
    ProductController(ProductService service) { this.service = service; }

    record CreateProduct(String name, double price) {}

    @GetMapping
    List<Product> all() { return service.list(); }

    @GetMapping("/{id}")
    Product one(@PathVariable Long id) { return service.get(id); }

    @PostMapping
    ResponseEntity<Product> create(@RequestBody CreateProduct req) {
        Product p = service.create(req.name(), req.price());
        return ResponseEntity.status(HttpStatus.CREATED).body(p);
    }
}
```

Spring wires this whole graph for you: it creates the `ProductRepository`, injects it into `ProductService`, injects that into `ProductController`. You never write `new`.

---

## VI. GLOBAL EXCEPTION HANDLING

Don't let raw exceptions leak ugly stack traces to clients. Centralize error handling with `@RestControllerAdvice`.

```java
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import java.util.*;

@RestControllerAdvice    // applies to ALL controllers
class GlobalExceptionHandler {

    record ApiError(int status, String message) {}

    // Maps NoSuchElementException → 404
    @ExceptionHandler(NoSuchElementException.class)
    ResponseEntity<ApiError> handleNotFound(NoSuchElementException e) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
            .body(new ApiError(404, e.getMessage()));
    }

    // Maps IllegalArgumentException → 400
    @ExceptionHandler(IllegalArgumentException.class)
    ResponseEntity<ApiError> handleBadInput(IllegalArgumentException e) {
        return ResponseEntity.badRequest()
            .body(new ApiError(400, e.getMessage()));
    }
}
```

Now a missing product returns a clean `404` with `{"status":404,"message":"Product 9 not found"}` instead of a 500 and a stack trace.

---

## VII. VALIDATION

Add `spring-boot-starter-validation` and annotate your request objects. Spring validates before your method runs.

```java
import jakarta.validation.constraints.*;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/users")
class UserController {

    record CreateUser(
        @NotBlank(message = "name is required")        String name,
        @Email(message = "must be a valid email")       String email,
        @Min(value = 18, message = "must be 18+")       int age
    ) {}

    @PostMapping
    String create(@Valid @RequestBody CreateUser req) {   // @Valid triggers validation
        return "Created " + req.name();
    }
    // Invalid input → 400 with field error details, automatically.
}
```

Common constraints: `@NotNull`, `@NotBlank`, `@NotEmpty`, `@Size(min,max)`, `@Min`/`@Max`, `@Email`, `@Pattern(regexp=...)`, `@Positive`.

---

## VIII. CONFIGURATION — application.properties

Externalize configuration so the same `.jar` runs in dev, test, and prod with different settings.

```properties
# src/main/resources/application.properties

# Server
server.port=8080
server.servlet.context-path=/api

# Logging
logging.level.root=INFO
logging.level.com.example=DEBUG

# Custom properties (your own)
app.welcome-message=Welcome to the API
app.max-items=100
```

Read config into your code:

```java
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
class ConfigConsumer {
    // Inject a single property with @Value
    @Value("${app.welcome-message}")
    private String welcome;

    @Value("${app.max-items:50}")   // ':50' = default if the property is absent
    private int maxItems;
}
```

For grouped config, bind a whole prefix to a typed object with `@ConfigurationProperties`:

```java
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@ConfigurationProperties(prefix = "app")
class AppProperties {
    private String welcomeMessage;
    private int maxItems;
    // getters & setters bind app.welcome-message → welcomeMessage, app.max-items → maxItems
    public String getWelcomeMessage() { return welcomeMessage; }
    public void setWelcomeMessage(String v) { this.welcomeMessage = v; }
    public int getMaxItems() { return maxItems; }
    public void setMaxItems(int v) { this.maxItems = v; }
}
```

> **Profiles** let you keep environment-specific files: `application-dev.properties`, `application-prod.properties`. Activate one with `spring.profiles.active=prod` (or the `SPRING_PROFILES_ACTIVE` env var). YAML (`application.yml`) is a popular alternative to `.properties` for nested config.

> **Security note — never commit secrets.** Database passwords, API keys, and tokens should come from **environment variables** or a secrets manager, not be hardcoded in `application.properties` committed to git. Reference them like `spring.datasource.password=${DB_PASSWORD}`.

---

## IX. TESTING A CONTROLLER

Spring Boot includes excellent test support. `@WebMvcTest` spins up just the web layer with a `MockMvc` to fire fake requests.

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.test.web.servlet.MockMvc;
import org.junit.jupiter.api.Test;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(GreetingController.class)
class GreetingControllerTest {

    @Autowired MockMvc mvc;

    @Test
    void helloReturnsGreeting() throws Exception {
        mvc.perform(get("/api/greetings/hello/Ada"))
           .andExpect(status().isOk())
           .andExpect(jsonPath("$.message").value("Hello, Ada!"));
    }
}
```

---

## X. THE REQUEST LIFECYCLE (HOW IT ALL CONNECTS)

```
1. Client sends:  POST /api/products  {"name":"Pen","price":2.5}
2. Embedded Tomcat receives the TCP request
3. DispatcherServlet (Spring's front controller) routes by URL + verb
4. Finds @PostMapping in ProductController
5. Jackson deserializes the JSON body → CreateProduct record
6. (@Valid) validates it
7. Controller calls ProductService.create(...)   ← injected bean
8. Service applies business rules, calls ProductRepository.save(...) ← injected bean
9. Return value bubbles back up
10. Jackson serializes the Product → JSON
11. ResponseEntity sets status 201; Tomcat sends the HTTP response
```

Every arrow that says "injected bean" is the IoC container doing its job. You wrote the logic; Spring wired the wires.

---

## XI. COMMON PITFALLS

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| Beans outside the scanned package | `NoSuchBeanDefinitionException` | Keep beans under the `@SpringBootApplication` package tree |
| Field injection (`@Autowired` field) | Hard to test, can't be `final` | Constructor injection |
| Business logic in controllers | Untestable, duplicated | Push logic into `@Service` |
| Returning entities directly | Leaks DB internals, lazy-load errors | Return DTOs/records |
| No status codes (always 200) | Poor REST semantics | Use `ResponseEntity` |
| Forgetting `@RequestBody` | Body not bound; nulls | Annotate the body param |
| Hardcoded secrets in properties | Security leak | Env vars / secrets manager |
| Two beans of the same type, no `@Qualifier` | Ambiguous injection error | `@Qualifier` or `@Primary` |
| Catching exceptions per-controller | Duplicated handling | `@RestControllerAdvice` |

---

## 🧠 KEY TAKEAWAYS

- **Spring** is an IoC container + module ecosystem; **Spring Boot** adds auto-configuration, starters, and an embedded server so an API is a runnable `.jar`.
- **Dependency Injection** is the core: classes declare what they need and the container supplies it. Use **constructor injection** with `final` fields.
- Beans are declared with stereotypes: **`@RestController`** (web), **`@Service`** (logic), **`@Repository`** (data), `@Component`/`@Configuration`.
- Build REST APIs with **`@GetMapping`/`@PostMapping`/...**, **`@PathVariable`**, **`@RequestParam`**, **`@RequestBody`**, and **`ResponseEntity`** for correct status codes.
- Structure code in layers: **Controller (HTTP) → Service (logic) → Repository (data)**. Keep controllers thin.
- Centralize errors with **`@RestControllerAdvice`**, validate input with **`@Valid`** + constraints, and externalize settings in **`application.properties`** (never commit secrets).
- The **DispatcherServlet** routes each request through your injected beans and Jackson handles JSON both ways.

---

**Prev:** [`06-Concurrency-And-Multithreading.md`](./06-Concurrency-And-Multithreading.md) · **Next:** [`08-Spring-Boot-Data-And-JPA.md`](./08-Spring-Boot-Data-And-JPA.md) · **Index:** [`00-Index.md`](./00-Index.md)
