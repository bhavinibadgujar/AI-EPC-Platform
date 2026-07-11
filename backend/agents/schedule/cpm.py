from collections import deque

from .graph_builder import ScheduleGraphBuilder


class CriticalPathMethod:
    """
    Performs Critical Path Method (CPM) calculations.
    """

    def __init__(self, graph_builder: ScheduleGraphBuilder):
        self.graph = graph_builder.graph

    def calculate(self):
        """
        Run full CPM calculation.
        """

        order = list(self.topological_order())

        # --------------------------
        # Forward Pass
        # --------------------------

        for node in order:

            predecessors = list(self.graph.predecessors(node))

            if not predecessors:
                es = 0
            else:
                es = max(
                    self.graph.nodes[p]["EF"]
                    for p in predecessors
                )

            activity = self.graph.nodes[node]["activity"]

            ef = es + activity.duration_days

            self.graph.nodes[node]["ES"] = es
            self.graph.nodes[node]["EF"] = ef

        # --------------------------
        # Project Duration
        # --------------------------

        project_duration = max(
            self.graph.nodes[node]["EF"]
            for node in self.graph.nodes
        )

        # --------------------------
        # Backward Pass
        # --------------------------

        for node in reversed(order):

            successors = list(self.graph.successors(node))

            if not successors:
                lf = project_duration
            else:
                lf = min(
                    self.graph.nodes[s]["LS"]
                    for s in successors
                )

            activity = self.graph.nodes[node]["activity"]

            ls = lf - activity.duration_days

            self.graph.nodes[node]["LF"] = lf
            self.graph.nodes[node]["LS"] = ls

        # --------------------------
        # Float Calculation
        # --------------------------

        critical_path = []

        for node in order:

            es = self.graph.nodes[node]["ES"]
            ls = self.graph.nodes[node]["LS"]

            total_float = ls - es

            self.graph.nodes[node]["FLOAT"] = total_float

            activity = self.graph.nodes[node]["activity"]

            activity.total_float = total_float

            if total_float <= 0:
                activity.is_critical = True
                critical_path.append(node)
            else:
                activity.is_critical = False

        return {
            "project_duration": project_duration,
            "critical_path": critical_path,
        }

    def topological_order(self):
        """
        Returns activities in execution order.
        """

        indegree = {
            node: self.graph.in_degree(node)
            for node in self.graph.nodes
        }

        queue = deque(
            [
                node
                for node in self.graph.nodes
                if indegree[node] == 0
            ]
        )

        while queue:

            node = queue.popleft()

            yield node

            for successor in self.graph.successors(node):

                indegree[successor] -= 1

                if indegree[successor] == 0:
                    queue.append(successor)