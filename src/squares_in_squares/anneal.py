"""Optional simulated annealing improvement over a deterministic layout."""
from __future__ import annotations
import math, random
from .geometry import Square, enclosing_side, validate_layout
from .layouts import rectangular_layout

def optimize(n: int, steps: int = 10000, seed: int = 0) -> tuple[list[Square], float]:
    rng = random.Random(seed + n)
    current, L0 = rectangular_layout(n)
    best, bestL = current, L0
    # Keep a slightly generous box during search, then shrink to the actual bounds.
    L = L0
    poses = [[s.x, s.y, s.angle] for s in current]
    def energy(ps):
        ss = [Square(*p) for p in ps]
        bad = 0.0
        for s in ss:
            xmin,ymin,xmax,ymax=s.bounds()
            bad += max(0,-xmin)**2 + max(0,-ymin)**2 + max(0,xmax-L)**2 + max(0,ymax-L)**2
        for i in range(n):
            for j in range(i):
                if validate_layout([Square(*ps[i]), Square(*ps[j])], L, 1e-8):
                    # overlap test is the last error; boundary errors are also penalized above
                    from .geometry import overlaps
                    if overlaps(Square(*ps[i]), Square(*ps[j])): bad += 100.0
        return enclosing_side(Square(*p) for p in ps) + 10.0*bad
    curE = energy(poses)
    for t in range(max(0, steps)):
        frac = t / max(1, steps-1)
        temp = 0.25*(1-frac) + 0.002
        k = rng.randrange(n); old = poses[k][:]
        scale = 0.35*(1-frac) + 0.01
        poses[k][0] += rng.gauss(0, scale); poses[k][1] += rng.gauss(0, scale)
        poses[k][2] = (poses[k][2] + rng.gauss(0, scale)) % math.pi
        newE = energy(poses)
        if newE < curE or rng.random() < math.exp(min(0.0, (curE-newE)/temp)):
            curE = newE
        else: poses[k] = old
        cand = [Square(*p) for p in poses]
        side = enclosing_side(cand)
        if not validate_layout(cand, side, 1e-7) and side < bestL - 1e-10:
            best, bestL = cand, side
    return best, bestL
