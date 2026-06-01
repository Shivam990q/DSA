# Multiply Strings

**Platform**: LeetCode 43 · **Difficulty**: Medium · **Topics**: Math, String, Simulation · **Pattern**: Schoolbook digit convolution

---

## 📜 Problem Statement

Given two non-negative integers `num1` and `num2` represented as strings, return the product of `num1` and `num2`, also represented as a string.

**Note**: You must not use any built-in BigInteger library or convert the inputs to integer directly.

### Examples

**Example 1:**
```
Input:  num1 = "2", num2 = "3"
Output: "6"
```

**Example 2:**
```
Input:  num1 = "123", num2 = "456"
Output: "56088"
```

**Example 3:**
```
Input:  num1 = "0", num2 = "99999"
Output: "0"
```

### Constraints
```
1 <= num1.length, num2.length <= 200
num1 and num2 consist of digits only.
Both num1 and num2 do not contain any leading zero, except the number 0 itself.
```

---

## 🧠 Understanding the problem

We're forbidden from converting to native integers (the numbers can be 200 digits — far beyond 64-bit). So we reimplement **long multiplication** by hand.

The positional key insight: when you multiply digit `num1[i]` by digit `num2[j]`, the product belongs at decimal positions `i + j + 1` (the units of that partial product) and `i + j` (the carry). If we index from the **left** (so `i = 0` is the most significant digit), then a number of length `m × n` has at most `m + n` digits, and the contribution of `(i, j)` lands in a result array `prod[i + j]` and `prod[i + j + 1]`.

So: allocate `prod` of size `m + n`, accumulate every digit-by-digit product into the right two slots (carrying as we go), then convert the digit array back to a string, stripping leading zeros.

---

## Approach 1 — Schoolbook digit-by-digit (optimal) ⭐

### Intuition
For each pair of digits, add the product into `prod[i+j+1]`, push the overflow into `prod[i+j]`. Process from the least significant digits so carries flow naturally.

### Algorithm
1. If either input is `"0"` → return `"0"`.
2. `prod` = array of `m + n` zeros.
3. For `i` from `m-1` down to `0`, for `j` from `n-1` down to `0`:
   - `mul = (num1[i]-'0') * (num2[j]-'0')`.
   - `sum = mul + prod[i+j+1]`.
   - `prod[i+j+1] = sum % 10`; `prod[i+j] += sum / 10`.
4. Build the string from `prod`, skipping leading zeros.

### Dry run on `num1="123", num2="456"`
```
prod size 6. Accumulate all 9 digit products into positions i+j, i+j+1
with carrying. Final digit array → 0,5,6,0,8,8 → strip leading 0 → "56088"  ✓
```

### Code
```cpp
string multiply(string num1, string num2) {
    if (num1 == "0" || num2 == "0") return "0";
    int m = num1.size(), n = num2.size();
    vector<int> prod(m + n, 0);
    for (int i = m - 1; i >= 0; i--) {
        for (int j = n - 1; j >= 0; j--) {
            int mul = (num1[i] - '0') * (num2[j] - '0');
            int p1 = i + j, p2 = i + j + 1;
            int sum = mul + prod[p2];
            prod[p2] = sum % 10;
            prod[p1] += sum / 10;
        }
    }
    string res;
    for (int d : prod)
        if (!(res.empty() && d == 0)) res += char(d + '0');
    return res.empty() ? "0" : res;
}
```
```java
public String multiply(String num1, String num2) {
    if (num1.equals("0") || num2.equals("0")) return "0";
    int m = num1.length(), n = num2.length();
    int[] prod = new int[m + n];
    for (int i = m - 1; i >= 0; i--) {
        for (int j = n - 1; j >= 0; j--) {
            int mul = (num1.charAt(i) - '0') * (num2.charAt(j) - '0');
            int p1 = i + j, p2 = i + j + 1;
            int sum = mul + prod[p2];
            prod[p2] = sum % 10;
            prod[p1] += sum / 10;
        }
    }
    StringBuilder sb = new StringBuilder();
    for (int d : prod)
        if (!(sb.length() == 0 && d == 0)) sb.append((char) (d + '0'));
    return sb.length() == 0 ? "0" : sb.toString();
}
```
```python
def multiply(num1, num2):
    if num1 == "0" or num2 == "0":
        return "0"
    m, n = len(num1), len(num2)
    prod = [0] * (m + n)
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            mul = (ord(num1[i]) - 48) * (ord(num2[j]) - 48)
            p1, p2 = i + j, i + j + 1
            total = mul + prod[p2]
            prod[p2] = total % 10
            prod[p1] += total // 10
    res = "".join(map(str, prod)).lstrip("0")
    return res or "0"
```

### Complexity
- **Time**: O(m·n) — every digit pair processed once.
- **Space**: O(m + n) for the product array.

### Verdict
**Optimal** for this problem size. The `i+j` / `i+j+1` positional rule is the entire trick; once you trust it, the carries take care of themselves.

---

## Approach 2 — Sum of shifted partial products

### Intuition
The way you'd do it on paper: multiply `num1` by each digit of `num2`, shift left by the digit's position, and add all partial products together. It's the same arithmetic, organized as "multiply then add strings."

### Algorithm
1. For each digit `j` of `num2` (from the right), compute `num1 × digit` as a string, append `(n-1-j)` trailing zeros.
2. String-add all partial products.

### Dry run on `num1="123", num2="45"`
```
123 × 5 = 615
123 × 4 = 492, shift one zero → 4920
615 + 4920 = 5535  ✓
```

### Code
```cpp
class Solution {
    string addStrings(string a, string b) {
        int i = a.size() - 1, j = b.size() - 1, carry = 0;
        string res;
        while (i >= 0 || j >= 0 || carry) {
            int s = carry;
            if (i >= 0) s += a[i--] - '0';
            if (j >= 0) s += b[j--] - '0';
            res += char(s % 10 + '0');
            carry = s / 10;
        }
        reverse(res.begin(), res.end());
        return res;
    }
public:
    string multiply(string num1, string num2) {
        if (num1 == "0" || num2 == "0") return "0";
        string result = "0";
        int n = num2.size();
        for (int j = n - 1; j >= 0; j--) {
            int d = num2[j] - '0', carry = 0;
            string partial;
            for (int i = num1.size() - 1; i >= 0; i--) {
                int s = (num1[i] - '0') * d + carry;
                partial += char(s % 10 + '0');
                carry = s / 10;
            }
            if (carry) partial += char(carry + '0');
            reverse(partial.begin(), partial.end());
            partial += string(n - 1 - j, '0');     // shift
            result = addStrings(result, partial);
        }
        return result;
    }
};
```
```java
class Solution {
    public String multiply(String num1, String num2) {
        if (num1.equals("0") || num2.equals("0")) return "0";
        String result = "0";
        int n = num2.length();
        for (int j = n - 1; j >= 0; j--) {
            int d = num2.charAt(j) - '0', carry = 0;
            StringBuilder partial = new StringBuilder();
            for (int i = num1.length() - 1; i >= 0; i--) {
                int s = (num1.charAt(i) - '0') * d + carry;
                partial.append((char) (s % 10 + '0'));
                carry = s / 10;
            }
            if (carry > 0) partial.append((char) (carry + '0'));
            partial.reverse();
            for (int z = 0; z < n - 1 - j; z++) partial.append('0');  // shift
            result = addStrings(result, partial.toString());
        }
        return result;
    }
    private String addStrings(String a, String b) {
        int i = a.length() - 1, j = b.length() - 1, carry = 0;
        StringBuilder res = new StringBuilder();
        while (i >= 0 || j >= 0 || carry > 0) {
            int s = carry;
            if (i >= 0) s += a.charAt(i--) - '0';
            if (j >= 0) s += b.charAt(j--) - '0';
            res.append((char) (s % 10 + '0'));
            carry = s / 10;
        }
        return res.reverse().toString();
    }
}
```
```python
def multiply(num1, num2):
    if num1 == "0" or num2 == "0":
        return "0"
    def add_strings(a, b):
        i, j, carry = len(a) - 1, len(b) - 1, 0
        res = []
        while i >= 0 or j >= 0 or carry:
            s = carry
            if i >= 0:
                s += ord(a[i]) - 48; i -= 1
            if j >= 0:
                s += ord(b[j]) - 48; j -= 1
            res.append(str(s % 10))
            carry = s // 10
        return "".join(reversed(res))
    result = "0"
    n = len(num2)
    for j in range(n - 1, -1, -1):
        d = ord(num2[j]) - 48
        carry = 0
        partial = []
        for i in range(len(num1) - 1, -1, -1):
            s = (ord(num1[i]) - 48) * d + carry
            partial.append(str(s % 10))
            carry = s // 10
        if carry:
            partial.append(str(carry))
        partial_str = "".join(reversed(partial)) + "0" * (n - 1 - j)
        result = add_strings(result, partial_str)
    return result
```

### Complexity
- **Time**: O(m·n) — plus the string additions, still O(m·n) overall.
- **Space**: O(m + n).

### Verdict
More faithful to hand multiplication but wordier (needs a string-add helper). The digit-array convolution (Approach 1) is shorter and less error-prone — prefer it.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Digit convolution | **O(mn)** | O(m+n) | shortest, positional trick ⭐ |
| Shifted partial sums | O(mn) | O(m+n) | mirrors paper method, more code |

For very large inputs, FFT-based multiplication achieves O(k log k), but it's overkill for `k ≤ 200` and never expected in an interview.

---

## 🧪 Edge cases & pitfalls
- **Either input `"0"`** → return `"0"` early; otherwise you'd emit a string of zeros like `"00"`.
- **Leading zeros in the result** → strip them, but keep one digit if the whole thing is zero.
- **Max size** → `200 × 200` digits → up to 400-digit result; the `m + n` array is exactly right.
- **Pitfall — position indices**: mixing up `i+j` and `i+j+1` shifts everything by one decimal place. Remember: the *units* of `num1[i]*num2[j]` go to `i+j+1`.
- **Pitfall — forgetting to add the existing `prod[p2]`** before taking `% 10`, which loses accumulated value.

---

## 🔗 Related problems
- **Add Strings** (LC 415) — the string-addition helper alone.
- **Add Binary** (LC 67) — base-2 version.
- **Plus One** (LC 66) — carry propagation (later in this set).
- **Pow(x, n)** (LC 50) — another numeric/structure problem (previous).

---

**→ Next:** [`06-Happy-Number.md`](./06-Happy-Number.md) | **Prev:** [`04-Pow-X-N.md`](./04-Pow-X-N.md) | [Problem set index](./00-Index.md)
