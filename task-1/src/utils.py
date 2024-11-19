from typing import Tuple, TypeAlias, Dict, List


Model: TypeAlias = Dict[int, bool]


def print_sudoku(model: Model, size: int):
    table = [["."] * size for _ in range(size)]
    for literal, value in model.items():
        if value:
            row, column, value = decode_literal(literal, size)
            table[row - 1][column - 1] = str(value)
    for row in table:
        print("".join(row))


def encode_literal(row: int, column: int, value: int, size: int) -> int:
    if size == 16:
        return value + 17 * (column + 17 * row)
    else:
        return value + 10 * (column + 10 * row)


def decode_literal(literal: int, size: int) -> Tuple[int, int, int]:
    if size == 16:
        value = literal % 17
        literal = literal // 17
        column = literal % 17
        row = literal // 17
        return row, column, value
    else:
        value = literal % 10
        literal = literal // 10
        column = literal % 10
        row = literal // 10
        return row, column, value


def list_diff(left: List, right: List) -> List:
    return list(set(left) - set(right))
