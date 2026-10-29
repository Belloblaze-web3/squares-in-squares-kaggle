"""Safe deterministic baseline layouts."""
from __future__ import annotations
from math import ceil, sqrt
from .geometry import Square

def rectangular_layout(n: int) -> tuple[list[Square], float]:
    """Choose the best integer rectangle for n cells, with no rotation."""
    best = None
    for cols in range(1, int(sqrt(n)) + 2):
        rows = ceil(n / cols)
        L = max(cols, rows)
        key = (L, abs(cols-rows), cols)
        if best is None or key < best[0]: best = (key, cols, rows)
    _, cols, rows = best
    squares = [Square((i % cols)+.5, (i // cols)+.5, 0.0) for i in range(n)]
    return squares, float(max(cols, rows))

def square_grid_layout(n: int) -> tuple[list[Square], float]:
    side = ceil(sqrt(n))
    return [Square((i % side)+.5, (i // side)+.5, 0.0) for i in range(n)], float(side)
