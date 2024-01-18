from __future__ import annotations
from dataclasses import dataclass

# =========================
# Original Code: https://gist.github.com/Nicholas-Swift/003e1932ef2804bebef2710527008f44
# Edited by: https://github.com/DragonOfShuu
# =========================

@dataclass
class Coords:
    x: int
    y: int

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent: Node|None = None, position: Coords|None = None):
        self.parent = parent
        self.position = position if position is not None else Coords(0, 0)

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other: Node):
        return self.position == other.position
    

def findPathTaken(current_node: Node):
    path = []
    current: Node|None = current_node
    # Travel through each of 
    # the nodes parent's until
    # you reach the beginning
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1] # Return reversed path


def whileGrid(open_list: list[Node], closed_list: list[Node], start_node: Node, end_node: Node, map: list[list[int]]):
    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        # Attempt to find the best next node to travel to
        for index, item in enumerate(open_list):
            # If the looped item is better than the currently selected node
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        # (Node is now closed and not discoverable)
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            return findPathTaken(current_node)

        # Generate children
        children: list[Node] = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = Coords(current_node.position.x + new_position[0], current_node.position.y + new_position[1])

            # Make sure within range
            if (node_position.y > (len(map) - 1) 
                or node_position.y < 0 
                or node_position.x > (len(map[node_position.y]) -1) 
                or node_position.x < 0):
                continue

            # Make sure walkable terrain
            if map[node_position.y][node_position.x] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            if child in closed_list: continue
            # for closed_child in closed_list:
            #     if child == closed_child:
            #         continue # Doesn't work as expected

            # Create the f, g, and h values
            child.g = (current_node.g + 10)
            child.h = ((child.position.y - end_node.position.y) ** 2) + ((child.position.x - end_node.position.x) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            should_continue = False
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    # continue # Doesn't work as expected
                    should_continue = True
                    break
            if should_continue: continue

            # Add the child to the open list
            open_list.append(child)


def astar(map: list[list[int]], start: Coords, end: Coords):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list: list[Node] = []
    closed_list: list[Node] = []

    # Add the start node
    open_list.append(start_node)

    return whileGrid(open_list, closed_list, start_node, end_node, map)


def main():
    maze = [
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]*2,
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]*2,
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]*2,
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]*2,
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]*2,
        [0, 0, 0, 0, 1, 0, 0, 1, 0, 0]*2,
        [0, 0, 0, 0, 1, 0, 0, 1, 0, 0]*2,
        [0, 0, 0, 0, 1, 0, 0, 1, 0, 0]*2,
        [0, 0, 0, 0, 1, 0, 0, 1, 0, 0]*2,
        [0, 0, 0, 0, 1, 0, 0, 1, 0, 0]*2,
    ]

    start = Coords(0, 0)
    end = Coords(19, 0)

    path = astar(maze, start, end)
    if path is None: print("No path found..."); return

    printable_map = maze.copy()
    for coord in path:
        printable_map[coord.y][coord.x] = '█'
    
    for i in printable_map:
        for j in i:
            print(j, end=" ")
        print()
    # print(printable_map)


if __name__ == '__main__':
    main()