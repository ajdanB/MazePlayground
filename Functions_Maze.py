## Import libraries
import random
from Node import Node
from rich import print

# Design of the maze ███
wall = "▓▓▓"
path = "   "
path_solved = ["[bold green] ● [/bold green]", "🐾 ", "❅  "]
end = ["🏆 ", "🐈 ", "🐕 ", "🐁 ", "🌼 ", "🌺 ", "🌙 ", "🏆 ", "🎯 ", "🐔 ", "☃  ", "⛄ "]
start = ["🚗 ", "🐾 ", "🐾 ", "🐈 ", "🐝 ", "🐝 ", "🚀 ", "🏇 ", "🏹 ", "🐤 ", "❆  ", "❆  "]

# Functions
def random_start(maze):
    """
    Function to get a random start node at the borders of the maze.
    Args:       maze (list): list of nodes
    Returns:    start_node (node): the start node to entry the maze
    """
    list_borders = []  # empty list to store the boarder nodes of the maze
    for row in maze:
        for node in row:
            if node.x == 0 or node.x == len(maze) - 1 or node.y == 0 or node.y == len(
                    row) - 1:  # if node is at the border of the maze, append it to the list
                list_borders.append(node)
    start_node = random.choice(list_borders)  # choose a random node from the list
    start_node.is_start = True
    start_node.is_wall = False
    return start_node

def connect_nodes(maze, height, width):
    """
    Function to connect the nodes of the maze in the four directions (north, south, east, west), to make a connected grid.
    Args:   maze (list): list of nodes
            height (int): height of the maze
            width (int): width of the maze
    """
    for row in range(0, height):
        for column in range(0, width):
            if column > 0:
                maze[row][column].west = maze[row][column - 1]
                maze[row][column - 1].east = maze[row][column]
            if row > 0:
                maze[row][column].north = maze[row - 1][column]
                maze[row - 1][column].south = maze[row][column]

def alg_recursive_backtracking(start_node: Node):
    """
    Function to implement the recursive backtracking algorithm (simple)
    Args:   start_node (node): the start node to entry the maze
    """
    stack = [start_node]  # list with start node (we only need a stack) to store more nodes
    start_node.is_wall = False  # set the start node to a path

    while len(stack) > 0:  # loop until the stack is empty
        current_node = stack[-1]  # get the last node of the stack
        next_possible_nodes = current_node.get_changeable_walls()
        if len(next_possible_nodes) > 0:  # if there are changeable walls, choose a random one
            next_node = random.choice(next_possible_nodes)
            next_node.is_wall = False
            stack.append(next_node)  # append the next node to the stack
        else:
            stack.pop()  # if there are no changeable walls, pop the last node from the stack and go back to the previous node

def alg_recursive_backtracking2(start_node: Node, branching_factor=0.05):
    """
    Function to implement the recursive backtracking algorithm with a branching factor
    Args:   start_node (node): the start node to entry the maze
    """
    stack = []
    stack_jump_backs = []
    stack.append(start_node)
    start_node.is_wall = False

    while len(stack) > 0 or len(stack_jump_backs) > 0:  # loop until the stack and the stack_jump_backs are empty
        current_node = stack[-1]
        next_possible_nodes = current_node.get_changeable_walls()
        if len(next_possible_nodes) > 0:
            if random.random() < branching_factor:  # jump back to a random node by a given branching factor (chance)
                stack_jump_backs.append(stack.copy())  # notice the current stack for later
                stack = stack[:random.randint(1, len(stack))]

            else:
                next_node = random.choice(next_possible_nodes)
                next_node.is_wall = False
                stack.append(next_node)
        else:
            stack.pop()
        if len(stack) == 0 and len(stack_jump_backs) > 0:  # go back to the last stack of nodes
            stack = stack_jump_backs.pop()

def print_maze(maze, design_index=None):
    """
    Function to print the completed maze.
    Args:       maze (list): list of nodes
                design_index (int): index of the design
    Returns:    design_index (int): index of the design
    """
    output = "███" * (len(maze[0]) + 2) + "\n"  # top border of the maze

    if design_index == None:  # if design_index is None, choose a random design
        design_index = random.randint(0, len(start) - 1)
    if design_index == 3 or design_index == 2 or design_index == 1:  # choose a design for the solved path depending on the design of the start and the end node
        design_path = path_solved[1]
    elif design_index == 10 or design_index == 11:
        design_path = path_solved[2]
    else:
        design_path = path_solved[0]

    for row in maze:  # loop through the maze and print the nodes
        output += "███"  # left border of the maze
        for node in row:
            if node.is_wall == True:
                output += wall
            if node.is_wall == False:
                if node.is_start == True:
                    output += start[design_index]
                elif node.is_end == True:
                    output += end[design_index]
                elif node.is_path_solved == True:
                    output += design_path
                else:
                    output += path

        output += "███\n"  # right border of the maze
    output += "███" * (len(maze[0]) + 2)  # bottom border of the maze
    print("\n" + output + "\n")
    return design_index  # return the design index for the solved maze

def path_finding(start_node: Node):
    """
    Function to find the shortest path through the maze from start to all nodes (breath-first search).
    Find also the node on a boarder (end node) with the longest distance to the start node.
    Args:       start_node (node): the start node to entry the maze
    Returns:    end_node (node): the end node to exit the maze with the longest distance to the start node
    """
    next_nodes = set()  # set to store the nodes for the next iteration (prevent duplicates)
    start_node.path_finding = 0
    end_node = None
    next_nodes.add(start_node)
    while len(next_nodes) > 0:
        next_nodes_tmp = set()  # initialize a set to hold the nodes that will be processed in the next iteration
        for node in next_nodes:
            for next_node in node.get_visitable_nodes():
                if next_node.path_finding == None:
                    next_node.path_finding = node.path_finding + 1  # set the distance to the start node
                    next_nodes_tmp.add(next_node)
                    if next_node.on_boarder() != None:
                        end_node = next_node  # get the node on a boarder with the longest distance to the start node
        next_nodes = next_nodes_tmp  # fresh next_nodes for next iteration
    end_node.is_end = True
    return end_node

def path_solving(end_node: Node):
    """
    Function to solve the maze. Start at the end node and go back to the start node (backwards breadth-first search).
    Args:       end_node (node): the end node to exit the maze
    """
    current_node = end_node
    while current_node.is_start == False:
        possible_nodes = current_node.get_visitable_nodes()
        for node in possible_nodes:
            if node.path_finding == current_node.path_finding - 1:  # if the distance to the start node is one less than the current node, set the node to a solved path
                node.is_path_solved = True  # set the node to a solved path (for printing)
                current_node = node
                break
