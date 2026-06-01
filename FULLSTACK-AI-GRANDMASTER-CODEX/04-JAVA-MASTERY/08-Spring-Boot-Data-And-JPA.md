# ☕ 08 — Spring Boot Data & JPA

> *"A web app without a database is a demo. JPA lets you work with Java objects and lets Spring Data write the SQL — so you spend your time on the domain, not on boilerplate queries."*

**Prev:** [`07-Spring-Boot-Essentials.md`](./07-Spring-Boot-Essentials.md) · **Next:** — (end of Java Mastery) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. THE STACK — JPA, HIBERNATE, SPRING DATA

Three layers sit between your Java objects and the database rows. Knowing who does what prevents a lot of confusion:

- **JPA (Jakarta Persistence API)** — a *specification* (a set of interfaces and annotations like `@Entity`, `@Id`) for **Object-Relational Mapping (ORM)**: mapping Java objects to database tables. JPA itself is just the contract.
- **Hibernate** — the most common *implementation* of JPA. It generates and runs the actual SQL. Spring Boot uses it by default.
- **Spring Data JPA** — a Spring layer on top that eliminates boilerplate. You declare a *repository interface* and Spring writes the implementation at runtime, including queries derived from method names.

```
Your code  →  Spring Data JPA  →  JPA (spec)  →  Hibernate  →  JDBC  →  Database
 (Entities + Repository interface)   (annotations)  (writes SQL)        (rows)
```

**ORM** is the big idea: a `User` *object* maps to a row in a `users` *table*; a field maps to a column; a `List<Order>` field maps to a foreign-key relationship. You manipulate objects; the ORM keeps the database in sync.

> **Why ORM?** You stop hand-writing repetitive `INSERT`/`SELECT`/`UPDATE` SQL and stop manually mapping `ResultSet` rows to objects. You still *can* write SQL when you need to — but 90% of CRUD vanishes.

---

## II. PROJECT SETUP

On [start.spring.io](https://start.spring.io), add **Spring Web**, **Spring Data JPA**, and a database driver. We'll use **H2** (an in-memory database, perfect for learning — zero setup) and show the swap to PostgreSQL.

```xml
<!-- pom.xml dependencies -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
<dependency>
    <groupId>com.h2database</groupId>
    <artifactId>h2</artifactId>
    <scope>runtime</scope>
</dependency>
```

```properties
# application.properties — H2 in-memory (development)
spring.datasource.url=jdbc:h2:mem:testdb
spring.datasource.driver-class-name=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=

# Show the SQL Hibernate generates (great for learning)
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true

# Auto-manage the schema from your entities (see the warning below)
spring.jpa.hibernate.ddl-auto=update

# Browse the DB at http://localhost:8080/h2-console
spring.h2.console.enabled=true
```

> **`ddl-auto` — handle with care.** `update` (auto-add tables/columns) and `create-drop` (rebuild on each start) are great for development. In **production use `validate` or `none`** and manage schema changes with a migration tool like **Flyway** or **Liquibase**. Letting Hibernate alter a production schema automatically is a recipe for data loss.

---

## III. ENTITIES — MAPPING OBJECTS TO TABLES

An `@Entity` is a class whose instances are persisted as table rows.

```java
package com.example.shop;

import jakarta.persistence.*;
import java.time.Instant;

@Entity
@Table(name = "products")          // table name (defaults to class name if omitted)
public class Product {

    @Id                                            // primary key
    @GeneratedValue(strategy = GenerationType.IDENTITY)  // DB auto-increments it
    private Long id;

    @Column(nullable = false, length = 100)        // NOT NULL, VARCHAR(100)
    private String name;

    @Column(nullable = false)
    private double price;

    @Column(name = "stock_qty")                     // map to a differently-named column
    private int stock;

    @Enumerated(EnumType.STRING)                    // store the enum NAME, not its ordinal
    private Status status = Status.ACTIVE;

    @Column(updatable = false)
    private Instant createdAt = Instant.now();

    public enum Status { ACTIVE, DISCONTINUED }

    // JPA REQUIRES a no-arg constructor (it instantiates via reflection)
    protected Product() {}

    public Product(String name, double price, int stock) {
        this.name = name; this.price = price; this.stock = stock;
    }

    // Getters and setters (JPA uses them; omitted here for brevity except a couple)
    public Long getId() { return id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public double getPrice() { return price; }
    public void setPrice(double price) { this.price = price; }
    public int getStock() { return stock; }
    public void setStock(int stock) { this.stock = stock; }
    public Status getStatus() { return status; }
}
```

Key annotations:

| Annotation | Purpose |
|------------|---------|
| `@Entity` | mark a class as persistent |
| `@Table(name=...)` | specify the table name |
| `@Id` | mark the primary key field |
| `@GeneratedValue` | how the PK is generated (`IDENTITY`, `SEQUENCE`, `AUTO`) |
| `@Column` | column constraints (`nullable`, `length`, `unique`, `name`) |
| `@Enumerated(EnumType.STRING)` | persist enums by name (always prefer STRING) |
| `@Transient` | a field NOT persisted |
| `@Lob` | large object (long text / binary) |

> **Gotcha — JPA needs a no-arg constructor.** Hibernate creates entity instances via reflection and requires a (at least `protected`) no-argument constructor. Records can't be `@Entity` (they're immutable with no no-arg constructor) — use classes for entities, records for DTOs.

> **Gotcha — `@Enumerated` defaults to `ORDINAL`.** Without `EnumType.STRING`, enums are stored as integers (0, 1, 2). Reorder the enum later and existing data silently means something different. Always use `STRING`.

---

## IV. REPOSITORIES — CRUD FOR FREE

This is the magic of Spring Data. Declare an *interface* extending `JpaRepository<Entity, IdType>` and Spring generates the implementation — full CRUD, no code.

```java
package com.example.shop;

import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface ProductRepository extends JpaRepository<Product, Long> {
    // You write NOTHING here and already get:
    //   save(entity), saveAll(...), findById(id), findAll(), count(),
    //   existsById(id), deleteById(id), delete(entity) ...

    // DERIVED QUERIES — Spring parses the method NAME and writes the SQL:
    List<Product> findByName(String name);                       // WHERE name = ?
    List<Product> findByPriceLessThan(double max);               // WHERE price < ?
    List<Product> findByNameContainingIgnoreCase(String part);   // WHERE LOWER(name) LIKE %?%
    List<Product> findByStatusOrderByPriceDesc(Product.Status s);// WHERE status=? ORDER BY price DESC
    List<Product> findByStockGreaterThanEqual(int min);          // WHERE stock >= ?
    long countByStatus(Product.Status status);                   // SELECT COUNT(*) WHERE status=?
    boolean existsByName(String name);
}
```

Spring Data's **query derivation** understands keywords: `findBy`, `And`, `Or`, `Between`, `LessThan`, `GreaterThan`, `Like`, `Containing`, `IgnoreCase`, `OrderBy`, `In`, `IsNull`, `True`/`False`, `Top`/`First`. The method name *is* the query.

### Custom queries with @Query

When method names get unwieldy, write the query explicitly. JPQL queries operate on *entities and fields*, not tables and columns.

```java
import org.springframework.data.jpa.repository.*;
import org.springframework.data.repository.query.Param;
import java.util.List;

public interface ProductRepository extends JpaRepository<Product, Long> {

    // JPQL — note 'Product p' (the entity) and p.price (the field)
    @Query("SELECT p FROM Product p WHERE p.price BETWEEN :min AND :max")
    List<Product> inPriceRange(@Param("min") double min, @Param("max") double max);

    // Native SQL when you need database-specific features
    @Query(value = "SELECT * FROM products WHERE stock_qty = 0", nativeQuery = true)
    List<Product> findOutOfStock();

    // Modifying query (UPDATE/DELETE) needs @Modifying + a transaction
    @Modifying
    @Query("UPDATE Product p SET p.status = 'DISCONTINUED' WHERE p.stock = 0")
    int discontinueOutOfStock();
}
```

---

## V. A COMPLETE CRUD API

Wiring entity + repository + service + controller into a working REST API.

```java
// --- DTOs (records): the shapes the API exposes — never expose entities directly ---
package com.example.shop;

record ProductResponse(Long id, String name, double price, int stock, String status) {
    static ProductResponse from(Product p) {
        return new ProductResponse(p.getId(), p.getName(), p.getPrice(),
                                   p.getStock(), p.getStatus().name());
    }
}
record CreateProductRequest(String name, double price, int stock) {}
record UpdateProductRequest(String name, double price, int stock) {}
```

```java
// --- Service: business logic + transactions ---
package com.example.shop;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.*;

@Service
public class ProductService {
    private final ProductRepository repo;
    public ProductService(ProductRepository repo) { this.repo = repo; }

    @Transactional(readOnly = true)
    public List<ProductResponse> list() {
        return repo.findAll().stream().map(ProductResponse::from).toList();
    }

    @Transactional(readOnly = true)
    public ProductResponse get(Long id) {
        Product p = repo.findById(id)
            .orElseThrow(() -> new NoSuchElementException("Product " + id + " not found"));
        return ProductResponse.from(p);
    }

    @Transactional
    public ProductResponse create(CreateProductRequest req) {
        if (req.name() == null || req.name().isBlank())
            throw new IllegalArgumentException("Name is required");
        if (req.price() < 0) throw new IllegalArgumentException("Price cannot be negative");
        Product saved = repo.save(new Product(req.name().strip(), req.price(), req.stock()));
        return ProductResponse.from(saved);
    }

    @Transactional
    public ProductResponse update(Long id, UpdateProductRequest req) {
        Product p = repo.findById(id)
            .orElseThrow(() -> new NoSuchElementException("Product " + id + " not found"));
        p.setName(req.name());          // a managed entity: changes are flushed automatically
        p.setPrice(req.price());
        p.setStock(req.stock());
        return ProductResponse.from(p); // no explicit save() needed — see "dirty checking" below
    }

    @Transactional
    public void delete(Long id) {
        if (!repo.existsById(id))
            throw new NoSuchElementException("Product " + id + " not found");
        repo.deleteById(id);
    }
}
```

```java
// --- Controller: HTTP only ---
package com.example.shop;

import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/products")
public class ProductController {
    private final ProductService service;
    public ProductController(ProductService service) { this.service = service; }

    @GetMapping
    public List<ProductResponse> all() { return service.list(); }

    @GetMapping("/{id}")
    public ProductResponse one(@PathVariable Long id) { return service.get(id); }

    @PostMapping
    public ResponseEntity<ProductResponse> create(@RequestBody CreateProductRequest req) {
        return ResponseEntity.status(HttpStatus.CREATED).body(service.create(req));
    }

    @PutMapping("/{id}")
    public ProductResponse update(@PathVariable Long id, @RequestBody UpdateProductRequest req) {
        return service.update(id, req);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        service.delete(id);
        return ResponseEntity.noContent().build();
    }
}
```

```java
// --- Global error handling (from file 07) maps exceptions to status codes ---
package com.example.shop;

import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import java.util.NoSuchElementException;

@RestControllerAdvice
class ApiExceptionHandler {
    record ApiError(int status, String message) {}

    @ExceptionHandler(NoSuchElementException.class)
    ResponseEntity<ApiError> notFound(NoSuchElementException e) {
        return ResponseEntity.status(404).body(new ApiError(404, e.getMessage()));
    }
    @ExceptionHandler(IllegalArgumentException.class)
    ResponseEntity<ApiError> badRequest(IllegalArgumentException e) {
        return ResponseEntity.badRequest().body(new ApiError(400, e.getMessage()));
    }
}
```

That's a complete, layered, production-shaped CRUD API. Try it:

```bash
# Create
curl -X POST localhost:8080/api/products -H "Content-Type: application/json" \
     -d '{"name":"Notebook","price":4.99,"stock":120}'
# List
curl localhost:8080/api/products
# Get one
curl localhost:8080/api/products/1
# Update
curl -X PUT localhost:8080/api/products/1 -H "Content-Type: application/json" \
     -d '{"name":"Notebook XL","price":6.99,"stock":80}'
# Delete
curl -X DELETE localhost:8080/api/products/1
```

> **Dirty checking.** Inside a `@Transactional` method, an entity fetched via the repository is *managed*. Change its fields and Hibernate detects the change ("dirty checking") and writes an `UPDATE` automatically when the transaction commits — no explicit `save()` required. This surprises everyone the first time.

---

## VI. RELATIONSHIPS — THE HEART OF RELATIONAL DATA

Real domains have relationships: a customer has many orders; an order has many items. JPA maps these with four annotations.

### @OneToMany / @ManyToOne — the most common pairing

```java
package com.example.shop;

import jakarta.persistence.*;
import java.util.*;

@Entity
@Table(name = "customers")
public class Customer {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String name;

    // One customer → many orders.
    // mappedBy = "customer" → the Order side OWNS the foreign key (no extra column here).
    // cascade = ALL → saving/deleting a customer cascades to its orders.
    // orphanRemoval → removing an order from this list deletes it.
    @OneToMany(mappedBy = "customer", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Order> orders = new ArrayList<>();

    protected Customer() {}
    public Customer(String name) { this.name = name; }

    // Helper keeps BOTH sides of the relationship in sync — always do this
    public void addOrder(Order order) {
        orders.add(order);
        order.setCustomer(this);
    }
    public Long getId() { return id; }
    public String getName() { return name; }
    public List<Order> getOrders() { return orders; }
}
```

```java
package com.example.shop;

import jakarta.persistence.*;
import java.time.Instant;

@Entity
@Table(name = "orders")
public class Order {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private Instant placedAt = Instant.now();
    private double total;

    // Many orders → one customer. This side owns the FK column "customer_id".
    // FetchType.LAZY → don't load the customer until accessed (the right default).
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "customer_id")
    private Customer customer;

    protected Order() {}
    public Order(double total) { this.total = total; }

    public void setCustomer(Customer c) { this.customer = c; }
    public Customer getCustomer() { return customer; }
    public Long getId() { return id; }
    public double getTotal() { return total; }
}
```

### The four relationship types

| Annotation | Meaning | Example |
|------------|---------|---------|
| `@OneToOne` | one ↔ one | User ↔ Profile |
| `@OneToMany` | one → many | Customer → Orders |
| `@ManyToOne` | many → one | Order → Customer (owns the FK) |
| `@ManyToMany` | many ↔ many | Student ↔ Course (needs a join table) |

```java
// @ManyToMany with an explicit join table
@Entity
class Student {
    @Id @GeneratedValue Long id;

    @ManyToMany
    @JoinTable(name = "student_course",
        joinColumns = @JoinColumn(name = "student_id"),
        inverseJoinColumns = @JoinColumn(name = "course_id"))
    private Set<Course> courses = new HashSet<>();
}
```

> **Gotcha — `EAGER` fetching kills performance.** `@ManyToOne` defaults to `EAGER` (loads the relation immediately), `@OneToMany` to `LAZY`. Prefer **`LAZY` everywhere** and load relations explicitly when needed. Eager loading silently fires extra queries and drags in half your database.

> **Gotcha — the N+1 query problem.** Looping over 100 orders and accessing `order.getCustomer()` on each (lazily) fires 1 query for the orders + 100 for the customers = 101 queries. Fix with a **fetch join**: `@Query("SELECT o FROM Order o JOIN FETCH o.customer")` loads everything in one query. This is the most common JPA performance bug — watch your SQL logs.

> **Gotcha — bidirectional `toString`/`equals` infinite loop.** If `Customer.toString()` prints its `orders` and `Order.toString()` prints its `customer`, they recurse forever (StackOverflowError). Exclude the back-reference from `toString`/`equals`/`hashCode`.

---

## VII. TRANSACTIONS

A **transaction** groups operations so they all succeed or all roll back — atomicity. `@Transactional` makes a method run in one transaction; if it throws, everything rolls back.

```java
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class TransferService {
    private final AccountRepository accounts;
    public TransferService(AccountRepository accounts) { this.accounts = accounts; }

    @Transactional   // both updates commit together, or neither does
    public void transfer(Long fromId, Long toId, double amount) {
        Account from = accounts.findById(fromId).orElseThrow();
        Account to   = accounts.findById(toId).orElseThrow();

        from.withdraw(amount);   // if this succeeds...
        // imagine an exception here →
        to.deposit(amount);      // ...but this fails: the withdrawal is ROLLED BACK too

        // dirty checking flushes both on commit; no explicit save() needed
    }
}
```

> **Gotcha — `@Transactional` only works through Spring proxies.** Calling a `@Transactional` method *from another method in the same class* bypasses the proxy, so the annotation is ignored. Put transactional methods on a separate bean, or call them through the injected reference. Also: by default Spring rolls back only on **unchecked** exceptions — checked exceptions don't roll back unless you set `rollbackFor`.

> Use `@Transactional(readOnly = true)` on pure reads — it lets the database and Hibernate optimize (no dirty-checking overhead).

---

## VIII. PAGINATION AND SORTING

Never return a million rows. Spring Data has paging built in.

```java
import org.springframework.data.domain.*;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/products")
class ProductPageController {
    private final ProductRepository repo;
    ProductPageController(ProductRepository repo) { this.repo = repo; }

    // GET /api/products/page?page=0&size=20&sortBy=price
    @GetMapping("/page")
    public Page<Product> page(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size,
            @RequestParam(defaultValue = "id") String sortBy) {
        Pageable pageable = PageRequest.of(page, size, Sort.by(sortBy).descending());
        return repo.findAll(pageable);   // returns content + total pages + total elements
    }
}
```

A `Page` response includes the content plus metadata: `totalElements`, `totalPages`, `number`, `size` — everything a paginated UI needs.

---

## IX. SWITCHING TO A REAL DATABASE (PostgreSQL)

The beauty of JPA: your entities and repositories don't change. Swap the driver and connection settings.

```xml
<!-- Replace the H2 dependency with PostgreSQL -->
<dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
    <scope>runtime</scope>
</dependency>
```

```properties
# application-prod.properties
spring.datasource.url=jdbc:postgresql://localhost:5432/shop
spring.datasource.username=${DB_USER}          # from environment — never hardcode
spring.datasource.password=${DB_PASSWORD}
spring.jpa.database-platform=org.hibernate.dialect.PostgreSQLDialect
spring.jpa.hibernate.ddl-auto=validate         # production: validate, don't auto-alter
```

Run a local Postgres with Docker in seconds:

```bash
docker run --name shop-db -e POSTGRES_DB=shop -e POSTGRES_PASSWORD=secret \
           -p 5432:5432 -d postgres:16
```

> **In production, manage schema with migrations.** Add **Flyway** (`spring-boot-starter` picks it up) and put versioned SQL in `src/main/resources/db/migration/V1__init.sql`. Migrations are reviewable, repeatable, and safe — unlike letting Hibernate guess.

---

## X. SEEDING DATA AND VERIFYING

A `CommandLineRunner` bean runs once at startup — handy for seeding dev data.

```java
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.SpringApplication;

@SpringBootApplication
public class ShopApplication {
    public static void main(String[] args) {
        SpringApplication.run(ShopApplication.class, args);
    }

    @Bean
    CommandLineRunner seed(ProductRepository repo) {
        return args -> {
            repo.save(new Product("Pen", 1.50, 200));
            repo.save(new Product("Notebook", 4.99, 120));
            repo.save(new Product("Backpack", 39.95, 30));
            System.out.println("Seeded " + repo.count() + " products");
        };
    }
}
```

Test the data layer with `@DataJpaTest` (spins up just JPA + an in-memory DB):

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.junit.jupiter.api.Test;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;

@DataJpaTest
class ProductRepositoryTest {
    @Autowired ProductRepository repo;

    @Test
    void findsByNameContaining() {
        repo.save(new Product("Red Pen", 1.0, 10));
        repo.save(new Product("Blue Pen", 1.2, 5));
        repo.save(new Product("Eraser", 0.5, 20));

        List<Product> pens = repo.findByNameContainingIgnoreCase("pen");
        assertEquals(2, pens.size());
    }
}
```

---

## XI. COMMON PITFALLS

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| `ddl-auto=update`/`create` in prod | Schema corruption / data loss | `validate`/`none` + Flyway/Liquibase |
| EAGER fetching | Loads too much, slow | Default to `LAZY`, fetch joins when needed |
| N+1 queries | 100s of queries per request | `JOIN FETCH` / `@EntityGraph` |
| Returning entities from controllers | Leaks internals; lazy-init exceptions | Map to DTOs/records |
| `@Transactional` self-invocation | Annotation silently ignored | Call via another bean |
| Enum stored as `ORDINAL` | Reordering breaks data | `@Enumerated(EnumType.STRING)` |
| Bidirectional `toString`/`equals` | StackOverflowError | Exclude the back-reference |
| Not syncing both sides of a relation | Stale in-memory state | Use add/remove helper methods |
| Hardcoded DB credentials | Security leak | Env vars / secrets manager |
| No pagination on list endpoints | Huge payloads, OOM | `Pageable` + `Page<T>` |
| Using a `record` as an `@Entity` | Won't work (no no-arg ctor) | Class for entities, record for DTOs |

---

## 🧠 KEY TAKEAWAYS

- **JPA** is the ORM spec, **Hibernate** the implementation, **Spring Data JPA** the boilerplate-killer on top. ORM maps objects↔rows so you work with Java, not SQL.
- **`@Entity`** classes map to tables (need a no-arg constructor and `@Id`/`@GeneratedValue`); use `@Enumerated(STRING)` for enums.
- Extending **`JpaRepository`** gives full CRUD free; **derived query methods** turn method names into SQL, and **`@Query`** handles the complex cases.
- Keep the layered shape: **Entity → Repository → Service (`@Transactional`) → Controller**, and **always return DTOs**, never entities.
- Model relationships with **`@OneToMany`/`@ManyToOne`/`@ManyToMany`**; default to **`LAZY`** and beware the **N+1 problem** (fix with fetch joins).
- **`@Transactional`** gives all-or-nothing atomicity (mind self-invocation and the unchecked-only rollback default); **dirty checking** auto-saves managed entities.
- Use **pagination** for list endpoints, externalize DB config, and manage production schema with **migrations** — never `ddl-auto` in prod.

---

**Prev:** [`07-Spring-Boot-Essentials.md`](./07-Spring-Boot-Essentials.md) · **Next:** — you've finished Java Mastery! · **Index:** [`00-Index.md`](./00-Index.md)

---

> 🎓 **You've completed the Java Mastery track.** You can now write idiomatic Java, design with OOP, wield collections, generics, and streams, handle errors and I/O, reason about concurrency, and build a database-backed REST API with Spring Boot. Next up in the codex: pair this with [`08-SQL-DATABASES`](../08-SQL-DATABASES/) to deepen the data layer, then [`11-FULLSTACK-ENGINEERING`](../11-FULLSTACK-ENGINEERING/) for auth, testing, and deployment.
