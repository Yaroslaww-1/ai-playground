from typing import List

from domain.map import Map
from domain.minimax.evaluator import Evaluator
from domain.position import Position
from domain.score import Score


class MinimaxNode:
    def __init__(
        self,
        value: int,
        children: List["MinimaxNode"],
        position: Position
    ):
        self.value = value
        self.children = children
        self.position = position


class MinimaxTreeBuilder:
    def __init__(self, map: Map):
        self.map = map
        self.evaluator = Evaluator(map)
        self.MAX_DEPTH = 6

    def build(
        self,
        current_position: Position,
        enemy_positions: List[Position],
        score: Score,
        depth
    ) -> MinimaxNode:
        if depth >= self.MAX_DEPTH:
            return None

        node = MinimaxNode(
            self.evaluator.evaluate(current_position, enemy_positions, score.has_point(current_position)),
            [],
            current_position
        )

        for neighbour_position in self.map.get_all_adjacent_positions(current_position):
            node.children.append(self.build(
                neighbour_position,
                enemy_positions,
                score,
                depth + 1
            ))

        return node