from typing import List

from domain.map import Map
from domain.minimax.minimax_tree_builder import MinimaxNode, MinimaxTreeBuilder
from domain.position import Position
from domain.score import Score

MIN = -1000
MAX = 1000


class Minimax:
    def __init__(self):
        self.reset_parameters()

    def reset_parameters(self):
        self.MIN = MIN
        self.MAX = MAX
        self.MAX_DEPTH = 5
        self.ALPHA = MIN
        self.BETA = MAX

    def find_optimal_next_position(
        self,
        map: Map,
        position: Position,
        enemy_positions: List[Position],
        score: Score
    ) -> Position:
        self.reset_parameters()
        starting_node = MinimaxTreeBuilder(map).build(position, enemy_positions, score, 0)
        next = self._minimax(0, starting_node, True)
        # print(next.value, next.position.x, next.position.y)
        return next.position

    def _minimax(
        self,
        depth: int,
        current_node: MinimaxNode,
        maximizing_player: bool
    ) -> MinimaxNode:
        if depth >= self.MAX_DEPTH:
            return current_node

        alpha = self.ALPHA
        beta = self.BETA

        if maximizing_player:
            best_node = MinimaxNode(self.MIN, current_node.children, current_node.position)

            for child in current_node.children:
                if child is None:
                    continue

                best_for_child = self._minimax(depth + 1, child, not maximizing_player)

                if best_for_child.value > best_node.value:
                    best_node = best_for_child

                alpha = max(alpha, best_node.value)

                if beta <= alpha:
                    break

            return best_node
        else:
            best_node = MinimaxNode(self.MAX, current_node.children, current_node.position)

            for child in current_node.children:
                if child is None:
                    continue

                best_for_child = self._minimax(depth + 1, child, not maximizing_player)

                if best_for_child.value < best_node.value:
                    best_node = best_for_child

                beta = min(beta, best_node.value)

                if beta <= alpha:
                    break

            return best_node
