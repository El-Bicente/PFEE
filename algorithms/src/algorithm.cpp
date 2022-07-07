#include "higra/graph.hpp"
#include <iostream>

using namespace hg;


int main() {
// create a graph with 4 vertices and no edge
    ugraph g(4);

// add an edge, between vertex 0 and 1
    add_edge(0, 1, g);
// add an edge, between vertex 1 and 2
    auto e = add_edge(1, 2, g);

    auto s = source(e, g); // 1
    auto t = target(e, g); // 2
    auto ei = index(e, g); // 1

// add the two edges (3, 0) and (3, 1)
    add_edges({3, 3}, {0, 1}, g);

    auto ne = num_edges(g); // 4

    auto edges = edge_list(g); // edges.first = {0, 1, 0, 1}, edges.second = {1, 2, 3, 3}

    auto msf = hg.minimum_spanning_tree(g, NULL);

    cout << msf;

    return 0;
}
