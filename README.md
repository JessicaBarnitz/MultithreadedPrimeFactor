# MultithreadedPrimeFactor

# Description:
The prime factorization finds the prime factors of a large int N, parsed from a text file, in the form of p and q. It uses multithreaded processing when parsing each line and utilizes Brent's alogrithm, a variation on the Pollard Rho alogorithm for finding factors of a number. Additionally, it creates a global primes list that is comprised of primes found for the N's parsed thus far, and uses these primes to also compare to current N's being evaluated, this makes the most significant decrease in computation time. All N=p*q are written to a text file named: 'FoundFactors.txt' and printed to the user screen in the order that they are processed. 

# Compile: 
''' $ make ''''

# Usage:
''' $ make run '''