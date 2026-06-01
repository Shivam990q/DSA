# 🖥️ Operating Systems — Interview Prep

> The most-asked core subject after DBMS. Master the concepts + crisp answers.

---

## THE SYLLABUS (interview-relevant)
1. **Processes & Threads** — PCB, process states, context switching, thread vs process
2. **CPU Scheduling** — FCFS, SJF, SRTF, Round Robin, Priority, MLFQ; preemptive vs non-preemptive
3. **Synchronization** — race conditions, critical section, mutex, semaphore, monitors
4. **Classic problems** — producer-consumer, readers-writers, dining philosophers
5. **Deadlocks** — 4 conditions (mutual exclusion, hold-and-wait, no preemption, circular wait), prevention, avoidance (Banker's), detection
6. **Memory Management** — paging, segmentation, virtual memory, page faults
7. **Page Replacement** — FIFO, LRU, Optimal, Clock; Belady's anomaly
8. **File Systems** — allocation methods, directory structures, inodes
9. **Disk Scheduling** — FCFS, SSTF, SCAN, C-SCAN, LOOK

---

## THE TOP 20 INTERVIEW QUESTIONS
1. Process vs Thread?
2. What is a context switch?
3. What is a deadlock? The 4 necessary conditions?
4. Difference between mutex and semaphore?
5. What is virtual memory? How does paging work?
6. What is thrashing?
7. Explain LRU page replacement.
8. What is a race condition? How to prevent it?
9. Preemptive vs non-preemptive scheduling?
10. What is the critical section problem?
11. Explain the producer-consumer problem.
12. What is a zombie process? Orphan process?
13. What is the difference between paging and segmentation?
14. What is Belady's anomaly?
15. What is a page fault? What happens on one?
16. User mode vs kernel mode?
17. What is a system call? Examples?
18. Internal vs external fragmentation?
19. What is the Banker's algorithm?
20. Multiprogramming vs multitasking vs multiprocessing?

---

## CRISP ANSWER EXAMPLES
**Process vs Thread**: A process is an independent program in execution with its own memory space. A thread is the smallest unit of execution within a process; threads of the same process share memory (heap, code) but have their own stack and registers. Threads are lighter (cheaper context switch).

**Deadlock 4 conditions**: Mutual exclusion, Hold and wait, No preemption, Circular wait. All four must hold simultaneously; breaking any one prevents deadlock.

---

## RESOURCES
### YouTube ⭐
- **[Gate Smashers](https://www.youtube.com/@GateSmashers)** — complete OS playlist (placement gold)
- **[Neso Academy](https://www.youtube.com/@nesoacademy)** — OS playlist
- **[Knowledge Gate](https://www.youtube.com/@KnowledgeGate.in)** — OS in depth

### Written
- **[GeeksforGeeks](https://www.geeksforgeeks.org)** — OS Last Minute Notes + interview questions ⭐
- **[InterviewBit](https://www.interviewbit.com)** — OS section

### Books / Free
- **[OSTEP](https://pages.cs.wisc.edu/~remzi/OSTEP/) (Operating Systems: Three Easy Pieces)** — FREE, excellent ⭐
- **Operating System Concepts** (Silberschatz) — the "dinosaur book"

---

## PREP PLAN (5 days)
- Day 1: Processes, threads, scheduling
- Day 2: Synchronization, classic problems
- Day 3: Deadlocks
- Day 4: Memory management, paging, page replacement
- Day 5: File systems, disk scheduling + revise top 20 Qs

---

**→ Next:** [`02-DBMS.md`](./02-DBMS.md)
