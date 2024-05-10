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
            self.board = [[]]
            self.size = size

    def add_line(self, line):
        """Guarda uma linha do board"""
        self.board.append(line)

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board[row][col]

    def adjacent_vertical_values(self, row: int, col: int) -> tuple[str, str]:
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        if row == 0:
            up = None
        else:
            up = self.board[row - 1][col]
        if row == self.size-1:
            down = None
        else:
            down = self.board[row + 1][col]
        return (up, down)

    def adjacent_horizontal_values(self, row: int, col: int) -> tuple[str, str]:
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if col == 0:
            left = None
        else:
            left = self.board[row][col - 1]
        if row == self.size-1:
            right = None
        else:
            right = self.board[row][col + 1]
        return (left, right)

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
                if (state.board.get_value(row,col)[0] == 'L'):
                    actions.append((row,col,1))
                else:
                    actions.append((row,col,-1),(row,col,1),(row,col,2))
        return actions

    def result(self, state: PipeManiaState, action: tuple[int, int, int]):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        val = state.board.get_value(action[0], action[1])
        if (val[0] == 'L'):
            if (val[1] == 'H'):
                return "LV"
            else:
                return "LH"
        elif (val[0] == 'V'):
            poss = ["VB", "VD", "VC", "VE"]
            i = poss.index(val)
            return poss[(i + action[2])%4]
        elif (val[0] == 'B'):
            poss = ["BB", "BD", "BC", "BE"]
            i = poss.index(val)
            return poss[(i + action[2])%4]
        else:
            poss = ["FB", "FD", "FC", "FE"]
            i = poss.index(val)
            return poss[(i + action[2])%4]

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        up_conects = ["FC", "BC", "BE", "BD", "VC", "VD", "LV"]
        down_conects = ["FB", "BB", "BE", "BD", "VB", "VE", "LV"]
        left_conects = ["FE", "BC", "BE", "BB", "VC", "VE", "LH"]
        right_conects = ["FD", "BC", "BB", "BD", "VB", "VD", "LH"]
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
        for obama in range(state.board.size):
            if (checker.__contains__(0)):
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
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
