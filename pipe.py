# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 29:
# 106211 Tomás Dias Monteiro
# 106196 Diogo Cruz Diniz

import numpy as np
import sys
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

# [=== Constants ===]
# == Pieces == 
PIECE_NONE = 0
PIECE_VB = 1
PIECE_VD = 2
PIECE_VC = 3
PIECE_VE = 4
PIECE_FB = 5
PIECE_FD = 6
PIECE_FC = 7
PIECE_FE = 8
PIECE_BB = 9
PIECE_BD = 10
PIECE_BC = 11
PIECE_BE = 12
PIECE_LH = 13
PIECE_LV = 14
PIECE_MAX = 14

PIECE_TO_STR = ["NONE", "VB", "VD", "VC", "VE", "FB", "FD", "FC", "FE", "BB", "BD", "BC", "BE", "LH", "LV"]
STR_TO_PIECE = { "LH": PIECE_LH, "LV": PIECE_LV, "VB": PIECE_VB, "VD": PIECE_VD, "VC": PIECE_VC, "VE": PIECE_VE, "BB": PIECE_BB, "BD": PIECE_BD, "BC": PIECE_BC, "BE": PIECE_BE, "FB": PIECE_FB, "FD": PIECE_FD, "FC": PIECE_FC, "FE": PIECE_FE }

# == Connections ==
CONNECTS_UP = [PIECE_FC, PIECE_BC, PIECE_BE, PIECE_BD, PIECE_VC, PIECE_VD, PIECE_LV]
CONNECTS_DOWN = [PIECE_FB, PIECE_BB, PIECE_BE, PIECE_BD, PIECE_VB, PIECE_VE, PIECE_LV]
CONNECTS_LEFT = [PIECE_FE, PIECE_BC, PIECE_BE, PIECE_BB, PIECE_VC, PIECE_VE, PIECE_LH]
CONNECTS_RIGHT = [PIECE_FD, PIECE_BC, PIECE_BB, PIECE_BD, PIECE_VB, PIECE_VD, PIECE_LH]

# == Indices ==
PIECE_IDX = 0
MOVABLE_IDX = 1



# [=== Code ===]

def piece_to_str(piece : int) -> str:
    return PIECE_TO_STR[piece]

def str_to_piece(name : str) -> int:
    return STR_TO_PIECE.get(name, PIECE_NONE)

class Board:
    """Representação interna de um tabuleiro de PipeMania."""

    board : np.ndarray[int]
    size : int
    
    def __init__(self, size):
            self.board = np.ndarray((size, size, 2))
            self.size = size

    def get_value(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board[row, col, PIECE_IDX]
    
    def set_value(self, row: int, col: int, val: int) -> None:
        """Define o valor na respetiva posição do tabuleiro"""
        self.board[row, col, PIECE_IDX] = val;
    
    def get_movable(self, row: int, col: int) -> bool:
        """Devolve se a peça pode ser movida"""
        return self.board[row, col, MOVABLE_IDX] == 0
    
    def set_moved(self, row: int, col: int) -> None:
        """Define a peça como imovível"""
        self.board[row, col, MOVABLE_IDX] = False

    def adjacent_vertical_values(self, row: int, col: int) -> tuple[int, int]:
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        if row == 0:
            up = PIECE_NONE
        else:
            up = self.get_value(row - 1, col)
        if row == self.size-1:
            down = PIECE_NONE
        else:
            down = self.get_value(row + 1, col)
        return (up, down)

    def adjacent_horizontal_values(self, row: int, col: int) -> tuple[int, int]:
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if col == 0:
            left = PIECE_NONE
        else:
            left = self.get_value(row, col - 1)
        if row == self.size-1:
            right = PIECE_NONE
        else:
            right = self.get_value(row, col + 1)
        return (left, right)
    
    def parse_line(self, line: list[str], line_num: int) -> None:
        """Guarda uma linha do board"""
        for i in range(len(line)):
            self.set_value(line_num, i, str_to_piece(line[i]))
            pass

    def __setup_corners(self) -> None:
        # == Check valid corners if they are V pieces ==
        # Top left corner
        canto = self.get_value(0, 0)
        if (canto <= PIECE_VE):
            self.set_value(0, 0, PIECE_VB)
            self.set_moved(0, 0)

        # Top right corner
        canto = self.get_value(0, self.size - 1)
        if (canto <= PIECE_VE):
            self.set_value(0, self.size - 1, PIECE_VE)
            self.set_moved(0, self.size - 1)

        # Bottom left corner
        canto = self.get_value(self.size - 1, 0)
        if (canto <= PIECE_VE):
            self.set_value(self.size - 1, 0, PIECE_VD)
            self.set_moved(self.size - 1, 0)

        #Bottom right corner
        canto = self.get_value(self.size - 1, self.size - 1)
        if (canto <= PIECE_VE):
            self.set_value(self.size - 1, self.size - 1, PIECE_VC)
            self.set_moved(self.size - 1, self.size - 1)

    def __check_connects_no_edge(self, row: int, col: int):
        pass

    def setup(self) -> None:
        """Algoritmo que descobre peças que só podem ter uma posição certa e coloca-as
        nessa posição."""

        # Defaulting rules:
        # Prefer vertical
        # Prefer positive growing (right or down)

        self.__setup_corners();
        
        # == Check non-corner edges if they are B or L pieces ==
        # == At the same time, build list to check later ==
        to_check : list[tuple[int, int]] = []
        for i in range(1, self.size - 1):
            # Top edge
            piece = self.get_value(0, i)
            if (piece >= PIECE_BB and piece <= PIECE_BE):
                self.set_value(0, i, PIECE_BB)
                self.set_moved(0, i)
                to_check.append((1, i))
            elif (piece == PIECE_LV or piece == PIECE_LH):
                self.set_value(0, i, PIECE_LH)
                self.set_moved(0, i)
                to_check.append((1, i))
            
            # Bottom edge
            piece = self.get_value(self.size - 1, i)
            if (piece >= PIECE_BB and piece <= PIECE_BE):
                self.set_value(self.size - 1, i, PIECE_BC)
                self.set_moved(self.size - 1, i)
                to_check.append((self.size - 2, i))
            elif (piece == PIECE_LV or piece == PIECE_LH):
                self.set_value(self.size - 1, i, PIECE_LH)
                self.set_moved(self.size - 1, i)
                to_check.append((self.size - 2, i))

            # Left edge
            piece = self.get_value(i, 0)
            if (piece >= PIECE_BB and piece <= PIECE_BE):
                self.set_value(i, 0, PIECE_BD)
                self.set_moved(i, 0)
                to_check.append((i, 1))
            elif (piece == PIECE_LV or piece == PIECE_LH):
                self.set_value(i, 0, PIECE_LV)
                self.set_moved(i, 0)
                to_check.append((i, 1))

            # Right edge
            piece = self.get_value(i, self.size - 1)
            if (piece >= PIECE_BB and piece <= PIECE_BE):
                self.set_value(i, self.size - 1, PIECE_BE)
                self.set_moved(i, self.size - 1)
                to_check.append((i, self.size - 2))
            elif (piece == PIECE_LV or piece == PIECE_LH):
                self.set_value(i, self.size - 1, PIECE_LV)
                self.set_moved(i, self.size - 1)
                to_check.append((i, self.size - 2))
        
        while (len(to_check)):
            x, y = to_check.pop()


    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board."""
        from sys import stdin
        line = stdin.readline().split("\t")
        size = line.count()
        board = Board(size)
        board.parse_line(line, 0)
        for obama in range(1, size):
            line = stdin.readline().split("\t")
            board.parse_line(line, obama - 1)
        return board

    # TODO: outros metodos da classe

class PipeManiaState:
    state_id = 0

    def __init__(self, board: Board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        """ Este método é utilizado em caso de empate na gestão da lista
        de abertos nas procuras informadas. """
        return self.id < other.id

    # TODO: outros metodos da classe

class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = PipeManiaState(board)

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        actions = []
        for row in range(state.board.size):
            for col in range(state.board.size):
                if (state.board.get_movable(row, col)):
                    if (state.board.get_value(row, col) <= 1):
                        actions.append((row, col, 1))
                    else:
                        actions.append((row, col, 3), (row, col, 1), (row, col, 2))
        return actions

    def result(self, state: PipeManiaState, action: tuple[int, int, int]):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        #TODO
        state.board.set_moved(action[0], action[1])
        val = state.board.get_value(action[0], action[1])
        if (val == 0):
            return 1
        elif (val == 1):
            return 0
        elif (val <= 5):
            return ((val - 2) + action[2]%4) + 2
        elif (val <= 9):
            return ((val - 6) + action[2]%4) + 6
        else:
            return ((val - 10) + action[2]%4) + 10

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        
        checker = [[]]
        for row in range(state.board.size):
            for col in range(state.board.size):
                checker[row][col] = 0
                val = state.board.get_value(row,col)
                (up, down) = state.board.adjacent_vertical_values(row,col)
                if (CONNECTS_UP.__contains__(val) != CONNECTS_DOWN.__contains__(up)):
                    return False
                if (CONNECTS_DOWN.__contains__(val) != CONNECTS_UP.__contains__(down)):
                    return False
                (left, right) = state.board.adjacent_horizontal_values(row,col)
                if (CONNECTS_LEFT.__contains__(val) != CONNECTS_RIGHT.__contains__(left)):
                    return False
                if (CONNECTS_RIGHT.__contains__(val) != CONNECTS_LEFT.__contains__(right)):
                    return False
                
        def flow(row, col):
            checker[row][col] = 1
            valu = state.board.get_value(row, col)
            if (CONNECTS_UP.__contains__(valu) and checker[row-1][col] == 0):
                flow(row-1, col)
            if (CONNECTS_DOWN.__contains__(valu) and checker[row+1][col] == 0):
                flow(row+1, col)
            if (CONNECTS_LEFT.__contains__(valu) and checker[row][col-1] == 0):
                flow(row, col-1)
            if (CONNECTS_RIGHT.__contains__(valu) and checker[row][col+1] == 0):
                flow(row, col+1)

        flow(0, 0)
        for obama in checker:
            if (obama.__contains__(0)):
                return False
        return True


    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    board = Board.parse_instance()
    # TODO:
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
