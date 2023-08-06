"""
- Title:            Utils Network Graph for User Interface (networkx)
- Project/Topic:    Utils Tabular Data. Practical functions for Data Science
- Author/s:         Angel Martinez-Tenor
- Dev Date:         2017 - 2022

- Status:           Planning
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import plotly.graph_objs as go
from plotly.offline import iplot  # init_notebook_mode, download_plotlyjs


def info_graph(graph: nx.DiGraph) -> str:
    """Return a msg with graph info: Type, nodes and edges. e.g.: 'DiGraph with 30 nodes and 225 edges'
    Args:
        graph (nx.DiGraph): Directed Graph
    Returns:
        str: msg with graph info: Type, nodes and edges
    """
    return str(graph)


def plot_graph(graph: nx.DiGraph):
    """Show a static plot of the input networkx 'graph'  with degree graphs
    source: https://networkx.org/documentation/latest/auto_examples/
    Args:
        graph (nx.DiGraph): Directed Graph
    """

    undirected_graph = graph.to_undirected()

    degree_sequence = sorted((d for node, d in undirected_graph.degree()), reverse=True)

    fig = plt.figure("Degree of a random graph", figsize=(15, 15))
    # Create a gridspec for adding subplots of different sizes
    axgrid = fig.add_gridspec(5, 4)

    ax0 = fig.add_subplot(axgrid[0:3, :])
    gcc = undirected_graph.subgraph(sorted(nx.connected_components(undirected_graph), key=len, reverse=True)[0])
    pos = nx.spring_layout(gcc, seed=10396953)
    nx.draw_networkx_nodes(gcc, pos, ax=ax0, node_size=20)
    nx.draw_networkx_edges(gcc, pos, ax=ax0, alpha=0.4)
    ax0.set_title("Dependency Graph of Assembly Plan")
    ax0.set_axis_off()

    ax1 = fig.add_subplot(axgrid[3:, :2])
    ax1.plot(degree_sequence, "b-", marker="o")
    ax1.set_title("Degree Rank Plot")
    ax1.set_ylabel("Degree")
    ax1.set_xlabel("Rank")

    ax2 = fig.add_subplot(axgrid[3:, 2:])
    ax2.bar(*np.unique(degree_sequence, return_counts=True))
    ax2.set_title("Degree histogram")
    ax2.set_xlabel("Degree")
    ax2.set_ylabel("# of Nodes")

    fig.tight_layout()
    plt.show()


def plot_graph_plotly(graph: nx.DiGraph, labels_dict: dict[str, str] = None):
    """Show a customized plotly plot of the input networkx Graph.
        A dictionary 'labels_dict' can be passed to replace the name of the nodes
        Adapted from: https://www.kaggle.com/anand0427/network-graph-with-at-t-data-using-plotly
    Args:
        graph (nx.DiGraph): Directed Graph
        labels_dict (dict[str,str], optional): keys=node, value=caption. Defaults to None.
    """
    # graph = nx.Graph(graph)
    pos = nx.kamada_kawai_layout(graph)
    # pos = nx.spring_layout(graph, seed=1000)

    for node, position in pos.items():
        graph.nodes[node]["pos"] = position

    edge_trace = go.Scatter(x=[], y=[], line={"width": 0.5, "color": "#888"}, hoverinfo="none", mode="lines")

    for edge in graph.edges():
        x0, y0 = graph.nodes[edge[0]]["pos"]
        x1, y1 = graph.nodes[edge[1]]["pos"]
        edge_trace["x"] += tuple([x0, x1, None])
        edge_trace["y"] += tuple([y0, y1, None])

    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode="markers",
        hoverinfo="text",
        # marker=dict(
        #     showscale=True,
        #     colorscale="RdBu",
        #     reversescale=True,
        #     color=[],
        #     size=15,
        #     colorbar=dict(
        #         thickness=10,
        #         title="Number of Connections",
        #         xanchor="left",
        #         titleside="right",
        #     ),
        marker={
            "showscale": True,
            "colorscale": "RdBu",
            "reversescale": True,
            "color": [],
            "size": 15,
            "Line": {"width": 0},
            "colorbar": {
                "thickness": 10,
                "title": "Number of Connections",
                "xanchor": "left",
                "titleside": "right",
            },
        },
    )

    for node in graph.nodes():
        x, y = graph.nodes[node]["pos"]
        node_trace["x"] += tuple([x])
        node_trace["y"] += tuple([y])

    for node, adjacencies in enumerate(graph.adjacency()):
        node_trace["marker"]["color"] += tuple([len(adjacencies[1])])
        if labels_dict:
            node_info = labels_dict[adjacencies[0]] + " [" + str(len(adjacencies[1])) + "]"
        else:
            node_info = str(adjacencies[0]) + " [" + str(len(adjacencies[1])) + "]"
        node_trace["text"] += tuple([node_info])

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title="<br>Precedence Graph",
            titlefont={"size": 16},
            showlegend=False,
            hovermode="closest",
            # margin=dict(b=20, l=5, r=5, t=40),
            # xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            # yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            margin={"b": 20, "l": 5, "r": 5, "t": 40},
            xaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
            yaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
        ),
    )

    iplot(fig)
    # fig.plot()
    # plotly.plot(fig)
