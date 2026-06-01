#!/bin/bash
# Stress-test runner — finds bugs by comparing two solutions on random inputs
# Usage: ./stress-test-runner.sh [num_iterations]

# Compile all
g++ -std=c++17 -O2 -o gen gen.cpp || { echo "gen.cpp compile failed"; exit 1; }
g++ -std=c++17 -O2 -o brute brute.cpp || { echo "brute.cpp compile failed"; exit 1; }
g++ -std=c++17 -O2 -o sol sol.cpp || { echo "sol.cpp compile failed"; exit 1; }

iterations=${1:-1000}
echo "Running $iterations iterations..."

for ((i=1; i<=iterations; i++)); do
    ./gen $i > in.txt
    ./brute < in.txt > out_brute.txt
    ./sol < in.txt > out_sol.txt
    if ! diff -q out_brute.txt out_sol.txt > /dev/null; then
        echo "MISMATCH on seed $i"
        echo "--- Input ---"
        cat in.txt
        echo "--- Brute output ---"
        cat out_brute.txt
        echo "--- Sol output ---"
        cat out_sol.txt
        exit 1
    fi
    if (( i % 100 == 0 )); then echo "  $i / $iterations passed"; fi
done

echo "ALL $iterations TESTS PASSED ✓"

# Sample gen.cpp:
#   #include <bits/stdc++.h>
#   using namespace std;
#   int main(int argc, char* argv[]) {
#       srand(atoi(argv[1]));
#       int n = rand() % 10 + 1;
#       cout << n << "\n";
#       for (int i = 0; i < n; i++) cout << rand() % 100 << " \n"[i==n-1];
#       return 0;
#   }
