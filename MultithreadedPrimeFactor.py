from multiprocessing import Pool
import math
import random
import time
start_time = time.time()

#creating a global list of prime factors to store primes that are known p and q values for previous N's
globalPrimeFactors = []

def writeToFile(N, p, q):
	"""
	This function opens the file in append mode and writes to the file the found factors of N, in the form N=p*q, 
	converting all ints to strings, after it has finished it closes the file.
	Parameters: integer N, and the prime factors p and q, where N=pq
	Returns: none
	"""
	fileName = 'FoundFactors.txt'
	with open(fileName, 'a') as file:
		file.write(str(N) + " = " + str(p) + "*" + str(q) + "\n")	
	file.close()	
#end of writeToFile(number,factors)	

def processLine(line):
	"""
	This function processes each line as it is parsed from the text file parsed in main(). Each line is stripped of the new line character
	as well as ensures each line is valid, for each line converted into a long int it makes a function call to findPrimeFactors(number)
	Parameters: line
	Returns: none 
	"""
	line = line.strip()
	number = long(line)
	if number:
		findPrimeFactors(number)		
#end of processLine(line)

def gcd(a,b):
	"""
	This function finds the greatest common divisior given two numbers. The while loop iterates until the value of b = 0, and continually 
	shifts the values of a and b, where a=b, and b=a%b.
	Parameters: values a,b to find the gcd between
	Returns: the gcd
	"""
	while b:
		a, b = b, a%b
	return a
#end of gcd(a,b)

def findPrimeFactors(number):
	"""
	This function finds the prime factors of integer N in the form of p and q. This function utilizes a variation upon the Pollard Rho 
	algorithm, in which the cycle detection uses Brent's cycle finding method. This algorithm decreases the computation time by repetitively 
	updating the variable y, in the form y = ((y*y)%N+c)%N, it does so inside two nested for loops, this is the case as defining a z to be 
	the product of numerous |x-y|mod n, and then computing a single call to the gcd function with that z and N, would yield a greater 
	success rate in finding the gcd of N and a significant decrease in computation time. Additionally, inside the nested while loop we set 
	ys = y, which will be a previous version of y, and once the code exits the outer while loop, when g!=1, if it is still the case that 
	g==N the code can revert to the previous version of y, and implement an iterative call to the gcd(), with the parameters x-ys and N, 
	for each new computation of y = ys = ((ys*ys)%N+c)%N. Additionally, once a p and q are found for the first N, those values are added to 
	a global list named globalPrimeFactors that stores the values of prime factors known to be a factor of the N's we have encountered. Thus 
	after finding the first pair of factors, every consequent N that is passed into the findPrimeFactorsBrent function, first assesses whether 
	a previous prime factor is also a prime factor of that number, this then sets a boolean to true, and thus the alogrithm will not enter the 
	second stage, which utilizes Brents alogrithm. Fundamentally, this is just creating a primes list that starts at a much larger number than 
	2. Once the pair of primes are found, a function call is made to write the values to a file in the form of N=p*q as well as print this to 
	the screen.  
	#Brent alogrithm adapted from http://maths-people.anu.edu.au/~brent/pd/rpb051i.pdf and https://comeoncodeon.wordpress.com/2010/09/18/pollard-rho-brent-integer-factorization/
	Parameters: the number being factored into the two primes p and q
	Returns: none
	"""
	N = number
	primesNotFound = True
	globalPrimesSuccess = False

	#check first if any of the globalPrimeFactors will work for this N
	for p in globalPrimeFactors:
		if (N % p == 0):
			q = (N/p)
			globalPrimesSuccess = True
			break

	#if N is not composed of one of the previous prime factors found
	if (globalPrimesSuccess == False):
		sqrtN = int(N**0.5)	
		#find initial value for y, and randomly assigns c and m
		y,c,m = random.randint(1, sqrtN),random.randint(1, sqrtN),random.randint(1, sqrtN)
		g,r,z = 1,1,1
		#while we do not have a value that could be the greatest common divisor
		while g==1:
			x = y
			for i in range(r):
				y = ((y*y)%N+c)%N
			k = 0
			while (k<r and g==1):
				#update the value of ys, to be used if the alogrithm exits without a valid gcd (in our case), can restore previous version of y
				ys = y
				for i in range(min(m,r-k)):
					y = ((y*y)%N+c)%N
					#find z, such that z is the product of x-y mod n
					z = z*(x-y)%N	
				g = gcd(z,N)
				k = k + m
			r = r*2
		#if either N is prime or there is not a valid gcd
		if g==N:
			while True:
				ys = ((ys*ys)%N+c)%N
				g = gcd(x-ys,N)
				if g>1:
					break
		p=g
		q=number/p

	globalPrimeFactors.append(p) if p not in globalPrimeFactors else None
	globalPrimeFactors.append(q) if q not in globalPrimeFactors else None
	print number, "=", p, "*", q
	writeToFile(number, p, q)
#end of findPrimeFactors(number)

def main():
	print "+++++++++++++++++++++++++++++++"
	print "           CSCI 2428           "
	print "       Factoring Numbers       "
	print "+++++++++++++++++++++++++++++++"
	fileName = "nums.txt"
	#use four cores to when processing the the data from the text file
	p = Pool(4)
	with open(fileName, 'r') as file:
		p.map(processLine,file)
		p.close()
		p.join()
	file.close()
	print "\nExecution time:", (" %s seconds " % (time.time() - start_time))
#end of main()
	
if __name__ == '__main__':
	main()