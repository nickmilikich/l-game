# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.8
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

import networkx as nx
import numpy as np
import random
import time

# Number of moves ahead to look
depth = 4


def print_board(board):
    
    if len(board) == 17:
        print()
        for k in range(4):
            print(board[(4 * k + 1):(4 * k + 5)])
        print()
    
    else:
        print(board)


def str_replace(s, index, character):
    
    l = list(s)
    l[index] = character
    return ''.join(l)


def get_poss_moves(board):
    
    # Separate board from current move
    curr_move = board[0]
    board = board[1:]
    
    # Restructure board
    board = np.reshape(list(board), (4, 4))
    
    # Save original board (move can't bring the board back to the same arrangement)
    orig_board = board.copy()
    
    # Get rid of piece of player who's moving
    board[board == curr_move] = ' '
    
    # The 4 L arrangements, each with the 4 cells that are used, relative to the top-left cell 
    vert_l_positions = {
        'tl': [(0, 0), (0, 1), (1, 1), (2, 1)],
        'tr': [(0, 0), (0, 1), (1, 0), (2, 0)],
        'bl': [(0, 1), (1, 1), (2, 0), (2, 1)],
        'br': [(0, 0), (1, 0), (2, 0), (2, 1)],
    }
    hor_l_positions = {
        'br': [(0, 0), (0, 1), (0, 2), (1, 2)],
        'bl': [(0, 0), (0, 1), (0, 2), (1, 0)],
        'tl': [(0, 0), (1, 0), (1, 1), (1, 2)],
        'tr': [(0, 2), (1, 0), (1, 1), (1, 2)],
    }
    
    # Empty list of possible moves
    poss_moves = []
    
    # Loop through valid top-left cells
    for x in range(2):
        for y in range(3):
            
            # Vertical L's: loop through valid positions
            for pos in vert_l_positions.keys():
                
                # Check if all relevant cells are empty
                if all([board[x + offset[0]][y + offset[1]] == ' ' for offset in vert_l_positions[pos]]):
                                        
                    # Place piece on board
                    new_board = board.copy()
                    for offset in vert_l_positions[pos]:
                        new_board[x + offset[0]][y + offset[1]] = curr_move
                                        
                    # If new board is the same as original, piece has not moved, and move is invalid
                    if not np.array_equal(new_board, orig_board):
                                            
                        # Put board back in string format
                        new_board = ''.join(new_board.flat)

                        # Add board without moving any neutral pieces to solution set
                        poss_moves.append(f"{('1' if curr_move == '0' else '0')}{new_board}")

                        ############################################
                        # Find all options for moving neutral pieces
                        ############################################

                        # Get indexes of neutral pieces and open spaces
                        neutral_pos = [i for i, c in enumerate(new_board) if c == 'n']
                        open_pos = [i for i, c in enumerate(new_board) if c == ' ']

                        # Loop through all combinations of neutral index and open index to swap
                        for neutr in neutral_pos:
                            for op in open_pos:

                                # Do the swap
                                newer_board = new_board
                                newer_board = str_replace(newer_board, neutr, new_board[op])
                                newer_board = str_replace(newer_board, op, new_board[neutr])

                                # Save the board
                                poss_moves.append(f"{('1' if curr_move == '0' else '0')}{newer_board}")
                    
    # Loop through valid top-left cells
    for x in range(3):
        for y in range(2):
            
            # Horizontal L's: loop through valid positions
            for pos in hor_l_positions.keys():
                
                # Check if all relevant cells are empty
                if all([board[x + offset[0]][y + offset[1]] == ' ' for offset in hor_l_positions[pos]]):
                    
                    # Place piece on board
                    new_board = board.copy()
                    for offset in hor_l_positions[pos]:
                        new_board[x + offset[0]][y + offset[1]] = curr_move
                                                                    
                    # If new board is the same as original, piece has not moved, and move is invalid
                    if not np.array_equal(new_board, orig_board):
                        
                        # Put board back in string format
                        new_board = ''.join(new_board.flat)

                        # Add board without moving any neutral pieces to solution set
                        poss_moves.append(f"{('1' if curr_move == '0' else '0')}{new_board}")

                        ############################################
                        # Find all options for moving neutral pieces
                        ############################################

                        # Get indexes of neutral pieces and open spaces
                        neutral_pos = [i for i, c in enumerate(new_board) if c == 'n']
                        open_pos = [i for i, c in enumerate(new_board) if c == ' ']

                        # Loop through all combinations of neutral index and open index to swap
                        for neutr in neutral_pos:
                            for op in open_pos:

                                # Do the swap
                                newer_board = new_board
                                newer_board = str_replace(newer_board, neutr, new_board[op])
                                newer_board = str_replace(newer_board, op, new_board[neutr])

                                # Save the board
                                poss_moves.append(f"{('1' if curr_move == '0' else '0')}{newer_board}")
    
    # Return list, dropping duplicates
    return list(set(poss_moves))


def add_child_nodes(G, pos):
    
    poss_moves = get_poss_moves(pos)
    
    if len(poss_moves) == 0:
        
        # Add winner attribute to this node since it's terminal
        G.add_edge(pos, '1 wins' if pos[0] == '0' else '0 wins')
    
    else:
        
        for move in poss_moves:
            G.add_edge(pos, move)
                    
    return G


def get_terminal_nodes(G):
            
    # Return anything that is a valid board (not an end node) and that has no outward edges yet (has not been called yet)
    return [x for x in G.nodes() if G.out_degree(x) == 0 and len(x) == 17]


def build_graph():
    
    init_pos = '0n00  10  10  11n'
    
    # Initialize empty graph
    G = nx.DiGraph()
    
    # Add initial board position
    G.add_node(init_pos)
    
    # Get all moves from starting position
    G = add_child_nodes(G, init_pos)
    
    # Set list of "terminal nodes"
    term_nodes = get_terminal_nodes(G)
        
    # While there are any unfinished games
    while len(term_nodes) > 0:
        
        # Go one layer deeper for each terminal node
        for node in term_nodes:
            G = add_child_nodes(G, node)

        # Reset list of terminal nodes
        term_nodes = get_terminal_nodes(G)
            
    return G


def flatten(l):
    
    return list(np.concatenate(l).flat) if len(l) > 0 else []


def intersect(a, b):
    return [x for x in a if x in b]


# Returns the best move for the current player, given the current board
def get_best_move(G, pos):
        
    # Short everything else if move is impossible
    if len(list(G.successors(pos))) == 1 and list(G.successors(pos))[0][2:] == 'wins':
        return list(G.successors(pos))[0]
        
    # Get distance from each move to player winning
    dists = {}
    for move in G.successors(pos):
        dists[move] = {
            'dist_to_win': len(nx.shortest_path(G, move, f'{pos[0]} wins')) \
                if f'{pos[0]} wins' in G.nodes() and nx.has_path(G, move, f'{pos[0]} wins') else np.inf,
            'dist_to_loss': len(nx.shortest_path(G, move, f"{('1' if pos[0] == '0' else '0')} wins")) \
                if f"{('1' if pos[0] == '0' else '0')} wins" in G.nodes() and nx.has_path(G, move, f"{('1' if pos[0] == '0' else '0')} wins") else np.inf,
        }
                
    # Start with all possible moves
    poss_moves = list(G.successors(pos))
        
    # Knock out any moves that could cause you to lose (unless that includes all moves)
    dists_to_loss = list(set([dists[p]['dist_to_loss'] for p in poss_moves]))
    dists_to_loss = sorted([x for x in dists_to_loss if not np.isinf(x)])
    while len(dists_to_loss) > 0:
        poss_moves_reduced = [x for x in poss_moves if not dists[x]['dist_to_loss'] == dists_to_loss[0]]
        if len(poss_moves_reduced) > 0:
            poss_moves = poss_moves_reduced
        dists_to_loss = dists_to_loss[1:]
    temp = len(poss_moves) # Delete later
        
    # If any moves have a visible path to winning, get all moves with lowest distance to win
    if any([not np.isinf(dists[p]['dist_to_win']) for p in poss_moves]):
        poss_moves = [x for x in poss_moves if dists[x]['dist_to_win'] == min([dists[p]['dist_to_win'] for p in poss_moves])]
    print(f'{len(list(G.successors(pos)))} -> {temp} -> {len(poss_moves)} possible moves')
        
    # Return random choice from remaining
    return random.choice(poss_moves)

# +
# G = build_graph()

# +
# board = '0n00  10  10  11n'
# print_board(board)

# while len(board) == 17:
#     board = get_best_move(G, board)
#     print_board(board)
# -






