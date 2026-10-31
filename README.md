# PROJET TEMPS REEL 
Elise Gimond

## Find minimum cache size to schedule two real-time programs

I chose to use python for this project.
I used the cachegrind logs because I was not able to run valgrind on my personal machine.

The goal was to find the minimal cache size to execute 2 programs : pca and disparity.
The periode of each programe has been defined as 1.75 ×execution time, with cache 0.

1) Recuperation of disparity_results and pca_results using the parse.py provided
2) Calcul of the programs periodes (370519862131.125 and 126948744038.375)
3) Branch and bound algo

To run my program, go in the Cachegrind-20261031 dir and execute : "python3 exploration.py"

To limit the number of valgrind execution, the results of a task with a cache size is stored tu use it again if needed
and I also check if the solution is better than the actual before anithing.

The best solution found is 131072 bytes for pca and 0 bytes for disparity.
It ran Valgrind 23 times.

## Find utilization-cache size Pareto front

The algo has to be adapted to explore the branche that can not have a lower cache size.
It means that we don't check if the solution is better, only if it's feasible and we stocke the U too.

You can see the algo adapted in pareto_front.py,
Obviously, it runs valgrind for all the 28 possibilities.
There are 7 feasible solutions.
I used maptolib to see the cache size and cpu use of each one.
You can see screenshot of the graph in pareto_front.png.

We can see that the 4th solution is dominated by all the others.

![alt text](image.png)