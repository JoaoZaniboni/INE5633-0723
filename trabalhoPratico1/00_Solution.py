
# Todas as implementações em um arquivo, permitimos o usuário escolher qual implementação quer utilizar

from random import shuffle
import time

boards_exemples = [[[2, 3, 6], [1, 5, None], [4, 7, 8]],
                   [[3, None, 6], [4, 2, 1], [7, 5, 8]],
                   [[2, 3, None], [1, 8, 4], [7, 5, 6]],
                   [[None, 4, 7], [2, 3, 1], [6, 8, 5]],
                   [[5, 3, 7], [8, 6, 2], [None, 1, 4]]]

# Definindo o estado objetivo do puzzle
goal_state = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, None]]

# Movimentos possíveis do quadrado vazio
moves_dict = {(0, -1): "left", (0, 1): "right",
              (-1, 0): "up", (1, 0): "down"}

def get_blank_position(board):
    """Retorna a posição do quadrado vazio no tabuleiro"""
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is None:
                return i, j

def is_valid_move(x, y):
    """Verifica se o movimento é válido"""
    return 0 <= x < 3 and 0 <= y < 3

def move_blank(board, move):
    """Move o quadrado vazio no tabuleiro"""
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
    """Imprime o tabuleiro"""
    for row in board:
        print(" ".join(str(cell) if cell is not None else " " for cell in row))
    print()

def is_goal_state(board):
    """Verifica se o tabuleiro está no estado objetivo"""
    return board == goal_state

def manhattan_distance(board):
    """Calcula a distância de Manhattan"""
    distance = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] is not None:
                value = board[i][j]
                goal_x, goal_y = (value - 1) // 3, (value - 1) % 3
                distance += abs(goal_x - i) + abs(goal_y - j)
    return distance

def out_of_order_pieces(board):
    """Calcula pecas fora da ordem certa"""
    count = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] != 0 and board[i][j] != goal_state[i][j]:
                count += 1
    return count

def solve_puzzle_with_heuristic(initial_board, simple=True):
    """Resolve o puzzle utilizando o algoritmo A* com uma heurística de manhattan"""
    if simple:
        heuritic = out_of_order_pieces
    else:
        heuritic = manhattan_distance
    visited = set()
    queue = [(initial_board, [], 0)]  # Armazena o estado do tabuleiro, o caminho até o estado atual e o custo acumulado

    start_time = time.time()

    while queue:
        current_board, current_path, cost = queue.pop(0)

        if is_goal_state(current_board):
            end_time = time.time()
            print("Solução encontrada em {:.6f} segundos".format(end_time - start_time))
            print("Total de nodos visitados:", len(visited))
            print("Tamanho do caminho:", len(current_path))
            return current_path

        visited.add(tuple(map(tuple, current_board)))  # Adiciona o estado atual aos visitados

        for move in moves_dict.keys():
            new_board = move_blank(current_board, move)
            if new_board is not None and tuple(map(tuple, new_board)) not in visited:
                new_path = current_path + [move]
                new_cost = cost + 1 + heuritic(new_board)  # custo acumulado + custo do movimento + heurística
                queue.append((new_board, new_path, new_cost))

        # Ordena a fila com base no custo acumulado
        queue = sorted(queue, key=lambda x: x[2])

    return None

def solve_puzzle_uniform_cost(initial_board):
    """Resolve o puzzle utilizando o algoritmo de busca A*."""
    visited = set()
    queue = [(initial_board, [])]  # Armazena o estado do tabuleiro e o caminho até o estado atual

    start_time = time.time()

    while queue:
        current_board, current_path = queue.pop(0)

        if is_goal_state(current_board):
            end_time = time.time()
            print("Solução encontrada em {:.4f} segundos".format(end_time - start_time))
            print("Total de nodos visitados:", len(visited))
            print("Tamanho do caminho:", len(current_path))
            return current_path

        visited.add(tuple(map(tuple, current_board)))  # Adiciona o estado atual aos visitados

        for move in moves_dict.keys():
            new_board = move_blank(current_board, move)
            if new_board is not None and tuple(map(tuple, new_board)) not in visited:
                new_path = current_path + [move]
                queue.append((new_board, new_path))

    return None

if __name__ == "__main__":
    # initial_state = generate_random_board()
    wich_one = int(input("qual modo quer rodar? 1- custo uniforme , 2 - simples , 3 - precisa\n"))
    start_time_total = time.time()
    for bd in boards_exemples:
        print("Estado inicial:")
        print_board(bd)

        print("Resolvendo o puzzle...")
        if wich_one == 1:
            solution = solve_puzzle_uniform_cost(bd)
        elif wich_one == 2:
            solution = solve_puzzle_with_heuristic(bd, simple=True)
        else:
            solution = solve_puzzle_with_heuristic(bd, simple=False)
        if solution:
            print("Caminho da solução:")
            for move in solution:
                print(moves_dict[move])
        else:
            print("Não foi possível encontrar uma solução.")
    end_time_total = time.time()
    print("Tempo total para resolver: {:.6f} segundos".format(end_time_total - start_time_total))
