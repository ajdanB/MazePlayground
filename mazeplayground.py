"""
    MazePlayground — Generating and Solving Mazes
    Delivery day: 27.01.2024
"""
__author__ = "Nadja Becker"

# Import libraries
from Node import Node
from Functions_Maze import *
from rich import print
from rich.prompt import Prompt, Confirm
from shutil import get_terminal_size

banner = '''[chartreuse4]
███╗   ███╗ █████╗ ███████╗███████╗     ██████╗ ███████╗███╗   ██╗███████╗██████╗  █████╗ ████████╗ ██████╗ ██████╗ 
████╗ ████║██╔══██╗╚══███╔╝██╔════╝    ██╔════╝ ██╔════╝████╗  ██║██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
██╔████╔██║███████║  ███╔╝ █████╗      ██║  ███╗█████╗  ██╔██╗ ██║█████╗  ██████╔╝███████║   ██║   ██║   ██║██████╔╝
██║╚██╔╝██║██╔══██║ ███╔╝  ██╔══╝      ██║   ██║██╔══╝  ██║╚██╗██║██╔══╝  ██╔══██╗██╔══██║   ██║   ██║   ██║██╔══██╗
██║ ╚═╝ ██║██║  ██║███████╗███████╗    ╚██████╔╝███████╗██║ ╚████║███████╗██║  ██║██║  ██║   ██║   ╚██████╔╝██║  ██║
╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝     ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
[/chartreuse4]'''
terminal_columns = get_terminal_size().columns
text_lines = banner.split('\n')
trimmed_banner = '\n'.join([line[:terminal_columns] for line in text_lines])   # trim the banner to the terminal width

print(trimmed_banner)

cycle_choice = True
while cycle_choice == True:   # loop to generate multiple mazes
    terminal_columns = get_terminal_size().columns

    # Implementation of the ability to adjust labyrinth parameters (size)
    height = input("Höhe des Labyrinths (10 oder größer): ")
    width_terminal = (terminal_columns - 6)//3  # calculate the width of the terminal subtracted with outer borders and divided by 3 (width of a node)
    width = input(f"Breite des Labyrinths (10-{width_terminal}): ")
    print("[bold]Verzweigungsgrad: [dodger_blue1]sehr leicht (langer Pfad, wenige Verzweigungen)[/dodger_blue1] bis [orange_red1]schwer (kürzere Pfade, viele Verzweigungen)[/orange_red1][/bold]")
    branching = input("Verzweigungsgrad (sehr leicht = 0, leicht = 1, mittel = 2, schwer = 3): ")
    branching_list = [0.0, 0.01, 0.05, 0.5]   # list of branching factors

    try:   # if input is not a number, set height to 10
        height = int(height)
    except ValueError:
        print("[bold red]Falsche Eingabe, Höhe wird auf 10 gesetzt.[/bold red]")
        height = 10
    if height < 5:   # if input is smaller than 5, set height to 5
        print("[bold blue]Falsche Eingabe, Höhe wird auf 5 gesetzt.[/bold blue]")
        height = 5

    try:   # if input is not a number, set width to 10
        width = int(width)
    except ValueError:
        print("[bold red]Falsche Eingabe, Breite wird auf 10 gesetzt.[/bold red]")
        width = 10
    if width < 5:   # if input is smaller than 5, set width to 5
        print("[bold blue]Falsche Eingabe, Breite wird auf 5 gesetzt.[/bold blue]")
        width = 5
    elif width > width_terminal:   # if input is bigger than width_terminal, set width to width_terminal
        print(f"[bold blue]Falsche Eingabe, Breite wird auf {width_terminal} gesetzt.[/bold blue]")
        width = width_terminal

    if branching not in ["0", "1", "2", "3"]:   # if input is not 0, 1, 2 or 3, set branching to 2
        print("[bold red]Falsche Eingabe, Verzweigungsgrad wird auf mittel gesetzt.[/bold red]")
        branching = 2
    branching = int(branching)

    maze = []   # create an empty maze

    for i in range(0, height):   # fill the maze with nodes (create a grid/matrix)
        maze.append([])
        for j in range(0, width):
            maze[i].append(Node(i, j))

    connect_nodes(maze, height, width)   # connect the nodes of the maze
    start_node = random_start(maze)   # choose a random start node

    if branching == 0:   # generate the maze with the recursive backtracking algorithm
        alg_recursive_backtracking(start_node)   # recursive backtracking algorithm
    else:
        alg_recursive_backtracking2(start_node, branching_list[branching])   # recursive backtracking algorithm with a branching factor

    final_end = path_finding(start_node)   # find all shortest paths to the start node with the breadth-first search algorithm. Also returns the final end node (longest distance to the start node on the boarder).

    design_index = print_maze(maze)   # print the generated maze and choose a design, which is reused for the solved maze
    Prompt.ask("[bold green]Um das Labyrinth zu lösen, drücke Enter[/bold green]")   # wait for user input to solve the maze

    path_solving(final_end)   # solving the maze, by following the shortest path from the end to the start node

    print_maze(maze, design_index)   # print the completed maze with path
    cycle_choice = Confirm.ask("[bold green]Möchtest du ein weiteres Labyrinth?[/bold green]", default=True)   # ask the user if he wants to generate another maze (default = yes)

    if cycle_choice == False:   # if the user doesn't want to generate another maze, print a thank you message
        print("[bold gold1]Vielen Dank fürs Spielen![/bold gold1]")   # print a thank you message
        break   # break the loop
