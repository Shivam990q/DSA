# 🗃️ SQL Practice — For Coding + Data Roles

> SQL appears in DBMS interviews, data engineering/analyst roles, and many backend interviews.

---

## CORE SQL TO MASTER
- SELECT, WHERE, ORDER BY, LIMIT
- Aggregate functions: COUNT, SUM, AVG, MIN, MAX
- GROUP BY, HAVING
- JOINs: INNER, LEFT, RIGHT, FULL, SELF, CROSS
- Subqueries (correlated & non-correlated)
- Window functions: ROW_NUMBER, RANK, DENSE_RANK, LEAD, LAG, partitioning ⭐
- CTEs (WITH clause), recursive CTEs
- CASE statements
- Set operations: UNION, INTERSECT, EXCEPT
- DDL: CREATE, ALTER, DROP; DML: INSERT, UPDATE, DELETE

---

## PRACTICE PLATFORMS ⭐
- **[LeetCode](https://leetcode.com) SQL** (Database problems + SQL 50 study plan) ⭐
- **[HackerRank](https://www.hackerrank.com) SQL** (SQL track, basic → advanced) ⭐
- **[StrataScratch](https://www.stratascratch.com)** — real company SQL questions (data roles) ⭐
- **[DataLemur](https://datalemur.com)** — SQL interview questions (by Nick Singh)
- **[SQLZoo](https://sqlzoo.net)** — interactive tutorial
- **Mode SQL Tutorial** — analytics-focused
- **PostgreSQL Exercises** (pgexercises.com)

---

## THE TOP SQL INTERVIEW PATTERNS
1. **Nth highest salary** (window function or subquery)
2. **Duplicate detection** (GROUP BY + HAVING COUNT > 1)
3. **Department-wise top earner** (window + PARTITION BY)
4. **Self-join** (employee-manager, consecutive rows)
5. **Running totals** (window with frame)
6. **Date-based queries** (last N days, month-over-month)
7. **Pivot / conditional aggregation** (CASE + SUM)
8. **Gaps and islands** (consecutive sequences)

---

## CLASSIC PROBLEMS
- Second/Nth highest salary (LeetCode 176, 177)
- Department highest salary (LeetCode 184)
- Consecutive numbers (LeetCode 180)
- Rank scores (LeetCode 178)
- Trips and users (LeetCode 262)
- Employees earning more than managers (LeetCode 181)
- Duplicate emails (LeetCode 182)

---

## PREP PLAN (1 week for interviews)
- Day 1-2: SELECT, WHERE, GROUP BY, HAVING, aggregates
- Day 3: All JOIN types + self-join
- Day 4: Subqueries + CTEs
- Day 5: Window functions ⭐ (the differentiator)
- Day 6-7: LeetCode SQL 50 + HackerRank SQL track

---

## THE WINDOW FUNCTION EMPHASIS
Window functions (ROW_NUMBER, RANK, LEAD/LAG, PARTITION BY) separate beginners from strong candidates. Many "hard" SQL problems become easy with them. Master these.

---

**→ Back to:** [`00-Index.md`](./00-Index.md)
