import heapq
from typing import Callable, Optional
from puzzle.base_search import BaseSearch
from puzzle.state import State, GOAL_STATE
from puzzle.result import SearchResult

class AStar(BaseSearch):
    @staticmethod
    def heuristic(state: State) -> int:
        """Calcula a Distância de Manhattan até o estado objetivo."""
        distance = 0
        for i, tile in enumerate(state.tiles):
            if tile != 0:  
                current_row, current_col = i // 3, i % 3
                
                goal_index = GOAL_STATE.index(tile)
                goal_row, goal_col = goal_index // 3, goal_index % 3
                
                distance += abs(current_row - goal_row) + abs(current_col - goal_col)
        return distance

    def search(self, initial: State) -> SearchResult:
        counter = 0
        frontier = []
        
        h_initial = self.heuristic(initial)
        heapq.heappush(frontier, (initial.cost + h_initial, counter, initial))
        
        best_g = {initial: initial.cost}
        
        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))
            f_score, _, current = heapq.heappop(frontier)

            if current.cost > best_g.get(current, float('inf')):
                continue
                
            nodes_expanded += 1

            if current.is_goal:
                return SearchResult(
                    solution=current,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=current.cost
                )

            for neighbor in current.neighbors():
                g_score = neighbor.cost 
                
                if neighbor not in best_g or g_score < best_g[neighbor]:
                    best_g[neighbor] = g_score
                    f_score_neighbor = g_score + self.heuristic(neighbor)
                    
                    counter += 1
                    heapq.heappush(frontier, (f_score_neighbor, counter, neighbor))
                    nodes_generated += 1

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size
        )
