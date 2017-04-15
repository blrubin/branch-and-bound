This is an implementation of the branch and bound algorithm to solve the a variation of the 0-1 Knapsack problem. It was an assignment for the Algorithms course at Queen's University. These were the instructions:

Earth has been invaded and you alone are forced to relocate to another planet. You can take whatever you like, so long as the total mass of your choices does not exceed K kilograms. You have put together quite a long list of things that you would like to take ... too many items to take them all. You've been able to assign a “desirability value” to each object. You need to choose a set of objects that maximizes the total value without exceeding the limit of K kilograms.

Input for this assignment consists of a text file containing an instance of the problem. The  first line of the file contains a string that identifies the problem instance. The second line contains an integer that specifies K (the capacity limit), and an integer that specifies the number of items in the list. Each subsequent line of the file contain a trio of integers: an item's ID number, value and mass.

The input files are named input1.txt and input2.txt

Output for each instance must contain
- the string that identifies the instance
- the value of an optimal solution
- the list of item identifiers that make up an optimal solution
- the number of partial solutions your program generated during its search for an optimal solution

The reason for reporting the number of partial solutions is to allow you to compare different lower and upper bound functions. You are required to implement at least two ways of computing the lower bound and at least two ways of computing the upper bound for each partial solution.

For each instance of the problem, solve it using your weaker lower and upper bound functions, and then solve it again using your stronger lower and upper bound functions. Comment on whether the number of partial solutions is significantly reduced by using stronger bounding functions.
