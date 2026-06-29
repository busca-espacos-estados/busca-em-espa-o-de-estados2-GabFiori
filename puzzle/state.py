from __future__ import annotations
from typing import List, Optional, Tuple

GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)


class State:
    """Representa um estado do 8-puzzle como tupla imutável de 9 inteiros (0 = espaço vazio)."""

    def __init__(self, tiles: Tuple[int, ...], parent: Optional["State"] = None, action: Optional[str] = None, cost: int = 0):
        if len(tiles) != 9 or set(tiles) != set(range(9)):
            raise ValueError("Estado inválido: deve conter exatamente os valores 0-8.")
        self.tiles = tiles
        self.parent = parent
        self.action = action
        self.cost = cost

    @property
    def is_goal(self) -> bool:
        return self.tiles == GOAL_STATE

    @property
    def blank_index(self) -> int:
        return self.tiles.index(0)

    def neighbors(self) -> List["State"]:
        """Retorna os estados filhos válidos a partir deste estado."""
        valid_neighbors = []
        idx = self.blank_index

        row, col = idx // 3, idx % 3

        moves = [
            (-1, 0, "Cima"),
            (1, 0, "Baixo"),
            (0, -1, "Esquerda"),
            (0, 1, "Direita")
        ]
        
        for dr, dc, action_name in moves:
            new_row, new_col = row + dr, col + dc
            
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_idx = new_row * 3 + new_col
                tiles_list = list(self.tiles)
                tiles_list[idx], tiles_list[new_idx] = tiles_list[new_idx], tiles_list[idx]
                
                new_state = State(
                    tiles=tuple(tiles_list),
                    parent=self,
                    action=action_name,
                    cost=self.cost + 1
                )
                valid_neighbors.append(new_state)
                
        return valid_neighbors

    def path(self) -> List["State"]:
        """Retorna a sequência de estados do estado inicial até este."""
        current = self
        states_sequence = []
        
        while current is not None:
            states_sequence.append(current)
            current = current.parent
            
        return list(reversed(states_sequence))

    def actions(self) -> List[str]:
        """Retorna a sequência de ações do estado inicial até este."""
        return [state.action for state in self.path() if state.action is not None]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, State) and self.tiles == other.tiles

    def __hash__(self) -> int:
        return hash(self.tiles)

    def __lt__(self, other: "State") -> bool:
        return self.cost < other.cost

    def __repr__(self) -> str:
        t = self.tiles
        return (
            f"+-------+\n"
            f"| {t[0]} {t[1]} {t[2]} |\n"
            f"| {t[3]} {t[4]} {t[5]} |\n"
            f"| {t[6]} {t[7]} {t[8]} |\n"
            f"+-------+"
        ).replace("0", " ")
