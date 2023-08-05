"""This module is used to simulate graphs from a exponential random graph
models.
"""
import random
import warnings

import networkx as nx
import numpy as np

from ..statistics import CachedStatsComp


def simulate(
    ngraphs,
    param,
    stats_comp,
    init,
    burnin=0,
    thin=1,
    summary=False,
    warn=None,
    return_cache=False,
):
    """Simulate ngraphs graphs with respect to the param and the sufficient
    statistics.

    :param ngraphs: The number of graphs to simulate.
    :type ngraphs: Integer.
    :param param: The parameter of the model.
    :type param: Numpy array.
    :param stats_comp: The sufficient statistics computer.
    :type stats_comp: A callable object.
    :param init: The initial graph to start the chain, or the number of nodes.
    :type init: NetworkX graph., optional
    :param burnin: The number of graphs to burn. If none is given, then no
        graphs will be burned., defaults to None
    :type burnin: int, optional
    :param thin: The thinning factor. By default, None is given.
    :type thin: int, optional.
    :param summary: A flag for requesting to collect information about the
        chain such as the acceptance rate. By default, False is given.
    :type summary: Boolean.
    :param warn: If an integer passed, then a warning is thrown if the
        graphs are near-empty or near-complete for this number of interation.
    :type warn: An integer, optional.
    """
    stats_comp = CachedStatsComp(stats_comp)

    if type(init) is int:
        peek = nx.random_graphs.binomial_graph(init, 0.5)
    else:
        peek = init.copy()
    peek_stats = stats_comp(peek)
    nodes = list(peek.nodes())

    if summary:
        naccepted = 0

    if warn is not None:
        ndeg = 0
        n = peek.number_of_nodes()
        ndyadslim = n * (n - 1) / 2 - 1

    nits = burnin + thin * ngraphs
    logunifs = np.log(np.random.uniform(size=nits))
    graphs = [None] * nits

    for i in range(nits):
        u, v = random.sample(nodes, 2)
        in_graph = peek.has_edge(u, v)

        if in_graph:
            peek.remove_edge(u, v)
        else:
            peek.add_edge(u, v)
        temp_stats = stats_comp(peek)

        if logunifs[i] < param @ (temp_stats - peek_stats):  # Accept the state
            peek_stats = temp_stats
            if summary:
                naccepted += 1
        else:  # Refuse the state.
            # Return to the previous graph.
            if in_graph:
                peek.add_edge(u, v)
            else:
                peek.remove_edge(u, v)

        if warn is not None:
            ndeg = (
                ndeg + 1
                if (
                    peek.number_of_edges() <= 1
                    or peek.number_of_edges() >= ndyadslim
                )
                else 0
            )
            if ndeg >= warn:
                warnings.warn(
                    message="The graph states are near-degenerated.",
                    category=RuntimeWarning,
                )

        graphs[i] = peek.copy()

    # Return phase
    return_objects = [graphs[burnin::thin]]
    if summary:
        return_objects.append({"rate": naccepted / nits})
    if return_cache:
        return_objects.append(stats_comp)
    return (
        tuple(return_objects) if len(return_objects) > 1 else return_objects[0]
    )
