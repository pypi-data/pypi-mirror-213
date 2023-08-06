# Author: lizhiyuan  <lizhiyuan@baqis.ac.cn>  2021/08/17
from graphlib import TopologicalSorter

__all__ = [
    'graph_reverse',
    'get_subgraph',
    'get_all_nodes',
    'get_topo_order',
    'get_node_priority',
    'get_priority_node',
    'get_exec_order',
    'extract_graph',
]


def graph_reverse(graph_forward):
    '''
    Parameter:
        graph_forward: dict，参考 graphlib.TopologicalSorter 参数graph的定义，如下
                    graph argument must be a dictionary representing a directed acyclic graph 
                    where the keys are nodes and the values are iterables of all predecessors of that node in the graph 
                    (the nodes that have edges that point to the value in the key).
                    graph = {"D": {"B", "C"}, "C": {"A"}, "B": {"A"}}
                    其中key是节点，value是此节点的前置节点。
    Return：
        graph_backward: 反转逆向的图
    '''
    graph_backward = {}
    for k, v in graph_forward.items():
        for _v in v:
            if _v not in graph_backward.keys():
                graph_backward[_v] = set()
            graph_backward[_v].add(k)
    return graph_backward


def get_subgraph(keys=None, graph=None, graph_backward=None, _new_graph=None):
    '''
    Parameter:
        keys: list/tuple/set/iterable, 子图的起始节点或包含在子图中的节点
        graph: dict，参考 graphlib.TopologicalSorter 参数graph的定义，
            graph = {"D": {"B", "C"}, "C": {"A"}, "B": {"A"}}
            其中key是节点，value是此节点的前置节点。
        graph_backward: graph的反向图，graph和graph_backward二选一，优先使用graph_backward
        _new_graph: 用于递归的中间参量
    Return：
        _new_graph: 新生成的子图
    '''
    keys = set() if keys is None else keys
    graph = {} if graph is None else graph
    _new_graph = {} if _new_graph is None else _new_graph
    graph_backward = graph_reverse(
        graph) if graph_backward is None else graph_backward

    next_add_keys = set()
    for k in keys:
        next_nodes = graph_backward.get(k, set())
        next_add_keys.update(next_nodes)
        for next_node in next_nodes:
            if next_node not in _new_graph.keys():
                _new_graph[next_node] = set()
            _new_graph[next_node].add(k)

    if next_add_keys:
        _new_graph = get_subgraph(
            next_add_keys, graph_backward=graph_backward, _new_graph=_new_graph)
    return _new_graph


def get_all_nodes(graph):
    '''
    Parameter:
        graph: dict，参考 graphlib.TopologicalSorter 参数graph的定义，
            graph = {"D": {"B", "C"}, "C": {"A"}, "B": {"A"}}
            其中key是节点，value是此节点的前置节点。
    Return：
        all_nodes: set，图所有节点的集合，比如
            {'A', 'B', 'C', 'D'}
    '''
    all_nodes = set()
    for k, v in graph.items():
        all_nodes.add(k)
        all_nodes.update(v)
    return all_nodes


def get_topo_order(graph):
    '''
    Parameter:
        graph: dict，参考 graphlib.TopologicalSorter 参数graph的定义，
            graph = {"D": {"B", "C"}, "C": {"A"}, "B": {"A"}}
            其中key是节点，value是此节点的前置节点。
    Return：
        topo_order: list，按照拓扑序排列的节点列表，比如
            ['A', 'B', 'C', 'D']
    '''
    ts = TopologicalSorter(graph)
    return list(ts.static_order())


def get_node_priority(graph):
    '''
    Parameter:
        graph: dict，参考 graphlib.TopologicalSorter 参数graph的定义，
            graph = {"D": {"B", "C"}, "C": {"A"}, "B": {"A"}}
            其中key是节点，value是此节点的前置节点。
    Return：
        node_priority: dict，节点和优先度组成的键值对字典，比如
            {'A': 1, 'C': 2, 'B': 2, 'D': 3}
    '''
    ts = TopologicalSorter(graph)
    node_priority = {}
    for k in ts.static_order():
        prenode_priority = [node_priority[_k] for _k in graph.get(k, set())]
        max_prenode = max(prenode_priority, default=0)
        node_priority[k] = max_prenode+1
    return node_priority


def get_priority_node(graph):
    '''
    Parameter:
        graph: dict，参考 graphlib.TopologicalSorter 参数graph的定义，
            graph = {"D": {"B", "C"}, "C": {"A"}, "B": {"A"}}
            其中key是节点，value是此节点的前置节点。
    Return：
        priority_node: dict，优先度和节点组成的键值对字典，比如
            {1: {'A'}, 2: {'B', 'C'}, 3: {'D'}}
    '''
    node_priority = get_node_priority(graph)
    priority_node = {}
    for node, priority in node_priority.items():
        if priority not in priority_node.keys():
            priority_node[priority] = set()
        priority_node[priority].add(node)
    return priority_node


def get_exec_order(graph):
    '''
    Parameter:
        graph: dict，参考 graphlib.TopologicalSorter 参数graph的定义，
            graph = {"D": {"B", "C"}, "C": {"A"}, "B": {"A"}}
            其中key是节点，value是此节点的前置节点。
    Return：
        exec_order: list，按照优先度排序的节点序列，比如
            [{'A'}, {'B', 'C'}, {'D'}]
    '''
    priority_node = get_priority_node(graph)
    exec_order = [priority_node[p+1] for p in range(len(priority_node.keys()))]
    return exec_order


def extract_graph(constrains):
    '''
    Parameter:
        constrains: tuple(deps,func,targets)，其中 deps/targets 为 str|tuple(str)
    Return：
        graph_forward, graph_backward: 前向图和反向图
    '''
    graph_forward = {}
    graph_backward = {}

    for deps, func, targets in constrains:
        if isinstance(deps, str):
            deps = (deps,)
        if isinstance(targets, str):
            targets = (targets,)

        for target in targets:
            if target not in graph_forward.keys():
                graph_forward[target] = set()
            graph_forward[target].update(deps)

        for dep in deps:
            if dep not in graph_backward.keys():
                graph_backward[dep] = set()
            graph_backward[dep].update(targets)

    return graph_forward, graph_backward
