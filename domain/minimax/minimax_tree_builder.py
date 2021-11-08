from typing import List, Optional

from domain.map import Map
from domain.minimax.evaluator import Evaluator
from domain.position import Position


class MinimaxNode:
    def __init__(
        self,
        value: int,
        children: List["MinimaxNode"],
        position: Position,
        parent: Optional["MinimaxNode"]
    ):
        self.value = value
        self.children = children
        self.position = position
        self.parent = parent


class MinimaxTreeBuilder:
    def __init__(self, map: Map):
        self.map = map
        self.evaluator = Evaluator(map)
        self.MAX_DEPTH = 5  # 5 for minimax

    def build(
        self,
        parent_node: Optional[MinimaxNode],
        player_position: Position,
        enemy_positions: List[Position],
        available_points: List[Position],
        depth
    ) -> MinimaxNode:
        if depth >= self.MAX_DEPTH:
            return None

        if depth % 2 == 0:
            # pacman turn
            node = MinimaxNode(
                self.evaluator.evaluate(
                    player_position,
                    enemy_positions,
                    available_points.count(player_position) > 0,
                    available_points
                ),
                [],
                player_position,
                parent_node
            )

            # print("e for player", node.value, depth)

            for neighbour_position in self.map.get_all_adjacent_positions(player_position):
                cp = available_points.copy()
                if available_points.count(player_position) > 0:
                    cp.remove(player_position)
                node.children.append(self.build(
                    node,
                    neighbour_position,
                    enemy_positions,
                    cp,
                    depth + 1,
                ))
        else:
            # enemy turn
            node = MinimaxNode(
                self.evaluator.evaluate(
                    player_position,
                    enemy_positions,
                    available_points.count(player_position) > 0,
                    available_points
                ),
                [],
                enemy_positions[0],
                parent_node
            )

            #enemy_positions[0].x, enemy_positions[0].y, player_position.x, player_position.y,
            # print("e for enemy", node.value, depth)

            for enemy_position in enemy_positions:
                for neighbour_position in self.map.get_all_adjacent_positions(enemy_position):
                    cp = enemy_positions.copy()
                    cp.remove(enemy_position)
                    cp.append(neighbour_position)
                    node.children.append(self.build(
                        node,
                        player_position,
                        cp,
                        available_points,
                        depth + 1
                    ))

        return node