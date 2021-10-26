from typing import List

from domain.map import Map
from domain.minimax.minimax_tree_builder import MinimaxNode, MinimaxTreeBuilder
from domain.position import Position
from domain.score import Score

MIN = -1000
MAX = 1000


class Expectimax:
    def __init__(self):
        self.reset_parameters()

    def reset_parameters(self):
        self.MIN = MIN
        self.MAX = MAX

    def find_optimal_next_position(
        self,
        map: Map,
        position: Position,
        enemy_positions: List[Position],
        score: Score
    ) -> Position:
        self.reset_parameters()
        starting_node = MinimaxTreeBuilder(map).build(None, position, enemy_positions, score.available_points.copy(), 0)
        starting_node.parent = None
        next = self._minimax(0, starting_node, True)
        # while True:
        #     if next.parent is None:
        #         break
        #     next = next.parent
        while True: #TODO: simplify
            if next.parent is None or next.parent.parent is None or next.parent.parent.parent is None:
                break
            next = next.parent
        print("end expectimax", next.value, position, ' -> ', next.position)
        return next.position

    def _minimax(
        self,
        depth: int,
        current_node: MinimaxNode,
        maximizing_player: bool
    ) -> MinimaxNode:
        if depth >= 4:
            return current_node
        # all_child_none = True
        # for child in current_node.children:
        #     if child is not None:
        #         all_child_none = False
        #
        # if all_child_none:
        #     return current_node

        if maximizing_player:
            best_node = MinimaxNode(self.MIN, current_node.children, current_node.position, current_node)

            for child in current_node.children:
                if child is None:
                    continue

                best_for_child = self._minimax(depth + 1, child, not maximizing_player)

                if best_for_child.value > best_node.value:
                    best_node = best_for_child

            return best_node
        else:
            child_sum = 0
            child_count = 0
            first_child = None

            for child in current_node.children:
                if child is None:
                    continue

                child = self._minimax(depth + 1, child, not maximizing_player)
                first_child = child

                child_sum += child.value
                child_count += 1

            if child_count == 0:
                return current_node
            return MinimaxNode((int)(child_sum / child_count), current_node.children, current_node.position, first_child)
