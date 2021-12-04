from typing import List, Union

from . import path_to_input


class Board:
    """
    This contains the Bingo board and a parallel 2D list that starts as a 5x5 grid of 0s.
    When a number is called, the 0 that corresponds with the position of the number of the board is flipped to 1.
    
    To determine whether a board is in a winning state, sum each row and each column until the sum of a row or column
    if 5, indicating all 1s in that row or column.
    """
    def __init__(self, board: List[List[int]]):
        self.board = board
        self.results = [[0, 0, 0, 0, 0] for _ in range(5)]
        self.already_won = False

    def call_number(self, number) -> Union[int, bool]:
        """
        :param number:
        :return: either an int (the score) if the number resulted in a win, False otherwise
        """
        if self.already_won:
            return False
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                if self.board[row][col] == number:
                    self.results[row][col] = 1
                    if self.has_won():
                        self.already_won = True
                        return self.compute_score(number)
        return False

    def has_won(self):
        for row in range(len(self.board)):
            if sum(self.results[row]) == 5:
                return True
            cols = [self.results[i][row] for i in range(len(self.results))]
            if sum(cols) == 5:
                return True
        return False

    def compute_score(self, number_called):
        score = 0
        for row in range(len(self.results)):
            for col in range(len(self.results[row])):
                if self.results[row][col] == 0:
                    score += self.board[row][col]
        return score * number_called


def generate_boards(lines):
    current_board = None
    boards = []
    for line in lines[1:]:
        strip_line = line.strip()
        if not strip_line:
            if current_board:
                boards.append(Board(current_board))
            current_board = None
            continue
        elif not current_board:
            current_board = [[int(num) for num in strip_line.split()]]
        else:
            current_board.append([int(num) for num in strip_line.split()])
    return boards


def part_one():
    path = path_to_input('4.txt')
    with open(path) as input_file:
        lines = input_file.readlines()
        call_numbers = [int(num) for num in lines[0].strip().split(',')]
        boards = generate_boards(lines)
        for call_num in call_numbers:
            for board in boards:
                score_if_won = board.call_number(call_num)
                if score_if_won:
                    return score_if_won


def part_two():
    path = path_to_input('4.txt')
    with open(path) as input_file:
        lines = input_file.readlines()
        call_numbers = [int(num) for num in lines[0].strip().split(',')]
        boards = generate_boards(lines)
        winning_scores = []
        for call_num in call_numbers:
            for board in boards:
                score_if_won = board.call_number(call_num)
                if score_if_won:
                    winning_scores.append(score_if_won)
        return winning_scores[-1]
