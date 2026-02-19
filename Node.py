class Node:
    """
    Class for the nodes of the maze
    """
    def __init__(self, x, y):
        """
        Constructor of the node
        Args:       x (int): x coordinate (height) of the node
                    y (int): y coordinate (width) of the node
        """
        self.x = x  # coordinates of the node (x = height, y = width)
        self.y = y
        self.north = None  # reference to each node in the north, south, east and west
        self.south = None
        self.east = None
        self.west = None
        self.is_wall = True  # boolean to check if the node is a wall (default: True) or a path (False)
        self.is_visited = False  # boolean to check if the node is visited
        self.is_start = False  # boolean to check if the node is the start node
        self.is_end = False  # boolean to check if the node is the end node
        self.is_path_solved = False  # boolean to check if the node is part of the solved path
        self.path_finding = None  # distance to the start node

    def on_boarder(self):
        """
        Function to check if the node is on the boarder of the maze.
        Returns:    one of the touching boarders (north, south, east, west (str)) or None
        """
        possible_boarders = ['north', 'south', 'east', 'west']
        for boarder in possible_boarders:
            if getattr(self, boarder) is None:  # iterates through self.north, self.south, self.east, self.west
                return boarder
        return None

    def get_visitable_nodes(self, prev_node=None):
        """
        Function to get the visitable nodes, which are not walls. If given, the previous node is excluded.
        Args:       prev_node (node): previous node
        Returns:    nodes (list): list of nodes
        """
        nodes = []
        for node in [self.north, self.south, self.east, self.west]:
            if node != None and node.is_wall == False:
                nodes.append(node)
        if (prev_node in nodes) and node != None:
            nodes.remove(node)
        return nodes

    def get_changeable_walls(self):
        '''
        Function to get the surrounding walls, which have the potential to be changed to a path,
        without connecting into an other path of the maze.
        Returns:    changeable_walls (list): list of nodes

        Ascii-Art:
        ┌───┬───┬───┬───┬───┐   
        │   │   │ • │   │   │   X = current node
        ├───┼───┼───┼───┼───┤   ┌───┐
        │   │ • │ ↑ │ • │   │   │   │ = walls
        ├───┼───┼───┼───┼───┤   └───┘
        │ • │ ← │ X │ → │ • │   ↑, ↓, ←, → = potentially changeable walls
        ├───┼───┼───┼───┼───┤   ──────────
        │   │ • │ ↓ │ • │   │   following checks needed:
        ├───┼───┼───┼───┼───┤   1. ↑, ↓, ←, → != None (not out of range) AND is_wall == True
        │   │   │ • │   │   │   2. • can be None (so ↑, ↓, ←, → is at boarder) OR is_wall == True
        └───┴───┴───┴───┴───┘   3. ↑, ↓, ←, → is changeable, if 1. is true and 2. for all 3x surrounding • is true

        Examples [□ - no wall (path), ■ - wall]:
        ┌───┐                   ┌───┐                     ┌───┬───┬───┐
        │ ↓ │ ↓ is changeable   │ ↓ │ ↓ is not changeable │ ■ │ ↓ │ □ │ ↓ & → are not changeable
        ├───┤                   ├───┤                     ├───┼───┼───┤
        │ ■ │                   │ □ │                     │ * │ ■ │ * │ * can be □ or ■
        └───┘                   └───┘                     └───┴───┴───┘  
        
        Notice: code can be written extremely shorter, but for better understanding it is written like this.
        '''
        changeable_walls = []  # empty list of changeable walls
        # check if ↑ is changeable
        if self.north != None and self.north.is_wall == True:
            if (self.north.north != None and self.north.north.is_wall == True) or self.north.north == None:
                if (self.north.east != None and self.north.east.is_wall == True) or self.north.east == None:
                    if (self.north.west != None and self.north.west.is_wall == True) or self.north.west == None:
                        changeable_walls.append(self.north)
        # check if ↓ is changeable
        if self.south != None and self.south.is_wall == True:
            if (self.south.south != None and self.south.south.is_wall == True) or self.south.south == None:
                if (self.south.east != None and self.south.east.is_wall == True) or self.south.east == None:
                    if (self.south.west != None and self.south.west.is_wall == True) or self.south.west == None:
                        changeable_walls.append(self.south)
        # check if → is changeable
        if self.east != None and self.east.is_wall == True:
            if (self.east.east != None and self.east.east.is_wall == True) or self.east.east == None:
                if (self.east.north != None and self.east.north.is_wall == True) or self.east.north == None:
                    if (self.east.south != None and self.east.south.is_wall == True) or self.east.south == None:
                        changeable_walls.append(self.east)
        # check if ← is changeable
        if self.west != None and self.west.is_wall == True:
            if (self.west.west != None and self.west.west.is_wall == True) or self.west.west == None:
                if (self.west.north != None and self.west.north.is_wall == True) or self.west.north == None:
                    if (self.west.south != None and self.west.south.is_wall == True) or self.west.south == None:
                        changeable_walls.append(self.west)

        return changeable_walls

    def __repr__(self):
        return f"({self.x}, {self.y})"
