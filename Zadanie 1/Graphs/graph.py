from __future__ import annotations

import time
from typing import Callable, Dict, List, Optional, Tuple

from graphviz import Digraph

from .node import Node


class Graph:
    def __init__(
        self,
        data: Dict[str or Tuple[str, str], List[Tuple[str, str]]] = None
    ):
        self.nodes = []
        if data:
            for k, v in data.items():
                self.addNode(k, v)

    def addNode(
        self,
        label: str or Tuple[str, str],
        neighbors: List[Tuple[str, str]]
    ) -> None:
        self.nodes.append(Node(label, neighbors))

    def __getitem__(self, key: str) -> Node:
        for i in filter(lambda x: x.idx == key, self.nodes):
            return i

    def __str__(self) -> str:
        return '\n'.join([str(i) for i in self.nodes])

    def iterNodes(self) -> Node:
        for i in self.nodes:
            yield i

    def render(self, name: Optional[str] = None) -> str:
        graph = Digraph(name or f"graph_{time.strftime('%H.%M-%d.%m.%Y')}")
        for node in self.nodes:
            graph.node(node.idx, node.label)
        for node in self.nodes:
            for neigbour in node.neigbours:
                graph.edge(node.idx, self[neigbour[0]].idx, neigbour[1])
        graph.render(format='png')
        return graph.name

    @staticmethod
    def fromString(
        data: str,
        genIdx: Callable[[str], str] = None,
        parseEdgeData: Callable[[str], str or Tuple[str, str]] = None
    ) -> Graph:
        data = [i.strip() for i in data.split('\n')]
        out = {}
        for line in data:
            if line == '':
                continue
            label, _, *neigbours = line.split()
            if genIdx:
                label = (label, genIdx(label))
            if parseEdgeData:
                neigbours = [parseEdgeData(i) for i in neigbours]
            else:
                neigbours = [(i, '') for i in neigbours]
            out[label] = neigbours
        return Graph(out)
