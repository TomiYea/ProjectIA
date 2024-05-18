# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 29:
# 106211 Tomás Dias Monteiro
# 106196 Diogo Cruz Diniz

import numpy as np
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
PIECE_BB = 1
PIECE_BD = 2
PIECE_BC = 3
PIECE_BE = 4
PIECE_VB = 5
PIECE_VD = 6
PIECE_VC = 7
PIECE_VE = 8
PIECE_FB = 9
PIECE_FD = 10
PIECE_FC = 11
PIECE_FE = 12
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

# == Rotations ==
ROTATIONS_OF = [
    [], # NONE
    #BX
    [PIECE_BD, PIECE_BC, PIECE_BE],
    [PIECE_BB, PIECE_BC, PIECE_BE],
    [PIECE_BB, PIECE_BD, PIECE_BE],
    [PIECE_BB, PIECE_BD, PIECE_BC],
    #VX
    [PIECE_VD, PIECE_VC, PIECE_VE],
    [PIECE_VB, PIECE_VC, PIECE_VE],
    [PIECE_VB, PIECE_VD, PIECE_VE],
    [PIECE_VB, PIECE_VD, PIECE_VC],
    #FX
    [PIECE_FD, PIECE_FC, PIECE_FE],
    [PIECE_FB, PIECE_FC, PIECE_FE],
    [PIECE_FB, PIECE_FD, PIECE_FE],
    [PIECE_FB, PIECE_FD, PIECE_FC],
    #LX
    [PIECE_LV],
    [PIECE_LH],
]

# == Indices ==
PIECE_IDX = 0
MOVABLE_IDX = 1

# == Mobility ==
MOVABLE = 0
IMOVABLE = 1



# [=== Code ===]

def piece_to_str(piece : int) -> str:
    return PIECE_TO_STR[piece]

def str_to_piece(name : str) -> int:
    return STR_TO_PIECE.get(name, PIECE_NONE)

class Board:
    """Representação interna de um tabuleiro de PipeMania."""

    board : np.ndarray
    size : int
    
    def __init__(self, size: int):
        self.board = np.ndarray((size, size, 2), np.int32)
        self.size = size

    def deep_copy(self) -> 'Board':
        ret = Board(self.size)
        ret.board = self.board.copy()
        return ret

    def get_value(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board[row, col, PIECE_IDX]
    
    def set_value(self, row: int, col: int, val: int) -> None:
        """Define o valor na respetiva posição do tabuleiro"""
        self.board[row, col, PIECE_IDX] = val
    
    def get_movable(self, row: int, col: int) -> bool:
        """Devolve se a peça pode ser movida"""
        return self.board[row, col, MOVABLE_IDX] == MOVABLE
    
    def set_movable(self, row: int, col: int, val: int) -> None:
        """Define a peça como movível se 0 e imovível se 1"""
        self.board[row, col, MOVABLE_IDX] = val
    
    def set_moved(self, row: int, col: int) -> None:
        """Define a peça como imovível"""
        self.board[row, col, MOVABLE_IDX] = IMOVABLE

    def adjacent_vertical_values(self, row: int, col: int) -> "tuple[int, int]":
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

    def adjacent_horizontal_values(self, row: int, col: int) -> "tuple[int, int]":
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if col == 0:
            left = PIECE_NONE
        else:
            left = self.get_value(row, col - 1)
        if col == self.size-1:
            right = PIECE_NONE
        else:
            right = self.get_value(row, col + 1)
        return (left, right)
    
    def parse_line(self, line: "list[str]", line_num: int) -> None:
        """Guarda uma linha do board"""
        for i in range(len(line)):
            self.set_value(line_num, i, str_to_piece(line[i]))
            self.set_movable(line_num, i, MOVABLE)

    def __check_connects_immovable(self, row: int, col: int, val: int) -> bool:
        """Retorna False se a peça estiver definitivamente numa posição errada"""
        (up, down) = self.adjacent_vertical_values(row,col)
        if (up != PIECE_NONE):
            if (not self.get_movable(row - 1, col) and CONNECTS_UP.__contains__(val) != CONNECTS_DOWN.__contains__(up)):
                return False
        else:
            if (CONNECTS_UP.__contains__(val)):
                return False
        if (down != PIECE_NONE):
            if (not self.get_movable(row + 1, col) and CONNECTS_DOWN.__contains__(val) != CONNECTS_UP.__contains__(down)):
                return False
        else:
            if (CONNECTS_DOWN.__contains__(val)):
                return False
        (left, right) = self.adjacent_horizontal_values(row,col)
        if (left != PIECE_NONE):
            if (not self.get_movable(row, col - 1) and CONNECTS_LEFT.__contains__(val) != CONNECTS_RIGHT.__contains__(left)):
                return False
        else:
            if (CONNECTS_LEFT.__contains__(val)):
                return False
        if (right != PIECE_NONE):
            if (not self.get_movable(row, col + 1) and CONNECTS_RIGHT.__contains__(val) != CONNECTS_LEFT.__contains__(right)):
                return False
        else:
            if (CONNECTS_RIGHT.__contains__(val)):
                return False
        return True

    def __check_adjacents(self, row: int, col: int) -> None:
        """Põe as peças possíveis na posição certa"""
        to_check : list[tuple[int, int]] = []

        if (row != 0 and self.get_movable(row - 1, col)):
            to_check.append((row - 1, col))
        if (row != self.size - 1 and self.get_movable(row + 1, col)):
            to_check.append((row + 1, col))
        if (col != 0 and self.get_movable(row, col - 1)):
            to_check.append((row, col - 1))
        if (col != self.size - 1 and self.get_movable(row, col + 1)):
            to_check.append((row, col + 1))
        while (len(to_check)):
            x, y = to_check.pop()
            if (not self.get_movable(x, y)): #TODO: Pensar melhor nisto
                continue
            piece = self.get_value(x, y)
            valid = []
            if (self.__check_connects_immovable(x, y, piece)):
                valid.append(piece)

            for rotation in ROTATIONS_OF[piece]:
                if (self.__check_connects_immovable(x, y, rotation)):
                    valid.append(piece)

            if (len(valid) == 1):
                self.set_value(x, y, valid[0])
                self.set_moved(x, y)
                # Add unmoved neighbours
                if (x != 0 and self.get_movable(x - 1, y)):
                    to_check.append((x - 1, y))
                    self.set_moved(x - 1, y)
                if (x != self.size - 1 and self.get_movable(x + 1, y)):
                    to_check.append((x + 1, y))
                    self.set_moved(x + 1, y)
                if (y != 0 and self.get_movable(x, y - 1)):
                    to_check.append((x, y - 1))
                    self.set_moved(x, y - 1)
                if (y != self.size - 1 and self.get_movable(x, y + 1)):
                    to_check.append((x, y + 1))
                    self.set_moved(x, y + 1)

    def __setup_corners(self) -> None:
        # == Check valid corners if they are V pieces ==
        # Top left corner
        canto = self.get_value(0, 0)
        if (canto <= PIECE_VE):
            self.set_value(0, 0, PIECE_VB)
            self.set_moved(0, 0)
            self.__check_adjacents(0, 0)

        # Top right corner
        canto = self.get_value(0, self.size - 1)
        if (canto <= PIECE_VE):
            self.set_value(0, self.size - 1, PIECE_VE)
            self.set_moved(0, self.size - 1)
            self.__check_adjacents(0, self.size - 1)

        # Bottom left corner
        canto = self.get_value(self.size - 1, 0)
        if (canto <= PIECE_VE):
            self.set_value(self.size - 1, 0, PIECE_VD)
            self.set_moved(self.size - 1, 0)
            self.__check_adjacents(self.size - 1, 0)

        #Bottom right corner
        canto = self.get_value(self.size - 1, self.size - 1)
        if (canto <= PIECE_VE):
            self.set_value(self.size - 1, self.size - 1, PIECE_VC)
            self.set_moved(self.size - 1, self.size - 1)
            self.__check_adjacents(self.size - 1, self.size - 1)

    def setup(self) -> None:
        """Algoritmo que descobre peças que só podem ter uma posição certa e coloca-as
        nessa posição."""

        self.__setup_corners()
        
        # == Check non-corner edges if they are B or L pieces ==
        # == At the same time, build list to check later ==
        for i in range(1, self.size - 1):
            # Top edge
            piece = self.get_value(0, i)
            if (piece <= PIECE_BE):
                self.set_value(0, i, PIECE_BB)
                self.set_moved(0, i)
                self.__check_adjacents(1, i)
            elif (piece >= PIECE_LH):
                self.set_value(0, i, PIECE_LH)
                self.set_moved(0, i)
                self.__check_adjacents(1, i)
            
            # Bottom edge
            piece = self.get_value(self.size - 1, i)
            if (piece <= PIECE_BE):
                self.set_value(self.size - 1, i, PIECE_BC)
                self.set_moved(self.size - 1, i)
                self.__check_adjacents(self.size - 2, i)
            elif (piece >= PIECE_LH):
                self.set_value(self.size - 1, i, PIECE_LH)
                self.set_moved(self.size - 1, i)
                self.__check_adjacents(self.size - 2, i)

            # Left edge
            piece = self.get_value(i, 0)
            if (piece <= PIECE_BE):
                self.set_value(i, 0, PIECE_BD)
                self.set_moved(i, 0)
                self.__check_adjacents(i, 1)
            elif (piece >= PIECE_LH):
                self.set_value(i, 0, PIECE_LV)
                self.set_moved(i, 0)
                self.__check_adjacents(i, 1)

            # Right edge
            piece = self.get_value(i, self.size - 1)
            if (piece <= PIECE_BE):
                self.set_value(i, self.size - 1, PIECE_BE)
                self.set_moved(i, self.size - 1)
                self.__check_adjacents(i, self.size - 2)
            elif (piece >= PIECE_LH):
                self.set_value(i, self.size - 1, PIECE_LV)
                self.set_moved(i, self.size - 1)
                self.__check_adjacents(i, self.size - 2)

    def __str__(self) -> str:
        ret = ""
        for row in range(self.size):
            ret += "\n"
            for col in range(self.size):
                ret += piece_to_str(self.get_value(row, col))
                ret += "\t"
            ret[:-1]
        return ret[1:]

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board."""
        from sys import stdin
        line = stdin.readline().split("\t")
        size = len(line)
        board = Board(size)
        board.parse_line(line, 0)
        for obama in range(1, size):
            line = stdin.readline().split("\t")
            board.parse_line(line, obama - 1)
        return board

class PipeManiaState:
    state_id: int = 0
    board: Board

    def __init__(self, board: Board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        """ Este método é utilizado em caso de empate na gestão da lista
        de abertos nas procuras informadas. """
        return self.id < other.id

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
                if (not state.board.get_movable(row, col)):
                    continue
                val = state.board.get_value(row, col)
                for pos in ROTATIONS_OF[val]:
                    actions.append((row, col, pos))
        return actions

    def result(self, state: PipeManiaState, action: "tuple[int, int, int]") -> PipeManiaState:
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        copy = state.board.deep_copy()
        copy.set_value(action[0], action[1], action[2])
        copy.set_moved(action[0], action[1])
        return PipeManiaState(copy)

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        
        flow_map = np.ndarray((state.board.size, state.board.size))
        for row in range(state.board.size - 1):
            for col in range(state.board.size - 1):
                flow_map[row, col] = 0
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
            flow_map[row, col] = 1
            valu = state.board.get_value(row, col)
            if (CONNECTS_UP.__contains__(valu) and flow_map[row-1, col] == 0):
                flow(row-1, col)
            if (CONNECTS_DOWN.__contains__(valu) and flow_map[row+1, col] == 0):
                flow(row+1, col)
            if (CONNECTS_LEFT.__contains__(valu) and flow_map[row, col-1] == 0):
                flow(row, col-1)
            if (CONNECTS_RIGHT.__contains__(valu) and flow_map[row, col+1] == 0):
                flow(row, col+1)

        flow(0, 0)
        return np.all(flow_map)

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

if __name__ == "__main__":
    board = Board.parse_instance()
    board.setup()
    problem = PipeMania(board)
    result = depth_first_tree_search(problem)
    if (result == None):
        print("No solution found")
        exit(1)
    print(result.state.board)
    pass
