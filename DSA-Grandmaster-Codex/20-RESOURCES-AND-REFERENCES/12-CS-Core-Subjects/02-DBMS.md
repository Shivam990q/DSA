# 🗄️ DBMS — Interview Prep

> The most-asked core subject. Normalization + transactions + SQL appear in almost every placement interview.

---

## THE SYLLABUS (interview-relevant)
1. **ER Model** — entities, attributes, relationships, cardinality
2. **Relational Model** — keys (primary, candidate, super, foreign, composite)
3. **Normalization** ⭐ — 1NF, 2NF, 3NF, BCNF; functional dependencies; anomalies
4. **SQL** ⭐ — DDL/DML/DCL, joins, subqueries, aggregate functions, GROUP BY, HAVING
5. **Transactions** — ACID properties, states
6. **Concurrency Control** — locks, 2-phase locking, deadlocks, isolation levels
7. **Indexing** — B-tree, B+ tree, hashing, clustered vs non-clustered
8. **Joins** — inner, outer (left/right/full), cross, self
9. **Recovery** — logging, checkpoints

---

## THE TOP 20 INTERVIEW QUESTIONS
1. What is normalization? Why normalize?
2. Explain 1NF, 2NF, 3NF, BCNF.
3. What are ACID properties?
4. Primary key vs unique key vs foreign key?
5. Clustered vs non-clustered index?
6. What is a transaction? Its states?
7. DELETE vs TRUNCATE vs DROP?
8. Inner join vs outer join?
9. What is a deadlock in DBMS? How is it handled?
10. What are isolation levels? (Read uncommitted → Serializable)
11. What is an index? How does it speed up queries?
12. What is denormalization? When is it used?
13. WHERE vs HAVING?
14. What is a candidate key vs super key?
15. What is referential integrity?
16. What is a view? Materialized view?
17. What is 2-phase locking?
18. What is a stored procedure vs trigger?
19. What is a functional dependency?
20. SQL vs NoSQL — when to use which?

---

## CRISP ANSWER EXAMPLES
**ACID**: Atomicity (all-or-nothing), Consistency (valid state to valid state), Isolation (concurrent transactions don't interfere), Durability (committed changes persist despite failures).

**3NF**: A table is in 3NF if it's in 2NF AND no non-key attribute is transitively dependent on the primary key (no non-key attribute depends on another non-key attribute).

---

## RESOURCES
### YouTube ⭐
- **[Gate Smashers](https://www.youtube.com/@GateSmashers)** — complete DBMS playlist
- **Jenny's Lectures** — DBMS
- **[Knowledge Gate](https://www.youtube.com/@KnowledgeGate.in)** — DBMS in depth

### Written
- **[GeeksforGeeks](https://www.geeksforgeeks.org)** — DBMS Last Minute Notes + interview questions ⭐
- **[InterviewBit](https://www.interviewbit.com)** — DBMS section

### Books / Free
- **Database System Concepts** (Silberschatz, Korth, Sudarshan)
- **GeeksforGeeks DBMS tutorial**

---

## SQL PRACTICE
See [`06-SQL-Practice.md`](./06-SQL-Practice.md) — [LeetCode](https://leetcode.com) SQL, [HackerRank](https://www.hackerrank.com) SQL, etc.

---

## PREP PLAN (5 days)
- Day 1: ER model, keys, relational model
- Day 2: Normalization (the big one) ⭐
- Day 3: SQL + joins + practice
- Day 4: Transactions, ACID, concurrency, isolation
- Day 5: Indexing + revise top 20 Qs

---

**→ Next:** [`03-Computer-Networks.md`](./03-Computer-Networks.md)
