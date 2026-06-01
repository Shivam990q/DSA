# 🗜️ Compression as Discovery

> *"To compress is to understand. The shortest description of data is its deepest truth."*

---

## I. THE CORE IDEA

**Kolmogorov complexity**: the complexity of an object = length of the shortest program that produces it.

A string like "010101...01" (1000 times) is *simple*: "print '01' 1000 times" — short program.

A random 1000-bit string is *complex*: no shorter description than itself.

**Insight for algorithm design**: finding a pattern = finding a shorter description = compression = understanding.

---

## II. COMPRESSION AND PATTERN RECOGNITION

When you "see a pattern" in a problem, you're *compressing* it:
- "These 1000 cases all follow the formula f(n) = n(n+1)/2." → 1000 cases compressed to one formula.
- "This sequence is Fibonacci." → infinite sequence compressed to a recurrence.

**The grandmaster compresses problems into patterns. The amateur stores them uncompressed.**

---

## III. COMPRESSION ALGORITHMS (the literal kind)

### Run-Length Encoding (RLE)
"aaabbbcccc" → "a3b3c4". Compresses repetition.

### Huffman Coding
Variable-length codes; frequent symbols get short codes. Optimal prefix code.

### LZ77 / LZ78 / LZW
Replace repeated substrings with references to earlier occurrences. Basis of gzip, PNG, GIF.

### Burrows-Wheeler Transform (BWT)
Reversible permutation that groups similar contexts. Basis of bzip2; also underlies FM-index for compressed search.

### Arithmetic coding
Encode entire message as a single fractional number. Approaches entropy bound.

---

## IV. THE ENTROPY BOUND

**Shannon's theorem**: you cannot compress data below its entropy H = −Σ p(x) log p(x) bits per symbol (on average, losslessly).

This is a *lower bound* on compression — analogous to algorithmic lower bounds.

---

## V. COMPRESSION-DRIVEN DATA STRUCTURES

Modern structures exploit compression:
- **FM-index**: searchable compressed text (used in genomics, e.g., Bowtie aligner)
- **Compressed suffix arrays**: substring search in compressed space
- **Succinct data structures**: store trees/graphs in near-information-theoretic-minimum space while supporting queries
- **Wavelet trees**: compressed rank/select

---

## VI. THE DEEP CONNECTION: LEARNING = COMPRESSION

Machine learning, at its core, is compression:
- A model that generalizes is one that *compressed* the training data into rules.
- Overfitting = memorizing (no compression).
- The best model is the shortest one that explains the data (Occam's razor, MDL principle).

**Minimum Description Length (MDL)**: choose the hypothesis that minimizes (model size + data-given-model size).

---

## VII. COMPRESSION IN PROBLEM SOLVING

When stuck on a problem:
1. **Compute many cases.** Look for the shortest rule that generates them.
2. **The shortest rule IS the insight.**

> Example: count binary strings of length n without "11".
> Cases: 2, 3, 5, 8, 13 → compress to "Fibonacci" → recurrence f(n) = f(n-1) + f(n-2).

The act of compressing data into a rule = discovering the algorithm.

---

## VIII. EXERCISES

1. Compute the entropy of a fair coin, a biased coin (p=0.9), a fair die.
2. Implement run-length encoding and decoding.
3. Build a Huffman tree for given frequencies; compute average code length.
4. Find the shortest rule generating: 1, 4, 9, 16, 25, ...
5. Find the recurrence for: 1, 1, 2, 4, 8, 16, 31, ... (sum of last few terms)

---

## IX. RECOMMENDED READING

- **Cover & Thomas**, *Elements of Information Theory* ⭐
- **Li & Vitányi**, *An Introduction to Kolmogorov Complexity*
- **MacKay**, *Information Theory, Inference, and Learning Algorithms* (free)
- **Navarro**, *Compact Data Structures*

---

**→ Next:** [`07-Reading-Research-Papers.md`](./07-Reading-Research-Papers.md)
