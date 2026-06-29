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
