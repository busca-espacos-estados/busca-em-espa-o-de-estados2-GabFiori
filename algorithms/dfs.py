from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

class DFS(BaseSearch):
    def search(self, initial: State) -> SearchResult:
        if initial.is_goal:
            return SearchResult(solution=initial, nodes_generated=1)

        frontier = [initial]
        explored = set()
        frontier_set = {initial}
        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))
            current = frontier.pop()
            frontier_set.remove(current)
            
            explored.add(current)
            nodes_expanded += 1

            if current.is_goal:
                return SearchResult(
                    solution=current,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=current.cost
                )

            for neighbor in reversed(current.neighbors()):
                if neighbor not in explored and neighbor not in frontier_set:
                    frontier.append(neighbor)
                    frontier_set.add(neighbor)
                    nodes_generated += 1

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size
        )
