class PipeManiaState:
    state_id = 0
    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        """ Este método é utilizado em caso de empate na gestão da lista
        de abertos nas procuras informadas. """
        return self.id < other.id


class Board:
    """ Representação interna de uma grelha de PipeMania. """
    def __init__(self, size):
        self.board = [[]]
        self.size = size
        pass

    def add_line(self, line):
        """Guarda uma linha do board"""
        self.board.append(line)

    def adjacent_vertical_values(self, row: int, col: int):
        """ Devolve os valores imediatamente acima e abaixo,
        respectivamente. """
        if row == 0:
            up = None
        else:
            up = self.board[row - 1][col]
        if row == self.size-1:
            down = None
        else:
            down = self.board[row + 1][col]
        return (up, down)

    def adjacent_horizontal_values(self, row: int, col: int):
        """ Devolve os valores imediatamente à esquerda e à direita,
        respectivamente. """
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

class PipeMania(Problem):
    def __init__(self, initial_state: Board, goal_state: Board):
        """ O construtor especifica o estado inicial. """
        # TODO
        pass

    def actions(self, state: State):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        # TODO
        pass

    def result(self, state: State, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state). """
        # TODO
        pass

    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        # TODO
        pass

board = Board.parse_instance()
print(board.adjacent_vertical_values(0, 0))
print(board.adjacent_horizontal_values(0, 0))
print(board.adjacent_vertical_values(1, 1))
print(board.adjacent_horizontal_values(1, 1))

