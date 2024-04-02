# Implementação versão 1, Custo Uniforme (sem heurística)

from random import shuffle
from collections import deque
import time

# Definindo o estado objetivo do puzzle
goal_state = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, None]]

# Movimentos possíveis do quadrado vazio
moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]

def get_blank_position(board):
    """Retorna a posição do quadrado vazio no tabuleiro."""
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is None:
                return i, j

def is_valid_move(x, y):
    """Verifica se o movimento é válido."""
    return 0 <= x < 3 and 0 <= y < 3

def move_blank(board, move):
    """Move o quadrado vazio no tabuleiro."""
    blank_x, blank_y = get_blank_position(board)
    new_x = blank_x + move[0]
    new_y = blank_y + move[1]

    if is_valid_move(new_x, new_y):
        new_board = [row[:] for row in board]
        new_board[blank_x][blank_y], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[blank_x][blank_y]
        return new_board
    else:
        return None

def print_board(board):
    """Imprime o tabuleiro."""
    for row in board:
        print(" ".join(str(cell) if cell is not None else " " for cell in row))
    print()

def is_goal_state(board):
    """Verifica se o tabuleiro está no estado objetivo."""
    return board == goal_state

def generate_random_board():
    """Gera um tabuleiro inicial aleatório."""
    numbers = list(range(1, 9)) + [None]
    shuffle(numbers)
    return [numbers[i:i+3] for i in range(0, 9, 3)]

def solve_puzzle(initial_board):
    """Resolve o puzzle utilizando o algoritmo de busca A*."""
    visited = set()
    queue = deque([(initial_board, [])])  # Armazena o estado do tabuleiro e o caminho até o estado atual

    start_time = time.time()

    while queue:
        current_board, current_path = queue.popleft()

        if is_goal_state(current_board):
            end_time = time.time()
            print("Solução encontrada em {:.4f} segundos".format(end_time - start_time))
            print("Total de nodos visitados:", len(visited))
            print("Tamanho do caminho:", len(current_path))
            return current_path

        visited.add(tuple(map(tuple, current_board)))  # Adiciona o estado atual aos visitados

        for move in moves:
            new_board = move_blank(current_board, move)
            if new_board is not None and tuple(map(tuple, new_board)) not in visited:
                new_path = current_path + [move]
                queue.append((new_board, new_path))

    return None

# Exemplo de uso
initial_state = generate_random_board()

print("Estado inicial:")
print_board(initial_state)

print("Resolvendo o puzzle...")
solution = solve_puzzle(initial_state)

if solution:
    print("Caminho da solução:")
    for move in solution:
        print(move)
else:
    print("Não foi possível encontrar uma solução.")
