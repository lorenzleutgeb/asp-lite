# 3-Clique

Consider a simple logic program that solve
Let's write a simple logic program that checks for a 3-Clique in an undirected graph.

## Instance Definition

We require a predicate to denote the set of vertices in the graph:

    vertex 1..4

Further, lets assume some connections between them:

    edge 1 2
    edge 1 3
    edge 1 4
    edge 2 3

For undirectedness we close this relation symmetrically:

    edge     U V
        edge V U

## Guess

Now, we guess for every vertex whether it is in the 3-clique or not:

    clique V | -clique V
        vertex V

## Check

We need to verify that there are at least three vertices in the clique:

    -
        < C 3
        #count V C
            clique V

Every two vertices that are in the clique must be connected through an edge.

    -
            clique U
            clique   V
            !=     U V
        not edge   U V
        not edge   V U
