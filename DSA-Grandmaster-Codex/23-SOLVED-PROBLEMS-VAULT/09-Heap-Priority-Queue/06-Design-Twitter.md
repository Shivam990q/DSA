# Design Twitter

**Platform**: LeetCode 355 · **Difficulty**: Medium · **Topics**: Hash Table, Linked List, Design, Heap (Priority Queue) · **Pattern**: Merge-K-recent with a max-heap

---

## 📜 Problem Statement

Design a simplified version of Twitter where users can post tweets, follow/unfollow another user, and is able to see the `10` most recent tweets in the user's news feed.

Implement the `Twitter` class:

- `Twitter()` Initializes your twitter object.
- `void postTweet(int userId, int tweetId)` Composes a new tweet with ID `tweetId` by the user `userId`. Each call to this function will be made with a unique `tweetId`.
- `List<Integer> getNewsFeed(int userId)` Retrieves the `10` most recent tweet IDs in the user's news feed. Each item in the news feed must be posted by users who the user followed or by the user themselves. Tweets must be **ordered from most recent to least recent**.
- `void follow(int followerId, int followeeId)` The user with ID `followerId` started following the user with ID `followeeId`.
- `void unfollow(int followerId, int followeeId)` The user with ID `followerId` started unfollowing the user with ID `followeeId`.

### Examples

**Example 1:**
```
Input:
["Twitter","postTweet","getNewsFeed","follow","postTweet","getNewsFeed","unfollow","getNewsFeed"]
[[],[1,5],[1],[1,2],[2,6],[1],[1,2],[1]]

Output:
[null,null,[5],null,null,[6,5],null,[5]]

Explanation:
Twitter twitter = new Twitter();
twitter.postTweet(1, 5);   // User 1 posts tweet id 5.
twitter.getNewsFeed(1);    // returns [5]. self tweet.
twitter.follow(1, 2);      // User 1 follows user 2.
twitter.postTweet(2, 6);   // User 2 posts tweet id 6.
twitter.getNewsFeed(1);    // returns [6, 5]. tweet 6 is more recent than 5.
twitter.unfollow(1, 2);    // User 1 unfollows user 2.
twitter.getNewsFeed(1);    // returns [5]. since 1 no longer follows 2.
```

**Example 2:**
```
Input:
["Twitter","postTweet","postTweet","postTweet","getNewsFeed"]
[[],[1,1],[1,2],[1,3],[1]]

Output:
[null,null,null,null,[3,2,1]]

Explanation: User 1's own three tweets, most recent first.
```

**Example 3:**
```
Input:
["Twitter","follow","getNewsFeed"]
[[],[1,2],[1]]

Output:
[null,null,[]]

Explanation: User 1 follows user 2, but nobody has tweeted, so the feed is empty.
```

### Constraints
```
1 <= userId, followerId, followeeId <= 500
0 <= tweetId <= 10^4
All the tweets have unique IDs.
At most 3 * 10^4 calls will be made to postTweet, getNewsFeed, follow, and unfollow.
```

---

## 🧠 Understanding the problem

This is a **design** problem: pick data structures so all four operations are efficient. The interesting one is `getNewsFeed`, which must merge tweets from the user and everyone they follow, then return the **10 most recent** by post time.

To order by recency we need a notion of time. A simple **global monotonic counter** (a clock that increments on each `postTweet`) stamps every tweet with a strictly increasing timestamp. Larger timestamp = more recent.

Now `getNewsFeed` becomes a **merge-K-lists by latest timestamp** problem: each relevant user has a time-ordered list of tweets, and we want the 10 with the largest timestamps across all of them. That's exactly what a **max-heap keyed by timestamp** does. Because we only need the top 10, we don't merge everything — we only ever pull 10 items out.

Data model:
- `tweets`: `userId → list of (timestamp, tweetId)`, appended in post order.
- `following`: `userId → set of followeeIds`.
- A global `clock`.

`follow`/`unfollow`/`postTweet` are O(1). The feed is the heap merge.

---

## Approach 1 — Collect all relevant tweets, sort, take 10 (baseline)

### Intuition
For the feed, gather every tweet from the user and their followees into one list, sort by timestamp descending, and slice the first 10.

### Algorithm
1. `postTweet`: append `(clock++, tweetId)` to the user's list.
2. `getNewsFeed`: union the user with their followees; collect all their tweets into a list; sort by timestamp descending; return the first 10 tweet IDs.
3. `follow`/`unfollow`: add/remove in the set.

### Dry run on Example 1 (final getNewsFeed(1) after unfollow)
```
clock progression: post(1,5)→t0; post(2,6)→t1
following[1] after unfollow = {} ; users = {1}
collect tweets of user 1 → [(t0,5)]
sort desc → [(t0,5)] → first 10 → [5]
```

### Code
```cpp
class Twitter {
    int clock = 0;
    unordered_map<int, vector<pair<int,int>>> tweets;   // user -> (time, tweetId)
    unordered_map<int, unordered_set<int>> following;
public:
    Twitter() {}
    void postTweet(int userId, int tweetId) {
        tweets[userId].push_back({clock++, tweetId});
    }
    vector<int> getNewsFeed(int userId) {
        vector<pair<int,int>> all;
        for (auto& t : tweets[userId]) all.push_back(t);
        for (int f : following[userId])
            for (auto& t : tweets[f]) all.push_back(t);
        sort(all.begin(), all.end(), [](auto& a, auto& b){ return a.first > b.first; });
        vector<int> res;
        for (int i = 0; i < (int)all.size() && i < 10; i++) res.push_back(all[i].second);
        return res;
    }
    void follow(int a, int b) { if (a != b) following[a].insert(b); }
    void unfollow(int a, int b) { following[a].erase(b); }
};
```
```java
class Twitter {
    private int clock = 0;
    private Map<Integer, List<int[]>> tweets = new HashMap<>();      // user -> [time, tweetId]
    private Map<Integer, Set<Integer>> following = new HashMap<>();

    public Twitter() {}
    public void postTweet(int userId, int tweetId) {
        tweets.computeIfAbsent(userId, x -> new ArrayList<>()).add(new int[]{clock++, tweetId});
    }
    public List<Integer> getNewsFeed(int userId) {
        List<int[]> all = new ArrayList<>(tweets.getOrDefault(userId, new ArrayList<>()));
        for (int f : following.getOrDefault(userId, new HashSet<>()))
            all.addAll(tweets.getOrDefault(f, new ArrayList<>()));
        all.sort((a, b) -> b[0] - a[0]);                            // time desc
        List<Integer> res = new ArrayList<>();
        for (int i = 0; i < all.size() && i < 10; i++) res.add(all.get(i)[1]);
        return res;
    }
    public void follow(int a, int b) {
        if (a != b) following.computeIfAbsent(a, x -> new HashSet<>()).add(b);
    }
    public void unfollow(int a, int b) {
        if (following.containsKey(a)) following.get(a).remove(b);
    }
}
```
```python
from collections import defaultdict

class Twitter:
    def __init__(self):
        self.clock = 0
        self.tweets = defaultdict(list)          # user -> [(time, tweetId)]
        self.following = defaultdict(set)

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.tweets[userId].append((self.clock, tweetId))
        self.clock += 1

    def getNewsFeed(self, userId: int):
        users = self.following[userId] | {userId}
        all_tweets = []
        for u in users:
            all_tweets.extend(self.tweets[u])
        all_tweets.sort(key=lambda t: t[0], reverse=True)
        return [tid for _, tid in all_tweets[:10]]

    def follow(self, a: int, b: int) -> None:
        if a != b:
            self.following[a].add(b)

    def unfollow(self, a: int, b: int) -> None:
        self.following[a].discard(b)
```

### Complexity
- **Time**: `getNewsFeed` O(M log M) where M = total tweets across the user and followees — sorts everything even though we keep only 10.
- **Space**: O(M) for the collected list.

### Verdict
Correct and simple. Wasteful in that it sorts *all* candidate tweets to keep just 10. The heap merge only ever touches the recent few per user.

---

## Approach 2 — Max-heap merge of recent tweets (optimal) ⭐

### Intuition
Each user's tweet list is already in time order, so the only candidates for the top 10 are each user's **last 10 tweets**. Push those tail tweets into a **max-heap keyed by timestamp** and pop 10. We never look at older tweets, and we never fully sort.

### Algorithm
1. `postTweet`: append `(clock++, tweetId)` to the user's list (O(1)).
2. `getNewsFeed`:
   - Build the candidate set: the user plus their followees.
   - For each, push only its **last 10** `(time, tweetId)` pairs into a max-heap.
   - Pop up to 10 times, collecting tweet IDs in order. Return them.
3. `follow`/`unfollow`: set insert/remove (O(1)).

### Dry run on Example 1, getNewsFeed(1) after follow(1,2) & post(2,6)
```
clock: post(1,5)→t0 ; post(2,6)→t1
users = {1, 2}
push last≤10 of user1: (t0,5) ; of user2: (t1,6)
max-heap by time → top (t1,6) then (t0,5)
pop 6, pop 5 → feed [6, 5] ✓
```

### Code
```cpp
class Twitter {
    int clock = 0;
    unordered_map<int, vector<pair<int,int>>> tweets;       // user -> (time, tweetId)
    unordered_map<int, unordered_set<int>> following;
public:
    Twitter() {}
    void postTweet(int userId, int tweetId) {
        tweets[userId].push_back({clock++, tweetId});
    }
    vector<int> getNewsFeed(int userId) {
        priority_queue<pair<int,int>> maxHeap;              // max-heap by time
        auto consider = [&](int u) {
            auto& v = tweets[u];
            for (int i = (int)v.size() - 1, taken = 0; i >= 0 && taken < 10; i--, taken++)
                maxHeap.push(v[i]);
        };
        consider(userId);
        for (int f : following[userId]) consider(f);
        vector<int> res;
        while (!maxHeap.empty() && (int)res.size() < 10) {
            res.push_back(maxHeap.top().second);
            maxHeap.pop();
        }
        return res;
    }
    void follow(int a, int b) { if (a != b) following[a].insert(b); }
    void unfollow(int a, int b) { following[a].erase(b); }
};
```
```java
class Twitter {
    private int clock = 0;
    private Map<Integer, List<int[]>> tweets = new HashMap<>();      // user -> [time, tweetId]
    private Map<Integer, Set<Integer>> following = new HashMap<>();

    public Twitter() {}
    public void postTweet(int userId, int tweetId) {
        tweets.computeIfAbsent(userId, x -> new ArrayList<>()).add(new int[]{clock++, tweetId});
    }
    public List<Integer> getNewsFeed(int userId) {
        PriorityQueue<int[]> maxHeap = new PriorityQueue<>((a, b) -> b[0] - a[0]); // time desc
        Set<Integer> users = new HashSet<>(following.getOrDefault(userId, new HashSet<>()));
        users.add(userId);
        for (int u : users) {
            List<int[]> v = tweets.getOrDefault(u, new ArrayList<>());
            for (int i = v.size() - 1, taken = 0; i >= 0 && taken < 10; i--, taken++)
                maxHeap.offer(v.get(i));
        }
        List<Integer> res = new ArrayList<>();
        while (!maxHeap.isEmpty() && res.size() < 10)
            res.add(maxHeap.poll()[1]);
        return res;
    }
    public void follow(int a, int b) {
        if (a != b) following.computeIfAbsent(a, x -> new HashSet<>()).add(b);
    }
    public void unfollow(int a, int b) {
        if (following.containsKey(a)) following.get(a).remove(b);
    }
}
```
```python
import heapq
from collections import defaultdict

class Twitter:
    def __init__(self):
        self.clock = 0
        self.tweets = defaultdict(list)          # user -> [(time, tweetId)]
        self.following = defaultdict(set)

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.tweets[userId].append((self.clock, tweetId))
        self.clock += 1

    def getNewsFeed(self, userId: int):
        max_heap = []                            # use negated time for a max-heap
        users = self.following[userId] | {userId}
        for u in users:
            for t, tid in self.tweets[u][-10:]:  # only the last 10 per user
                heapq.heappush(max_heap, (-t, tid))
        res = []
        while max_heap and len(res) < 10:
            res.append(heapq.heappop(max_heap)[1])
        return res

    def follow(self, a: int, b: int) -> None:
        if a != b:
            self.following[a].add(b)

    def unfollow(self, a: int, b: int) -> None:
        self.following[a].discard(b)
```

### Complexity
- **Time**: `postTweet`, `follow`, `unfollow` O(1). `getNewsFeed` O(F·10·log(F·10)) where F = number of followees — we push at most 10 candidates per user and pop 10.
- **Space**: O(total tweets) stored; the heap holds at most ~10·(F+1) entries during a feed query.

### Verdict
**The intended design.** It exploits the per-user time ordering so the feed merge only inspects the recent tail of each list, never the full history. This is the canonical "merge K recent streams with a heap" pattern.

---

## ⚖️ Approach comparison

| Operation | Collect + sort | Heap merge ⭐ |
|-----------|----------------|---------------|
| postTweet | O(1) | O(1) |
| follow / unfollow | O(1) | O(1) |
| getNewsFeed | O(M log M) over **all** candidate tweets | O(F·10·log(F·10)) over only recent tails |
| Space | O(M) per query | O(total tweets) + small heap |

Both are correct; the heap version avoids sorting tweets it will never return by leveraging each list's existing time order and the fixed "10 most recent" cap.

---

## 🧪 Edge cases & pitfalls
- **User follows themselves**: guard `follow` with `a != b`; the feed already includes self-tweets, so a self-follow must not duplicate them. (Adding the user explicitly to the candidate set, plus the guard, keeps it clean.)
- **Unfollow a non-followed / nonexistent user**: removing a missing element from a set is a harmless no-op.
- **Empty feed**: no tweets from self or followees → return an empty list (Example 3).
- **Fewer than 10 tweets**: return whatever exists, most recent first.
- **Pitfall — timestamp source**: use a single **global** clock, not per-user counters. Per-user counters can't be compared across users to order the merged feed.
- **Pitfall (Python max-heap)**: negate the timestamp so the most recent pops first; forgetting this returns the *oldest* tweets.
- **Pitfall — pushing entire histories**: only the last 10 tweets per user can reach the top 10. Pushing all of them still works but wastes time; slicing to `[-10:]` keeps the heap small.

---

## 🔗 Related problems
- **Merge k Sorted Lists** (LC 23) — the pure "merge K streams with a heap" pattern this feed builds on.
- **Find Median from Data Stream** (LC 295) — another streaming design with heaps. *(file 07)*
- **Design Browser History** (LC 1472) — a different design problem with stacks.
- **LRU Cache** (LC 146) — design with hash map + linked list (recency, like a feed).

---

**→ Next:** [`07-Find-Median-From-Data-Stream.md`](./07-Find-Median-From-Data-Stream.md) | **← Prev:** [`05-Task-Scheduler.md`](./05-Task-Scheduler.md) | Back to [`00-Index.md`](./00-Index.md)
