"""Numerically robust geometry primitives for unit-square packing."""
from __future__ import annotations
from dataclasses import dataclass
from math import cos, sin, pi
from typing import Iterable

EPS = 1e-9

@dataclass(frozen=True)
class Square:
    x: float
    y: float
    angle: float = 0.0

    def vertices(self) -> tuple[tuple[float, float], ...]:
        c, s = cos(self.angle), sin(self.angle)
        out = []
        for dx, dy in ((-.5,-.5), (.5,-.5), (.5,.5), (-.5,.5)):
            out.append((self.x + c*dx - s*dy, self.y + s*dx + c*dy))
        return tuple(out)

    def bounds(self) -> tuple[float, float, float, float]:
        v = self.vertices()
        xs, ys = zip(*v)
        return min(xs), min(ys), max(xs), max(ys)

def _axes(poly: Iterable[tuple[float,float]]):
    p = list(poly)
    for i, a in enumerate(p):
        b = p[(i+1) % len(p)]
        ex, ey = b[0]-a[0], b[1]-a[1]
        yield (-ey, ex)

def _project(poly, axis):
    vals = [p[0]*axis[0] + p[1]*axis[1] for p in poly]
    return min(vals), max(vals)

def overlaps(a: Square, b: Square, tol: float = EPS) -> bool:
    """Return True only for positive-area interior overlap; touching is allowed."""
    pa, pb = a.vertices(), b.vertices()
    for axis in (*_axes(pa), *_axes(pb)):
        amin, amax = _project(pa, axis); bmin, bmax = _project(pb, axis)
        if min(amax, bmax) - max(amin, bmin) <= tol:
            return False
    return True

def inside(square: Square, L: float, tol: float = EPS) -> bool:
    return all(-tol <= x <= L+tol and -tol <= y <= L+tol for x,y in square.vertices())

def enclosing_side(squares: Iterable[Square]) -> float:
    sq = list(squares)
    if not sq: return 0.0
    lo = min(s.bounds()[0] for s in sq); bo = min(s.bounds()[1] for s in sq)
    hi = max(s.bounds()[2] for s in sq); to = max(s.bounds()[3] for s in sq)
    return max(hi-lo, to-bo)

def validate_layout(squares: list[Square], L: float, tol: float = 1e-8) -> list[str]:
    errors = []
    if L < 0: errors.append("container side must be nonnegative")
    for i, s in enumerate(squares):
        if not inside(s, L, tol): errors.append(f"square {i} violates boundary")
    for i in range(len(squares)):
        for j in range(i):
            if overlaps(squares[i], squares[j], tol): errors.append(f"squares {j} and {i} overlap")
    return errors
