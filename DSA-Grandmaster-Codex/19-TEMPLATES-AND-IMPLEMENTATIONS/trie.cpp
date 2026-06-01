// Trie (prefix tree) for lowercase English

struct TrieNode {
    TrieNode* children[26] = {};
    bool isEnd = false;
    int count = 0;  // number of strings passing through; useful for prefix counting
};

class Trie {
    TrieNode* root;
public:
    Trie() : root(new TrieNode()) {}
    
    void insert(const string& word) {
        TrieNode* cur = root;
        for (char c : word) {
            int i = c - 'a';
            if (!cur->children[i]) cur->children[i] = new TrieNode();
            cur = cur->children[i];
            cur->count++;
        }
        cur->isEnd = true;
    }
    
    bool search(const string& word) {
        TrieNode* cur = root;
        for (char c : word) {
            int i = c - 'a';
            if (!cur->children[i]) return false;
            cur = cur->children[i];
        }
        return cur->isEnd;
    }
    
    bool startsWith(const string& prefix) {
        TrieNode* cur = root;
        for (char c : prefix) {
            int i = c - 'a';
            if (!cur->children[i]) return false;
            cur = cur->children[i];
        }
        return true;
    }
    
    int countWithPrefix(const string& prefix) {
        TrieNode* cur = root;
        for (char c : prefix) {
            int i = c - 'a';
            if (!cur->children[i]) return 0;
            cur = cur->children[i];
        }
        return cur->count;
    }
};

// Binary Trie for XOR maximization (32-bit integers)
struct BinaryTrie {
    struct Node { Node* ch[2] = {nullptr, nullptr}; };
    Node* root = new Node();
    
    void insert(int x) {
        Node* cur = root;
        for (int b = 30; b >= 0; --b) {
            int bit = (x >> b) & 1;
            if (!cur->ch[bit]) cur->ch[bit] = new Node();
            cur = cur->ch[bit];
        }
    }
    
    int maxXor(int x) {
        Node* cur = root;
        int ans = 0;
        for (int b = 30; b >= 0; --b) {
            int bit = (x >> b) & 1;
            int opp = bit ^ 1;
            if (cur->ch[opp]) { ans |= (1 << b); cur = cur->ch[opp]; }
            else cur = cur->ch[bit];
        }
        return ans;
    }
};
