# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

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

class Board:
    """Representação interna de um tabuleiro de PipeMania."""
    
    def __init__(self, size):
            self.board = []
            self.size = size
            self.counter = 0

    def translate(piece):
        """Transforma as peças de string para int e vice-versa"""
        legenda = ["LH", "LV", "VB", "VD", "VC", "VE", "BB", "BD", "BC", "BE", "FB", "FD", "FC", "FE"]
        if (isinstance(piece, int)):
            return legenda[piece]
        else:
            return legenda.index(piece)

    def get_value(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board[row][col][0]
    
    def set_value(self, row: int, col: int, val: int):
        """Define o valor na respetiva posição do tabuleiro"""
        self.board[row][col][0] = val;
    
    def get_movable(self, row: int, col: int) -> bool:
        """Devolve se a peça pode ser movida"""
        return self.board[row][col][1]
    
    def set_moved(self, row: int, col: int):
        """Define a peça como imovível"""
        self.board[row][col][1] = False

    def adjacent_vertical_values(self, row: int, col: int) -> tuple[int, int]:
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        if row == 0:
            up = None
        else:
            up = self.board[row - 1][col][0]
        if row == self.size-1:
            down = None
        else:
            down = self.board[row + 1][col][0]
        return (up, down)

    def adjacent_horizontal_values(self, row: int, col: int) -> tuple[int, int]:
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if col == 0:
            left = None
        else:
            left = self.board[row][col - 1][0]
        if row == self.size-1:
            right = None
        else:
            right = self.board[row][col + 1][0]
        return (left, right)
    
    def add_line(self, line: list):
        """Guarda uma linha do board"""
        newline = []
        for p in line:
            newline.append((self.translate(p), True))
        self.board.append(newline)

    def setup(self):
        """Algoritmo que descobre peças que só podem ter uma posição certa e coloca-as
        nessa posição."""
        #             0     1     2     3    4     5     6      7     8    9     10    11    12    13
        #legenda = ["LH", "LV", "VB", "VD", "VC", "VE", "BB", "BD", "BC", "BE", "FB", "FD", "FC", "FE"]
        #up_conects = ["FC", "BC", "BE", "BD", "VC", "VD", "LV"]
        #down_conects = ["FB", "BB", "BE", "BD", "VB", "VE", "LV"]
        #left_conects = ["FE", "BC", "BE", "BB", "VC", "VE", "LH"]
        #right_conects = ["FD", "BC", "BB", "BD", "VB", "VD", "LH"]
        tochecklist = []
        canto = self.get_value(0, 0)
        if (canto <= 5):
            self.set_value(0, 0, 2)
            self.set_moved(0, 0)

        canto = self.get_value(0, self.size)
        if (canto <= 5):
            self.set_value(0, self.size, 5)
            self.set_moved(0, self.size)

        canto = self.get_value(self.size, 0)
        if (canto <= 5):
            self.set_value(self.size, 0, 3)
            self.set_moved(self.size, 0)

        canto = self.get_value(self.size, self.size)
        if (canto <= 5):
            self.set_value(self.size, self.size, 4)
            self.set_moved(self.size, self.size)
        
        for i in range(1, self.size - 1):
            pass

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board."""
        from sys import stdin
        line = stdin.readline().split("\t")
        size = line.count()
        board = Board(size)
        board.add_line(line)
        for obama in range(1, size):
            line = stdin.readline().split("\t")
            board.add_line(line)
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
                if (state.board.get_movable(row,col)):
                    if (state.board.get_value(row,col) <= 1):
                        actions.append((row,col,1))
                    else:
                        actions.append((row,col,3),(row,col,1),(row,col,2))
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
        #             0     1     2     3    4     5     6      7     8    9     10    11    12    13
        #legenda = ["LH", "LV", "VB", "VD", "VC", "VE", "BB", "BD", "BC", "BE", "FB", "FD", "FC", "FE"]
        #up_conects = ["FC", "BC", "BE", "BD", "VC", "VD", "LV"]
        up_conects = [12, 8, 9, 7, 4, 3, 1]
        #down_conects = ["FB", "BB", "BE", "BD", "VB", "VE", "LV"]
        down_conects = [10, 6, 9, 7, 2, 5, 1]
        #left_conects = ["FE", "BC", "BE", "BB", "VC", "VE", "LH"]
        left_conects = [13, 8, 9, 6, 4, 5, 0]
        #right_conects = ["FD", "BC", "BB", "BD", "VB", "VD", "LH"]
        right_conects = [11, 8, 6, 7, 2, 3, 0]
        checker = [[]]
        for row in range(state.board.size):
            for col in range(state.board.size):
                checker[row][col] = 0
                val = state.board.get_value(row,col)
                (up, down) = state.board.adjacent_vertical_values(row,col)
                if (up_conects.__contains__(val) != down_conects.__contains__(up)):
                    return False
                if (down_conects.__contains__(val) != up_conects.__contains__(down)):
                    return False
                (left, right) = state.board.adjacent_horizontal_values(row,col)
                if (left_conects.__contains__(val) != right_conects.__contains__(left)):
                    return False
                if (right_conects.__contains__(val) != left_conects.__contains__(right)):
                    return False
                
        def flow(row, col):
            checker[row][col] = 1
            valu = state.board.get_value(row,col)
            if (up_conects.__contains__(valu) and checker[row-1][col] == 0):
                flow(row-1, col)
            if (down_conects.__contains__(valu) and checker[row+1][col] == 0):
                flow(row+1, col)
            if (left_conects.__contains__(valu) and checker[row][col-1] == 0):
                flow(row, col-1)
            if (right_conects.__contains__(valu) and checker[row][col+1] == 0):
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
    # TODO:
    # Ler o ficheiro do standard input,
    board = Board.parse_instance()
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
