import networkx as nx

from .model import Activity, Relationship


class ScheduleGraphBuilder:
    """
    Builds a directed graph from project activities and relationships.
    """

    def __init__(self):
        self.graph = nx.DiGraph()

    def build_graph(
        self,
        activities: list[Activity],
        relationships: list[Relationship],
    ) -> nx.DiGraph:
        """
        Create a directed graph.

        Nodes:
            Activities

        Edges:
            Relationships
        """

        self.graph.clear()

        # -----------------------------
        # Add Activity Nodes
        # -----------------------------
        for activity in activities:
            self.graph.add_node(
                activity.activity_id,
                activity=activity
            )

        # -----------------------------
        # Add Dependency Edges
        # -----------------------------
        for relation in relationships:
            self.graph.add_edge(
                relation.predecessor,
                relation.successor,
                relationship_type=relation.relationship_type,
                lag=relation.lag
            )

        return self.graph

    def get_start_nodes(self):
        """
        Activities without predecessors.
        """

        return [
            node
            for node in self.graph.nodes
            if self.graph.in_degree(node) == 0
        ]

    def get_end_nodes(self):
        """
        Activities without successors.
        """

        return [
            node
            for node in self.graph.nodes
            if self.graph.out_degree(node) == 0
        ]

    def has_cycle(self) -> bool:
        """
        Check whether the schedule contains a cycle.
        """

        return not nx.is_directed_acyclic_graph(self.graph)

    def topological_sort(self):
        """
        Return activities in execution order.
        """

        if self.has_cycle():
            raise ValueError(
                "Schedule contains circular dependencies."
            )

        return list(nx.topological_sort(self.graph))

    def predecessors(self, activity_id: str):
        return list(self.graph.predecessors(activity_id))

    def successors(self, activity_id: str):
        return list(self.graph.successors(activity_id))