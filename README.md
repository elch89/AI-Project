# AI-Project
An implementation of Partitioning problem - solved using Uniform-Cost

## The problem: 
Given a set S, do subsets S1 and S2 a partition of S exists, such that sum of S1 equals sum of S2?
- this problem is a famous NP-Hard problem
## Definition of the search problem:
State space = all possible subsets of S such that subset <= sum of S/2

Initial state = empty group {}

Finish state = sum of subset that equals to sum of S/2

Successor function = add a number from S to subset group

Cost = sum of given subset in state


# Solving the problem using Uniform-Cost algorithm
This project was created to show this 
**is not efficient**

This method was compared with a Genetic algorithm (Not uploaded here)

# See presentation and source code
- [PRESENTATION](AI-Project.pptx)
- [CODE](partition_uc.py)
